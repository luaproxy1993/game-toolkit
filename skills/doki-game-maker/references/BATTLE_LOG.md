# 实战备忘（写入 skill 的原因）

## heartbeat-70 / 高嶺愛花

- 可玩主路径必须是 **前端**；开发明确：点卡拉起的包不能靠用户机 Node 生产运行。
- 顶栏假 Dokiworld UI 必须删；用户截图验收过两次「还在」。
- 入口必须 **根 index.html**；`play/` 深埋导致路径混乱。
- 交付物要中文桌面文件夹名，否则「找不到」。
- 小机制（Lofi）用独立 JSON+JS，主循环不缠死。
- ST 自然语言合并卡：展示与语料一体，少空字段。
- DMG/Windows = 外发预览；大厅形态 = game-packs 静态挂载 + 宿主桥。

## 架构共识（作者侧）

- 卡面入口可接结构乱七八糟的东西。
- 野生 demo（含 AR+R2 霸总陪伴）可通过薄封装进标准格式。
- 标准凝练的是插座，不是先要求 demo 结实。

## PixVerse R1（v2.1 融合）

- R1 是 **实时棚**，不是异步出片；HTTP 订棚 + Agora 出画 + DataStream 导播。
- 官方文档字段/3.x·4.x 易错 → **以 pixverse-r1 skill 实测为准**，doki-game-maker 只收卡带形状。
- 密钥与 session HTTP **必须宿主代理**；pack 只收短时 Agora 四件套。
- 不关 Session → `500044` 占坑；close 是契约一部分，不是可选项。
- `world/create` 用 `world_setting`（+ 必填 `style`），禁用示例里的 `prompt` 字段。
- Agora 用 `live` + `host`，不要用 `rtc` mode。
- 人设 system ≠ world_setting ≠ seed ≠ 导播 prompt，四层分开。
- 角色 chat 与画面导播默认可分轨（`chat_to_director`）。
- 野生 R1 demo 准入：先能点开，再抽 key、标 `stream-client`。

## 唐朝高门贵女 · 数字人 × 完整德州（v2.2）

路径：`packs/tang-noble-lady/`（preset 218168 · test-api）

- **要真桌不要假牌：** 用户明确拒绝气泡「六人德州」文字牌；必须 `games/game-c` 完整 SPA 同页 iframe。  
- **女主参与：** init 注入 character；补丁 SPA 把贵女映射 seat；开局/操作/终局 `characterSay`。  
- **心理战：** game 发 `dokiworld-game-event` / `hero_action`（fold/check/call/raise）→ 嘲讽台词；DeepSeek 挂了要本地 fallback。  
- **R1 必须有进程感知：** 不能只 prompt「笑一下」；要带第几手、街道、底池、公共牌、刚发生操作；进房中途 force 同步；对局心跳。  
- **台词与导播分轨：** 心理战可 `skip_live`，画面走 `buildLiveDirectorPrompt`。  
- **R1 下行无角色对话 JSON：** 禁止编假聊天对白；画面只靠 DataStream。  
- **布局：** 左 portrait/live 不卸；右大牌桌 `body.game-active`。  
- **并发 500044：** 释放坑位 + exclusive/reuse + pagehide close。  
- **缓存：** 旧 app.js 会复活假牌 → no-store + `?v=`。  
- 契约写入：`references/DIGITAL_HUMAN_GAME.md`。

## R2 `realtime_dialogue` 后台提示词（v2.3）

示范：哈兰德困在维米尔《戴珍珠耳环的少女》里、手里啤酒。

- 说话层是独立信封：`tts.speaker` + `type: realtime_dialogue` + `dialog.{bot_name,system_role,audit_response,speaking_style,character_manifest}`。  
- **写具体那个，不写原型。** 哈兰德不是「挪威前锋能量」，是网上已经在玩的那个人。  
- `speaking_style` 是味道词（`邪恶的，搞笑的`），不是小作文。  
- `audit_response` 必须能念、必须在戏里。  
- 默认 1–2 短行，给口型；事实不准编，不确定就人设挡。  
- `character_manifest` v0 允许与 `system_role` 全文相同。  
- 世界 / seed / 说话 / 导播 四层分开。契约：`references/R2_DIALOGUE_PROMPT.md`。

## Locked-portrait seed（v2.4）

小幅度、高稳定数字人：优秀 seed 是人物绝对中心、近景或中景、fixed camera、~40s idle 词库 loop、背景 still plate。

- 语态 / lipsync / 动作稳不稳，**先看 seed**。  
- 幅度小 × 词库多：不走不挥手，但 40s 里要有多种闲着。  
- 背景零动态，绝对不参与人物动效。  
- 单一事实源：`~/.grok/skills/pixverse-r1/references/SEED_VIDEO.md`。pack 只收 `assets/r1/seed.mp4`。

## 与 galgame-maker / pixverse-r1 / dokiimport

| 需求 | Skill |
|------|--------|
| Dokiworld 卡带 / pack / 点卡进游戏 | **doki-game-maker** |
| 数字人 × 完整 game 同页整合 | **doki-game-maker** + DIGITAL_HUMAN_GAME |
| R2 出画说话 / realtime_dialogue 提示词 | **doki-game-maker** + R2_DIALOGUE_PROMPT |
| SillyTavern Gal / stage / 扩展 | galgame-maker |
| R1 HTTP/Agora 字段级对接与 CLI | **pixverse-r1** |
| 数字人 locked-portrait seed | **pixverse-r1** `SEED_VIDEO.md` |
| R1 收成卡带 + 宿主桥 | **doki-game-maker** + 引用 pixverse-r1 |
| 外部 App SDK / manifest.json / dist 交付 | **dokiimport** |
