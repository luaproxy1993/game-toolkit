#!/usr/bin/env python3
"""PixVerse R1 realtime HTTP client (verified fields).

Usage:
  export PIXVERSE_API_KEY=sk-...
  python3 r1_client.py list
  python3 r1_client.py world --setting "雨夜东京巷" --style Ambient
  python3 r1_client.py reserve --preset 6 --mode queue
  python3 r1_client.py query --rid 123
  python3 r1_client.py session --rid 123 --preset 6
  python3 r1_client.py close --db-session 123
  python3 r1_client.py record --db-session 123

Looks for PIXVERSE_API_KEY in env, then common project .env paths.
Never prints the full API key.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

BASE = os.environ.get("PIXVERSE_BASE_URL", "https://app-api.pixverse.ai").rstrip("/")
CURL = "/usr/bin/curl" if Path("/usr/bin/curl").exists() else "curl"


def load_dotenv_files() -> None:
    candidates = [
        Path.cwd() / "config" / ".env",
        Path.cwd() / ".env",
        Path.home() / "sillytavern-wework-lunch-case" / "config" / ".env",
    ]
    for env_path in candidates:
        if not env_path.is_file():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def api_key() -> str:
    load_dotenv_files()
    key = os.environ.get("PIXVERSE_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "PIXVERSE_API_KEY missing. export it or put it in config/.env"
        )
    return key


def call(
    method: str,
    path: str,
    body: dict | None = None,
    timeout: int = 120,
    form: list[str] | None = None,
) -> dict:
    """HTTP via curl (urllib may hit Cloudflare 1010)."""
    url = f"{BASE}{path}"
    trace = str(uuid.uuid4())
    cmd = [
        CURL,
        "-sS",
        "--location",
        "-X",
        method,
        url,
        "--header",
        f"API-KEY: {api_key()}",
        "--header",
        f"Ai-Trace-Id: {trace}",
        "--header",
        "User-Agent: pixverse-r1-client/1.0",
        "--max-time",
        str(timeout),
    ]
    if form is not None:
        for item in form:
            cmd += ["--form", item]
    elif body is not None:
        cmd += [
            "--header",
            "Content-Type: application/json",
            "--data",
            json.dumps(body, ensure_ascii=False),
        ]
    try:
        raw = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"curl failed: {e}") from e
    except FileNotFoundError:
        raise SystemExit(f"curl not found at {CURL}") from None
    if not raw.strip():
        raise SystemExit("empty response body")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit(f"non-JSON response: {raw[:500]}") from None


def dump(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_list(_: argparse.Namespace) -> None:
    dump(call("GET", "/openapi/v2/video/realtime/scenario_list"))


def cmd_world(args: argparse.Namespace) -> None:
    body: dict = {
        "style": args.style,
        "prompt_enhance": args.prompt_enhance,
        "sound_effect": args.sound_effect,
    }
    if args.setting:
        body["world_setting"] = args.setting
    if args.image_url:
        body["image_url"] = args.image_url
    if args.aspect_ratio:
        body["aspect_ratio"] = args.aspect_ratio
    if not args.setting and not args.image_url:
        raise SystemExit("need --setting and/or --image-url")
    data = call("POST", "/openapi/v2/video/realtime/world/create", body, timeout=60)
    dump(data)
    pid = (data.get("Resp") or {}).get("preset_id")
    if pid is not None:
        print(f"\n# preset_id={pid}", file=sys.stderr)


def cmd_reserve(args: argparse.Namespace) -> None:
    body: dict = {"mode": args.mode}
    if args.preset is not None:
        body["preset_id"] = args.preset
    data = call("POST", "/openapi/v2/video/realtime/reservation/create", body)
    dump(data)
    rid = (data.get("Resp") or {}).get("reservation_id")
    if rid is not None:
        print(f"\n# reservation_id={rid}", file=sys.stderr)


def cmd_query(args: argparse.Namespace) -> None:
    dump(
        call(
            "POST",
            "/openapi/v2/video/realtime/reservation/query",
            {"reservation_id": args.rid},
        )
    )


def cmd_cancel(args: argparse.Namespace) -> None:
    dump(
        call(
            "POST",
            "/openapi/v2/video/realtime/reservation/cancel",
            {"reservation_id": args.rid},
        )
    )


def cmd_session(args: argparse.Namespace) -> None:
    body: dict = {"reservation_id": args.rid}
    if args.preset is not None:
        body["preset_id"] = args.preset
    data = call("POST", "/openapi/v2/video/realtime/session/create", body)
    dump(data)
    out = Path(args.out)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n# saved {out.resolve()}", file=sys.stderr)
    resp = data.get("Resp") or {}
    if resp:
        print(
            f"# db_session_id={resp.get('db_session_id')} channel={resp.get('agora_channel')}",
            file=sys.stderr,
        )


def cmd_close(args: argparse.Namespace) -> None:
    dump(
        call(
            "POST",
            "/openapi/v2/video/realtime/session/close",
            {"db_session_id": args.db_session},
        )
    )


def cmd_record(args: argparse.Namespace) -> None:
    dump(
        call(
            "GET",
            f"/openapi/v2/video/realtime/session/record/{args.db_session}",
        )
    )


def cmd_upload(args: argparse.Namespace) -> None:
    path = Path(args.image).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"image not found: {path}")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = call(
        "POST",
        "/openapi/v2/image/upload",
        form=[f"image=@{path};type={mime}"],
        timeout=120,
    )
    dump(data)
    resp = data.get("Resp") or {}
    if resp.get("img_url"):
        print(f"\n# img_id={resp.get('img_id')} img_url={resp.get('img_url')}", file=sys.stderr)


def cmd_voice_list(_: argparse.Namespace) -> None:
    dump(call("POST", "/openapi/v2/video/realtime/character/voice/list", {}))


def cmd_character_create(args: argparse.Namespace) -> None:
    if args.json:
        body = json.loads(Path(args.json).read_text(encoding="utf-8"))
    else:
        missing = [
            n
            for n, v in (
                ("--title", args.title),
                ("--thumbnail-uri", args.thumbnail_uri),
                ("--tts-speaker", args.tts_speaker),
                ("--bot-name", args.bot_name),
                ("--system-role", args.system_role),
                ("--speaking-style", args.speaking_style),
                ("--audit-response", args.audit_response),
            )
            if not v
        ]
        if missing:
            raise SystemExit("need --json or " + " ".join(missing))
        body = {
            "title": args.title,
            "thumbnail_uri": args.thumbnail_uri,
            "aspect_ratio": args.aspect_ratio,
            "tts_speaker": args.tts_speaker,
            "dialog_bot_name": args.bot_name,
            "dialog_system_role": args.system_role,
            "dialog_speaking_style": args.speaking_style,
            "dialog_audit_response": args.audit_response,
        }
    # public API maps user from API-KEY; do not send user_id
    body.pop("user_id", None)
    data = call(
        "POST",
        "/openapi/v2/video/realtime/world/character-create",
        body,
        timeout=120,
    )
    dump(data)
    pid = (data.get("Resp") or {}).get("preset_id")
    if pid is not None:
        print(f"\n# preset_id={pid}  poll: preprocess --preset {pid}", file=sys.stderr)
    if data.get("ErrCode") == 712001:
        print(
            "# 712001 here is text/image audit, not the old world_setting field error",
            file=sys.stderr,
        )


def cmd_preprocess(args: argparse.Namespace) -> None:
    dump(
        call(
            "POST",
            "/openapi/v2/video/realtime/world/preprocess-status",
            {"preset_id": args.preset},
        )
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PixVerse R1 realtime HTTP client")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="scenario_list").set_defaults(func=cmd_list)

    w = sub.add_parser("world", help="world/create")
    w.add_argument("--setting", default=None, help="world_setting text")
    w.add_argument("--image-url", default=None)
    w.add_argument(
        "--style",
        default="Ambient",
        choices=["POV", "Ambient", "Dramatic"],
    )
    w.add_argument("--aspect-ratio", default="16:9")
    w.add_argument("--prompt-enhance", action="store_true")
    w.add_argument("--sound-effect", action="store_true", default=False)
    w.set_defaults(func=cmd_world)

    r = sub.add_parser("reserve", help="reservation/create")
    r.add_argument("--preset", type=int, default=None)
    r.add_argument("--mode", default="queue", choices=["exclusive", "queue"])
    r.set_defaults(func=cmd_reserve)

    q = sub.add_parser("query", help="reservation/query")
    q.add_argument("--rid", type=int, required=True)
    q.set_defaults(func=cmd_query)

    c = sub.add_parser("cancel", help="reservation/cancel")
    c.add_argument("--rid", type=int, required=True)
    c.set_defaults(func=cmd_cancel)

    s = sub.add_parser("session", help="session/create")
    s.add_argument("--rid", type=int, required=True)
    s.add_argument("--preset", type=int, default=None)
    s.add_argument("--out", default="pixverse_r1_session.json")
    s.set_defaults(func=cmd_session)

    cl = sub.add_parser("close", help="session/close")
    cl.add_argument("--db-session", type=int, required=True)
    cl.set_defaults(func=cmd_close)

    rec = sub.add_parser("record", help="session/record")
    rec.add_argument("--db-session", type=int, required=True)
    rec.set_defaults(func=cmd_record)

    up = sub.add_parser("upload", help="image/upload → img_url for thumbnail_uri")
    up.add_argument("--image", required=True)
    up.set_defaults(func=cmd_upload)

    sub.add_parser("voice-list", help="character/voice/list").set_defaults(
        func=cmd_voice_list
    )

    ch = sub.add_parser("character", help="world/character-create (R2 digital human)")
    ch.add_argument("--json", default=None, help="full request body JSON")
    ch.add_argument("--title", default=None)
    ch.add_argument("--thumbnail-uri", default=None)
    ch.add_argument("--tts-speaker", default=None)
    ch.add_argument("--bot-name", default=None)
    ch.add_argument("--system-role", default=None)
    ch.add_argument("--speaking-style", default=None)
    ch.add_argument("--audit-response", default=None)
    ch.add_argument("--aspect-ratio", default="9:16")
    ch.set_defaults(func=cmd_character_create)

    pp = sub.add_parser("preprocess", help="world/preprocess-status")
    pp.add_argument("--preset", type=int, required=True)
    pp.set_defaults(func=cmd_preprocess)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    # redact key length only
    load_dotenv_files()
    key = os.environ.get("PIXVERSE_API_KEY", "")
    if key:
        print(f"# key ok len={len(key)} base={BASE}", file=sys.stderr)
    args.func(args)


if __name__ == "__main__":
    main()
