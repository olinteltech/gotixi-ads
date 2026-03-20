"""
Bootstrap the Meta Marketing API SDK from environment variables.

Every other module in this package imports `ad_account_id` and `page_id`
from here — credentials are loaded exactly once.
"""

import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

load_dotenv()

_REQUIRED = [
    "META_APP_ID",
    "META_APP_SECRET",
    "META_ACCESS_TOKEN",
    "META_AD_ACCOUNT_ID",
    "META_PAGE_ID",
]

_missing = [k for k in _REQUIRED if not os.getenv(k)]
if _missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(_missing)}\n"
        "Copy .env.example to .env and fill in your Meta credentials."
    )

app_id = os.environ["META_APP_ID"]
app_secret = os.environ["META_APP_SECRET"]
access_token = os.environ["META_ACCESS_TOKEN"]
ad_account_id = os.environ["META_AD_ACCOUNT_ID"]  # must include act_ prefix
page_id = os.environ["META_PAGE_ID"]
link_url = os.getenv("GOTIXI_LINK_URL", "https://gotixi.com")

FacebookAdsApi.init(app_id, app_secret, access_token)
account = AdAccount(ad_account_id)
