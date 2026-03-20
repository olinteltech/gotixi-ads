# Create GoTixi Meta Ad (Full Workflow)

End-to-end orchestrator skill for creating a GoTixi Facebook/Instagram ad.
Runs the full pipeline: brief → brand-safe copy → approval → Meta API.

---

## Progress Tracker

Show this checklist at the start and update it as each step completes:

```
[ ] Brief received & validated
[ ] On-brand copy generated
[ ] Copy approved by user
[ ] Meta API calls executed
[ ] Ad created (PAUSED) ✓
```

---

## Step 1 — Parse Brief from $ARGUMENTS

Expected format: `"destination · audience_segment · offer · image_path"`

Example: `"Bali · couples · 7-night romantic itinerary · /tmp/bali.jpg"`

Extract:
- **destination** (string)
- **audience_segment** (must be one of: `families`, `couples`, `solo_explorers`, `adventurers`, `luxury_travelers`, `first_timers`)
- **offer** (string — no price framing)
- **image_path** (string — local file path)

If any field is missing or ambiguous, ask for it before continuing.

Validate that the image file exists:
```bash
ls -lh <image_path>
```

If the file doesn't exist, ask the user to provide the correct path.

---

## Step 2 — Confirm Brief

Show the user a summary and ask for confirmation before generating copy:

```
Brief Summary:
  Destination:  [destination]
  Audience:     [audience_segment]
  Offer:        [offer]
  Image:        [image_path] ([file size])

Proceed to generate ad copy?
```

---

## Step 3 — Generate Copy

Invoke `/generate-ad-copy` with the brief fields:

```
/generate-ad-copy "[destination] · [audience_segment] · [offer] · [image_path]"
```

This will load the brand guidelines and produce 3 on-brand copy variants for approval.

**Wait here. Do not proceed until the user selects and approves a copy variant.**

Update checklist: `[x] On-brand copy generated`

---

## Step 4 — Copy Approval Gate

Once the user approves a variant, confirm the final `ad_params.json` block is ready.

Update checklist: `[x] Copy approved by user`

Ask: "Ready to create the ad? I'll run the Meta API now."

**Wait for explicit confirmation.**

---

## Step 5 — Execute API

Invoke `/launch-ad` with the approved params JSON.

Update checklist: `[x] Meta API calls executed`

---

## Step 6 — Final Status

On success, update the checklist:
```
[x] Brief received & validated
[x] On-brand copy generated
[x] Copy approved by user
[x] Meta API calls executed
[x] Ad created (PAUSED) ✓
```

Display the campaign, ad set, creative, and ad IDs.

Remind the user: "All objects are PAUSED. Review in Ads Manager before going live."

---

## Optional Arguments

You can also pass a pre-built JSON file instead of a brief string:

```
/create-ad path/to/ad_brief.json
```

In this case, read the JSON, validate it against `schemas/ad_brief.schema.json`, and skip to Step 3.
