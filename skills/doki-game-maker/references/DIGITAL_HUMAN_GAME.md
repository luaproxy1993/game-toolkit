# 数字人 × 完整玩法 · 同页整合契约（v2.2）

> 实战包：`packs/tang-noble-lady`（唐朝高门贵女 · preset 218168 · game-c 德州）  
> 本文件是 **doki-game-maker** 对「R1 数字人 + Dokiworld 完整 game SPA + 同页心理战」的收口规范。  
> R1 字段级 API 仍以 `~/.grok/skills/pixverse-r1/` 为准；game 桥协议对齐 `dokiimport` / `dokiworld.game/1`。  
> **说话层**（`type: realtime_dialogue` 信封）见 `R2_DIALOGUE_PROMPT.md`，不要把人设长文写进导播。  
> **Seed 层**（locked-portrait idle loop）见 pixverse-r1 `SEED_VIDEO.md`。小幅度高稳定数字人先过 seed 再订棚。

---

## 0. 产品一句话

```text
左侧：角色立绘 / R1 实时视频数字人
右侧：Interactive Story 聊天气泡 + 同页嵌入完整 Dokiworld game（game-a/b/c…）
女主：开局调侃 · 按操作打心理战 · 终局评价
视频模型：必须持续感知牌局/玩法进程（街道、底池、操作），用 DataStream prompt 导播表情
```

**禁止：**

| 禁止 | 原因 |
|------|------|
| 文字假牌桌（聊天气泡里画 3♣ 弃牌跟注）冒充完整玩法 | 用户要的是 Dokiworld 真 SPA |
| 新开浏览器窗口 / 跳岛式 iframe 全屏盖掉角色 | 女主与牌桌必须同壳 |
| 只给 R1 发情绪词、不带牌局状态 | 数字人对进程无感知 |
| 假 LLM 对白冒充 R1 口型/台词 | R1 下行无角色对话 JSON 时禁止编屁话 |
| API key / DeepSeek key 进静态 pack | 仅 `config.local` / 宿主 env |

---

## 1. 架构分层

```text
┌─ pack 根 index.html ─────────────────────────────────────┐
│  Interactive Story 壳（portrait + chat + dokiGameHost）   │
│                                                          │
│  play/app.js                                             │
│    · 关键词/Director → startFullDokiGame                 │
│    · iframe → /games/game-c/index.html                   │
│    · postMessage: ready/init/initialized/result/event    │
│    · characterSay（DeepSeek/本地降级）开局/心理战/终局   │
│    · pushGameToLiveVideo（R1 进程感知导播）              │
│                                                          │
│  play/r1-stream.js  Agora live+host · init/prompt        │
│  server/r1_proxy.py 本地：R1 open/close + director + say │
│  games/game-a|b|c/  完整 SPA（可从 dev 仓 vendoring）    │
└──────────────────────────────────────────────────────────┘
         │ stream-open/session/close      │ game-event
         ▼                                ▼
   宿主或本地代理                    数字人 prompt_message
   PIXVERSE_API_KEY                  【实时*进程感知】…
```

| 通道 | 用途 | 与数字人 |
|------|------|----------|
| `dokiworld-pack-chat` / `/api/character/say` | 角色台词、记忆、心理战文案 | 可选 `skip_live`；台词≠导播；R2 出画说话优先吃 `r2_realtime_dialogue.json` |
| DataStream `prompt_message` | **改实时画面** | 必须带进程摘要 |
| `dokiworld-game-*` | 完整 game 桥 | 事件驱动感知 |
| 隐藏 Director `/api/director/observe` | 是否 launch_game | 不对玩家说话 |

---

## 2. 目录增量（在 v2.1 pack 形之上）

```text
packs/<slug>/
  index.html                 # Interactive Story + #dokiGameHost iframe
  play/
    app.js                   # 嵌入完整 game + 心理战 + R1 感知
    r1-stream.js
    director.js              # 可选：DeepSeek 导演客户端
    styles.css               # body.game-active 大牌桌布局
  mechanics/data/
    r1_world.json            # preset / 无 key / no_fake_chat_reply
    director.json            # game-a/b/c 目录 + 系统提示（禁文字假牌）
  prompts/r2_realtime_dialogue.json  # 出画说话信封（见 R2_DIALOGUE_PROMPT.md）
  games/
    game-c/                  # 完整德州 SPA（及 a/b）
      index.html
      assets/*.js
      art/index.json         # 可空 {"assets":[]} 消 404
  server/r1_proxy.py         # 本地：R1 + director + character/say
  config.local.json          # gitignore：PIXVERSE + DEEPSEEK
```

