# GoTixi Ads — Claude Instructions

This repo contains code, Claude skills, and creative generation pipelines for producing GoTixi ads.

## Skills

### `/brand-guidelines`
Run this skill at the start of any ad, copy, or creative generation task. It loads the complete GoTixi brand system — colors, typography, voice, audiences, photography direction, and positioning — so every output stays on-brand.

```
/brand-guidelines
```

**Always invoke this before:**
- Writing ad copy or headlines
- Generating HTML/CSS ad layouts
- Briefing image generation prompts
- Creating social media posts or email creative

## Brand Files

| File | Purpose |
|---|---|
| `brand/guidelines.html` | Full brand bible (rendered HTML) |
| `brand/design-system.md` | Concise ad-ready reference (quick lookup) |
| `.claude/commands/brand-guidelines.md` | The `/brand-guidelines` skill |

## Key Brand Rules (Quick Reference)

- Brand name: **GoTixi** (capital G, capital T — always)
- Primary color: `#F08802` Sunset Orange
- Dark color: `#323729` Forest Green
- Headlines: **Volkhov** serif · Body: **Poppins** · Labels: **Inter** · Accent: **Caveat**
- Voice: warm knowledgeable friend — never hype, never price-led
- Never call GoTixi an OTA or booking platform
- Customers are called **Ducklings**

## Repo Structure

```
brand/
  guidelines.html       # Full brand bible
  design-system.md      # Ad-ready design system reference
.claude/
  commands/
    brand-guidelines.md # /brand-guidelines skill
CLAUDE.md               # This file
README.md
```
