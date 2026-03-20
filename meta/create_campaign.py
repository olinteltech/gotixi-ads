"""
Create a Meta Campaign. Always created in PAUSED status.
"""

from facebook_business.adobjects.campaign import Campaign
from meta.client import account


def create_campaign(campaign_name: str, objective: str) -> str:
    """
    Create a campaign and return its ID.

    Args:
        campaign_name: Human-readable name shown in Ads Manager
        objective: Meta campaign objective constant, e.g. 'OUTCOME_TRAFFIC'

    Returns:
        campaign_id (str)
    """
    campaign = account.create_campaign(
        fields=[],
        params={
            "name": campaign_name,
            "objective": objective,
            "status": Campaign.Status.paused,
            "special_ad_categories": [],
            "is_adset_budget_sharing_enabled": False,
        },
    )
    return campaign["id"]
