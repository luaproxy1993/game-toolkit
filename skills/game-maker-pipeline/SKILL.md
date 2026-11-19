---
name: game-maker-pipeline
description: >-
  v1.8.1 game production orchestrator: Design Bible (≥99p) + RE pipeline (intent
  → mockup → reverse-extract → art production RE-19~28 → whitebox → ship .rpc).
  Art iron laws: registry 1:1, prompt_block+prompt_delta, no ad-hoc pic gen,
  wireframe-to-pixel contract, master-anchor match (RE-27), impressionist single-sprite
  locomotion (RE-28). Use for /game-maker-pipeline, 游戏制作, 策划案,
  design bible, screenshot-first RP Pocket idle/incremental games.
argument-hint: "[project_path] [layer_id]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task, TodoWrite
---

# Game Maker Pipeline v1.8.1

**截图反推 + 强框架策划案 + 美术铁律 RE-19～28 + 写意角色 locomotion + 偏差终止**

## 固定工作区（勿重装）

| 常量 | 值 |
|------|-----|
| `GROKMAKER_ROOT` | `/Users/a123/grokmaker` |
| Skill 源 | `{GROKMAKER_ROOT}/game-maker-pipeline/` |
| 项目根 | `{GROKMAKER_ROOT}/{slug}/` |
| Grok 入口 | `~/.grok/skills/game-maker-pipeline` → **符号链接**（非副本） |

**Session 规则（强制）：**
- **禁止**解压 `game-maker-pipeline-v1.8-skill.tar.gz`
- **禁止**每会话 `rsync` / 覆盖安装 skill
- 读写在 `{GROKMAKER_ROOT}` 完成；`references/`、`scripts/` 一律用绝对路径或 `{GROKMAKER_ROOT}/game-maker-pipeline/...`
- 仅当链接断裂时跑一次：`{GROKMAKER_ROOT}/game-maker-pipeline/scripts/sync_skill.sh`（创建 symlink，不复制）

| 组件 | 路径 |
|------|------|
| 机器规格 v1.8 | `references/Reverse-Engineering-Game-Pipeline.v1.8.json` |
| 美术铁律 | `references/art-production-iron-laws.md` |
| 层速查 | `references/pipeline-layers.md` |
| 血泪教训 | `references/lessons-learned.md` |
| **写意角色 locomotion** | `references/impressionist-character-locomotion.md` |
| Registry 模板 | `references/art-prompt-registry.TEMPLATE.json` |
| 线框合同模板 | `references/wireframe-to-pixel-contract.TEMPLATE.json` |
| 脚手架 | `scripts/scaffold_project.sh` |
| 圣经生成 | `scripts/generate_design_bible.py` |
| 美术验收 | `scripts/art_verify.sh` |
| Master 对齐 (RE-27) | `scripts/match_and_correct.sh` |
| **SuperGrok Imagine 批量** | `scripts/supergrok_imagine.sh` |
| 出货打包 | `scripts/ship.sh` |

## Invocation

```
/game-maker-pipeline
/game-maker-pipeline grokmaker/my-game
/game-maker-pipeline grokmaker/my-game re_layer_06b_art_production
```

## 最高原则

1. **圣经 > idea-brief > 模型常识** — TERMINATE（T-DOC-01）。`/world-bible` 是气质种子，不是本管线的 ≥99p Design Bible；re_00 可引用，不可替代。
2. **★ 门** — 无作者显式回复不得前进
3. **RE-19～27 美术铁律** — `references/art-production-iron-laws.md`
4. **mockup 线框 ≠ 终稿** — 像素替换走 `art/wireframe-to-pixel-contract.json`
5. **没写在策划案/mockup 里的不做**
6. **角色默认写意单图**（RE-28）— 1 PNG + bob/tilt/flipX/squash/shake；禁擅自扩 sprite sheet

## 写意角色表意（RE-28 · 默认 locomotion）

> 详见 `references/impressionist-character-locomotion.md`

| 工业做法 | 本流水线默认 |
|----------|----------------|
| 多方向 walk 帧 | **1 张图** |
| 转身动画 | **scaleX 翻转** |
| 上下朝向 | **去掉**（俯视/侧视锁死） |
| 走路 | **sin bob + tilt** |
| 受击/攻击 | **shake / squash**（代码，非资产） |

**Session 必读：** re_00 写 GDD 时登记 `character_locomotion.model: impressionist_single_sprite`。  
**RE-10 豁免：** 上述程序动效不算「动画资产 phase-2」。  
**偏离默认：** 须 `locomotion: accept sprite_sheet` + registry 多帧合同，否则 T-LOC-01。

## Session Bootstrap

