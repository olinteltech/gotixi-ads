# Generate GoTixi Ad Copy

Generate on-brand Meta ad copy for GoTixi. Always invokes brand guidelines before writing a single word.

---

## Step 1 — Load Brand Guidelines

Run `/brand-guidelines` now to load the full GoTixi design system into context before generating any copy.

---

## Step 2 — Parse the Brief

Extract these four fields from `$ARGUMENTS` (format: `"destination · audience_segment · offer · image_path"`):

- **destination** — e.g. "Bali", "Switzerland", "Japan"
- **audience_segment** — one of: `families`, `couples`, `solo_explorers`, `adventurers`, `luxury_travelers`, `first_timers`
- **offer** — the experience angle (no price framing)
- **image_path** — local path to the ad image

If any field is missing, ask for it before proceeding.

---

## Step 3 — Generate 3 Copy Variants

For each variant, produce all four copy fields. Apply every rule below — no exceptions.

### Headline rules (max 40 chars — count carefully)
- Warm friend voice, not corporate
- No exclamation marks
- No price, discount, or "deal" language
- No ALL CAPS
- Should evoke the destination or feeling, not the product
- Volkhov-feel: editorial, authoritative, slightly poetic

### Primary text rules (max 125 chars)
- Lead with the destination or experience, not the company
- End with a soft directional cue (not a hard sell)
- First-person plural where brand appears: "We…", "Our team…"
- No "Book NOW", no "Limited time", no "!"
- Confident and calm — demonstrate value, don't shout it

### Description rules (max 30 chars)
- Reinforces quality, curation, or peace of mind
- Never price, discount, or "cheapest"

### CTA — pick the most appropriate:
`LEARN_MORE` · `BOOK_TRAVEL` · `CONTACT_US` · `GET_QUOTE` · `SIGN_UP`

---

## Step 4 — Output Format

For each variant output a labeled JSON block:

```json
{
  "variant": 1,
  "headline": "...",
  "primary_text": "...",
  "description": "...",
  "call_to_action": "LEARN_MORE"
}
```

After all 3 variants, show a character count table:

| Field | V1 | V2 | V3 | Limit |
|---|---|---|---|---|
| headline | N | N | N | 40 |
| primary_text | N | N | N | 125 |
| description | N | N | N | 30 |

---

## Step 5 — Wait for Approval

Ask: "Which variant would you like to use? Or describe any changes."

**Do not proceed to ad creation until the user explicitly approves a variant.**

Once approved, output the final complete `ad_params.json` block ready for `/launch-ad`:

```json
{
  "headline": "...",
  "primary_text": "...",
  "description": "...",
  "call_to_action": "...",
  "campaign_name": "GoTixi — [Destination] — [YYYY-MM]",
  "ad_set_name": "[Destination] · [audience_segment] · [YYYY-MM-DD]",
  "ad_name": "[Destination] · [audience_segment] · V[N]",
  "image_path": "...",
  "audience_segment": "...",
  "daily_budget_inr": 500,
  "campaign_objective": "OUTCOME_TRAFFIC",
  "targeting": {
    "countries": ["IN"],
    "age_min": 25,
    "age_max": 55,
    "genders": []
  }
}
```

Tell the user: "Pass this JSON to `/launch-ad` when you're ready to create the ad."
