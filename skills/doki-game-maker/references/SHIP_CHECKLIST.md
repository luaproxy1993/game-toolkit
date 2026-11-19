# 合入 / 交付清单

## P0 发现页卡

- [ ] 卡面图可上传
- [ ] name / tagline / greeting / tags / rating
- [ ] 能 Start chat + opening
- [ ] 无密钥

## P1 Persona

- [ ] prompts 进 muse/system
- [ ] mood 立绘若支持则挂上
- [ ] 安全边界生效
- [ ] （R1）人设与 `r1_world.world_setting` 分工清楚
- [ ] （R2 出画说话）`prompts/r2_realtime_dialogue.json` 字段齐；`speaking_style` 短；`audit_response` 人设一句；对照 `R2_DIALOGUE_PROMPT.md`

## P2 玩法壳

- [ ] 静态树挂 public/game-packs/<slug>/
- [ ] 点卡 iframe/路由 → index.html?host=bridge
- [ ] 宿主实现 pack-chat 桥（或明确仅脚本降级）
- [ ] 3 分钟可感机制
- [ ] server/ 未进生产 bundle

## P2-stream（runtime: stream-client / PixVerse R1）

- [ ] pack.json：`runtime: stream-client` + `stream.provider: pixverse-r1`
- [ ] `host_requirements` 含 `stream_session`
- [ ] `mechanics/data/r1_world.json` 存在且无 key
- [ ] 宿主实现 stream-open →（proxy）→ stream-session
- [ ] 宿主实现 stream-close（iframe 卸载兜底）
- [ ] pack：Agora live+host、init 等 generation_started
- [ ] （数字人）seed 对照 pixverse-r1 `SEED_VIDEO.md`：近景中景、fixed camera、~40s loop、still plate
- [ ] 导播 prompt 后画面可感变化
- [ ] 无 PIXVERSE_API_KEY / 长存 token 在静态资源
- [ ] 并发满 / 排队有 UI 或错误文案
- [ ] FRONTEND_HOST.md 含 stream 代理说明
- [ ] （可选）record 拉成片

## P2-dh-game（数字人 × 完整玩法 · v2.2）

对照 `references/DIGITAL_HUMAN_GAME.md`：

- [ ] 完整 game 在 `games/<id>/` 真 SPA，**无**文字假牌路径
- [ ] 同页 `#dokiGameHost` iframe，左 portrait/live 保留
- [ ] ready → init(character scopes) → initialized 握手成功
- [ ] 女主 open / 操作 taunt / 终局 result（LLM 失败有 fallback）
- [ ] game 事件：`hero_action` / `street_change`（或等价）到达宿主
- [ ] R1：`【…进程感知】` 导播含手号/街道/底池/操作（或玩法等价字段）
- [ ] 中途进房会同步当前 `liveGameState`；对局中有心跳或等价
- [ ] 离开/结束 close session；无 key 在静态
- [ ] 硬刷新后一键「德州」等可复现，非缓存假 UI

## Handoff zip

- [ ] 00-START-HERE.zh.md 写清「非已上线成品」
- [ ] DEPLOY_TO_DOKIWORLD.md
- [ ] 无 config.local / 无 API key / 无 pixverse_r1_session.json
- [ ] pack.json id 与目录一致
- [ ] （R1）写明依赖宿主 stream 代理与 env 名

## 外发 DMG / Windows

- [ ] 标注预览壳 ≠ 大厅卡带
- [ ] 内嵌 runtime 说明（Node 需求或便携 Node）
- [ ] 与当前 frontend 同 commit 的 play 资源
- [ ] （R1）预览若含代理，密钥仅本机 env，说明书勿贴 key