`pack.json` 建议：

```json
{
  "integration": {
    "runtime": "stream-client",
    "frontend_entry": "index.html",
    "play_modes": ["interactive_story", "embed_full_game", "r1_digital_human"],
    "stream": {
      "provider": "pixverse-r1",
      "protocol": "agora-rtc + datastream",
      "host_proxy": true,
      "game_awareness": true,
      "skill_ref": "pixverse-r1"
    }
  },
  "host_requirements": [
    "dialogue",
    "stream_session",
    "client_state",
    "optional_director",
    "optional_character_say"
  ]
}
```

---

## 3. 完整 game 同页嵌入（铁律）

### 3.1 启动

1. 硬关键词（「来一把德州」）或隐藏 Director → `launch_game`  
2. **禁止** `InChatTable` / 文字牌路径（已废弃）  
3. `#dokiGameHost` 去 hidden，`body.game-active`，iframe  
   `src=/games/{game-c}/index.html?host=bridge&v=…`  
4. 等 `dokiworld-game-ready` → `dokiworld-game-init`（含 character scopes）  
5. 收到 `initialized` → 可自动「开始上桌」（pack 内补丁或菜单）  

### 3.2 init 载荷（dokiworld.game/1）

```js
{
  type: "dokiworld-game-init",
  protocolVersion: 1,
  gameId: "game-c",
  runId: "<uuid>",
  grantedScopes: [
    "character.identity",
    "character.avatar",
    "character.card"
  ],
  locale: "zh-cn",
  context: {
    schemaVersion: 1,
    character: {
      id: "…",
      displayName: "…",
      avatar: { url: "<absolute>", alt: "…" },
      card: { description: "…", tags: ["…"] }
    }
  }
}
```

**注意：** 部分 vendored game 校验 scopes 与 character 字段极严；avatar URL 必须绝对路径。  
女主入座：若 SPA 支持 `session.seats`，把 character 映射为 seat card（`adultConfirmed: true` + name + avatarUrl）。

### 3.3 从 game 回传的事件（pack 可补丁 SPA）

| event | 何时 | 宿主动作 |
|-------|------|----------|
| `hero_action` | 玩家 fold/check/call/raise/allin | 心理战台词 + **R1 进程导播** |
| `street_change` | 公共牌增加 | 更新 state + R1 导播 |
| `phase_change` | showdown / gameover… | R1 导播 |
| `hand_result` | 一手结束 | 输赢调侃 + R1 |
| `table_open` | 点开始上桌 | R1「入席」 |
| `state_snapshot` | 可选 | 只合并状态，避免双推 |
| `dokiworld-game-result` | 整局分数 | 终局评价 + R1 |

事件信封：

```js
{
  type: "dokiworld-game-event",
  protocolVersion: 1,
  gameId: "game-c",
  event: "hero_action",
  action: { kind: "raise", to: 100 },
  public: {
    pot, handNo, street, phase,
    board: "A♠ K♥ 2♦",
    heroHole: "…",   // 宿主可存；导播勿让模型「偷看」点数
    heroStack, toCall, playerCount
  }
}
```

### 3.4 UI 布局

- 对局中：右侧大 iframe（约 70%+），聊天区压缩  
- 左侧 portrait / 实时视频 **保留**  
- 一键按钮：「♠ 德州」等，不依赖纯闲聊触发  

---

## 4. 数字人进程感知（R1）

### 4.1 原则

1. **每一个有意义的玩法节点** 都尝试 `stream.prompt(buildLiveDirectorPrompt(…))`  
2. Prompt **必须**含：游戏名、第几手、街道、底池、公共牌、刚发生事件、表演要求  
3. 固定前缀：`【实时德州进程感知·必须据此表演】`（其他玩法改名即可）  
4. 对局中 **心跳**（建议 20–25s）重推状态，防止模型「忘了在打牌」  
5. 中途「进入实时」：init 拼上当前 `liveGameState`；`onLive` 立刻 force 同步  
6. 结束牌局：发「离开对局神态」再 close  

### 4.2 导播模板（示意）

```text
【实时*进程感知·必须据此表演】
你是{角色}，正坐在{玩法}与公子对弈，半身镜头面向镜头。
第{N}手，街道={翻牌前|翻牌|…}，底池={pot}，需跟注={toCall}。
公共牌：{board 或 无}。
刚发生：{弃牌|加注到100|公共牌更新·翻牌 A♠…}。
表演要求：根据进程做微表情与肢体（戏谑/施压/沉吟…），保持人设立仪，不要出画，不要念规则。镜头与背景保持 seed 原样。
```

