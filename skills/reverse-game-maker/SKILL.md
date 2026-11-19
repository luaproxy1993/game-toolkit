---
name: reverse-game-maker
description: >-
  Run the Reverse Engineering Game Maker pipeline: generate functional UI
  screenshots, wait for author pick, reverse-extract specs (hotspots, content
  slots, state machine), build screenshot-driven whitebox. Use when the user
  asks for reverse engineering game maker, screenshot-first pipeline,
  /reverse-game-maker, or 截图反推游戏制作.
argument-hint: "[project_path] [layer_id]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task, TodoWrite
---

# Reverse Engineering Game Maker

Orchestrator for **screenshot-first** game production. Spec reads `grokmaker/Reverse-Engineering-Game-Pipeline.json`.

## Invocation

```
/reverse-game-maker
/reverse-game-maker grokmaker/my-game
/reverse-game-maker grokmaker/my-game re_layer_03_reverse_extract
```

| Argument | Meaning |
|----------|---------|
| `project_path` | Dir with `pipeline_state.json` and `pipeline_id: reverse-engineering-game-pipeline` |
| `layer_id` | Optional override to run one layer (must respect gates) |

**New project:**

```bash
cd grokmaker && ./reverse-game-template/scripts/init_project.sh {slug}
```

## Tool-Call Discipline

1. Session start: read `Reverse-Engineering-Game-Pipeline.json` + project `pipeline_state.json`
2. **Never** advance past a ★ gate without author explicit reply
3. **Never** write `gameplay-spec` before `screenshot-spec` exists
4. **Never** implement features listed only in `phase_2_features`
5. **Never** ship grey-box/placeholder diegetic elements (cards, icons, frames) — RE-15 aesthetic contract
6. re_layer_03: **must** image-read `author-selection` primary image
7. re_00: true_gamer expands author vague input → 策划案; never skip to re_01 without `intent: accept`
8. End at gates with STOP + gate prompt

## Todo Scaffold

- `load` — read pipeline spec + state
- `layer-work` — execute current layer tasks
- `preflight` — disk + schema checks
- `preview` — HTTP gallery or game smoke
- `checkpoint` — update pipeline_state + session-state
- `report` — author-facing STOP

## Layer Runner

### re_layer_00_intent

**true_gamer 拓展策划案** — 作者常给笼统词；本层禁止直抄进 `idea-brief` 就进 re_01。

1. **存档** `author_raw_input`（作者原文/JSON，一字不漏）
2. **true_gamer 推断**：`primary_archetype`、2–5 `exemplar_works`（steal UI / avoid 剧情 IP）
3. **re_00a 拓展笼统词** → 专业字段，写入 `idea-brief.json#策划案`：
   - `elevator_pitch`、`core_loop`（≥3 步）、`player_role`、`emotional_tone`
   - `setting`、`narrative_lock`（谁在哪、为何 UI 合理）
   - `systems_phase_1`（mockup 合同）vs `systems_phase_2`（默认不做）
   - `must_have_ui_blocks`、`exemplar_steal`、`exemplar_reject`
4. 写 `gamer-brief.json`（含 `expansion_log`）
5. **STOP intent gate** — `intent: accept | intent: revise — {note}`

**re_00b GDD + 美术合同（RE-17/RE-18，re_01 前硬门槛）**

6. 写 `art/style-anchor.json` + `art/art-prompt-registry.json`（`prompt_delta` + `references[]` + `verification`；RE-19～26 见 `game-maker-pipeline/references/art-production-iron-laws.md`）
7. 写 `gdd/` 全套满足 `gdd_minimum_contract`（economy/producers/upgrades/combo/tick/input/ui-binding/narrative/state-machine-draft/content-slots-draft + `gdd/MANIFEST.json`）
8. 合并 `gdd_manifest` + `art_prompt_contract` 入 `idea-brief.json#策划案`
9. 写 `visual-scan/true-gamer-intent-expansion.json`
10. 填 `aesthetic_tokens`；写 `re_workflow_hints.mockup_variant_hints`
11. **STOP gdd gate** — `gdd: accept | gdd: revise — {note}`

- On intent accept: stay re_00 → run re_00b
- On gdd accept: advance → `re_layer_01_screenshot_gen`（或若 mockup 已存在 → `re_layer_02_author_pick`）
- On revise: stay re_00b, merge note into `expansion_log`

### re_layer_01_screenshot_gen

