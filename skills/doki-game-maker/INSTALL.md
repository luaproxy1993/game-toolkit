# doki-game-maker v2.4

## 位置

`~/.grok/skills/doki-game-maker/SKILL.md`

## 调用

- `/doki-game-maker`
- `/doki-game-maker new my-slug dating-calendar`
- `/doki-game-maker new my-slug stream-r1` · `r1` · `r1-scaffold` · `r1-host-doc`
- `/doki-game-maker r2-prompt`
- `/doki-game-maker seed` · `r1-seed`
- `/doki-game-maker new my-slug stream-r1-game` · `dh-game` · `digital-human-game`
- `/doki-game-maker frontend` · `export-static` · `handoff` · `wild`

## 依赖工作区

优先：`/Users/a123/grokmaker/Dokiworlddevwong`  
或环境变量 `DOKI_WORKSPACE`。

## 关联 skill

| 需求 | Skill |
|------|--------|
| Dokiworld 卡带 / pack / 点卡进游戏 | **doki-game-maker** |
| 数字人 × 完整 game 同页 | **doki-game-maker** + `DIGITAL_HUMAN_GAME.md` |
| R2 出画说话 / 后台提示词 | **doki-game-maker** + `R2_DIALOGUE_PROMPT.md` |
| 数字人 seed / locked-portrait idle | **pixverse-r1** `SEED_VIDEO.md`（doki 命令 `seed` 转交） |
| SillyTavern Gal / stage / 扩展 | galgame-maker |
| PixVerse R1 API / Agora / CLI 实测 | **pixverse-r1**（`~/.grok/skills/pixverse-r1`） |
| 外部 App SDK / manifest.json / dist 交付 | **dokiimport** |

做 `stream-client` / R1 卡带时会同时 load：

- `doki-game-maker/references/PIXVERSE_R1_RUNTIME.md`
- `pixverse-r1/SKILL.md`（及 VERIFIED_API / AGORA_PROTOCOL）

做 R2 数字人说话 / 后台提示词时再 load：

- `doki-game-maker/references/R2_DIALOGUE_PROMPT.md`
- 模板 `packs/_template/prompts/r2_realtime_dialogue.json`

做数字人 seed / 小幅度高稳定时再 load：

- `pixverse-r1/references/SEED_VIDEO.md`

做数字人 × 完整玩法时再 load：

- `doki-game-maker/references/DIGITAL_HUMAN_GAME.md`
- 参考包 `packs/tang-noble-lady/`（若存在）

## v2.4 变更摘要

- 收纳 **locked-portrait seed**（小幅度高稳定数字人的视觉先验）
- 世界 / seed / 说话 / 导播 四层分轨
- 命令 `seed` / `r1-seed` 转交 pixverse-r1 `SEED_VIDEO.md`；pack 路径 `assets/r1/seed.mp4`
- 口令：近景、死镜头、死背景、~40s idle 词库

## v2.3 变更摘要

- 正式收纳 **R2 `realtime_dialogue` 后台提示词**（示范：哈兰德）
- 新增 `references/R2_DIALOGUE_PROMPT.md` + 命令 `r2-prompt`
- pack 模板增加 `prompts/r2_realtime_dialogue.json`；卡可指针 `r2_dialogue`
- 说话 / 世界 / 导播 分轨（v2.4 起含 seed 为四层）；默认 1–2 行可念

## v2.2 变更摘要

- 正式收纳 **数字人 × 完整 Dokiworld game 同页**（`stream-r1-game` / `dh-game`）
- 新增 `references/DIGITAL_HUMAN_GAME.md`：真 SPA 嵌入、心理战、R1 进程感知、分轨、验收
- 反模式：文字假牌、跳岛新窗口、无状态导播、假聊天对白
- 合入清单 **P2-dh-game**；参考包 `tang-noble-lady`
- 口令：完整玩法嵌同页；数字人必须吃进程

## v2.1 变更摘要（保留）

- 正式收纳 **PixVerse R1** 为 `runtime: stream-client` 的标准实现
- 新增 stream postMessage 扩展与 `host_requirements: stream_session`
- 新增 `r1_world.json` / `r1-scaffold` / 合入 P2-stream 清单
- 密钥与订棚归宿主；pack 只负责出画与导播