```
GROKMAKER_ROOT=/Users/a123/grokmaker   # 或读 {GROKMAKER_ROOT}/.grokmaker-root
SKILL_ROOT={GROKMAKER_ROOT}/game-maker-pipeline

load:
  - {SKILL_ROOT}/references/Reverse-Engineering-Game-Pipeline.v1.8.json
  - {GROKMAKER_ROOT}/{slug}/pipeline_state.json
  - {GROKMAKER_ROOT}/{slug}/production/design-bible/MANIFEST.json (若存在)
  - {SKILL_ROOT}/references/art-production-iron-laws.md
  - {SKILL_ROOT}/references/impressionist-character-locomotion.md
preflight:
  - 不检查/不安装 tar.gz；不跑 sync 除非链接断裂
  - pipeline_id === reverse-engineering-game-pipeline
  - pipeline_version >= 1.8.0 或项目 revision 对齐
```

## 作者门速查（v1.8）

| 阶段 | Accept |
|------|--------|
| db_00 | `constitution: accept` |
| re_00a | `intent: accept` |
| re_00b | `gdd: accept` |
| re_02 | `screenshot: pick v01` |
| re_05 | `scope: accept` |
| re_06b | `art: accept` |
| re_07 | `whitebox: accept` |
| re_08 | `playtest: accept` |

## re_01 mockup 双模式

| 模式 | 何时 | re_01 做法 |
|------|------|------------|
| `layout_wireframe` | 剪影/城堡扩建/模块化主反馈 | HTML/CSS 线框锁 anchor；**禁**室内整场景 image_gen 作主视觉 |
| `scene_plate` | VN/小店单场景气质 | registry 先行 → 场景板 + HTML UI |

## re_06b 美术生产（铁律摘要）

```
1. art-prompt-registry.json 全量登记（prompt_delta + references + verification）
2. prompt = style_anchor.prompt_block + asset.prompt_delta + negative_block
3. 按 generation_order；references[] → image_edit
4. grokmaker/game-maker-pipeline/scripts/art_verify.sh {project}
5. grokmaker/game-maker-pipeline/scripts/match_and_correct.sh {project}
6. art/prompt-audit.json 双轨审计
7. STOP → art: accept | art: regen — {asset_id}
```

**禁止：** ad-hoc 临时 prompt · registry 一行摘要 · v1/v2 anchor 混装 · object-fit 硬贴

## RE-27 Master 对齐（art-asset-matcher-v1.0）

批量资产生成后，以 `art/style-anchor.json` 为唯一真理源审计漂移：

```bash
grokmaker/game-maker-pipeline/scripts/match_and_correct.sh grokmaker/{slug}
# 或项目内：
cd grokmaker/{slug} && ./scripts/match_and_correct.sh
```

**容差：** anchor_px ±3% · palette Euclidean < 15 · orthographic side view · ground_line bottom aligned

**输出：**
- `art/art-match-audit.json` — 每张资产的 `issues_detected` + `correction_prompt_delta`
- `scripts/batch_fix_commands.sh` — `image_edit` 修复指令（master reference 必附）

**退出码：** `0` = 全通过 · `2` = 有漂移（按 batch_fix 修正后重跑）

剪影/城堡模块（`screenshots/silhouette/`）额外检查：透明底、地平线对齐、palette 亮度。

## SuperGrok Imagine Pipeline v1.0（推荐美术生产）

**Builder 禁止直接 GenerateImage 进 registry。** 用 SuperGrok Imagine 生产，Builder 只跑脚本。

```bash
# 1. 生成可复制 prompt 包
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} prompts

# 2. SuperGrok Imagine：每批 ≤5，master image_gen，其余 image_edit + reference
#    落盘：art/incoming/{ASSET_ID}.png

# 3. 导入 + 晋升到 registry output_path
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} ingest

# 4. 验收
grokmaker/game-maker-pipeline/scripts/supergrok_imagine.sh grokmaker/{slug} verify
```

详见 `references/supergrok-imagine-pipeline.md`

## re_09 ship

```bash
grokmaker/game-maker-pipeline/scripts/art_verify.sh grokmaker/{slug}
grokmaker/game-maker-pipeline/scripts/match_and_correct.sh grokmaker/{slug}
grokmaker/game-maker-pipeline/scripts/ship.sh grokmaker/{slug}
# 或项目内（scaffold 已复制）：
cd grokmaker/{slug} && ./scripts/art_verify.sh && ./scripts/match_and_correct.sh && ./scripts/ship.sh
```

Preflight: `art: accept` + `art_verify` PASS + `match_and_correct` PASS（RE-27）

## 新项目

```bash
grokmaker/game-maker-pipeline/scripts/scaffold_project.sh my-slug
# 或显式根目录：
grokmaker/game-maker-pipeline/scripts/scaffold_project.sh my-slug /Users/a123/grokmaker
# 编辑 idea-brief author_raw_input
# /game-maker-pipeline grokmaker/my-slug
```

## 子代理委派

```
- layer: {re_layer_XX} only
- art: references/art-production-iron-laws.md
- locomotion: references/impressionist-character-locomotion.md (RE-28 default)
- forbidden: ad-hoc pic gen, one-line prompts, anchor mix, wireframe as final art, walk frame sheets without sprite_sheet contract
- match: scripts/match_and_correct.sh → art/art-match-audit.json
- on_violation: TERMINATE T-ART-04/05/06/07
```