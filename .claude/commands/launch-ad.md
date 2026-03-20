# Launch GoTixi Meta Ad

Execute the Meta API calls to create a fully structured ad from approved parameters.
**Only run this after copy has been approved via `/generate-ad-copy`.**

---

## Step 1 — Receive Approved Params

The input should be a JSON block conforming to `schemas/ad_params.schema.json`.

If `$ARGUMENTS` contains a file path ending in `.json`, read that file.
Otherwise, expect the JSON to be pasted directly in the conversation.

Confirm with the user:
- Campaign name
- Audience segment
- Headline (show it)
- Daily budget (INR)
- Image path (confirm file exists with `ls`)

Ask: "Ready to create this ad? All objects will be created in PAUSED status."

Wait for explicit confirmation before proceeding.

---

## Step 2 — Write Params to Temp File

Write the approved JSON to `/tmp/gotixi_ad_params_<timestamp>.json`.

Use the current timestamp (YYYYMMDD_HHMMSS) in the filename to avoid collisions.

---

## Step 3 — Run the Script

```bash
python3 meta/create_full_ad.py /tmp/gotixi_ad_params_<timestamp>.json
```

Stream stderr to the user so they can see the progress steps (image upload, campaign, ad set, creative, ad).

---

## Step 4 — Handle the Result

**On success** (exit code 0), parse the JSON from stdout and display:

```
✓ Ad created successfully — all objects PAUSED

Campaign ID:  [id]
Ad Set ID:    [id]
Creative ID:  [id]
Ad ID:        [id]

→ Review and activate at: https://www.facebook.com/adsmanager/
```

**On failure** (exit code 1), read the JSON from stderr and display the error message clearly.

Common fixes by error code:
- **190** — Access token expired. Run: `META_ACCESS_TOKEN=<new_token>` in .env, then retry.
- **100** — Invalid parameter in ad_params.json. Check field values against the schema.
- **278 / 200** — Permission error. Ensure token has `ads_management` and `manage_pages` permissions.
- **368** — Ad account restricted. Check Meta Business Manager for policy violations.

If partial objects were created (shown in the error JSON), list their IDs so the user can clean up in Ads Manager.

---

## Step 5 — Reminder

Always close with:

> All objects are in **PAUSED** status. Nothing is live. Go to Meta Ads Manager to review creative, check targeting, set your schedule, and activate when ready.
