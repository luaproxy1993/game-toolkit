---
name: pixverse-r1
description: >
  PixVerse R1 实时视频世界模型对接：世界观列表/自定义 World、预约与查询、创建 Session、
  Agora 进房与 DataStream 指令（init/prompt）、成片拉取与关闭会话。数字人 locked-portrait
  seed（近景中景、fixed camera、~40s idle loop、still plate 背景）。基于本机实测校正，
  修正官方 AI 文档中的字段错误与 3.x/4.x 矛盾。Use when the user runs /pixverse-r1,
  says "R1", "PixVerse R1", "实时生成", "realtime session", "scenario_list",
  "world/create", "reservation", "agora r1", "实时世界观", "seed video",
  "数字人种子", "idle loop", "locked-portrait", or wants to build
  products on PixVerse real-time video API.
argument-hint: "[list|world|reserve|query|session|demo|close|record|guide|seed]"
user-invocable: true
metadata:
  short-description: PixVerse R1 实时视频 API 对接
  version: "1.2.0"
  verified: "2026-07-30 against app-api.pixverse.ai"
  product_packaging: "doki-game-maker@>=2.1.0 stream-client / r1-scaffold"
---

# PixVerse R1 — 实时视频对接 Skill

把 **PixVerse R1 实时世界模型**接到产品里：选/建世界观 → 预约 → Session → Agora 出画 → 文字导播 → 关会话/拉成片。

**默认 `SKILL_ROOT`** = `~/.grok/skills/pixverse-r1`

**必读参考（按需）：**

| 文件 | 用途 |
|------|------|
| `references/HUMAN_GUIDE.zh-CN.md` | 非技术可读总览（产品/验收） |
| `references/VERIFIED_API.md` | 已实测字段、错误码、与官方文档差异 |
| `references/AGORA_PROTOCOL.md` | 进房、DataStream、上下行消息与 ACK |
| `references/SEED_VIDEO.md` | 数字人 locked-portrait seed：构图、idle loop、still plate |
| `scripts/r1_client.py` | 命令行：list / world / reserve / query / session / close / record |

---

## 0. 调用

```text
/pixverse-r1
/pixverse-r1 guide              # 人话版流程
/pixverse-r1 list               # 官方世界观列表
/pixverse-r1 world              # 自定义 World → preset_id
/pixverse-r1 reserve [preset]   # 创建预约
/pixverse-r1 query <rid>        # 查预约
/pixverse-r1 session <rid> [preset]
/pixverse-r1 close <db_session_id>
/pixverse-r1 record <db_session_id>
/pixverse-r1 demo               # 脚手架 React/Agora 最小页
/pixverse-r1 seed               # 数字人 locked-portrait seed 制作/审计
```

Session 启动：

1. 读本 SKILL.md + `references/VERIFIED_API.md`
2. 确认 `PIXVERSE_API_KEY`（env 或项目 `config/.env`，**永不打印完整 key**）
3. 按用户目标走：只查文档 / 调 API / 写客户端 / 做产品 demo / **做数字人 seed**
4. 长链路用 `todo_write`：world → reserve → ACTIVE → session → Agora → close
5. 数字人小幅度高稳定：先 load `references/SEED_VIDEO.md`，seed 不合格不靠导播补镜头

---

## 1. 心智模型（铁律）

R1 **不是**「提交 → 轮询 → 下载 MP4」的普通文生视频。

```text
HTTP API          = 订棚、拿钥匙、关灯
Agora RTC         = 看实时画面 + 听声音
Agora DataStream  = 文字对讲（开机 / 导播）
```

顺序不能乱：

```text
preset/scenario → reservation → status=ACTIVE → session/create
  → Agora join + host → init_message (等 generation_started)
  → prompt_message … → session/close → (可选) record
```

**并发：** 不关 Session 会占坑 → 常见 `500044 Reached the limit for concurrent generations.`

