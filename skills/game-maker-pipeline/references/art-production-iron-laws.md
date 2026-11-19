# 美术资产生成铁律（通用 · v1.8）

> 来源：`crimson-orb-castle-idle` rev1→rev2 血泪教训 + `art/prompt-audit.json`

## 最高原则

**合同登记 = 唯一合法生成入口。** 磁盘上的每张图，都必须能追溯到 `art/art-prompt-registry.json` 的一条完整记录。

---

## 铁律 RE-19～RE-28

| ID | 铁律 | 违反后果 |
|----|------|----------|
| RE-19 | **Registry 全覆盖**：`output_path` 落盘 ↔ `assets[]` 1:1；`forbidden_assets[]` 退役图不得进 game/ | T-ART-04 TERMINATE |
| RE-20 | **Prompt 拼接**：`prompt = style_anchor.prompt_block`（verbatim）+ `asset_delta` + `negative_block`；禁一行摘要 | T-ART-05 |
| RE-21 | **禁 ad-hoc**：禁止会话中临时拼 prompt 绕过 registry | T-ART-05 |
| RE-22 | **Edit 链**：`references[]` 非空 → 必须 `image_edit` 或 parent 已落盘；按 `generation_order` | T-ART-02 |
| RE-23 | **线框≠终稿**：mockup CSS/色块 = `layout_wireframe_only`；须 `art/wireframe-to-pixel-contract.json` | T-ART-03 |
| RE-24 | **Anchor 单调**：`style_anchor.supersedes` 后旧 anchor 资产全部退役，禁止混装 | T-ART-06 |
| RE-25 | **生成验收**：透明底/地平线/anchor_px ±3%；失败 → `art: regen` 禁止 CSS object-fit 硬贴 | T-ART-02 |
| RE-26 | **Prompt 审计**：批量生成后写/更新 `art/prompt-audit.json`（registry + runtime 双轨） | 硬 block pre-ship |
| RE-27 | **Master 对齐**：`match_and_correct.sh` 审计 batch 资产 vs `style-anchor`；漂移 → `image_edit` + `batch_fix_commands.sh` | T-ART-07 |
| RE-28 | **写意 locomotion 默认**：每角色 **1 PNG** + 程序动效（bob/tilt/flipX/squash/shake）；禁无合同生成 walk 多帧 sprite sheet | T-LOC-01/02/03 |

> RE-28 全文：`references/impressionist-character-locomotion.md`

---

## 写意角色（RE-28 · 默认）

- **资产：** 每角色 registry **仅 1 条** `category: character_single_sprite`
- **动画：** runtime `impressionist-sprite.js`（或等价）；**不是** pic gen 批次
- **换向：** `facing ±1` 翻转；**禁止** reverse 图或 walk_01..N.png
- **RE-10 豁免：** 程序 bob/shake/squash 不算「动画资产 phase-2」
- **偏离：** `locomotion: accept sprite_sheet` + 多帧 registry 合同，否则 TERMINATE T-LOC-01

---

## Prompt 拼接公式（强制）

```
full_prompt = {style_anchor.prompt_block} {asset.prompt_delta}
negative    = {style_anchor.negative_block} [+ asset.negative_delta]
```

**asset 字段禁止只写** `COCI-XXX: one line summary`。

**正确示例：**

```json
{
  "asset_id": "CASTLE_T00_RUIN_KEEP",
  "prompt_delta": "ONE modular slice: orthographic side-view ruined gothic keep 96×120px. Ground-aligned flat base at bottom edge. Broken battlements, weathered stone pixel dither.",
  "negative_prompt_ref": "style-anchor.negative_block",
  "references": ["COCI-SILHOUETTE-ANCHOR-v2"],
  "layout_ref": "castle-progression.json#structural_tiers[0].anchor_px",
  "author_layout_ref": "screenshots/author-ref/{pick}-wireframe.jpg"
}
```

---

## 生成顺序（dependency_graph）

1. `style_anchor` 落盘 → gate
2. registry 全量登记（**先登记，后生成**）
3. 按 `generation_order`：base module → derived modules（edit 链）
4. 每资产落盘后跑 `scripts/art_verify.sh`（或手工 checklist）
5. 跑 `scripts/match_and_correct.sh` → `art/art-match-audit.json`（RE-27）
6. 更新 `art/prompt-audit.json`
7. **STOP** → `art: accept | art: regen — {asset_id}`

---

## 线框 → 像素（模块化游戏通用）

| 阶段 | mockup / 白盒 | 终稿 |
|------|---------------|------|
| re_01 / re_07 初版 | HTML/CSS 模块 = **布局合同** | — |
| 作者 pick + whitebox accept | 锁定 anchor_px / attach_edge | — |
| re_06b / post-whitebox | — | registry pic gen 替换 `<img>`，**不改 anchor** |

`wireframe-to-pixel-contract.json` 必填：
- `what_is_locked`：机位、anchor、叠层顺序、出现条件
- `what_is_not_locked`：CSS 几何、纯色材质
- `author_reference`：作者确认的线框截图路径

---

## 模块化剪影类（castle / kingdom / base-builder）

- 主 playfield = **2D 正交侧视**模块叠层（非室内场景 hero）
- 里程碑 + 生产者购买 = **剪影上可见模块 delta**
- 场景板 `image_gen` 整张室内 → **默认禁止**（除非策划案明确）

---

## 验收清单（每张 module）

- [ ] registry 有完整 `prompt_delta` + `references`
- [ ] 运行时 prompt = 合同拼接（记入 audit）
- [ ] 透明底或可抠底（非整图风景）
- [ ] `anchor_px.bottom` 与地面线对齐 ±3%
- [ ] palette 与 `style_anchor.palette_lock` 一致
- [ ] 与同 `anchor_id` 父模块轮廓可拼（目视或叠层测试）

---

## 作者门

```
art: accept
art: regen — {asset_id}[, ...]
art: regen all
```

`art: accept` 后方可替换 game/ 内资产或打入 `.rpc`。