- **Preflight:** `gdd_minimum_contract` PASS + `art_prompt_contract` PASS（RE-17/RE-18）；选定 `mockup_mode`: layout_wireframe | scene_plate
- **Read first:** `gamer-brief.json` + `idea-brief.json#策划案` + `gdd/MANIFEST.json` + `art/art-prompt-registry.json`
- Generate 3–6 variants → `screenshots/variants/`
- Update `screenshot-gen-manifest.json` + `screenshots/gallery.html`
- Contract: 640×480, functional UI visible, **no device chrome**
- **Author-facing**: concrete game screenshot mockups (`v0X-mockup.jpg` or scene plate + UI composite) — humans must read game structure from the image, not abstract canvas wireframes
- **Machine-facing**: `screenshot-structure-spec.json` + composite HTML overlay for exact text/hotzones (exemplar remix: Coffee Talk / VA-11 / Lofi)
- **Each variant requires `mockup-briefs.json` entry first** (who/where/why UI makes sense); mockup copy grows from brief
- Steal exemplar **UI layout only** — never steal shop/customer narrative (e.g. Coffee Talk café → private kitchen = inner monologue not 阿姨/客人)
- Pipeline: (1) aesthetic_tokens (2) brief + per-variant aesthetic_theme (3) image_gen scene plate (4) image_gen diegetic art (cards/icons, no text) (5) HTML UI overlay with aesthetic-matched frames (6) gallery
- **RE-15**: every visible element matches unified game aesthetic — card faces, HUD, icons, frames share scene palette; no deferring look to re_06
- Do **not** ship image_gen JPG with baked dialogue text (garbles / invents wrong NPCs)
- Use `imagine` skill: image_gen for scenes + creature/portrait art; HTML/CSS for frames, stats, exact copy
- Set `awaiting_author_gate` = `re_layer_02_author_pick`
- **STOP** — present gallery URL

### re_layer_02_author_pick

- **HALT until** `screenshot: pick {id}` or `screenshot: revise — {note}`
- On pick: write `author-selection.json`, clear gate, advance to re_03
- On revise: back to re_01 with note

### re_layer_03_reverse_extract

- Image-read primary + any state variants
- Fill `screenshot-spec.json` per artifact schema
- Write `visual-scan/reverse-scan.json`
- Advance to re_04

### re_layer_04_logic_derive

- Fill `interaction-spec.json`, `content-slots.json`, `state-machine.json`
- Use `scripts/reverse_extract_checklist.md`
- Unseen features → `phase_2_features` only
- Advance to re_05, set gate

### re_layer_05_scope_contract

- Derive `delivery-contract.json`, `content-units-tracker.json`, `gameplay-spec.json` from slots
- **STOP** — `scope: accept | scope: revise — {note}`

### re_layer_06_asset_decompose

- Fill `asset-decomposition.json`
- Prefer `html_css_diegetic` for UI planks

### re_layer_06b_art_production ★

- 铁律 RE-19～26：`art-production-iron-laws.md`
- 全量 registry → `generation_order` pic gen / image_edit
- `scripts/art_verify.sh` + `art/prompt-audit.json`
- **STOP** — `art: accept | art: regen — {asset_id}`

### re_layer_07_whitebox

- Implement `game/` matching anchors ±3%
- Bind hotspots from `interaction-spec.json`
- `./scripts/serve.sh` smoke
- **STOP** — `whitebox: accept | whitebox: revise — {note}`

### re_layer_08_playtest

- Fill `playtime-regression.json`
- **STOP** — `playtest: accept | playtest: revise — {note}`

### re_layer_09_ship

- Preflight: `art_verify.sh` PASS + `art: accept` on record
- Package `.rpc` per target spec

## Preflight (each layer)

| Check | FAIL action |
|-------|-------------|
| `pipeline_id` matches | STOP |
| Prior gate decisions set | STOP |
| Expected files on disk (`ls`) | `blocked_note` |
| re_01: no placeholder diegetic art (RE-15) | back to re_01 |
| re_00: gamer-brief + idea-brief.策划案 on disk | STOP |
| re_01: gamer-brief exists; idea-brief.策划案 not empty | `blocked_note` |
| re_01: aesthetic_tokens + variant aesthetic_theme on disk | `blocked_note` |
| re_03: screenshot-spec ui_regions non-empty | STOP |
| re_07: game/index.html exists | STOP |

## Migration from Text2Game

If user has existing mockups (e.g. `mockups/combo-*.jpg`):

1. Copy to `screenshots/variants/`
2. Fill `author-selection.json` as if re_02 passed
3. Start at `re_layer_03_reverse_extract`
4. Set `pipeline_state.pipeline_id` to reverse-engineering

## Author Gate Quick Reference

| Layer | Accept |
|-------|--------|
| re_00a | `intent: accept` |
| re_00b | `gdd: accept` |
| re_02 | `screenshot: pick v01` |
| re_05 | `scope: accept` |
| re_07 | `whitebox: accept` |
| re_08 | `playtest: accept` |

## Session Checkpoint

Write `production/session-state/active.md` after each layer:

```markdown
# RE Session — {date}
- layer: {current}
- gate: {awaiting or none}
- primary_screenshot: {path}
- next: {one line}
```