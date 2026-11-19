---
name: doki-game-maker
description: >-
  Dokiworld Game-as-Card / 卡带创作管线 v2.4：角色卡是入口，后面可挂结构参差的玩法
  （日程、小机制、静态页、AR/实时 demo、PixVerse R1 数字人、R2 realtime_dialogue
  后台提示词、locked-portrait seed、同页嵌入完整 Dokiworld game SPA）。开发用薄契约收成标准 doki.pack。
  吸收 galgame-maker 的 Doki 轨 + heartbeat-70 / 爱花实战 + pixverse-r1 实测实时流
  + 哈兰德 R2 示范提示词 + tang-noble-lady 数字人×完整德州。Use for
  /doki-game-maker, doki pack, 卡带, Game-as-Card, Mutator, heartbeat, 点卡进游戏,
  frontend-static, host bridge, stream-client, pixverse-r1, R1 实时陪伴, R2,
  realtime_dialogue, 数字人提示词, seed video, locked-portrait, idle loop,
  完整德州, game-c 嵌入, 心理战, 进程感知,
  唐朝高门贵女, 高嶺愛花, 日程养成, or when building Dokiworlddevwong packs.
argument-hint: "[project_path] [phase|command]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task, TodoWrite
metadata:
  author: dokiworlddevwong + battle-lessons + pixverse-r1 + tang-noble-lady
  short-description: Dokiworld 卡带 / Pack 创作 v2.4（R2 说话信封 + locked-portrait seed + R1 × 完整玩法）
  version: "2.4.0"
  supersedes_partial: "galgame-maker Route A (Doki); ST Route B remains in galgame-maker"
  integrates: "pixverse-r1@>=1.0.0; dokiimport@>=2 App SDK (manifest.json / dokiworld.app/2); embed_full_game + R1 game_awareness; R2 realtime_dialogue"
---

# Doki Game Maker v2.4 — 卡入口 · 薄宿主 · 乱得起 · 收得住 · 可挂实时数字人

## 0. 产品公式（每次会话先对齐）

```text
发现页 / 大厅 = 永远是「角色卡」
        │ 点击
        ▼
卡带（doki.pack.*）= 独立封装单元
        │ 内部可以很乱：
        │   日程 / Lofi / 半成品 HTML / AR demo /
        │   PixVerse R1 数字人（Agora 出画 + 文字导播）
        │   同页嵌入完整 Dokiworld game（game-a/b/c…）
        │   女主心理战 + 视频模型进程感知
        ▼
宿主只提供插座：加载 entry · 可选 LLM/记忆/计费 · 可选 result 回写
               · （R1 时）可选 stream 代理：订棚/Session/密钥不出前端
```

**规范做在边界，不规范做在单元内部。**

| 必须整齐 | 允许乱七八糟 |
|----------|----------------|
| 卡面入口、pack id、entry 路径 | 包内目录、规则文案、实验机制 |
| 宿主薄协议（ready/chat/result/close） | 实现用何 API、是否结实 |
| **stream 密钥与 HTTP 订棚只在宿主/本地代理** | pack 内 Agora 播放器与导播 UI |
| **完整玩法 = 真 SPA 嵌入，不是文字假机制** | 包内 vendoring 的 game 构建产物 |
| **数字人对进程可感知（带状态的 prompt）** | 具体玩法数值平衡 |
| 无密钥进仓、前端优先上生产 | 本地代理、野生 demo |
| 3 分钟可感「不是纯聊」 | 完美数值平衡 |

**禁止：** 绕过角色卡做独立 App 商店当分发主路径（调试壳可以，不能替代卡）。  
**禁止：** 把 `PIXVERSE_API_KEY` / 完整 Agora token 写进 pack 静态资源或 handoff zip。  
**禁止：** 用聊天气泡假牌桌冒充完整 Dokiworld 玩法；禁止新窗口跳岛导致女主与牌桌分离。  
**禁止：** R1 下行无角色对话 JSON 时编造假聊天对白。

---

## 1. 与 galgame-maker / pixverse-r1 / 实战的关系

| 来源 | inheriting |
|------|-------------|
| galgame-maker Route A | pack 目录、Mutator、资产命名、handoff、作者门 |
| galgame-maker Route B | **不**作为本 skill 主线；ST 仍用 `/galgame-maker st` |
| heartbeat-70 实战 | **frontend-static 入口在 pack 根 `index.html`**；无生产 Node；小机制 JSON；宿主 postMessage 桥；P0 卡 → P1 人设 → P2 玩法壳 |
| 卡带哲学实战 | 爱花包 + Lofi 电台 = 标准插座上的杂电器；霸总 AR+R2 = 同一格式的另一 runtime |
| **pixverse-r1 skill** | R1 **字段级 API、Agora DataStream、CLI、已知坑** 以 `~/.grok/skills/pixverse-r1/` 为准；本 skill 只规定 **如何收成卡带** |
| **dokiimport** | 外部 App 交付：`@dokiworld/app-sdk` + `manifest.json` + `dokiworld.app/2`（见 skill v2；旧 v1 game.json 桥仅 legacy） |
| **tang-noble-lady 实战** | 数字人 + Interactive Story + **同页完整 game-c** + 心理战 + **R1 进程感知** |

