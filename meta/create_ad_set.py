"""
Create a Meta Ad Set with targeting. Always created in PAUSED status.

Default targeting is Indian market (IN), ages 25-55, all genders —
aligned with GoTixi's primary Duckling audience.
"""

from facebook_business.adobjects.adset import AdSet
from meta.client import account

# Segment-specific targeting presets (override with targeting param in brief)
SEGMENT_TARGETING = {
    "families": {"age_min": 28, "age_max": 50, "genders": []},
    "couples": {"age_min": 24, "age_max": 45, "genders": []},
    "solo_explorers": {"age_min": 22, "age_max": 40, "genders": []},
    "adventurers": {"age_min": 22, "age_max": 45, "genders": []},
    "luxury_travelers": {"age_min": 30, "age_max": 60, "genders": []},
    "first_timers": {"age_min": 22, "age_max": 40, "genders": []},
}


def create_ad_set(
    campaign_id: str,
    ad_set_name: str,
    daily_budget_paise: int,
    audience_segment: str,
    targeting_overrides: dict = None,
) -> str:
    """
    Create an ad set and return its ID.

    Args:
        campaign_id: ID of the parent campaign
        ad_set_name: Human-readable name shown in Ads Manager
        daily_budget_paise: Daily budget in smallest currency unit (paise for INR)
        audience_segment: GoTixi Duckling segment key
        targeting_overrides: Optional dict to override segment defaults

    Returns:
        ad_set_id (str)
    """
    base = SEGMENT_TARGETING.get(audience_segment, {"age_min": 25, "age_max": 55, "genders": []})
    overrides = targeting_overrides or {}

    countries = overrides.get("countries", ["IN"])
    age_min = overrides.get("age_min", base["age_min"])
    age_max = overrides.get("age_max", base["age_max"])
    genders = overrides.get("genders", base["genders"])

    targeting = {
        "geo_locations": {"countries": countries},
        "age_min": age_min,
        "age_max": age_max,
        "targeting_automation": {"advantage_audience": 0},
    }
    if genders:
        targeting["genders"] = genders

    adset = account.create_ad_set(
        fields=[],
        params={
            "name": ad_set_name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget_paise,
            "targeting": targeting,
            "optimization_goal": AdSet.OptimizationGoal.link_clicks,
            "billing_event": AdSet.BillingEvent.impressions,
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "status": AdSet.Status.paused,
        },
    )
    return adset["id"]
