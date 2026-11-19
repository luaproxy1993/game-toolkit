# stream-client · PixVerse R1 卡带契约

> 本文件是 **doki-game-maker 侧** 的 R1 收口规范。  
> HTTP 字段、错误码、Agora 4.x 细节、CLI：**以** `~/.grok/skills/pixverse-r1/` **为准**（VERIFIED_API / AGORA_PROTOCOL / r1_client.py）。

## 1. 产品位置

```text
发现页角色卡
    → 点开 pack（runtime: stream-client）
        → 宿主代理：scenario/world → reserve → session
        → pack：Agora 进房 → init → 出画 → 用户导播 / 可选角色聊
        → 离开：close（放并发坑）
```

R1 **不是** 异步文生视频（提交等 MP4）。是 **预约时间窗内的实时生成直播**。

| 能力 | 谁做 |
|------|------|
| 持有 `PIXVERSE_API_KEY` | 宿主生产服务 或 本地 `server/` 预览 |
| scenario_list / world/create | 宿主代理 |
| reservation create/query/cancel | 宿主代理 |
| session create/close/record | 宿主代理 |
| 下发 Agora 四件套给 iframe | 宿主 → postMessage |
| join / subscribe / play | **pack 前端** |
| init_message / prompt_message | **pack 前端**（DataStream） |
| 角色人设对话 LLM | 宿主 pack-chat（可选并联） |
| 卡面 / tagline / 降级 UI | pack |

## 2. pack.json 片段

```json
{
  "id": "doki.pack.example-r1",
  "slug": "example-r1",
  "integration": {
    "runtime": "stream-client",
    "frontend_entry": "index.html",
    "host_mount_hint": "/game-packs/example-r1/index.html?host=bridge",
    "stream": {
      "provider": "pixverse-r1",
      "protocol": "agora-rtc + datastream",
      "host_proxy": true,
      "skill_ref": "pixverse-r1"
    }
  },
  "host_requirements": ["dialogue", "stream_session", "client_state"],
  "needs_schema_change": false
}
```

`needs_schema_change: true` 仅当主仓完全没有 stream 代理、必须先合 P0 宿主能力时使用，并在 FRONTEND_HOST.md 写最小 diff。

## 3. mechanics：`r1_world.json`

路径：`mechanics/data/r1_world.json`（无密钥）。

| 字段 | 说明 |
|------|------|
| `provider` | 固定 `pixverse-r1` |
| `mode` | `queue`（推荐）\| `exclusive` |
| `style` | `POV` \| `Ambient` \| `Dramatic`（自定义 world 必填） |
| `aspect_ratio` | `16:9` \| `9:16` |
| `world_setting` | 世界观文案（非具体剧情）；与 `image_url` 至少一个（自定义时） |
| `image_url` | 可选参考图 URL（宿主可代传） |
| `preset_id` / `scenario_id` | 官方世界观；建会话时 scenario 当 preset 用 |
| `init_prompt` | 开机可选 prompt |
| `sample_directors` | UI 快捷导播句 |
| `chat_to_director` | `true` 时用户聊天句同步 `prompt_message` |
| `auto_close_on_unload` | 默认 `true` |
| `prompt_enhance` | 可选 bool，交给 world/create |

**分工：**

- `prompts/*.md` / 角色 system → 宿主纯聊怎么说  
- `prompts/r2_realtime_dialogue.json` → **R2 出画说话**（`R2_DIALOGUE_PROMPT.md`）  
- `assets/r1/seed.mp4` → **数字人静息态**（pixverse-r1 `SEED_VIDEO.md`；小幅度高稳定必做）  
- `world_setting` → 世界长什么样（静景；不写动效）  
- `prompt_message` → 此刻发生什么  

## 4. postMessage 扩展

兼容原有 ready/init/chat/result/close。Stream 增量：

### 4.1 开流

```js
// child → parent
{
  type: "dokiworld-stream-open",
  requestId: "uuid",
  provider: "pixverse-r1",
  // 二选一或组合：有 preset 则少 world
  preset_id: 6,
  world: {
    world_setting: "…",
    style: "Ambient",
    aspect_ratio: "9:16",
    image_url: null,
    prompt_enhance: false
  },
  mode: "queue"
}
```

宿主职责（逻辑顺序，细节见 pixverse-r1）：

1. 若仅有 world → `world/create` → `preset_id`  
2. `reservation/create` → 轮询至 `ACTIVE`（或返回排队状态给 UI）  
3. `session/create` → 回传 Agora 字段  
4. **绝不**把 API-KEY 回传 child  

```js
// parent → child 成功
{
  type: "dokiworld-stream-session",
  requestId: "uuid",
  agora_app_id: "…",
  agora_token: "…",
  agora_channel: "…",
  agora_uid: 123,
  session_id: "…",
  db_session_id: 456,
  reservation_end_timestamp: 1710000000000
}

// parent → child 失败
{
  type: "dokiworld-stream-session",
  requestId: "uuid",
  error: "Reached the limit for concurrent generations."
}
```