参考实现（只读）：

```text
{DOKI_WORKSPACE}/packs/heartbeat-70/
{DOKI_WORKSPACE}/packs/tang-noble-lady/     # ★ v2.2 数字人×完整德州参考包
{DOKI_WORKSPACE}/card-spec/
{DOKI_WORKSPACE}/docs/MUTATOR_ARCHITECTURE.md
{DOKI_WORKSPACE}/docs/PLAY_SKILL.md
{DOKI_WORKSPACE}/PRINCIPLES.md
~/.grok/skills/pixverse-r1/SKILL.md
~/.grok/skills/pixverse-r1/references/VERIFIED_API.md
~/.grok/skills/pixverse-r1/references/AGORA_PROTOCOL.md
~/.grok/skills/pixverse-r1/references/SEED_VIDEO.md   # 数字人 locked-portrait seed
~/.grok/skills/dokiimport/SKILL.md
```

默认 `DOKI_WORKSPACE`：`$DOKI_WORKSPACE` → `…/Dokiworlddevwong` → 询问。

### 1.1 能力分工（R1 / 数字人融合铁律）

```text
doki-game-maker          = 卡带形状 · 宿主契约 · 管线 · 合入 · 数字人×玩法整合
pixverse-r1              = HTTP 订棚 · Session · Agora · 实测字段 · locked-portrait seed
dokiimport               = App SDK 交付 · manifest.json · dist/ · createAppClient
pack (stream-client)     = 卡面 + 播放壳 + 导播 UI + mechanics + 可选 games/*
宿主 / 本地 server       = 持有 PIXVERSE_API_KEY · 代理 reserve/session/close
                         + 可选 director / character.say（DeepSeek 等，密钥不进静态）
```

做 R1 卡带时 Agent **必须**额外 load：

1. `{SKILL_ROOT}/references/PIXVERSE_R1_RUNTIME.md`
2. `~/.grok/skills/pixverse-r1/SKILL.md`（及按需 VERIFIED_API / AGORA_PROTOCOL）

做 **数字人说话 / R2 后台提示词** 时 **必须再 load**：

3. `{SKILL_ROOT}/references/R2_DIALOGUE_PROMPT.md`

做 **数字人小幅度高稳定 / seed 视频** 时 **必须再 load**：

4. `~/.grok/skills/pixverse-r1/references/SEED_VIDEO.md`（构图 / idle loop / still plate 的单一事实源）

做 **数字人 + 完整玩法同页** 时 **必须再 load**：

5. `{SKILL_ROOT}/references/DIGITAL_HUMAN_GAME.md`
6. 参考包 `{DOKI_WORKSPACE}/packs/tang-noble-lady/`（若存在）

---

## 2. 路径与调用

```
SKILL_ROOT=~/.grok/skills/doki-game-maker
PIXVERSE_R1_SKILL=~/.grok/skills/pixverse-r1
DOKI_WORKSPACE=<Dokiworlddevwong>
PACK=<DOKI_WORKSPACE>/packs/<slug>
```

```text
/doki-game-maker
/doki-game-maker /path/to/pack
/doki-game-maker new <slug> [mutator_id]
/doki-game-maker new <slug> stream-r1     # R1 实时陪伴脚手架
/doki-game-maker new <slug> stream-r1-game  # R1 数字人 + 同页完整 game（德州等）
/doki-game-maker card | mechanics | assets | frontend | micro
/doki-game-maker r1 | r1-scaffold | r1-host-doc
/doki-game-maker r2-prompt                      # 写/审计 R2 realtime_dialogue
/doki-game-maker seed | r1-seed                 # 数字人 locked-portrait seed（转交 pixverse-r1 SEED_VIDEO）
/doki-game-maker dh-game | digital-human-game   # 数字人×玩法整合 / 审计
/doki-game-maker host-doc | export-static | handoff | ship-p0
/doki-game-maker wild   # 把野生 demo 收成档 1 薄封装
```

Session：读 `PACK/pipeline_state.json` 续步；无则问 slug + 意图（新品 / 改现有 / 收野 / **R1 实时** / **数字人×完整玩法**）。

---

## 3. 卡带创作格式（标准形状）

### 3.1 目录（v2 实战形）

