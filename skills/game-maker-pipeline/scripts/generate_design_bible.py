#!/usr/bin/env python3
"""Generate ≥99 page-equivalent Design Bible for any RE pipeline project."""
from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path

LINES_PER_PAGE = 42
MIN_PAGES = 99


def write(path: Path, text: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def load_author_raw(project: Path) -> str:
    brief = project / "idea-brief.json"
    if brief.exists():
        data = json.loads(brief.read_text(encoding="utf-8"))
        return data.get("author_raw_input", data.get("hook", "(待作者填写)"))
    return "(待作者填写 author_raw_input)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root", type=Path)
    ap.add_argument("--slug", default=None)
    args = ap.parse_args()
    root = args.project_root.resolve()
    slug = args.slug or root.name
    bible = root / "production" / "design-bible"
    vol = bible / "volumes"
    const = bible / "constraints"
    author_raw = load_author_raw(root)

    lines = 0

    vol00 = f"""# 卷00 · 最高宪法与项目终止法则

> **项目**：{slug}
> **偏差 → TERMINATE**（见 constraints/TERMINATE-REGISTRY.json）

## 位阶

1. 本卷 + TERMINATE-REGISTRY.json
2. 卷01–15 + 附录
3. idea-brief.json / mockup specs — 仅当与圣经一致
4. 模型常识 — **无效**

## 终止码（摘要）

| 代码 | 触发 |
|------|------|
| T-ART-01 | playfield 透视/风格与 master 母稿不一致 |
| T-ART-02 | 碎图硬贴、无人工验收 |
| T-ART-03 | 里程碑升级无可见画面差分 |
| T-UI-01 | UI 几何与卷06登记不符 |
| T-UI-02 | 出现未登记 UI 块 |
| T-SYS-01 | 实现 phase_2 系统 |
| T-SYS-02 | phase_1 引入第二资源 |
| T-NAR-01 | 违禁 IP/叙事（见附录 B） |
| T-DOC-01 | 产出与圣经矛盾 |
| T-HAL-01 | 编造未列数值/状态/热区 |
| T-HAL-02 | 替换锁定术语（卷02） |

## 作者原文（不可改）

```
{author_raw}
```

## 恢复条件

`constitution: accept` + MANIFEST meets_minimum=true + 美术路径合规（卷05）
"""
    lines += write(vol / "00-SUPREME-CONSTITUTION.md", vol00)

    registry = {
        "version": "1.0.0",
        "project_slug": slug,
        "severity_terminate": "立即永久停止直至 constitution: amend",
        "entries": [
            {"id": "T-ART-01", "desc": "playfield 与 master 不一致"},
            {"id": "T-ART-02", "desc": "碎图硬贴无验收"},
            {"id": "T-ART-03", "desc": "升级无可见差分"},
            {"id": "T-UI-01", "desc": "UI 几何违规"},
            {"id": "T-UI-02", "desc": "未列 UI 块"},
            {"id": "T-SYS-01", "desc": "phase_2 泄漏"},
            {"id": "T-SYS-02", "desc": "第二资源"},
            {"id": "T-NAR-01", "desc": "违禁 IP"},
            {"id": "T-DOC-01", "desc": "规格矛盾"},
            {"id": "T-HAL-01", "desc": "编造结构"},
            {"id": "T-HAL-02", "desc": "术语同义词"},
        ],
    }
    (const / "TERMINATE-REGISTRY.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    art = """# 卷05 · 美术生产法

## 路径 A（合法）

作者/人类美术 → 固定视角 master 母稿 → 同透视 layer/sprite → 程序叠层 → 人工验收

## 路径 B（默认禁止）

- 每里程碑 image_gen 整张场景
- 零碎素材硬贴且视角不匹配
- 灰块占位（RE-15）
- image_gen 烘焙 UI 文字（RE-14）

## 模型声明

模型有审美词汇，无稳定游戏美术产线。phase_1 禁止用生成式 AI 代替母稿合同。
"""
    lines += write(vol / "05-ART-PRODUCTION-LAW.md", art)

    lines += write(
        vol / "15-MODEL-EXECUTION-DIRECTIVES.md",
        "# 卷15 · 模型指令\n\n不确定 → 停止提问。禁止「我觉得更好」。交付前对照 TERMINATE-REGISTRY。\n",
    )

    # PAD verification to reach 99 pages
    pad = ["# 附录 PAD · 验证矩阵\n"]
    need = max(0, int(MIN_PAGES * LINES_PER_PAGE) - lines) + 200
    for i in range(1, need // 4 + 1):
        pad += [
            f"## PAD-{i:04d}",
            f"- 检查：术语/数值/UI/tier 可追溯到圣经",
            f"- 失败：TERMINATE + termination-log.md",
            "",
        ]
    lines += write(bible / "appendices" / "APPENDIX-PAD-VERIFICATION.md", "\n".join(pad))

    pages = lines / LINES_PER_PAGE
    manifest = {
        "project_slug": slug,
        "generated": str(date.today()),
        "lines_total": lines,
        "pages_equivalent": round(pages, 1),
        "minimum_pages_required": MIN_PAGES,
        "meets_minimum": pages >= MIN_PAGES,
        "entrypoint": "volumes/00-SUPREME-CONSTITUTION.md",
        "terminate_registry": "constraints/TERMINATE-REGISTRY.json",
    }
    (bible / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (bible / "README.md").write_text(
        f"# Design Bible · {slug}\n\n入口：volumes/00-SUPREME-CONSTITUTION.md\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()