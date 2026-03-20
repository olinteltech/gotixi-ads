"""
Create a Meta Ad Creative from approved copy and an uploaded image hash.
"""

from facebook_business.adobjects.adcreative import AdCreative
from meta.client import account, page_id, link_url as default_link_url


def create_ad_creative(
    headline: str,
    primary_text: str,
    description: str,
    call_to_action: str,
    image_hash: str,
    link_url: str = None,
) -> str:
    """
    Create an ad creative and return its ID.

    Args:
        headline: Ad headline (max 40 chars)
        primary_text: Main body copy (max 125 chars)
        description: Link description (max 30 chars)
        call_to_action: CTA button type, e.g. 'LEARN_MORE'
        image_hash: Hash from upload_image()
        link_url: Destination URL (falls back to GOTIXI_LINK_URL env var)

    Returns:
        creative_id (str)
    """
    destination = link_url or default_link_url

    creative = account.create_ad_creative(
        fields=[],
        params={
            "name": f"GoTixi Creative — {headline[:30]}",
            "object_story_spec": {
                "page_id": page_id,
                "link_data": {
                    "message": primary_text,
                    "link": destination,
                    "image_hash": image_hash,
                    "name": headline,
                    "description": description,
                    "call_to_action": {
                        "type": call_to_action,
                        "value": {"link": destination},
                    },
                },
            },
        },
    )
    return creative["id"]