```text
packs/<slug>/
  pack.json                 # id: doki.pack.<slug>
  game.json / manifest.json # 宿主清单：优先 App SDK manifest.json（/dokiimport）；旧 pack 可暂 game.json
  index.html                # ★ 前端入口在 pack 根（v2 铁律）
  content/characters/       # 卡面 + 扮演
  mechanics/
    manifest.json
    data/*.json             # 活动/地图/事件/小机制配置
    data/r1_world.json      # ★ stream-client / R1：世界观与导播默认（无密钥）
  prompts/                  # system / style / opening（展示≠system）
  prompts/r2_realtime_dialogue.json  # ★ R2 数字人说话信封（type: realtime_dialogue）
  assets/
    cards/ portraits/ scenes/ maps/ events/
  play/                     # app.js styles.css 小机制 js；play/index.html 可重定向到根
  play/r1-stream.js         # ★ 可选：Agora 进房 + init/prompt 封装
  play/director.js          # ★ 可选：隐藏导演（launch 完整 game）
  games/                    # ★ 可选：完整 Dokiworld SPA（game-a/b/c…）同页 iframe
  server/                   # 仅本地预览代理（含 R1 HTTP 代理）；禁止上生产
  FRONTEND_HOST.md          # 给主仓前端的接线说明（含 stream 代理时写清）
  MECHANICS_TUNING.md       # 小机制怎么改
  docs/                     # GDD / ART / PIPELINE
  dist/frontend-static/     # export 无 server 树
  pipeline_state.json
```

### 3.2 `pack.json` 必填精神

- `id` / `slug` / `version` / `display`（title, tagline, cover）
- `entry`: `single_character` | `role_card` | `world` | …
- `characters[]` + `is_entry_face`
- `mechanics.module_ids`
- `host_requirements`: dialogue, memory, client_state, **`stream_session`**（R1 时必填）…
- `integration.runtime`: **`frontend-static`**（默认）| `iframe-game` | `prompt_only` | `native-ar` | **`stream-client`** | `custom`
- `integration.frontend_entry`: **`index.html`**
- `integration.host_mount_hint`: `/game-packs/<slug>/index.html?host=bridge`
- `integration.stream`（仅 `stream-client`）：见 §3.4
- `needs_schema_change`: 默认 `false`（R1 若宿主尚无 stream 代理，可暂 `true` 并写清最小改动）

### 3.3 Runtime 枚举（乱电器的插座型号）

| runtime | 含义 | 例 |
|---------|------|-----|
| `frontend-static` | 纯静态页，宿主 iframe | heartbeat-70 |
| `iframe-game` | Play Skill 页 + score/plan | game-a/b/c, schedule |
| `prompt_only` | 几乎只靠对话+软状态 | 轻量陪伴 |
| `native-ar` | 眼镜/原生客户端 | 霸总 AR + R2 demo |
| **`stream-client`** | **实时音视频流客户端** | **PixVerse R1 实时世界 / 实时陪伴** |
| `custom` | 临时；必须写清宿主要改什么 | 野生实验 |

**野生 demo 合法**：先 `runtime: custom` + 能点开；跑通后再收成上表某一类。  
**R1 野生 → 标准**：先 `custom` 或直接 `stream-client` + `stream.provider: pixverse-r1`；密钥只走代理。

### 3.4 `stream-client` + PixVerse R1（v2.1 正式）

```json
{
  "integration": {
    "runtime": "stream-client",
    "frontend_entry": "index.html",
    "host_mount_hint": "/game-packs/<slug>/index.html?host=bridge",
    "stream": {
      "provider": "pixverse-r1",
      "protocol": "agora-rtc + datastream",
      "host_proxy": true,
      "capabilities": [
        "world_or_scenario",
        "reservation",
        "session",
        "live_video",
        "prompt_direct",
        "session_close",
        "optional_record"
      ],
      "skill_ref": "pixverse-r1"
    }
  },
  "host_requirements": ["dialogue", "stream_session", "client_state"]
}
```

**心智模型（与 pixverse-r1 一致）：**

```text
HTTP API（宿主代理）  = 订棚、拿钥匙、关灯
Agora RTC（pack 内）  = 看实时画面 + 听声音
Agora DataStream      = 文字导播（init / prompt）
角色卡对话（可选）    = 人设 LLM（宿主 pack-chat）≠ 视频导播，可并联
```

顺序不能乱：

```text
preset/scenario → reservation → ACTIVE → session/create
  → Agora join + host → init_message (等 generation_started)
  → prompt_message … → session/close → (可选) record
```

**并发：** 不关 Session 占坑 → `500044`。pack 与宿主都必须保证 **离开页 / close 按钮 / 超时** 调 close。

完整契约：`references/PIXVERSE_R1_RUNTIME.md`。

### 3.5 数字人 × 完整玩法同页（v2.2 正式 · `stream-r1-game`）

**产品形：** 左数字人（立绘 / R1 视频）+ 右 Interactive Story + **同页 iframe 完整 game SPA**（非文字假牌）。

