#!/usr/bin/env python3
"""
GoTixi Meta Ad Creator — top-level orchestrator.

Usage:
    python3 meta/create_full_ad.py path/to/ad_params.json

Takes a JSON file conforming to schemas/ad_params.schema.json,
validates it, then runs the full pipeline:
  upload_image → create_campaign → create_ad_set → create_ad_creative → create_ad

All objects are created in PAUSED status. Prints a JSON result to stdout.
On failure, prints a structured error to stderr and exits with code 1.
"""

import json
import sys
import os
from datetime import datetime

import jsonschema
from facebook_business.exceptions import FacebookRequestError

# ── Resolve schema path relative to this file ───────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCHEMA_PATH = os.path.join(_HERE, "..", "schemas", "ad_params.schema.json")


def load_schema() -> dict:
    with open(_SCHEMA_PATH) as f:
        return json.load(f)


def validate_params(params: dict, schema: dict):
    try:
        jsonschema.validate(instance=params, schema=schema)
    except jsonschema.ValidationError as e:
        _fail(f"Ad params validation failed: {e.message}", code=2)


def _fail(message: str, code: int = 1, partial: dict = None):
    payload = {"status": "error", "message": message}
    if partial:
        payload["partial_objects_created"] = partial
        payload["note"] = (
            "Some API objects were created before the failure. "
            "Delete them manually in Meta Ads Manager using the IDs above."
        )
    print(json.dumps(payload, indent=2), file=sys.stderr)
    sys.exit(code)


def _handle_api_error(err: FacebookRequestError, partial: dict):
    code = err.api_error_code()
    msg = err.api_error_message()
    hints = {
        190: "Access token is expired or invalid. Generate a new Page Access Token.",
        100: "Invalid parameter — check your ad_params.json for malformed values.",
        278: "Permission denied — ensure your token has ads_management and manage_pages.",
        200: "Permission denied — check ad account permissions.",
        368: "Ad account temporarily restricted. Check Meta Business Manager.",
    }
    hint = hints.get(code, "Check the Meta Marketing API error code documentation.")
    _fail(
        f"Meta API error {code}: {msg}\nHint: {hint}",
        partial=partial,
    )


def run(params_path: str):
    # ── Load and validate params ─────────────────────────────────────────────
    try:
        with open(params_path) as f:
            params = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        _fail(f"Could not load params file: {e}")

    schema = load_schema()
    validate_params(params, schema)

    # ── Extract fields ───────────────────────────────────────────────────────
    headline = params["headline"]
    primary_text = params["primary_text"]
    description = params["description"]
    cta = params["call_to_action"]
    campaign_name = params["campaign_name"]
    ad_set_name = params["ad_set_name"]
    ad_name = params["ad_name"]
    image_path = params["image_path"]
    audience_segment = params["audience_segment"]
    daily_budget_inr = params["daily_budget_inr"]
    campaign_objective = params["campaign_objective"]
    targeting_overrides = params.get("targeting", {})
    link_url = params.get("link_url")

    # Convert INR to paise (Meta uses smallest currency unit)
    daily_budget_paise = int(daily_budget_inr * 100)

    # ── Import modules here (after dotenv is loaded via client) ──────────────
    from meta.upload_image import upload_image
    from meta.create_campaign import create_campaign
    from meta.create_ad_set import create_ad_set
    from meta.create_ad_creative import create_ad_creative
    from meta.create_ad import create_ad

    created = {}

    try:
        # Step 1: Upload image
        print("→ Uploading image...", file=sys.stderr)
        image_hash = upload_image(image_path)
        print(f"  ✓ Image hash: {image_hash}", file=sys.stderr)

        # Step 2: Create campaign
        print("→ Creating campaign...", file=sys.stderr)
        campaign_id = create_campaign(campaign_name, campaign_objective)
        created["campaign_id"] = campaign_id
        print(f"  ✓ Campaign: {campaign_id}", file=sys.stderr)

        # Step 3: Create ad set
        print("→ Creating ad set...", file=sys.stderr)
        ad_set_id = create_ad_set(
            campaign_id=campaign_id,
            ad_set_name=ad_set_name,
            daily_budget_paise=daily_budget_paise,
            audience_segment=audience_segment,
            targeting_overrides=targeting_overrides,
        )
        created["ad_set_id"] = ad_set_id
        print(f"  ✓ Ad Set: {ad_set_id}", file=sys.stderr)

        # Step 4: Create creative
        print("→ Creating ad creative...", file=sys.stderr)
        creative_id = create_ad_creative(
            headline=headline,
            primary_text=primary_text,
            description=description,
            call_to_action=cta,
            image_hash=image_hash,
            link_url=link_url,
        )
        created["creative_id"] = creative_id
        print(f"  ✓ Creative: {creative_id}", file=sys.stderr)

        # Step 5: Create ad
        print("→ Creating ad...", file=sys.stderr)
        ad_id = create_ad(ad_name, ad_set_id, creative_id)
        created["ad_id"] = ad_id
        print(f"  ✓ Ad: {ad_id}", file=sys.stderr)

    except (FileNotFoundError, ValueError) as e:
        _fail(str(e), partial=created if created else None)
    except FacebookRequestError as e:
        _handle_api_error(e, partial=created if created else None)

    # ── Success output ───────────────────────────────────────────────────────
    result = {
        "status": "success",
        "ad_status": "PAUSED",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "campaign_id": campaign_id,
        "ad_set_id": ad_set_id,
        "creative_id": creative_id,
        "ad_id": ad_id,
        "note": (
            "All objects created in PAUSED status. "
            "Review in Meta Ads Manager before activating."
        ),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python3 meta/create_full_ad.py path/to/ad_params.json",
            file=sys.stderr,
        )
        sys.exit(1)
    run(sys.argv[1])
