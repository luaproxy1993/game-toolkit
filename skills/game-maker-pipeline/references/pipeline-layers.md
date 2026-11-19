# RE 流水线层（Reverse-Engineering-Game-Pipeline.json v1.8.1）

| 层 | Gate | 产出 |
|----|------|------|
| db_00 design_bible | constitution: accept | production/design-bible/ |
| re_00a intent | intent: accept | gamer-brief, idea-brief |
| re_00b gdd_art | gdd: accept | gdd/, art/style-anchor, art-prompt-registry shell |
| re_01 screenshot | — | mockup gallery（wireframe 或 scene_plate） |
| re_02 author_pick | screenshot: pick v0X | author-selection |
| re_03 reverse_extract | — | screenshot-spec |
| re_04 logic_derive | — | interaction-spec, state-machine |
| re_05 scope | scope: accept | gameplay-spec |
| re_06 asset_decompose | — | asset-decomposition |
| **re_06b art_production** | **art: accept** | pixel modules, prompt-audit |
| re_07 whitebox | whitebox: accept | game/（可先 wireframe） |
| re_08 playtest | playtest: accept | playtime-regression |
| re_09 ship | art_verify PASS | .rpc |

## RE 硬规则摘要（v1.8）

RE-01 可玩态静帧 · RE-14 HTML 文案 · RE-15 禁灰占位 · RE-16 true_gamer  
**RE-19 registry 1:1 · RE-20 prompt 拼接 · RE-21 禁 ad-hoc · RE-22 edit 链**  
**RE-23 线框≠终稿 · RE-24 anchor 单调 · RE-25 生成验收 · RE-26 prompt-audit · RE-27 master-match**  
**RE-28 写意单图角色**（bob/tilt/flipX；禁默认 sprite sheet）

详见 `art-production-iron-laws.md` · 角色：`impressionist-character-locomotion.md`