```text
关键词/Director → startFullDokiGame
  → iframe /games/game-c/index.html
  → ready → init(character scopes) → initialized
  → 玩家操作 → dokiworld-game-event (hero_action / street_change / …)
       ├→ characterSay 心理战（聊天气泡）
       └→ pushGameToLiveVideo（R1 进程感知导播，带手号/街道/底池/公共牌）
  → result → 终局评价 + R1 收势
```

| 层 | 必须 |
|----|------|
| 玩法 | vendoring `games/game-*` 真 SPA；**禁止** InChatTable 文字牌 |
| 角色 | init 注入 character；可选 seat 卡补丁让女主入座 |
| 台词 | open / taunt / result；LLM 失败有本地 fallback |
| 数字人 | 每个进程节点 `prompt_message` 带 **进程摘要**；对局心跳 20–25s |
| 布局 | `body.game-active` 大牌桌，左侧 portrait/live 保留 |
| 密钥 | PIXVERSE + DeepSeek 仅代理 / config.local |

**验收句默认：**  
「进入实时后点德州，真牌桌出、女主嘲讽操作，左侧视频随加注/翻牌变表情。」

完整契约与反模式：`references/DIGITAL_HUMAN_GAME.md`。  
参考包：`packs/tang-noble-lady/`。

---

## 4. 管线阶段（作者门：每步 STOP → `step N: accept`）

### D0 · 立项

```bash
cp -R {DOKI_WORKSPACE}/packs/_template packs/<slug>
# 或
cp -R {DOKI_WORKSPACE}/mutators/<mutator_id> … 再 mutate
# R1 快捷：
# /doki-game-maker new <slug> stream-r1
```

`pipeline_state.json`:

```json
{
  "route": "doki",
  "skill": "doki-game-maker",
  "skill_version": "2.4.0",
  "pack_slug": "<slug>",
  "mutator_id": null,
  "runtime": "frontend-static",
  "stream_provider": null,
  "embed_full_game": false,
  "game_awareness": false,
  "step": "D0",
  "status": "in_progress"
}
```

R1 立项时：

```json
{
  "runtime": "stream-client",
  "stream_provider": "pixverse-r1",
  "three_minute_accept": "点卡进房后 15s 内见动态世界，发一句导播画面有变化"
}
```

数字人 × 完整玩法立项时：

```json
{
  "runtime": "stream-client",
  "stream_provider": "pixverse-r1",
  "embed_full_game": true,
  "game_awareness": true,
  "games": ["game-c"],
  "three_minute_accept": "进入实时后点德州见真牌桌；操作有女主嘲讽；视频随进程变表情"
}
```

写清 **3 分钟验收句**（玩家感到什么不像纯聊）。

世界观未锁定时：先 `/core-rule-book`（`~/.grok/skills/world-bible`）。不要用手写一页 `docs/WORLD_BIBLE.md` 冒充气质锚。已有 CRB 时从 `entry_face` / `r1_world` excerpt / 3-minute accept 吸入 pack（见 core-rule-book `references/HANDOFF.md`）。

### D1 · 角色卡（发现页脸）

`content/characters/<key>.json` + 可选 `*_full.md`。

- 展示字段短；长设定进 `prompts/` / full.md  
- 自然语言扮演卡可以 **一整段**（实战：影院体 + 语料 + 示例对话），不要为省事拆成空 first_mes  
- 中文产品可中文 system；合主仓注意 English canonical 策略  
- **R1：** 卡面 hook 写「实时世界 / 可导播」，人设 system 与 `r1_world.world_setting` **分工**：人设=角色怎么说话；world=场景长什么样（非剧情）  
- **R2 数字人说话：** 另写 `prompts/r2_realtime_dialogue.json`（`type: realtime_dialogue`）。信封与写法以 `references/R2_DIALOGUE_PROMPT.md` 为准（示范：哈兰德）。卡 `r2_dialogue` 指针指向该文件。展示字段仍短。  
- **数字人 seed：** 小幅度高稳定必须先有 locked-portrait seed（近景/中景、fixed camera、~40s idle loop、still plate）。制作/审计转交 `pixverse-r1` `SEED_VIDEO.md`；pack 只收 `assets/r1/seed.mp4` + `seed_still.png`。  

**STOP** `step D1: accept`

### D2 · 机制 + 数据

`mechanics/manifest.json` + `data/*`。

- kind 优先：`prompt_only` | `soft_state` | `client_state`  
- **小机制**独立 JSON+JS（见 §6），勿塞进主状态机死结  
- 禁止一上来 `custom_host` + 新表  
- **R1：** 增加 `mechanics/data/r1_world.json`（preset 或自定义 world_setting/style；默认导播句；无 key）  