---

## 2. 鉴权与 Base

| 项 | 值 |
|----|-----|
| Base | `https://app-api.pixverse.ai` |
| Header | `API-KEY: <key>` |
| Header | `Ai-Trace-Id: <新 UUID 每请求>` |
| Content-Type | `application/json`（POST body） |

响应外壳统一：

```json
{ "ErrCode": 0, "ErrMsg": "Success", "Resp": { } }
```

`ErrCode !== 0` 视为失败；先读 `ErrMsg`。

环境变量：

```bash
export PIXVERSE_API_KEY=...
# 可选
export PIXVERSE_BASE_URL=https://app-api.pixverse.ai
```

本地常见路径：`sillytavern-wework-lunch-case/config/.env` 里的 `PIXVERSE_API_KEY`（与 R1 同一 Platform key，实测可用）。

---

## 3. HTTP 步骤（已验证）

### 3.1 官方世界观列表

```http
GET /openapi/v2/video/realtime/scenario_list
```

- `Resp.total` 很大；实测一次返回约 20 条精选
- 条目字段：`scenario_id`, `name`, `image_thumbnail`, `aspect_ratio`
- **建会话时把 `scenario_id` 当 `preset_id` 用**（官方文档命名混乱）

### 3.2 自定义 World

```http
POST /openapi/v2/video/realtime/world/create
```

**必填（实测）：**

| 字段 | 规则 |
|------|------|
| `world_setting` 和/或 `image_url` | **至少一个** |
| `style` | **必填**：`POV` \| `Ambient` \| `Dramatic` |

可选：`prompt_enhance` (bool, 默认 false)、`aspect_ratio` (`16:9`/`9:16`)、`sound_effect` (bool)

**禁止用示例里的 `prompt` 字段** → 会 712001「world_setting 和 image_url 必须至少提供一个」。

成功：`Resp.preset_id` (int)。

Style 人话：

| style | 用途 |
|-------|------|
| POV | 第一人称/跟随探索 |
| Ambient | 氛围稳定、小动作、少自主剧情 |
| Dramatic | 多人、台词、带叙事 |

World 文案写**世界观**不写具体剧情；建议 ≤100 字/词。  
数字人小幅度高稳定：`style: Ambient` + locked-portrait seed（`references/SEED_VIDEO.md`）；`world_setting` 只写静景。

### 3.3 创建预约

```http
POST /openapi/v2/video/realtime/reservation/create
{ "preset_id": <int>, "mode": "exclusive" | "queue" }
```

- `exclusive` 资源紧时易 `500044` → 改 `queue` 或等释放
- `is_new: false` = 返回了已有预约（可继续用）
- 成功拿 `reservation_id`

### 3.4 查询预约

```http
POST /openapi/v2/video/realtime/reservation/query
{ "reservation_id": <int> }
```

| status | 动作 |
|--------|------|
| PENDING | 轮询；看 `queue_position` / `estimated_wait_seconds` |
| **ACTIVE** | **立刻 session/create** |
| GENERATING | 多半已有会话 |
| COMPLETED / EXPIRED | 重新预约 |

注意：文档写「独占才能直接建 Session」——**不完全对**。实测 `mode=queue` + `status=ACTIVE` 可建 Session。

### 3.5 创建 Session

```http
POST /openapi/v2/video/realtime/session/create
{ "reservation_id": <int>, "preset_id": <int> }
```

`reservation_id` 用 **number** 即可（string 也可试）。

`Resp` 关键字段：

| 字段 | 用途 |
|------|------|
| `session_id` | 常与 channel 相同 |
| `db_session_id` | 关会话 / 拉成片 |
| `agora_app_id` | Agora App ID |
| `agora_token` | RTC Token（短时） |
| `agora_channel` | 频道名 |
| `agora_uid` | 客户端 UID |
| `reservation_end_timestamp` | 窗口结束（Unix ms） |

