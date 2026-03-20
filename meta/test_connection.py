#!/usr/bin/env python3
"""
Quick connection test for GoTixi Meta API setup.
Run: python3 meta/test_connection.py
"""

import sys

def check(label, fn):
    print(f"  {label}...", end=" ", flush=True)
    try:
        result = fn()
        print(f"✓  {result}")
        return True
    except Exception as e:
        print(f"✗  {e}")
        return False


print("\nGoTixi — Meta API Connection Test\n" + "─" * 40)

# 1. Env vars
print("\n[1] Environment variables")
try:
    from meta.client import app_id, ad_account_id, page_id, account
    check("APP_ID",         lambda: app_id)
    check("AD_ACCOUNT_ID",  lambda: ad_account_id)
    check("PAGE_ID",        lambda: page_id)
except EnvironmentError as e:
    print(f"  ✗ {e}")
    sys.exit(1)

# 2. Ad account reachable
print("\n[2] Ad Account")
ok = check("Fetch account name", lambda: account.api_get(
    fields=["name", "currency", "account_status"]
).get("name", "—"))

# 3. Account status
print("\n[3] Account details")
try:
    info = account.api_get(fields=["name", "currency", "account_status", "timezone_name"])
    status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW", 9: "IN_GRACE_PERIOD"}
    print(f"  Name:     {info.get('name')}")
    print(f"  Currency: {info.get('currency')}")
    print(f"  Timezone: {info.get('timezone_name')}")
    print(f"  Status:   {status_map.get(info.get('account_status'), info.get('account_status'))}")
except Exception as e:
    print(f"  ✗ Could not fetch account details: {e}")

# 4. Token permissions
print("\n[4] Token permissions")
try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.user import User
    me = User(fbid="me").api_get(fields=["name"])
    check("Token is valid", lambda: f"Authenticated as: {me.get('name')}")
except Exception as e:
    print(f"  ✗ Token check failed: {e}")

print("\n" + "─" * 40)
print("If all checks show ✓ you are ready to create ads.\n")