```json
{
  "provider": "pixverse-r1",
  "mode": "queue",
  "style": "Ambient",
  "aspect_ratio": "9:16",
  "world_setting": "雨夜东京小巷，霓虹倒影，拉面摊蒸汽",
  "preset_id": null,
  "scenario_id": null,
  "init_prompt": "镜头缓慢推进，环境微动",
  "sample_directors": ["突然下起更大的雨", "角色回头看向镜头"],
  "chat_to_director": false,
  "notes": "world_setting 写世界观；具体剧情留给导播 prompt"
}
```

数字人小幅度高稳定：`style: Ambient`；`world_setting` 只写静景；`init_prompt` 不写运镜/环境动效；seed 另见 `SEED_VIDEO.md`。上面示例是探索世界用，不是数字人用。

**STOP** `step D2: accept`

### D3 · 前端壳（生产形态依 runtime）

#### 3-A · frontend-static（默认）

铁律（heartbeat 实战）：

1. **入口在 pack 根 `index.html`**（不是深埋 play 才是主入口）  
2. `PACK_BASE` 按页面位置解析；资产 `assets/`、`mechanics/data/` 相对 pack 根  
3. **无顶栏宿主品牌条**（Dokiworld Download Library 等）——壳是游戏，不是再套一层假大厅  
4. 对话三通道：`host bridge` → 可选本地 `/api` → **脚本降级**（无后端日程仍可玩）  
5. `server/` 仅本地；`export-frontend-static` **剔除** server 与密钥  

宿主桥（最低）：

```text
child → parent: dokiworld-game-ready
parent → child: dokiworld-game-init
child → parent: dokiworld-pack-chat { requestId, messages, game_context }
parent → child: dokiworld-pack-chat-result { requestId, reply | error }
child → parent: dokiworld-game-result | dokiworld-game-close
```

#### 3-B · stream-client / PixVerse R1

在 3-A 之上叠加：

1. **入口仍是 pack 根 `index.html`**（全屏播放器 + 导播条 + 可选聊天气泡）  
2. **无 PIXVERSE_API_KEY 进前端**；订棚/Session 只经：  
   - `host=bridge` → stream postMessage（见下）  
   - 或本地 `server/` 代理（预览）  
3. Agora：`mode: "live"` + `setClientRole("host")`；进房后 `init_message`，**等 `generation_started`** 再宣称出画  
4. 导播：`prompt_message`；可选 `chat_to_director` 把用户句同步成导播（人设 LLM 仍走 pack-chat）  
5. 离开 / 卸载 / 超时 → **必须** `session/close`（经宿主或本地代理）  
6. 无 stream 时降级：展示卡面 + 文案「实时世界暂不可用」+ 纯聊仍可（若 host 有 dialogue）  

Stream 宿主桥（扩展，方向约定）：

```text
child → parent: dokiworld-stream-open {
  requestId,
  provider: "pixverse-r1",
  preset_id?: number,
  world?: { world_setting, style, aspect_ratio, image_url? },
  mode?: "queue" | "exclusive"
}
parent → child: dokiworld-stream-session {
  requestId,
  agora_app_id, agora_token, agora_channel, agora_uid,
  session_id, db_session_id, reservation_end_timestamp
} | { requestId, error }
child → parent: dokiworld-stream-close { requestId?, db_session_id }
parent → child: dokiworld-stream-closed { requestId?, ok | error }
# 可选
child → parent: dokiworld-stream-record { requestId, db_session_id }
parent → child: dokiworld-stream-record-result { requestId, video_url? | error }
```

写 `FRONTEND_HOST.md`：挂载路径 + **stream 代理伪代码** + 密钥环境变量名（不写值）。

#### 3-C · stream-r1-game / 数字人 × 完整玩法（v2.2）

在 3-B 之上叠加（详见 `DIGITAL_HUMAN_GAME.md`）：

1. **壳 = Interactive Story**：左 portrait/`#videoPlayer`，右 `#chatLog` + `#dokiGameHost` iframe  
2. **`games/game-*` 真 SPA** 同源静态服务；启动只走 `startFullDokiGame`，无文字假牌  
3. **桥：** ready → init(character) → initialized → result/close；**扩展** `dokiworld-game-event`  
4. **心理战：** `/api/character/say` 或宿主 LLM；phase = open/taunt/result；要 fallback  
5. **R1 进程感知：** `liveGameState` + `buildLiveDirectorPrompt` + 心跳；中途进房 force 同步  
6. **隐藏导演** 可选：关键词优先；只 launch 完整 game  
7. 布局：`body.game-active` 压缩聊天、放大 iframe，**不**卸左侧数字人  
8. 静态资源 `Cache-Control: no-store` + 脚本 `?v=`，避免旧假牌 JS  

**STOP** `step D3: accept`

### D4 · 资产

