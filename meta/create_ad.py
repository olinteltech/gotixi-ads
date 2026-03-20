"""
Create the final Meta Ad, linking an ad set to a creative.
Always created in PAUSED status.
"""

from facebook_business.adobjects.ad import Ad
from meta.client import account


def create_ad(ad_name: str, ad_set_id: str, creative_id: str) -> str:
    """
    Create an ad and return its ID.

    Args:
        ad_name: Human-readable name shown in Ads Manager
        ad_set_id: ID of the parent ad set
        creative_id: ID of the prepared ad creative

    Returns:
        ad_id (str)
    """
    ad = account.create_ad(
        fields=[],
        params={
            "name": ad_name,
            "adset_id": ad_set_id,
            "creative": {"creative_id": creative_id},
            "status": Ad.Status.paused,
        },
    )
    return ad["id"]
