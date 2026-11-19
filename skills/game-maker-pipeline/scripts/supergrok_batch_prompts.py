#!/usr/bin/env python3
"""Emit SuperGrok Imagine batch prompt packs from art-prompt-registry + style-anchor."""
from __future__ import annotations

import argparse
import json
import textwrap
from datetime import date
from pathlib import Path

NEGATIVE_DRIFT = (
    "perspective drift, warm tone drift, wrong camera angle, side view, front portrait, "
    "isometric confusion, floating off ground, bad composition, text, letters, watermark, "
    "logo, UI overlay, HUD, photorealistic, 3D render, multiple characters, blurry, "
    "grey placeholder, modern mobile UI"
)

BATCH_SIZE = 5


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def full_prompt(anchor: dict, asset: dict) -> str:
    block = anchor.get("prompt_block", "").strip()
    delta = asset.get("prompt_delta", "").strip()
    return f"{block} {delta}".strip()


def imagine_mode(asset: dict, anchor_ref: str) -> str:
    refs = asset.get("references") or []
    if anchor_ref in refs and len(refs) == 1:
        return "image_gen"
    return "image_edit"


def reference_hint(asset: dict, anchor: dict, is_master_spawn: bool) -> str:
    if is_master_spawn or asset.get("imagine_mode") == "image_gen":
        master = anchor.get("master_reference_path", "art/master/MASTER-ANCHOR.png")
        return f"NONE (image_gen) — also save copy as `{master}`"
    refs = asset.get("references") or []
    if not refs:
        return "none"
    if refs[0] == anchor.get("anchor_id"):
        master = anchor.get("master_reference_path", "art/master/MASTER-ANCHOR.png")
        return f"Upload master: {master}"
    return f"Upload reference: {refs[0]} (from art/staging/ or output_path)"


def build_batches(assets: list[dict]) -> list[list[dict]]:
    batches: list[list[dict]] = []
    for i in range(0, len(assets), BATCH_SIZE):
        batches.append(assets[i : i + BATCH_SIZE])
    return batches


def render_markdown(project: Path, anchor: dict, reg: dict) -> str:
    order = reg.get("dependency_graph", {}).get("generation_order", [])
    by_id = {a["asset_id"]: a for a in reg.get("assets", [])}
    ordered = [by_id[i] for i in order if i in by_id]
    batches = build_batches(ordered)
    anchor_id = anchor.get("anchor_id", "MASTER")
    lines = [
        f"# SuperGrok Imagine Batch Pack — {reg.get('project_slug', project.name)}",
        f"",
        f"Generated: {date.today().isoformat()}",
        f"Pipeline: supergrok-imagine-v1.0 · game-maker-pipeline RE-19~27",
        f"",
        f"## Rules (do NOT skip)",
        f"",
        f"1. **Batch size ≤ {BATCH_SIZE}** — finish verify before next batch",
        f"2. **Master first** — `{anchor_id}` via Imagine `image_gen`, save to `{anchor.get('master_reference_path', 'art/master/')}`",
        f"3. **All derivatives** — Imagine **Edit** with master/player as strong reference (never raw text-to-image alone)",
        f"4. **Save naming** — drop PNG to `art/incoming/{{asset_id}}.png` (exact ID, uppercase)",
        f"5. **Ingest** — `scripts/ingest_imagine_assets.sh` → staging → verify → registry path",
        f"",
        f"### Master Anchor Description (verbatim)",
        f"",
        f"```",
        anchor.get("prompt_block", "").strip(),
        f"```",
        f"",
        f"### Negative (append to every prompt)",
        f"",
        f"```",
        anchor.get("negative_block", "").strip() + " " + NEGATIVE_DRIFT,
        f"```",
        f"",
    ]

    first_id = ordered[0]["asset_id"] if ordered else ""
    for bi, batch in enumerate(batches, 1):
        lines.append(f"## Batch {bi} ({len(batch)} assets)")
        lines.append("")
        for asset in batch:
            aid = asset["asset_id"]
            mode = asset.get("imagine_mode") or imagine_mode(asset, anchor_id)
            is_master = aid == first_id
            lines.append(f"### `{aid}`")
            lines.append(f"- **Imagine mode**: `{mode}`")
            lines.append(f"- **Reference**: {reference_hint(asset, anchor, is_master)}")
            lines.append(f"- **Aspect**: {asset.get('aspect_ratio', '1:1')}")
            lines.append(f"- **Save as**: `art/incoming/{aid}.png`")
            lines.append(f"- **Registry output**: `{asset.get('output_path')}`")
            lines.append("")
            lines.append("**Prompt (copy entire block):**")
            lines.append("")
            lines.append("```")
            lines.append(full_prompt(anchor, asset))
            lines.append("")
            lines.append(f"Negative: {anchor.get('negative_block', '').strip()} {NEGATIVE_DRIFT}")
            lines.append("```")
            lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend(
        [
            "## Post-batch checklist",
            "",
            "- [ ] Each file named `{ASSET_ID}.png` in `art/incoming/`",
            "- [ ] Camera matches `camera_lock` in style-anchor",
            "- [ ] Single subject centered (sprites) OR tileable (tiles only)",
            "- [ ] Transparent background (sprites/pickups)",
            "- [ ] Palette matches master (no warm drift)",
            "- [ ] Run `scripts/ingest_imagine_assets.sh`",
            "- [ ] Run `scripts/art_verify.sh` + `scripts/match_and_correct.sh`",
            "- [ ] Author gate: `art: accept`",
            "",
        ]
    )
    return "\n".join(lines)