| 槽 | 路径 |
|----|------|
| 卡面 | `assets/cards/` 9:16 |
| mood | `assets/portraits/{mood}.png` |
| 场景 | `assets/scenes/{zone}/{id}/{day\|night}.png` |
| 地图 | `assets/maps/` |
| 事件 | `assets/events/<id>/key.png` |
| R1 世界缩略（可选） | `assets/r1/world_thumb.png`（自定义 world 有 image 时） |
| R1 数字人 seed | `assets/r1/seed.mp4` + `assets/r1/seed_still.png`（locked-portrait；规范在 pixverse-r1 `SEED_VIDEO.md`） |

昼夜分文件；美术默认对齐发现页半写实+轻二次元（可被 pack ART 覆盖）。  
R1 主画面来自直播流，静态场景图作 loading / 降级 / 卡面即可。

**STOP** `step D4: accept`

### D5 · 导出与分发形态

| 产物 | 用途 |
|------|------|
| `dist/frontend-static/<slug>/` | 拷进 `frontend/public/game-packs/<slug>/` |
| handoff zip | 合入文档 + pack，无 key / 无 production Node |
| macOS .app+dmg / Windows zip | **外发预览**，写明 ≠ 大厅卡带主分发 |
| ST 导出 | 可选；转交 galgame-maker Route B |

R1 额外：`export-static` **剔除** `server/`、`pixverse_r1_session.json`、`.env`、任何 token 文件；`FRONTEND_HOST.md` 必须说明宿主如何代理 stream。

**STOP** `step D5: accept`

### D6 · 合入主仓（分层 PR）

| 阶段 | 目标 | 不要夹带 |
|------|------|----------|
| **P0** | 发现页有卡、能开聊 | 完整玩法壳 / 完整 R1 |
| **P1** | persona / mood / opening | 新 DB |
| **P2** | iframe/路由挂 `index.html?host=bridge`，玩法可感 | 把 server 打进生产 |
| **P2-stream** | 宿主实现 `stream_session` 代理 + pack 出画可感 | API key 进前端；不关 session |
| **P2-dh-game** | 同页完整 game + 女主参与 + R1 进程感知可感 | 文字假牌；无 close；假聊天对白 |

验收清单见 `references/SHIP_CHECKLIST.md`。

---

## 5. 命令速查（Agent 执行协议）

### `new <slug> [mutator]`

1. 复制 template 或 mutator scaffold  
2. 填 pack.json + pipeline_state  
3. 建根 `index.html` 骨架（可从 heartbeat-70 减配）  
4. STOP D0  

### `new <slug> stream-r1` · `r1-scaffold`

1. 建 pack 骨架（同上）  
2. `runtime: stream-client`，`stream.provider: pixverse-r1`  
3. 写 `mechanics/data/r1_world.json` + `play/r1-stream.js` 最小 Agora 壳  
4. 本地可选 `server/r1-proxy`（只读 env `PIXVERSE_API_KEY`；勿提交 key）  
5. `FRONTEND_HOST.md` 写 stream 桥 + 代理契约  
6. pipeline_state 记 `stream_provider`  
7. STOP D0；提示作者下一步 D1 卡面 / D2 世界观文案  

字段与 curl/脚本细节：**转交** `pixverse-r1`（`r1_client.py` list/world/reserve/session…），本 skill 不复制易过期的字段表。

### `r1`

在已有 pack 上增强/调试 R1：

1. 确认 `runtime` + `r1_world.json`  
2. load `PIXVERSE_R1_RUNTIME.md` + pixverse-r1 skill  
3. 需要实测 API 时用 `python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py …`  
4. 修播放器 / 导播 / close 生命周期  
5. 不把 session json 提交 git  

### `r1-host-doc`

只生成/更新宿主侧说明：stream postMessage、代理路由建议、环境变量、close 责任、与 pack-chat 并联关系。

### `new <slug> stream-r1-game` · `dh-game` · `digital-human-game`

数字人 + 同页完整玩法（参考 tang-noble-lady）：

1. 先跑 stream-r1 scaffold（runtime + r1_world + r1-stream + 代理说明）  
2. load `references/DIGITAL_HUMAN_GAME.md`  
3. 建 Interactive Story 壳 + `#dokiGameHost`  
4. 置入或同步 `games/game-a|b|c`（完整 SPA，非 lite）  
5. 实现 `startFullDokiGame` + init character scopes + event 处理  
6. 实现 `characterSay`（open/taunt/result）+ 本地 fallback  
7. 实现 `pushGameToLiveVideo` / `liveGameState` / 心跳 / 进房同步  
8. 可选：隐藏 Director；补丁 SPA 发 `hero_action` / `street_change`  
9. pipeline_state：`embed_full_game` + `game_awareness`  
10. 按 DIGITAL_HUMAN_GAME §8 验收  

审计已有包时：`/doki-game-maker dh-game` → 对照清单，标出假牌路径 / 无 R1 感知 / 无 close。

### `card`