排队中可选用中间消息（可选约定）：

```js
{ type: "dokiworld-stream-status", requestId, status: "PENDING", queue_position, estimated_wait_seconds }
```

### 4.2 关流 / 成片

```js
// child → parent
{ type: "dokiworld-stream-close", requestId, db_session_id: 456 }
// parent → child
{ type: "dokiworld-stream-closed", requestId, ok: true }

// 可选成片
{ type: "dokiworld-stream-record", requestId, db_session_id: 456 }
{ type: "dokiworld-stream-record-result", requestId, video_url: "https://…" }
```

pack 在 `pagehide` / `beforeunload` / 用户点返回时 **尽量**发 close（`sendBeacon` 或宿主监听 iframe unload 兜底）。

## 5. pack 前端最小行为

```text
boot
  → load r1_world.json
  → UI: 进入世界 / 导播输入 / 关闭
  → on 进入:
        post stream-open
        wait stream-session
        Agora: live + host + join
        send init_message
        wait generation_started  (超时重试)
        play remote video/audio
  → on 导播:
        send prompt_message { content }
        可选等 prompt_updated / audit_result
  → on 关闭/卸载:
        post stream-close
        client.leave()
```

依赖建议：`agora-rtc-react@^2.5`（或宿主统一提供全局 Agora，写进 FRONTEND_HOST）。  
**禁止** `mode: "rtc"` 再 `setClientRole`（会 INVALID_OPERATION）。

## 6. 本地预览代理（server/ 仅开发）

```text
server/
  r1-proxy.js (或 .py)
  # 读 process.env.PIXVERSE_API_KEY
  # POST /api/r1/open  → world? + reserve + wait ACTIVE + session
  # POST /api/r1/close → session/close
  # GET  /api/r1/record/:db_session_id
```

- `config.local` / `.env` gitignore  
- export-static **删除整个 server/**  
- 生产由主仓 BFF 实现同等契约，不部署 pack 内代理  

联调 CLI（不经过 pack）：

```bash
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py list
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py world --setting "…" --style Ambient
# …
```

## 7. 与对话桥并联

| 通道 | 用途 |
|------|------|
| `dokiworld-pack-chat` | 角色扮演、记忆、文案回复 |
| DataStream `prompt_message` | 改实时画面 |

`chat_to_director: false`（默认）：用户句只走 LLM；另设「导播」输入框。  
`chat_to_director: true`：用户句同时 prompt_message（适合「说什么世界就演什么」）；LLM 可关或只做旁白。

## 8. 3 分钟验收（卡带）

- [ ] 发现页卡能讲清「实时世界」  
- [ ] bridge 下 15s 内有动态画面（或明确排队 UI）  
- [ ] 一句导播后画面可感知变化  
- [ ] 关闭后再进可重新预约  
- [ ] 无 key 出现在静态树 / 网络面板的 pack 源文件  
- [ ] 无流时有降级（卡面 + 说明 + 可选纯聊）  

API 级勾选见 pixverse-r1 §验收清单。

## 9. 已知坑（卡带视角）

| 现象 | 处理 |
|------|------|
| 500044 并发满 | close 旧会话；mode=queue；宿主全局限流 |
| 黑屏 | 未 init / 未等 generation_started / 未 subscribe |
| 导播无效果 | 未 host 角色 / payload 非 Uint8Array JSON |
| world 712001 | 不要用 `prompt` 字段建 world |
| token 泄露 | 只短期 postMessage；勿 localStorage 永存 API-KEY |
| 官方文档与实测不符 | 信 pixverse-r1 VERIFIED_API |

## 10. 脚手架检查表（`r1-scaffold`）

- [ ] pack.json runtime + stream 块  
- [ ] host_requirements 含 stream_session  
- [ ] r1_world.json  
- [ ] （数字人）`assets/r1/seed.mp4` 对照 pixverse-r1 `SEED_VIDEO.md`  
- [ ] index.html 播放容器 + 导播 UI  
- [ ] play/r1-stream.js（或等价）  
- [ ] FRONTEND_HOST.md stream 节  
- [ ] pipeline_state stream_provider  
- [ ] .gitignore：`.env*`, `pixverse_r1_session.json`  
- [ ] 无密钥进仓  

## 11. 与完整玩法 / 数字人整合（v2.2）

当 pack 同时挂 **R1 数字人** 与 **完整 game SPA** 时：

- 导播不仅是自由文本，更要 **玩法进程感知**（手号、街道、底池、玩家操作、公共牌）。  
- 角色台词（pack-chat / character.say）与 DataStream **分轨**；无下行对话 JSON 时禁止假聊。  
- 完整契约：`DIGITAL_HUMAN_GAME.md`；参考包 `packs/tang-noble-lady/`。

## 12. 一句话

> **宿主订棚拿钥匙；卡带进房出画导播；用完还坑；密钥永不进 pack；挂完整玩法时数字人必须吃进程。**
