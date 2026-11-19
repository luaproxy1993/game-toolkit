# SuperGrok Imagine Pipeline v1.0

> **Purpose:** Bypass Grok Builder visual weaknesses by making **SuperGrok Imagine** the sole art producer; Builder only runs registry, ingest, verify, and game wiring.

## Iron Law

| Who | May do |
|-----|--------|
| **SuperGrok Imagine** | `image_gen` (master only) + `image_edit` (all derivatives) |
| **Grok Builder** | `supergrok_batch_prompts.py`, `ingest_imagine_assets.py`, `art_verify.sh`, `match_and_correct.sh` |
| **Forbidden in Builder** | Ad-hoc `GenerateImage`, manual `cp` from session folders, promoting unverified assets |

## Flow

```
style-anchor.json (prompt_block + master_reference_path)
        ↓
supergrok_batch_prompts.py → art/supergrok/batch-prompts.md
        ↓
[Human] SuperGrok Imagine — batch ≤5, edit-with-reference
        ↓
art/incoming/{ASSET_ID}.png
        ↓
ingest_imagine_assets.sh --promote
        ↓
art_verify.sh + match_and_correct.sh
        ↓
art: accept → game/ wire
```

## Master Anchor (Batch 0)

1. Generate **one** master in SuperGrok Imagine (`image_gen`, 1:1).
2. Save to `art/master/{ANCHOR_ID}.png`.
3. Set `style-anchor.json` → `master_reference_path`.
4. All sprites: **Imagine Edit** with master uploaded as strong reference.

## Prompt Formula

```
{style_anchor.prompt_block verbatim} {asset.prompt_delta}
Negative: {style_anchor.negative_block} + drift/perspective/warm-tone block
```

## Commands

```bash
# 1. Emit copy-paste prompts
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} prompts

# 2. After dropping PNGs into art/incoming/
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} ingest

# 3. Verify
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} verify
```

## Drift Recovery

If `match_and_correct.sh` exits 2 → use `scripts/batch_fix_commands.sh` prompts in **SuperGrok Edit** (not Builder regen).

## Asset Type Contracts

| Type | Camera | Background | Size |
|------|--------|------------|------|
| survivor_sprite | top_down | transparent PNG | 64×64 feel |
| structural_module | orthographic_side | transparent PNG | per layout_ref |
| sky_plate | fixed horizon | opaque OK | 16:9 screen-space |
| ground_tile | top_down | tileable 128×128 | never full scene tile |
| pickup | top_down | transparent PNG | 32×32 feel |