写/改 `content/characters` + prompts；强调展示≠system。  
R1：同步检查 tagline 是否承诺「实时」且与降级策略一致。  
R2：若出画说话，按 `r2-prompt` 同时交信封。

### `r2-prompt`

写或审计 `prompts/r2_realtime_dialogue.json`：

1. load `references/R2_DIALOGUE_PROMPT.md`  
2. 信封字段齐：`tts.speaker` + `type: realtime_dialogue` + `dialog.{bot_name,system_role,audit_response,speaking_style,character_manifest}`  
3. `system_role` 按 §2 章节写；禁止职业原型腔；默认 1–2 行可念  
4. `speaking_style` 压成 2–6 味道词；`audit_response` 是人设一句，不是客服  
5. 卡面加 `r2_dialogue` 指针；**不要**把说话层糊进 `world_setting` 或导播  

脚手架可从 `{DOKI_WORKSPACE}/packs/_template/prompts/r2_realtime_dialogue.json` 复制再填。

### `seed` / `r1-seed`

数字人 locked-portrait seed 制作或审计：

1. load `~/.grok/skills/pixverse-r1/references/SEED_VIDEO.md`  
2. 按该文件 Agent 协议执行（master still → idle 段 → ~40s loop → 验收）  
3. 产物落到 pack `assets/r1/seed.mp4` + `seed_still.png`  
4. `r1_world.json`：`style: Ambient`，路径指针，**不**把运动写进 `world_setting`  
5. 本 skill 不复制构图铁律

### `mechanics`

改 manifest + data；保持 JSON 可编辑。  
R1：改 `r1_world.json`；world_setting ≤ 建议篇幅（世界观非剧情）。

### `frontend`

改根 index + play/app.js；保证 `python3 -m http.server` 在 pack 根可开 `index.html?host=static`。  
R1：static 模式应能打开壳并显示「需 bridge/代理」；`host=bridge` 才全链路。

### `micro` / 小机制

按 **MECHANICS_TUNING 套路**：

```text
mechanics/data/<name>.json
play/<name>.js
index.html 挂一点 UI
app.js boot 里 initXxx()
```

例：Lofi 电台 = `lofi_radio.json` + `lofi-radio.js` + 右下角控件。  
R1 导播条视为一种「重」小机制：独立 `r1-stream.js`，勿缠死主对话状态机。

### `wild`

把野生 demo 收成档 1：

1. 取 id / 入口 / runtime  
2. 写最小 pack.json + game.json  
3. 发现页卡面可先用占位  
4. 文档写清「内部仍乱、宿主只负责点开」  
5. **若是 R1/Agora demo：** 抽掉 hardcoded key → `stream_session` 宿主需求；runtime 标 `stream-client`  

### `export-static`

```bash
# 若 pack 有 scripts/export-frontend-static.sh 则跑
# 否则 rsync 排除 server、config.local、.git、zip、
#   pixverse_r1_session.json、**/*token*、.env*
```

### `handoff`

打 `dist/<slug>-dokiworld-handoff-YYYYMMDD/`：`00-START-HERE.zh.md` + DEPLOY + pack 无密钥。  
R1：START 文档写明「需宿主 stream 代理与 PIXVERSE_API_KEY」。

### `ship-p0`

只列发现页映射：卡面图、name/tagline/greeting、tags、safety；PR 描述一页纸。  
R1 可先 P0 纯聊，P2-stream 再出画。

---

## 6. 质量门槛（可合入前）

1. **一张卡能讲清** hook  
2. **3 分钟可感** 机制（不是纯聊）  
3. **失败可恢复**（localStorage / 重置；R1 含重新预约）  
4. **静态可玩主路径**（`frontend-static` 时）；**stream-client** 时 = 壳可开 + 无流时礼貌降级 + 有宿主时出画  
5. **无密钥 / 无生产 Node / 无擅自 DDL**  
6. **FRONTEND_HOST.md** 存在且路径与 entry 一致  
7. **R1 额外：** 用完 close；不关 session 不叫完成；init 等 `generation_started`  
8. **R2 出画说话：** `r2_realtime_dialogue.json` 对照 `R2_DIALOGUE_PROMPT.md`；默认两行能念  
9. **数字人 seed：** `assets/r1/seed.mp4` 对照 pixverse-r1 `SEED_VIDEO.md`；不合格不靠导播补镜头  

---

## 7. 反模式（实战踩过）

