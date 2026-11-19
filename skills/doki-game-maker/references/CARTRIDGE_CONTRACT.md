# 卡带契约 · 插座模型

## 一句话

Dokiworld 规范的是 **入口与宿主契约**，不是每个游戏内部同构。

## 插座（宿主保证）

1. 发现页能展示卡  
2. 点击能加载 `entry`（URL / iframe / native bridge）  
3. 可选提供：账号、对话 LLM、记忆、计费  
4. 可选接收：result / close  
5. 失败可退回纯聊或大厅  
6. **`stream_session`（stream-client / R1）：** 代理订棚与 Session，向 pack 下发短时 Agora 凭证；**永不**把 `PIXVERSE_API_KEY` 注入前端包  

## 插头（pack 最少字段）

```json
{
  "id": "doki.pack.example",
  "slug": "example",
  "entry_face": "character_key",
  "runtime": "frontend-static",
  "frontend_entry": "index.html",
  "host_mount_hint": "/game-packs/example/index.html?host=bridge",
  "host_requirements": ["dialogue", "client_state"],
  "safety": { "rating": "general" }
}
```

`stream-client` 时追加：

```json
{
  "runtime": "stream-client",
  "host_requirements": ["dialogue", "stream_session", "client_state"],
  "stream": {
    "provider": "pixverse-r1",
    "protocol": "agora-rtc + datastream",
    "host_proxy": true,
    "skill_ref": "pixverse-r1"
  }
}
```

## 野生 → 标准 三档

| 档 | 状态 | 宿主 |
|----|------|------|
| 0 野生 demo | 眼镜+R2、硬编码 R1 key | 可不经大厅 |
| 1 薄封装 | 有 id/entry/runtime + 卡面 | 点卡能调起 |
| 2 标准卡带 | 字段齐、可 export-static 或声明 native/stream | 可合入评审 |

R1 从 0→1：抽掉 hardcoded key，runtime 标 `stream-client`，声明 `stream_session`。

## postMessage 最低集

| type | 方向 |
|------|------|
| `dokiworld-game-ready` | child → parent |
| `dokiworld-game-init` | parent → child |
| `dokiworld-game-initialized` | child → parent |
| `dokiworld-pack-chat` | child → parent |
| `dokiworld-pack-chat-result` | parent → child |
| `dokiworld-game-result` | child → parent |
| `dokiworld-game-close` | child → parent |

## postMessage stream 扩展（`stream_session`）

| type | 方向 |
|------|------|
| `dokiworld-stream-open` | child → parent |
| `dokiworld-stream-status` | parent → child（可选，排队） |
| `dokiworld-stream-session` | parent → child |
| `dokiworld-stream-close` | child → parent |
| `dokiworld-stream-closed` | parent → child |
| `dokiworld-stream-record` | child → parent（可选） |
| `dokiworld-stream-record-result` | parent → child（可选） |

细节：`PIXVERSE_R1_RUNTIME.md`。

## 电器内部（不管）

日程 JSON 形态、Lofi 流地址、AR SDK、R2 路由、R1 导播文案、prompt 长短、是否完美平衡。  
**管边界：** 密钥位置、entry 路径、runtime 声明、close 还坑。