**Token/完整响应写入本地文件（如 `pixverse_r1_session.json`），勿贴聊天、勿提交 git。**

### 3.6 关 Session / 取消预约 / 成片

```http
POST /openapi/v2/video/realtime/session/close
{ "db_session_id": <int> }

POST /openapi/v2/video/realtime/reservation/cancel
{ "reservation_id": <int> }

GET /openapi/v2/video/realtime/session/record/{db_session_id}
→ Resp.video_url
```

无成片常见原因：未出画就 close；审核过滤。

### 3.7 延迟预期

| 步骤 | 时间 |
|------|------|
| world/create | 5–10s |
| reservation/create | &lt;1s |
| session + init 后出画 | 5–10s |
| 预约窗口 | 约数分钟（看 start/end timestamp） |

---

## 4. Agora + 消息协议（摘要）

依赖：`agora-rtc-react@^2.5`（内置 `agora-rtc-sdk-ng` 4.x，**不必**再装 sdk-ng）。

```js
import AgoraRTC from "agora-rtc-react";

// live + host 必需：rtc 模式下 setClientRole 会抛
// INVALID_OPERATION: rtc mode can not use setClientRole
const client = AgoraRTC.createClient({ mode: "live", codec: "h264" });
await client.setClientRole("host"); // DataStream 上行导播需要
await client.join(appId, channel, token, uid);

client.on("user-published", async (user, mediaType) => {
  await client.subscribe(user, mediaType);
  if (mediaType === "video") user.videoTrack?.play("#player");
  if (mediaType === "audio") user.audioTrack?.play();
});
```

### DataStream（4.x 校正）

官方文档 3.x/4.x **自相矛盾**。优先 4.x：

```js
async function sendMessage(data) {
  const payload = new TextEncoder().encode(JSON.stringify(data));
  await client.sendStreamMessage(payload);
}

// 仅当方法存在时兼容旧写法
if (typeof client.createDataStream === "function") {
  await client.createDataStream({ ordered: true, reliable: true });
}

client.on("stream-message", (uid, payload) => {
  const msg = JSON.parse(new TextDecoder().decode(payload));
  handleMessage(msg);
});
```

### 上行

```js
// 开机（prompt 可省略，表示开始推流）
await sendMessage({ type: "init_message", prompt: "..." });
// 必须等到 generation_started 才算真正开画

// 导播
await sendMessage({ type: "prompt_message", content: "Suddenly it rains harder" });

// 问下一段生效时间（不改画面）
await sendMessage({ type: "prompt_message", content: "detection_prompt" });
// → prompt_response.data.prompt_response_time 秒
```

### ACK（业务层可靠）

| 发送 | 等待 |
|------|------|
| `init_message` | **`generation_started`**（严格） |
| `prompt_message` | `prompt_updated` 和/或 `audit_result` |

DataStream **不保证可靠** → 超时重试。

详情：`references/AGORA_PROTOCOL.md`

---

## 5. 脚本用法

```bash
# 从项目 .env 或环境变量读 key
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py list
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py world \
  --setting "雨夜东京小巷，霓虹倒影" --style Ambient
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py reserve --preset 6 --mode queue
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py query --rid <reservation_id>
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py session --rid <id> --preset 267864
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py close --db-session <id>
python3 ~/.grok/skills/pixverse-r1/scripts/r1_client.py record --db-session <id>
```

Session 成功时默认写 `./pixverse_r1_session.json`（可用 `--out`）。

**Shell 注意：** 部分环境里 shell function 会弄丢 PATH；脚本用绝对 `curl`/`python3` 或纯 urllib，且 urllib 可能被 Cloudflare `1010` 拦 → 脚本优先 curl。

---

## 6. Agent 行为准则

