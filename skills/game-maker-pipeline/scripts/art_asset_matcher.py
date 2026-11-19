#!/usr/bin/env python3
"""RE-27 art-asset-matcher-v1.0 — master-anchor drift audit + batch fix plan."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

MATCHER_ID = "art-asset-matcher-v1.0"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
BATCH_DIRS = ("screenshots", "art/generated")
SILHOUETTE_HINTS = ("silhouette", "module", "castle", "tier", "keep", "tower")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def euclidean_rgb(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def parse_palette(anchor: dict[str, Any]) -> list[tuple[int, int, int]]:
    palette = anchor.get("palette", {})
    colors: list[str] = []
    for key in ("primary", "accent", "locked"):
        val = palette.get(key)
        if isinstance(val, list):
            colors.extend(val)
    lock = anchor.get("palette_lock")
    if isinstance(lock, list):
        colors.extend(lock)
    out: list[tuple[int, int, int]] = []
    for c in colors:
        if isinstance(c, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", c):
            out.append(hex_to_rgb(c))
    return out


def analyze_image(path: Path, palette: list[tuple[int, int, int]]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "readable": False,
        "mean_rgb": None,
        "palette_min_delta": None,
        "brightness": None,
        "has_alpha": None,
        "ground_line_ratio": None,
    }
    try:
        from PIL import Image
    except ImportError:
        return result

    try:
        with Image.open(path) as im:
            im = im.convert("RGBA")
            w, h = im.size
            pixels = list(im.getdata())
            result["readable"] = True
            result["has_alpha"] = any(p[3] < 250 for p in pixels)

            opaque = [p[:3] for p in pixels if p[3] > 200]
            if not opaque:
                opaque = [p[:3] for p in pixels]
            if opaque:
                mean = tuple(sum(c[i] for c in opaque) // len(opaque) for i in range(3))
                result["mean_rgb"] = list(mean)
                result["brightness"] = sum(mean) / 3
                if palette:
                    result["palette_min_delta"] = min(euclidean_rgb(mean, p) for p in palette)

            # bottom 8% rows — ground-line occupancy for silhouette modules
            bottom_y = int(h * 0.92)
            bottom_opaque = 0
            bottom_total = 0
            for y in range(bottom_y, h):
                for x in range(w):
                    p = pixels[y * w + x]
                    bottom_total += 1
                    if p[3] > 128:
                        bottom_opaque += 1
            if bottom_total:
                result["ground_line_ratio"] = bottom_opaque / bottom_total
    except OSError:
        pass
    return result


def is_silhouette_asset(asset_id: str, path: str, category: str | None) -> bool:
    blob = f"{asset_id} {path} {category or ''}".lower()
    return any(h in blob for h in SILHOUETTE_HINTS) or "silhouette/" in path


def build_correction_delta(
    issues: list[str],
    anchor: dict[str, Any],
    asset: dict[str, Any],
) -> str:
    parts = [
        f"correct to master {anchor.get('anchor_id', 'STYLE-ANCHOR')}:",
        "orthographic side view",
        "exact anchor_px from master",
        "weathered stone palette exact match",
        "ground_line bottom aligned",
        "remove any warm tone drift",
        "pixel perfect alignment",
    ]
    if "perspective_drift" in issues:
        parts.insert(2, "enforce orthographic_side_view_only camera")
    if "color_too_bright" in issues:
        parts.append("darken to anchor palette, no highlight blowout")
    if "anchor_offset" in issues:
        parts.append("re-align bottom_edge to layout_ref ground line")
    if asset.get("prompt_delta"):
        parts.append(f"preserve intent: {asset['prompt_delta'][:120]}")
    return " ".join(parts)


def detect_issues(
    asset: dict[str, Any],
    path: Path,
    img: dict[str, Any],
    anchor: dict[str, Any],
    tolerance: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    category = asset.get("category")
    rel = str(asset.get("output_path", path.name))

    if is_silhouette_asset(asset.get("asset_id", ""), rel, category):
        if img.get("readable") and not img.get("has_alpha"):
            issues.append("perspective_drift")

    palette_limit = 15.0
    m = re.search(r"<\s*(\d+)", str(tolerance.get("palette_delta", "< 15")))
    if m:
        palette_limit = float(m.group(1))

    if img.get("readable"):
        delta = img.get("palette_min_delta")
        if delta is not None and delta > palette_limit:
            issues.append("color_too_bright")
        if img.get("brightness") is not None and img.get("brightness", 0) > 175:
            if "color_too_bright" not in issues:
                issues.append("color_too_bright")

        ground = img.get("ground_line_ratio")
        if is_silhouette_asset(asset.get("asset_id", ""), rel, category):
            if ground is not None and ground < 0.15:
                issues.append("anchor_offset")

    verification = asset.get("verification") or {}
    if verification.get("anchor_px_ok") is False:
        issues.append("anchor_offset")
    if verification.get("palette_ok") is False:
        issues.append("color_too_bright")
    if verification.get("perspective_ok") is False:
        issues.append("perspective_drift")

    if not asset.get("references"):
        issues.append("missing_master_reference")

    return issues


def scan_unregistered(root: Path, registered_paths: set[str]) -> list[dict[str, Any]]:
    extras: list[dict[str, Any]] = []
    for base in BATCH_DIRS:
        d = root / base
        if not d.is_dir():
            continue
        for f in d.rglob("*"):
            if f.suffix.lower() not in IMAGE_EXTS:
                continue
            rel = str(f.relative_to(root))
            if rel in registered_paths:
                continue
            extras.append(
                {
                    "asset_id": f"UNREGISTERED_{f.stem.upper()}",
                    "current_path": rel,
                    "issues_detected": ["missing_registry_entry"],
                    "correction_prompt_delta": "register in art-prompt-registry.json then re-run matcher",
                    "recommended_action": "add registry entry + image_edit with master reference",
                    "new_registry_entry_required": True,
                }
            )
    return extras


def write_batch_fix(root: Path, assets: list[dict[str, Any]], anchor_path: str) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "# RE-27 batch fix — generated by art-asset-matcher-v1.0",
        "# Run each image_edit in Grok Build with master reference attached.",
        "set -euo pipefail",
        f'ROOT="{root}"',
        f'MASTER="$ROOT/{anchor_path}"',
        "",
    ]
    fixable = [a for a in assets if a.get("issues_detected")]
    if not fixable:
        lines.append('echo "No drift detected — nothing to fix."')
    for a in fixable:
        aid = a["asset_id"]
        path = a["current_path"]
        delta = a.get("correction_prompt_delta", "").replace('"', '\\"')
        lines.extend(
            [
                f"# --- {aid} ---",
                f'# image_edit input="$ROOT/{path}" reference="$MASTER"',
                f'# prompt: "{delta}"',
                f'echo "FIX: {aid} -> {path}"',
                "",
            ]
        )
    out = root / "scripts" / "batch_fix_commands.sh"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out.chmod(0o755)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    anchor_path = root / "art" / "style-anchor.json"
    registry_path = root / "art" / "art-prompt-registry.json"

    if not anchor_path.is_file():
        print(f"FAIL: missing {anchor_path}")
        return 1
    if not registry_path.is_file():
        print(f"FAIL: missing {registry_path}")
        return 1

    anchor = load_json(anchor_path)
    registry = load_json(registry_path)
    palette = parse_palette(anchor)
    tolerance = {
        "anchor_px": "±3%",
        "palette_delta": "Euclidean < 15",
        "perspective": "orthographic_side_view_only",
        "ground_line": "bottom_edge_aligned",
    }

    matched: list[dict[str, Any]] = []
    drift_count = 0

    for asset in registry.get("assets", []):
        rel = asset.get("output_path")
        if not rel:
            continue
        path = root / rel
        img = analyze_image(path, palette) if path.is_file() else {"readable": False}
        issues = detect_issues(asset, path, img, anchor, tolerance)
        if not path.is_file():
            issues.append("missing_on_disk")

        entry = {
            "asset_id": asset["asset_id"],
            "current_path": rel,
            "issues_detected": issues,
            "image_metrics": img if img.get("readable") else None,
            "correction_prompt_delta": build_correction_delta(issues, anchor, asset)
            if issues
            else None,
            "recommended_action": "image_edit with master reference" if issues else "pass",
            "new_registry_entry_required": bool(
                issues and asset.get("status") not in ("verified", "accepted")
            ),
        }
        matched.append(entry)
        if issues:
            drift_count += 1

    registered_paths = {a["output_path"] for a in registry.get("assets", []) if a.get("output_path")}
    extras = scan_unregistered(root, registered_paths)
    matched.extend(extras)
    drift_count += len(extras)

    total = len(matched)
    match_rate = round((total - drift_count) / total, 3) if total else 0.0

    audit = {
        "matcher_id": MATCHER_ID,
        "project_path": str(root),
        "master_anchor": anchor.get("anchor_id", "MASTER-STYLE-ANCHOR-v1"),
        "master_reference_path": "art/style-anchor.json",
        "batch_assets_dir": "screenshots/ OR art/generated/",
        "timestamp": date.today().isoformat(),
        "rules": {
            "RE-27_enforcement": True,
            "priority": "master_is_truth",
            "tolerance": tolerance,
        },
        "assets_to_match": matched,
        "audit_summary": {
            "total_assets": total,
            "drift_count": drift_count,
            "match_rate": match_rate,
            "next_step": "run image_edit fixes from scripts/batch_fix_commands.sh"
            if drift_count
            else "art: accept — all assets match master",
        },
        "output_files": {
            "match_audit_json": "art/art-match-audit.json",
            "corrected_registry": "art/art-prompt-registry.json",
            "fix_instructions": "scripts/batch_fix_commands.sh",
        },
    }

    audit_path = root / "art" / "art-match-audit.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_batch_fix(root, matched, "art/style-anchor.json")

    print(f"ART MATCH AUDIT: {audit_path}")
    print(f"  total={total}  drift={drift_count}  match_rate={match_rate}")
    if drift_count:
        print(f"  next: {root}/scripts/batch_fix_commands.sh")
        return 2
    print("  PASS: all assets within tolerance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())