def render_json(project: Path, anchor: dict, reg: dict) -> dict:
    order = reg.get("dependency_graph", {}).get("generation_order", [])
    by_id = {a["asset_id"]: a for a in reg.get("assets", [])}
    items = []
    for aid in order:
        if aid not in by_id:
            continue
        asset = by_id[aid]
        items.append(
            {
                "asset_id": aid,
                "imagine_mode": asset.get("imagine_mode") or imagine_mode(asset, anchor.get("anchor_id", "")),
                "reference_hint": reference_hint(asset, anchor, aid == order[0]),
                "aspect_ratio": asset.get("aspect_ratio", "1:1"),
                "incoming_path": f"art/incoming/{aid}.png",
                "output_path": asset.get("output_path"),
                "prompt": full_prompt(anchor, asset),
                "negative": f"{anchor.get('negative_block', '').strip()} {NEGATIVE_DRIFT}".strip(),
            }
        )
    return {
        "pipeline": "supergrok-imagine-v1.0",
        "project_slug": reg.get("project_slug", project.name),
        "master_anchor_id": anchor.get("anchor_id"),
        "master_reference_path": anchor.get("master_reference_path"),
        "batch_size_max": BATCH_SIZE,
        "generated": date.today().isoformat(),
        "items": items,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SuperGrok Imagine batch packs")
    ap.add_argument("project_root", type=Path, help="grokmaker/{slug}")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: {project}/art/supergrok")
    args = ap.parse_args()
    root = args.project_root.resolve()
    anchor_path = root / "art" / "style-anchor.json"
    reg_path = root / "art" / "art-prompt-registry.json"
    if not anchor_path.is_file() or not reg_path.is_file():
        raise SystemExit(f"Missing art/style-anchor.json or art/art-prompt-registry.json in {root}")

    anchor = load(anchor_path)
    reg = load(reg_path)
    out = args.out_dir or (root / "art" / "supergrok")
    out.mkdir(parents=True, exist_ok=True)

    md_path = out / "batch-prompts.md"
    json_path = out / "batch-prompts.json"
    md_path.write_text(render_markdown(root, anchor, reg), encoding="utf-8")
    json_path.write_text(json.dumps(render_json(root, anchor, reg), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote: {md_path}")
    print(f"Wrote: {json_path}")
    print(f"Items: {len(reg.get('assets', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())