#!/usr/bin/env python3
"""Build committed ChatGPT knowledge files and Gemini context offline."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "chatgpt/knowledge"
BUNDLES = [
    ("01-router.md", "oci-om-router"),
    ("02-ocl.md", "oci-ocl-queries"),
    ("03-apm-otel.md", "oci-apm-otel"),
    ("04-monitoring-alarms.md", "oci-monitoring-alarms"),
    ("05-logging-pipelines.md", "oci-logging-pipelines"),
    ("06-db-observability.md", "oci-db-observability"),
    ("07-stack-monitoring-agents.md", "oci-stack-monitoring-agents"),
    ("08-detections-sigma.md", "oci-detections-sigma"),
    ("09-maturity.md", "oci-om-maturity"),
]


def render_bundle(skill: str) -> str:
    path = ROOT / "skills" / skill / "SKILL.md"
    content = path.read_text(encoding="utf-8")
    linked = re.findall(r"\(\.\./\.\./references/([^)]+\.md)\)", content)
    sections = [content]
    for name in dict.fromkeys(linked):
        sections.extend(["\n---\n", (ROOT / "references" / name).read_text(encoding="utf-8")])
    return "\n".join(sections).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    gemini = agents.replace(
        "Install for Codex: `./install.sh codex`.",
        "Install for Gemini CLI: `./install.sh gemini`; for Antigravity: `./install.sh antigravity`.",
    )
    result = {ROOT / "GEMINI.md": gemini}
    for filename, skill in BUNDLES:
        result[KNOWLEDGE / filename] = render_bundle(skill)
    result[KNOWLEDGE / "services.json"] = (ROOT / "catalog/services.json").read_text(encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("stale: " + ", ".join(map(str, stale)))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
