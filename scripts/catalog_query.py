#!/usr/bin/env python3
"""Search the OCI Observability capability catalog without network access."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

if __package__:
    from .minivalidate import validate_catalog
else:
    from minivalidate import validate_catalog


CATALOG = Path(__file__).resolve().parents[1] / "catalog" / "services.json"
SYNONYMS = {
    "trace": "traces", "span": "traces", "latency": "traces", "slow": "traces",
    "alarm": "metrics", "threshold": "metrics", "cpu": "metrics",
    "sql": "sql", "awr": "sql", "ash": "sql", "siem": "logs", "detection": "logs",
    "prometheus": "agents", "agent": "agents",
}


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def search(question: str, top: int = 3, catalog: dict | None = None) -> list[dict]:
    catalog = catalog or load_catalog()
    terms = tokens(question)
    terms.update(SYNONYMS[word] for word in list(terms) if word in SYNONYMS)
    results = []
    for service in catalog["services"]:
        keyword_tokens = tokens(" ".join(service["keywords"]))
        use_case_tokens = tokens(" ".join(service["useCases"]))
        signal_tokens = set(service["signals"])
        keyword_hits = sorted(terms & keyword_tokens)
        use_case_hits = sorted(terms & use_case_tokens)
        signal_hits = sorted(terms & signal_tokens)
        score = 3 * len(keyword_hits) + 2 * len(use_case_hits) + len(signal_hits)
        results.append(
            {
                "id": service["id"],
                "name": service["name"],
                "score": score,
                "skill": service["skill"],
                "doc": service["docs"][0]["url"],
                "why": keyword_hits + use_case_hits + signal_hits,
            }
        )
    return sorted(results, key=lambda item: (-item["score"], item["id"]))[:top]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list", action="store_true", dest="list_services")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args(argv)
    catalog = load_catalog()
    if args.validate:
        validate_catalog(catalog)
    if args.list_services:
        result = [{"id": item["id"], "name": item["name"]} for item in catalog["services"]]
    else:
        result = search(args.question, args.top, catalog)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=False))
    else:
        for item in result:
            if "score" in item:
                print(f"{item['name']} ({item['score']}): {item['skill']} — {item['doc']}")
            else:
                print(f"{item['id']}: {item['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
