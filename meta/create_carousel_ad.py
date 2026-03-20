#!/usr/bin/env python3
"""
GoTixi Carousel Ad Creator

Creates a carousel ad from a folder of images.
Each image becomes one card in the carousel.

Usage:
    python3 meta/create_carousel_ad.py
"""

import json
import sys
import os
from datetime import datetime

from facebook_business.exceptions import FacebookRequestError
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad

# Must set PYTHONPATH=. before running
from meta.client import account, page_id, link_url as default_link_url
from meta.upload_image import upload_image
from meta.create_campaign import create_campaign
from meta.create_ad_set import create_ad_set
from meta.create_ad import create_ad

# ── Config ───────────────────────────────────────────────────────────────────

CAMPAIGN_FOLDER = "campaigns/may-escape-2026"
LINK_URL = os.getenv("GOTIXI_LINK_URL", "https://gotixi.com")

# Carousel cards — one per image, in order
CARDS = [
    {
        "image": "The_May_Holiday_Dilemma__version_1.png",
        "headline": "The May Holiday Dilemma",
        "description": "We've got you covered.",
    },
    {
        "image": "10_Cities,_3_Generations,_0_Clues__version_1.png",
        "headline": "10 Cities. 3 Generations.",
        "description": "Curated for every traveller.",
    },
    {
        "image": "Expert-Led,_24_7_Human_Support_version_1.png",
        "headline": "Expert-Led. 24/7 Support.",
        "description": "Real humans, every step.",
    },
    {
        "image": "Your_Perfect_Summer_Awaits_version_1.png",
        "headline": "Your Perfect Summer Awaits",
        "description": "Refined travel, planned for you.",
    },
]

PRIMARY_TEXT = (
    "This May, skip the chaos. GoTixi crafts international trips "
    "your whole family will remember — handled entirely by us."
)
CAMPAIGN_NAME  = "GoTixi — May Escape 2026 — Carousel [TEST]"
AD_SET_NAME    = "May Escape · Families · IN · May-2026 [TEST]"
AD_NAME        = "May Escape · Carousel · V1 [TEST]"
DAILY_BUDGET_INR = 500


# ── Helpers ──────────────────────────────────────────────────────────────────

def _fail(msg, partial=None):
    payload = {"status": "error", "message": msg}
    if partial:
        payload["partial_objects_created"] = partial
        payload["note"] = "Delete these in Meta Ads Manager to clean up."
    print(json.dumps(payload, indent=2), file=sys.stderr)
    sys.exit(1)


def _handle_api_error(err: FacebookRequestError, partial):
    code = err.api_error_code()
    msg  = err.api_error_message()
    hints = {
        190: "Access token expired — regenerate in Graph Explorer.",
        100: "Invalid parameter — check image hashes and page_id.",
        278: "Permission denied — token needs ads_management + manage_pages.",
        200: "Permission denied — check ad account permissions.",
    }
    hint = hints.get(code, "Check Meta Marketing API docs for this error code.")
    _fail(f"Meta API error {code}: {msg}\nHint: {hint}", partial=partial)


# ── Main ─────────────────────────────────────────────────────────────────────

def run():
    created = {}

    try:
        # 1. Upload all images
        print("\n→ Uploading images...", file=sys.stderr)
        child_attachments = []
        for card in CARDS:
            path = os.path.join(CAMPAIGN_FOLDER, card["image"])
            print(f"  Uploading: {card['image']}", file=sys.stderr)
            image_hash = upload_image(path)
            child_attachments.append({
                "link":        LINK_URL,
                "image_hash":  image_hash,
                "name":        card["headline"],
                "description": card["description"],
                "call_to_action": {
                    "type": "LEARN_MORE",
                    "value": {"link": LINK_URL},
                },
            })
            print(f"  ✓ Hash: {image_hash}", file=sys.stderr)

        # 2. Create campaign
        print("\n→ Creating campaign...", file=sys.stderr)
        campaign_id = create_campaign(CAMPAIGN_NAME, "OUTCOME_TRAFFIC")
        created["campaign_id"] = campaign_id
        print(f"  ✓ Campaign: {campaign_id}", file=sys.stderr)

        # 3. Create ad set
        print("\n→ Creating ad set...", file=sys.stderr)
        ad_set_id = create_ad_set(
            campaign_id=campaign_id,
            ad_set_name=AD_SET_NAME,
            daily_budget_paise=int(DAILY_BUDGET_INR * 100),
            audience_segment="families",
            targeting_overrides={"countries": ["IN"], "age_min": 28, "age_max": 50},
        )
        created["ad_set_id"] = ad_set_id
        print(f"  ✓ Ad Set: {ad_set_id}", file=sys.stderr)

        # 4. Create carousel creative
        print("\n→ Creating carousel creative...", file=sys.stderr)
        creative = account.create_ad_creative(
            fields=[],
            params={
                "name": f"GoTixi Carousel — May Escape 2026",
                "object_story_spec": {
                    "page_id": page_id,
                    "link_data": {
                        "message":           PRIMARY_TEXT,
                        "link":              LINK_URL,
                        "child_attachments": child_attachments,
                        "multi_share_optimized": True,
                        "call_to_action": {
                            "type": "LEARN_MORE",
                            "value": {"link": LINK_URL},
                        },
                    },
                },
            },
        )
        creative_id = creative["id"]
        created["creative_id"] = creative_id
        print(f"  ✓ Creative: {creative_id}", file=sys.stderr)

        # 5. Create ad
        print("\n→ Creating ad...", file=sys.stderr)
        ad_id = create_ad(AD_NAME, ad_set_id, creative_id)
        created["ad_id"] = ad_id
        print(f"  ✓ Ad: {ad_id}", file=sys.stderr)

    except (FileNotFoundError, ValueError) as e:
        _fail(str(e), partial=created or None)
    except FacebookRequestError as e:
        _handle_api_error(e, partial=created or None)

    # Success
    result = {
        "status":      "success",
        "ad_status":   "PAUSED",
        "created_at":  datetime.utcnow().isoformat() + "Z",
        "campaign_id": campaign_id,
        "ad_set_id":   ad_set_id,
        "creative_id": creative_id,
        "ad_id":       ad_id,
        "cards":       len(child_attachments),
        "note":        "All objects PAUSED. Review in Meta Ads Manager before activating.",
    }

    print("\n" + "─" * 40, file=sys.stderr)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
