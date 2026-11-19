# PixVerse R1 — Verified API Contract

Verified **2026-07-30** against `https://app-api.pixverse.ai` with Platform `API-KEY`.

When this file conflicts with partner PDF / 飞书 / blog copy, **trust this file**.

## Auth

```
API-KEY: <platform key>
Ai-Trace-Id: <uuid4 per request>
Content-Type: application/json   # POST only
```

Envelope:

```json
{ "ErrCode": 0, "ErrMsg": "Success", "Resp": {} }
```

## Endpoints

### GET `/openapi/v2/video/realtime/scenario_list`

List official worlds.

**Resp:**

```json
{
  "total": 8301,
  "data": [
    {
      "scenario_id": 6,
      "name": "Cyberpunk City",
      "image_thumbnail": "https://...",
      "aspect_ratio": "16:9"
    }
  ]
}
```

Notes:

- First page ~20 items observed; query pagination params (`page`, `limit`, …) did **not** change result set in probe.
- Use `scenario_id` as `preset_id` downstream.

---

### POST `/openapi/v2/video/realtime/world/create`

Custom world preset.

**Body (verified):**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `world_setting` | string | one of setting/url | World description, not plot |
| `image_url` | string | one of setting/url | PixVerse-accessible OSS URL |
| `style` | string | **yes** | `POV` \| `Ambient` \| `Dramatic` only |
| `prompt_enhance` | bool | no | default false; true = image dominates |
| `aspect_ratio` | string | no | `16:9` \| `9:16` |
| `sound_effect` | bool | no | |

**Wrong (official example):** `"prompt": "..."` → `712001` need world_setting or image_url.

**Missing style:** `400017` `invalid style, available style names: POV, Ambient, Dramatic`

**Success:**

```json
{ "ErrCode": 0, "ErrMsg": "Success", "Resp": { "preset_id": 267864 } }
```

Latency: ~5–10s.

---

### POST `/openapi/v2/video/realtime/reservation/create`

```json
{ "preset_id": 6, "mode": "exclusive" }
```

| Field | Notes |
|-------|-------|
| `preset_id` | optional in docs; pass real id when known |
| `mode` | `exclusive` \| `queue` |

**Resp fields:** `reservation_id`, `resource_id`, `status` (`PENDING`/`ACTIVE`), `queue_position`, `estimated_wait_seconds`, `scheduled_start_timestamp`, `scheduled_end_timestamp`, `is_new`, `mode`, `pipeline`

**Errors:**

- `500044` `Reached the limit for concurrent generations.` → close old sessions or use `queue`

**Observed:** `mode=queue` can return `status=ACTIVE`, `is_new=false` (reuse existing reservation).

---

### POST `/openapi/v2/video/realtime/reservation/query`

```json
{ "reservation_id": 166557886396352 }
```

**status:** `PENDING` | `ACTIVE` | `GENERATING` | `COMPLETED` | `EXPIRED`

Also: `is_connected`, `queue_position`, `estimated_wait_seconds`, `mode`, `pipeline`, timestamps.

**Policy:** If `ACTIVE`, create session immediately. Queue mode + ACTIVE works (verified).

---

### POST `/openapi/v2/video/realtime/reservation/cancel`

```json
{ "reservation_id": <int> }
```

Cannot cancel `COMPLETED` → error like `Cannot cancel reservation in COMPLETED status`.

---

### POST `/openapi/v2/video/realtime/session/create`

```json
{ "reservation_id": 166557886396352, "preset_id": 267864 }
```

- `reservation_id` as JSON number works.
- `preset_id` should be the world you want for this run.

**Resp:**

| Field | Example role |
|-------|----------------|
| `session_id` | UUID; often == channel |
| `db_session_id` | snowflake int; close + record |
| `agora_app_id` | string |
| `agora_token` | short-lived RTC token |
| `agora_channel` | channel name |
| `agora_uid` | int |
| `reservation_end_timestamp` | unix ms or null |

---

### POST `/openapi/v2/video/realtime/session/close`

```json
{ "db_session_id": 166557892988416 }
```

---

### GET `/openapi/v2/video/realtime/session/record/{db_session_id}`

```json
{ "Resp": { "video_url": "https://media.pixverse.ai/...." } }
```

No video if: closed before first frame; moderation filtered.

---

## Doc lies vs reality

| Official doc | Reality |
|--------------|---------|
| world body field `prompt` | Use `world_setting` |
| style optional | style required |
| exclusive only for direct session | queue + ACTIVE also OK |
| must createDataStream always | 4.x may not expose it; use sendStreamMessage |
| session reservation_id type "string" and description says mode | Copy-paste garbage; send reservation_id number |

### POST `/openapi/v2/image/upload`

Multipart field `image`. **Resp:** `img_id`, `img_url`. Use `img_url` as digital-human `thumbnail_uri`.

Verified 2026-09-14.

### POST `/openapi/v2/video/realtime/character/voice/list`

Empty JSON body. **Resp.data[]:** `name`, `url`, `desc`. Use `name` as `tts_speaker`. Do not invent Saturn ids.

### POST `/openapi/v2/video/realtime/world/character-create`

R2 digital human preset. **Do not send `user_id`** (mapped from API-KEY).

Required: `title`, `thumbnail_uri`, `tts_speaker`, `dialog_bot_name` (≤20 chars), `dialog_system_role`, `dialog_speaking_style`, `dialog_audit_response`. Optional: `aspect_ratio` (`9:16` default).

**Success:** `Resp.preset_id`. Then poll preprocess-status.

**712001 `text content audit failed`:** the *system_role* (or image) failed moderation — not the old world `prompt` field error. Strip crime/safety-keyword blocks; retry a shorter role.

Verified 2026-09-14: Gu Qing `preset_id` 318725 from Artgerm closeup.

### POST `/openapi/v2/video/realtime/world/preprocess-status`

```json
{ "preset_id": 318725 }
```

`Resp.status`: `PROCESSING` → **`SUCCESS`** before reservation. Other fail-like strings: do not reserve.

## Transport notes

- Prefer **curl** for automation. Pure Python `urllib` may get Cloudflare `error code: 1010`.
- Keep PATH intact (`/usr/bin/curl`); nested shell functions in broken envs can drop PATH.
- Never log full API key or long-lived secrets; session tokens are short-lived but still sensitive.

## Naming map

| Concept | IDs you may see |
|---------|-----------------|
| Official world | `scenario_id` from list |
| Custom world | `preset_id` from world/create |
| Session create body | always `preset_id` (pass either) |
| Close / record | `db_session_id` |
| Agora room | `agora_channel` ≈ `session_id` |
