#!/usr/bin/env python3
"""Render the official Oracle documentation registry from the service catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog/services.json"
OUTPUT = ROOT / "references/oracle-docs.md"


def render() -> str:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    lines = ["# Official Oracle documentation registry", "", f"Catalog checked: {data['checkedAt']}", ""]
    for service in data["services"]:
        lines.extend([f"## {service['name']}", ""])
        for doc in service["docs"]:
            lines.append(f"- **{doc['key']}**: [{doc['title']}]({doc['url']})")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    content = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print(f"stale: {OUTPUT.relative_to(ROOT)}")
            return 1
    else:
        OUTPUT.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
