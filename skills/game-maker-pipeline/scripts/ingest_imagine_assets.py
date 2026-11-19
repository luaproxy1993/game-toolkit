#!/usr/bin/env python3
"""Ingest SuperGrok Imagine PNGs from art/incoming/ → staging → registry output_path."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def find_incoming_file(incoming: Path, asset_id: str) -> Path | None:
    for ext in IMAGE_EXTS:
        p = incoming / f"{asset_id}{ext}"
        if p.is_file():
            return p
    for ext in IMAGE_EXTS:
        p = incoming / f"{asset_id.lower()}{ext}"
        if p.is_file():
            return p
    return None


def basic_checks(path: Path, asset: dict) -> list[str]:
    issues: list[str] = []
    if path.stat().st_size < 1024:
        issues.append("file_too_small")
    name = asset.get("asset_id", "")
    cat = asset.get("category", "")
    if "sprite" in cat or cat == "diegetic_prop":
        if path.suffix.lower() != ".png":
            issues.append("sprite_should_be_png_for_alpha")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest art/incoming into registry paths")
    ap.add_argument("project_root", type=Path)
    ap.add_argument("--promote", action="store_true", help="copy staging → output_path (default: staging only)")
    ap.add_argument("--asset", action="append", default=[], help="only ingest these asset_ids")
    args = ap.parse_args()

    root = args.project_root.resolve()
    incoming = root / "art" / "incoming"
    staging = root / "art" / "staging"
    reg_path = root / "art" / "art-prompt-registry.json"
    log_path = root / "art" / "ingest-log.jsonl"

    if not reg_path.is_file():
        raise SystemExit(f"Missing {reg_path}")
    incoming.mkdir(parents=True, exist_ok=True)
    staging.mkdir(parents=True, exist_ok=True)

    reg = load(reg_path)
    assets = reg.get("assets", [])
    if args.asset:
        allow = set(args.asset)
        assets = [a for a in assets if a["asset_id"] in allow]

    promoted = 0
    staged = 0
    missing = []
    issues_map: dict[str, list[str]] = {}

    for asset in assets:
        aid = asset["asset_id"]
        src = find_incoming_file(incoming, aid)
        if not src:
            missing.append(aid)
            continue
        issues = basic_checks(src, asset)
        if issues:
            issues_map[aid] = issues

        stage_path = staging / f"{aid}.png"
        if src.suffix.lower() == ".png":
            shutil.copy2(src, stage_path)
        else:
            shutil.copy2(src, staging / f"{aid}{src.suffix.lower()}")
            stage_path = staging / f"{aid}{src.suffix.lower()}"
        staged += 1

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "asset_id": aid,
            "source": str(src.relative_to(root)),
            "staging": str(stage_path.relative_to(root)),
            "sha256": sha256(src),
            "issues": issues,
            "promoted": False,
        }

        if args.promote and not issues:
            out = root / asset["output_path"]
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stage_path, out)
            asset["status"] = "ingested_supergrok"
            asset["ingested_at"] = date.today().isoformat()
            asset["content_sha256"] = entry["sha256"]
            promoted += 1
            entry["promoted"] = True
            entry["output_path"] = asset["output_path"]

        log_path.open("a", encoding="utf-8").write(json.dumps(entry, ensure_ascii=False) + "\n")

    reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Ingest summary: staged={staged} promoted={promoted} missing={len(missing)}")
    if missing:
        print("  missing incoming:", ", ".join(missing))
    if issues_map:
        print("  issues (review before promote):")
        for k, v in issues_map.items():
            print(f"    {k}: {v}")
    if issues_map and args.promote:
        print("WARN: promoted only issue-free assets")
        return 2
    return 0 if staged else 1


if __name__ == "__main__":
    raise SystemExit(main())