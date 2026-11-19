# 血泪教训（vampire-blood-castle-idle · crimson-orb-castle-idle）

## 美术

| 失败做法 | 后果 |
|----------|------|
| 每档 image_gen 新角度城堡 | 视角不一致，无法当合同 |
| 零碎 tower layer 硬贴 | 透视/像素网格不匹配 |
| 室内王座厅整场景作主视觉，城堡仅窗外剪影 | **核心爽点浪费**（T-ART-03） |
| registry 一行摘要 + 会话临时拼 prompt | 偷懒、气质漂移、无法审计（T-ART-05） |
| registry 7 条、磁盘 17 张图 | 合同与执行脱节（T-ART-04） |
| v1 室内 anchor 与 v2 剪影 anchor 混装 | 法球/图标/模块气质打架（T-ART-06） |
| 说 transparent bg 不验收，CSS object-fit 硬贴 | 叠层糊弄（T-ART-02） |
| 抽象 wireframe 当 mockup 终稿品质 | 违反 RE-13 / RE-23 |
| 为 survivor 小人生成 walk×方向×帧 sprite sheet | AI 帧间漂移、token 爆炸；改用 **RE-28 单图写意** |
| 背景强行拆血月+多层云 PNG 指望 AI 对齐 | 透视/网格对不上；用 scene_plate 或 CSS 程序化 |

## 角色 locomotion（RE-28 · 合法路径）

1. mockup 中 1 个小人 → `animation_model: impressionist_single_sprite`
2. registry 1 PNG → `game/impressionist-sprite.js` bob/tilt/flipX
3. 攻击/受击用 squash/shake，**不**加 attack_02.png
4. 仅格斗/平台跳跃类才申请 `locomotion: accept sprite_sheet`

## 策划

| 失败做法 | 后果 |
|----------|------|
| 仅 idea-brief 几段 JSON | 模型漂移无约束 |
| 无 TERMINATE 码 | 偏差无法机械停止 |

## 合法路径（v1.8+）

1. Design Bible ≥99 页 + constitution: accept
2. **mockup_mode 选型**：`layout_wireframe`（剪影扩建）| `scene_plate`（单场景气质）
3. 线框 mockup = 布局合同 → `wireframe-to-pixel-contract.json`
4. **先 registry 全量登记** → 按 `generation_order` pic gen / image_edit
5. **prompt = prompt_block + prompt_delta + negative**（RE-20）
6. `art_verify.sh` + `prompt-audit.json` → `art: accept` → ship
7. HTML 叠层 UI 文字；模块用透明 PNG 替换线框，**anchor 不漂移**