### 4.3 与角色台词分轨

| 层 | 实现 | 进 R1？ |
|----|------|---------|
| 心理战垃圾话 | `characterSay(game_taunt)` → 聊天气泡 | 默认 `skip_live: true`，另发进程导播 |
| 进程感知 | `pushGameToLiveVideo` | **是** |
| 用户闲聊（对局中） | 台词 + `buildLiveDirectorPrompt("公子说：…")` | 是 |
| 纯导播输入框 | `prompt_message` 原文 | 是（画面专用） |

**禁止：** R1 下行没有对话字段时，用假气泡冒充数字人说话。

### 4.4 节流

- 非紧急事件：≥ ~2s 合并  
- fold / raise / allin / street / phase / table_open：**force + urgent**  
- `state_snapshot`：只更新内存，不重复推 R1  

---

## 5. 心理战 / 女主参与

### 5.1 阶段

| phase | 触发 | 文案目标 |
|-------|------|----------|
| `game_open` | 嵌入完整 game | 答应上真桌、邀开打 |
| `game_taunt` | hero_action / 边打边聊 | 按操作打心理战（雅致带刺） |
| `game_result` | game result / 终局 | 输赢评价、记仇可夸 |

### 5.2 降级

DeepSeek/宿主 LLM 503 时 **必须**本地 fallback 句（按 fold/check/call/raise 分支），保证牌桌体验不断。

### 5.3 女主入座（可选增强）

Vendored game 若忽略 `context.character` 展示，可补丁 `t5(character)→session.seats[]`，把 displayName + avatar 注入对手位。

---

## 6. 隐藏导演（Director）

- 不对玩家输出；只 JSON：`action: none | launch_game` + `game_id`  
- 硬关键词优先于 LLM，避免「废话不发桌」  
- `director.json` 文案写明：**完整 SPA 嵌入，禁止文字假牌、禁止新窗口**  
- cooldown / max_launches 防刷  

---

## 7. 本地代理最小 API

```text
POST /api/r1/open | close | reset
POST /api/director/observe | status
POST /api/character/say   { phase, user_line, game }
静态：/games/game-c/…  Cache-Control: no-store（html/js/css）
```

`config.local.json`：`PIXVERSE_*`、`DEEPSEEK_*`，gitignore。

---

## 8. 3 分钟验收（数字人×玩法）

- [ ] 硬刷新后点「♠ 德州」出现 **真牌桌 SPA**，不是气泡假牌  
- [ ] 左侧立绘/实时仍在  
- [ ] 女主开局有台词；弃牌/加注有嘲讽  
- [ ] **进入实时** 后操作牌桌，导播日志出现 `[R1牌局感知]` / `[牌局进程→R1]`  
- [ ] 翻牌后公共牌变化有 R1 推送  
- [ ] 关牌局 / 离开实时会 close，不无故占坑  
- [ ] 无 key 在静态网络面板  

---

## 9. 脚手架命令（Agent）

```text
/doki-game-maker new <slug> stream-r1-game
/doki-game-maker dh-game | digital-human-game
```

步骤摘要：

1. 常规 stream-r1 scaffold  
2. 加 `games/game-*`（或文档写清从 dev 仓同步）  
3. 根壳 Interactive Story + dokiGameHost  
4. app.js：`startFullDokiGame` + `onTablePsychEvent` + `pushGameToLiveVideo`  
5. director.json + character/say  
6. 补丁 game SPA：hero_action / street_change 事件（若上游未发）  
7. 本文件勾选验收  

参考实现路径：

```text
{DOKI_WORKSPACE}/packs/tang-noble-lady/
```

---

## 10. 反模式（本轨专杀）

| 反模式 | 正确 |
|--------|------|
| 文字六人德州卡片 | 嵌入完整 game-c |
| 新窗口打开 game | 同页 iframe + 左女主 |
| 只 prompt「笑一下」 | 带手号/街道/底池/操作的进程导播 |
| 聊天假回复冒充视频说话 | 无下行 JSON 就不编；视频只导播 |
| 心理战与 R1 抢同一句无状态 | 台词 skip_live；R1 走 buildLiveDirectorPrompt |
| 无 close / 无释放坑位 | 顶栏释放 + pagehide beacon |
| 缓存旧 app.js 仍出假牌 | no-store + `?v=` cache bust |

---

## 11. 一句话

> **真桌嵌同页；女主打心理战；数字人吃进程；密钥只在代理；假牌与假屁话一律杀掉。**