| 反模式 | 正确 |
|--------|------|
| 顶栏再画一层假 Dokiworld Download/Library | 游戏壳全屏；宿主自己有大厅 |
| 入口深埋 `play/index.html` 却文档写错 | **根 `index.html`** 为主；play 可重定向 |
| 为每个小功能改主仓 | 先 pack 内 JSON+JS |
| 生产依赖 pack 内 DeepSeek 代理 | 宿主桥接主仓 LLM |
| 把 ST 模块标题栏当 Doki 标准 | ST 是支线；Doki 用影院/游戏 UI |
| 要求 demo 先工整再准入 | 先能点开；格式后凝练 |
| 一份文件拆十处又找不到 | 交付物路径写死中文桌面别名或 handoff 00-START |
| **API key / Agora token 写进 pack 静态** | **宿主或本地 server 代理；token 短时下发** |
| **R1 当普通「提交等 MP4」** | **实时棚：预约→Session→Agora→导播→close** |
| **用 `rtc` mode 导致无法 setClientRole** | **`live` + host**（见 pixverse-r1） |
| **world/create 用 `prompt` 字段** | **`world_setting` 和/或 `image_url` + 必填 `style`** |
| **把角色 system 长文塞进 world_setting** | **人设归 prompts / R2 信封；场景归 r1_world；构图归 seed** |
| **数字人 seed 远景/运镜/背景粒子/8s 单循环** | **locked-portrait：近景中景、fixed camera、~40s idle 词库、still plate**（`SEED_VIDEO.md`） |
| **R2 数字人只写卡面短字段、无信封** | **`prompts/r2_realtime_dialogue.json` 按示范字段** |
| **speaking_style 写成小作文 / audit 用客服腔** | **2–6 味道词；拒词也是角色一句** |
| **默认回复写成说明书** | **1–2 短行，给口型念** |
| **导播与角色对话混成一条无分流** | **明确 chat_to_director 开关；默认可分轨** |
| **复制整份 pixverse 字段表进 pack 文档后过期** | **skill_ref → pixverse-r1 实测文档** |
| **文字假德州/假麻将当完整玩法** | **同页嵌入 games/game-\* 真 SPA** |
| **新窗口打开牌桌、女主留在原页** | **同壳 iframe + 左数字人** |
| **R1 只收「笑一下」无牌局状态** | **【进程感知】手号/街道/底池/操作** |
| **无下行 JSON 却编数字人聊天** | **只导播画面；台词走 character.say** |
| **假牌旧 JS 缓存** | **no-store + ?v= cache bust** |

---

## 8. Session Bootstrap（Agent）

```
load:
  - {SKILL_ROOT}/SKILL.md
  - {SKILL_ROOT}/references/CARTRIDGE_CONTRACT.md
  - {SKILL_ROOT}/references/FRONTEND_STATIC.md
  - {SKILL_ROOT}/references/SHIP_CHECKLIST.md
  - {SKILL_ROOT}/references/BATTLE_LOG.md
  - {SKILL_ROOT}/references/PIXVERSE_R1_RUNTIME.md   # 若 runtime=stream-client 或用户提 R1
  - {SKILL_ROOT}/references/R2_DIALOGUE_PROMPT.md    # 若 R2 数字人说话 / realtime_dialogue
  - {PIXVERSE_R1_SKILL}/references/SEED_VIDEO.md     # 若数字人 seed / 小幅度高稳定
  - {SKILL_ROOT}/references/DIGITAL_HUMAN_GAME.md    # 若数字人×完整玩法 / stream-r1-game
  - {PIXVERSE_R1_SKILL}/SKILL.md                     # 同上 R1
  - {DOKI_WORKSPACE}/PRINCIPLES.md
  - {DOKI_WORKSPACE}/card-spec/CARD_PACK_SPEC.md
  - {PACK}/pack.json, pipeline_state.json, FRONTEND_HOST.md  # 若存在
  - ~/.grok/skills/world-bible/SKILL.md                      # 若无 temperament lock / WORLD_BIBLE
  - {DOKI_WORKSPACE}/packs/tang-noble-lady/          # 数字人×德州参考（若存在）
preflight:
  - DOKI_WORKSPACE 存在
  - slug / runtime / entry 已定
  - 不把 config.local / PIXVERSE_API_KEY / session json 拷进 dist
  - stream-client 时确认 host_requirements 含 stream_session
  - embed_full_game 时确认无文字假牌路径、有 R1 进程感知或文档标明「仅静态」
```

`todo_write` 跟踪 D0–D6；checkpoint → `pipeline_state.json`。

---

## 9. 一句话口令（给作者与开发）

> **卡是插座；卡带是电器身份证；内部可以野；宿主保持瘦；生产只跑前端；对话能力借宿主；实时数字人借宿主订棚，pack 只负责出画与导播；数字人 seed 用 locked-portrait（近景、死镜头、死背景、~40s idle）；R2 说话用 realtime_dialogue 信封，写具体那个不是原型，两行能念；完整玩法嵌同页真 SPA，假牌杀掉；数字人必须吃进程。**

细节：`references/*`。ST 全套仍用 `/galgame-maker`。R1 字段级对接用 `/pixverse-r1`。外部 game 交付用 `/dokiimport`。
