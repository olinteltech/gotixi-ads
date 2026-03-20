# GoTixi Ads — Claude Instructions

This repo contains code, Claude skills, and creative generation pipelines for producing GoTixi Meta ads.

---

## Skills

### `/create-ad` — Full ad creation workflow (start here)
End-to-end orchestrator. Pass a brief and it handles everything: copy generation, approval gate, Meta API execution.

```
/create-ad "Bali · couples · 7-night romantic itinerary · /tmp/bali.jpg"
```

Or pass a JSON brief file:
```
/create-ad path/to/ad_brief.json
```

### `/generate-ad-copy` — Generate on-brand copy only
Loads brand guidelines, produces 3 copy variants (headline, body, description), waits for approval. Use this standalone when you want to iterate on copy before committing to an API call.

```
/generate-ad-copy "Switzerland · luxury_travelers · private alpine experiences · /tmp/alps.jpg"
```

### `/launch-ad` — Execute Meta API from approved params
Takes a `schemas/ad_params.schema.json`-conforming JSON block and runs the full pipeline: upload image → campaign → ad set → creative → ad. All objects created PAUSED.

```
/launch-ad path/to/ad_params.json
```

### `/brand-guidelines` — Load full design system
Always invoked automatically by `/create-ad` and `/generate-ad-copy`. Run manually when you need brand context for any other task.

---

## Rules for All Ad Work

**Always:**
- Run `/brand-guidelines` (or use a skill that invokes it) before writing any copy or designing any layout
- Write "GoTixi" — capital G, capital T — in all content
- Use Sunset Orange `#F08802` for CTAs and Forest Green `#323729` for dark backgrounds
- Use Volkhov for headlines, Poppins for body, Caveat for one accent tagline max
- Lead with human expertise, not technology
- Speak warm, confident, calm — first-person plural ("We curate…", "Our team…")

**Never:**
- Lead with price, discounts, or "cheapest" framing
- Use ALL CAPS in body copy or exclamation overload
- Call GoTixi an OTA or booking platform (we are a travel partner)
- Use blues, purples, or any non-brand accent colors
- Create ads in ACTIVE status — always start PAUSED

---

## Workflow

```
User runs /create-ad with brief
        │
        ▼
/generate-ad-copy
  → loads /brand-guidelines
  → generates 3 variants
  → user approves
        │
        ▼
/launch-ad
  → validates JSON against schemas/ad_params.schema.json
  → python3 meta/create_full_ad.py <params.json>
      → upload_image      → image_hash
      → create_campaign   → campaign_id
      → create_ad_set     → ad_set_id
      → create_ad_creative → creative_id
      → create_ad         → ad_id
  → all PAUSED, IDs printed
```

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN,
# META_AD_ACCOUNT_ID (with act_ prefix), META_PAGE_ID
```

---

## Brand Files

| File | Purpose |
|---|---|
| `brand/guidelines.html` | Full brand bible (rendered HTML) |
| `brand/design-system.md` | Concise ad-ready reference |
| `schemas/ad_brief.schema.json` | Input brief schema |
| `schemas/ad_params.schema.json` | Ad params schema (Claude → Python contract) |

## Python Modules

| File | Purpose |
|---|---|
| `meta/client.py` | SDK init, credentials from env |
| `meta/upload_image.py` | Image pre-validation + upload → hash |
| `meta/create_campaign.py` | Campaign creation (always PAUSED) |
| `meta/create_ad_set.py` | Ad set + targeting, segment presets |
| `meta/create_ad_creative.py` | Creative from copy + image hash |
| `meta/create_ad.py` | Final ad object (always PAUSED) |
| `meta/create_full_ad.py` | Orchestrator — run this from CLI |

---

## Key Brand Quick Reference

| Element | Value |
|---|---|
| Primary color | `#F08802` Sunset Orange |
| Dark color | `#323729` Forest Green |
| Headline font | Volkhov (serif) |
| Body font | Poppins |
| Label font | Inter (ALL CAPS, letter-spacing 3–4px) |
| Accent font | Caveat (max 1 per layout) |
| Brand name | **GoTixi** (capital G, capital T) |
| Customers | Ducklings |
| Voice | Warm knowledgeable friend — never hype |
| Entry price | ₹75,000 |
| Target market | Indian international travelers |