1. **以本 skill 的 VERIFIED_API 为准**，官方飞书/PDF 有冲突时相信实测表。
2. 不向用户复述完整 API key / 完整 Agora token；指到本地 json 文件。
3. 创建 Session 后提醒：窗口短暂、用完 **close**，避免 500044。
4. 给非技术用户时用 `HUMAN_GUIDE` 语气；写代码时用 VERIFIED_API + AGORA_PROTOCOL。
5. 脚手架 demo：React + `agora-rtc-react`，中文按钮（预约/进房/开机/导播/关闭）。
6. 与普通 PixVerse 异步 i2v/t2v（`/openapi/v2/video/text/generate` 等）**分离模块**，勿混在一个 client 里硬编码同一套状态机。
7. 数字人小幅度高稳定：先 `SEED_VIDEO.md`；seed 不合格禁止用导播补镜头或背景戏。

---

## 7. 验收清单（产品可勾）

- [ ] 能列出或自建世界观并拿到 preset/scenario id  
- [ ] 预约后能到 ACTIVE（独占满则 queue）  
- [ ] Session 返回 Agora 四件套  
- [ ] 进房 5–15s 内有动态画面  
- [ ] 导播 prompt 后画面有可感知变化  
- [ ] close 后可再次预约  
- [ ] （可选）record 拿到 mp4  

---

## 8. 已知坑（速查）

| 现象 | 原因 / 处理 |
|------|-------------|
| world 712001 | 用了 `prompt` 而非 `world_setting` |
| world 400017 | 缺 `style` 或拼写不在 POV/Ambient/Dramatic |
| reserve 500044 | 并发满：close 旧 session，或 `mode: queue` |
| 黑屏 | 未 init / 未等 generation_started / 未 subscribe 远端 |
| 指令无效 | 未 `setClientRole('host')` / 未编码 Uint8Array |
| `rtc mode can not use setClientRole` | 应用 `mode: "live"` 再 `setClientRole('host')`，不要用 `rtc` |
| urllib 403 `1010` | 换 curl + 正常 User-Agent |
| 文档 createDataStream 必须 | 4.x 可能无此 API；以 sendStreamMessage + 监听为准 |

---

## 9. 收成 Dokiworld 卡带（产品形态）

若目标是 **发现页角色卡 → 点开实时世界**（而非单独 demo 页），用：

```text
/doki-game-maker new <slug> stream-r1
# 或
/doki-game-maker r1-scaffold
```

| 层 | 负责 |
|----|------|
| **pixverse-r1**（本 skill） | HTTP 字段、Agora DataStream、CLI、已知坑、**数字人 seed** |
| **doki-game-maker** | pack 形状、`stream-client` runtime、宿主 postMessage、`r1_world.json`、无密钥合入 |

铁律对齐：

- `PIXVERSE_API_KEY` **只在宿主 / 本地 server**，不进 pack 静态  
- pack：`runtime: stream-client` + `stream.provider: pixverse-r1`  
- 契约全文：`~/.grok/skills/doki-game-maker/references/PIXVERSE_R1_RUNTIME.md`

纯 API 联调、脚手架 React 页仍用本 skill 的 `demo` / `r1_client.py`。

---

## 10. 数字人 seed（小幅度 / 高稳定）

动作幅度小、说话口型稳的数字人：**先做 locked-portrait seed，再订棚。**

完整铁律、idle 词库、~40s 拼接、验收：`references/SEED_VIDEO.md`。

Agent 走 `/pixverse-r1 seed`：master still → 多段 idle → concat ~40s → 验 loop seam 与 still plate → `init_message.preset_video_uri` / pack `assets/r1/seed.mp4`。

---

## 11. 一句话

> **HTTP 订棚拿 Agora 钥匙；进房设 host；init 等 generation_started 才算出画；prompt 导播；用完 close 放坑。数字人先 locked-portrait seed 再说话。字段以本 skill 实测为准，不信 AI 拼的官方示例。进 Doki 大厅则走 doki-game-maker 卡带插座。**
