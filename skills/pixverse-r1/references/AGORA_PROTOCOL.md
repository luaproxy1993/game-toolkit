# PixVerse R1 — Agora + DataStream Protocol

NPM: `agora-rtc-react@^2.5` (bundles `agora-rtc-sdk-ng` 4.x).  
Do **not** require a separate `agora-rtc-sdk-ng` dependency unless you want it explicit.

## Join

```js
import AgoraRTC from "agora-rtc-react";

// Use live mode: setClientRole is invalid in rtc mode
// (AgoraRTCError INVALID_OPERATION: rtc mode can not use setClientRole)
const client = AgoraRTC.createClient({ mode: "live", codec: "h264" });
await client.setClientRole("host"); // required for uplink data / reliability of control
await client.join(agora_app_id, agora_channel, agora_token, agora_uid);

client.on("user-published", async (user, mediaType) => {
  await client.subscribe(user, mediaType);
  if (mediaType === "video") user.videoTrack?.play(containerEl);
  if (mediaType === "audio") user.audioTrack?.play();
});

client.on("connection-state-change", (cur, prev, reason) => {
  console.log("connection", prev, "->", cur, reason);
});
```

Credentials come from `POST .../session/create` → `agora_*` fields.

## Data channel: 3.x vs 4.x

Partner docs mix both. Prefer **4.x**:

| | 3.x | 4.x (ng) |
|--|-----|----------|
| Create stream | `createDataStream({ordered, reliable})` → streamId | Often **removed** |
| Send | `sendStreamMessage(streamId, payload)` | `sendStreamMessage(payload)` |
| Receive | callback includes streamId | `client.on("stream-message", (uid, payload) => {})` |

Recommended:

```js
async function sendMessage(obj) {
  const payload = new TextEncoder().encode(JSON.stringify(obj));
  // 4.x
  if (client.sendStreamMessage.length >= 1) {
    await client.sendStreamMessage(payload);
    return;
  }
}

if (typeof client.createDataStream === "function") {
  // optional compatibility if method still exists
  await client.createDataStream({ ordered: true, reliable: true });
}

client.on("stream-message", (uid, payload) => {
  const bytes = payload instanceof ArrayBuffer ? new Uint8Array(payload) : payload;
  const msg = JSON.parse(new TextDecoder().decode(bytes));
  handleMessage(msg);
});
```

## Uplink (client → server)

### init_message

```json
{
  "type": "init_message",
  "prompt": "optional initial scene prompt",
  "preset_video_uri": "optional",
  "bgm_volume": 50
}
```

- Send **immediately after join**.
- `prompt` may be omitted: means “start pushing frames”.
- `preset_video_uri`: optional seed video URI. For small-amplitude digital humans, this is the locked-portrait idle loop — see `SEED_VIDEO.md`.
- **Must wait for** downlink `generation_started` before assuming video is live.

### prompt_message

```json
{
  "type": "prompt_message",
  "content": "Suddenly a giant robot appears"
}
```

Special content `detection_prompt`: does not change generation; server may reply with timing:

```json
{
  "type": "prompt_response",
  "data": { "prompt_response_time": 8 }
}
```

Unit: seconds.

## Downlink (server → client)

Base shape:

```ts
interface WSMessage {
  type: string;
  data?: any;
  error?: string;
  session_id?: string;
}
```

| type | Meaning |
|------|---------|
| `session_init` | Session id announce |
| `generation_started` | ACK for init; generation live |
| `generation_status` | Progress / state |
| `prompt_updated` | Prompt applied |
| `audit_result` | Moderation result (also implies delivery) |
| `prompt_response` | Timing probe result |

Examples:

```json
{ "type": "generation_started", "data": { "session_id": "..." } }
{ "type": "prompt_updated", "data": { "content": "出现大象..." } }
{ "type": "audit_result", "data": { "status": "approved", "content": "出现大象" } }
```

## ACK table (application-level reliability)

DataStream is **not** fully reliable. Implement wait + timeout + retry.

| Send | Wait for |
|------|----------|
| `init_message` | `generation_started` (**strict**) |
| `prompt_message` | `prompt_updated` and/or `audit_result` |

## Troubleshooting

**No server messages**

1. Listening on `stream-message`?
2. Payload decoded as UTF-8 JSON?
3. Joined successfully (`connectionState`)?

**Send fails**

1. `setClientRole('host')`?
2. Payload is `Uint8Array`?
3. Still in channel?

**Black screen**

1. Subscribed to remote video track?
2. Sent `init_message` and received `generation_started`?
3. Reservation still inside end timestamp?

**Unstable connection**

- Handle `connection-state-change`
- Optional heartbeat / re-join with fresh session if expired

## React note

`agora-rtc-react` also exports hooks/components (`AgoraRTCProvider`, `useJoin`, `RemoteUser`, …).  
For R1 control plane you still need raw `client.sendStreamMessage` / `stream-message` on the RTC client instance (`useRTCClient()`).
