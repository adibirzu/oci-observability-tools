#!/usr/bin/env python3
"""Convert a supported, deterministic subset of Sigma YAML to OCL."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path

import yaml

if __package__:
    from .ocl_lint import lint
else:
    from ocl_lint import lint


ROOT = Path(__file__).resolve().parents[1]
FIELD_MAP = json.loads((ROOT / "catalog/sigma_field_map.json").read_text(encoding="utf-8"))


class UnsupportedSigma(ValueError):
    """The rule uses a condition outside the intentionally small supported subset."""


def quote(value: object) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def _term(field_spec: str, value: object, warnings: list[str]) -> str:
    parts = field_spec.split("|")
    sigma_field, modifiers = parts[0], parts[1:]
    mapping = FIELD_MAP["fields"].get(sigma_field)
    if mapping is None:
        mapping = {"ocl": sigma_field, "type": "string"}
        warnings.append(f"unknown field: {sigma_field}")
    field = quote(mapping["ocl"])
    modifier = next((item for item in modifiers if item != "all"), "")

    def render(single: object) -> str:
        if modifier == "contains":
            return f"{field} like {quote('*' + str(single) + '*')}"
        if modifier == "startswith":
            return f"{field} like {quote(str(single) + '*')}"
        if modifier == "endswith":
            return f"{field} like {quote('*' + str(single))}"
        if modifier == "re":
            return f"{field} matches {quote(single)}"
        literal = (
            str(single)
            if mapping["type"] == "number" and isinstance(single, (int, float))
            else quote(single)
        )
        return f"{field} = {literal}"

    if isinstance(value, list):
        if not modifier:
            literals = [
                str(item)
                if mapping["type"] == "number" and isinstance(item, (int, float))
                else quote(item)
                for item in value
            ]
            return f"{field} in ({', '.join(literals)})"
        joiner = " and " if "all" in modifiers else " or "
        return "(" + joiner.join(render(item) for item in value) + ")"
    return render(value)


def _selection(value: object, warnings: list[str]) -> str:
    if isinstance(value, list):
        return (
            "("
            + " or ".join(
                f"'Original Log Content' like {quote('*' + str(item) + '*')}" for item in value
            )
            + ")"
        )
    if not isinstance(value, dict):
        raise UnsupportedSigma("selection must be a mapping or keyword list")
    return "(" + " and ".join(_term(field, item, warnings) for field, item in value.items()) + ")"


def _condition(condition: str, selections: dict[str, str]) -> tuple[str, str | None]:
    aggregation = None
    match = re.fullmatch(
        r"(.+?)\s*\|\s*count\(\)(?:\s+by\s+([A-Za-z0-9_]+))?\s*>\s*(\d+)", condition.strip(), re.I
    )
    if match:
        condition, field, threshold = match.groups()
        mapped = FIELD_MAP["fields"].get(field or "", {"ocl": field})["ocl"] if field else None
        aggregation = "| stats count as Count"
        if mapped:
            aggregation += f" by {quote(mapped)}"
        aggregation += f" | where Count > {threshold}"
    condition = condition.strip()
    if condition in selections:
        return selections[condition], aggregation
    if condition.lower() == "all of them":
        return "(" + " and ".join(selections.values()) + ")", aggregation
    wildcard = re.fullmatch(r"1 of ([A-Za-z0-9_*?-]+)", condition, re.I)
    if wildcard:
        names = [name for name in selections if fnmatch.fnmatch(name, wildcard.group(1))]
        if not names:
            raise UnsupportedSigma("condition wildcard matched no selections")
        return "(" + " or ".join(selections[name] for name in names) + ")", aggregation
    binary = re.fullmatch(r"([A-Za-z0-9_]+)\s+(and|or)\s+(not\s+)?([A-Za-z0-9_]+)", condition, re.I)
    if binary and binary.group(1) in selections and binary.group(4) in selections:
        left, operator, negate, right = binary.groups()
        right_expr = f"not {selections[right]}" if negate else selections[right]
        return f"({selections[left]} {operator.lower()} {right_expr})", aggregation
    raise UnsupportedSigma(f"unsupported condition: {condition}")


def convert(rule: dict) -> dict:
    warnings: list[str] = []
    logsource = rule.get("logsource", {})
    source_key = f"{logsource.get('product', '')}/{logsource.get('service', '')}"
    sources = FIELD_MAP["logsources"].get(source_key)
    if not sources:
        sources = ["<LOG_SOURCE>"]
        warnings.append(f"unmapped logsource: {source_key}")
    source_expr = "(" + " or ".join(f"'Log Source' = {quote(item)}" for item in sources) + ")"
    detection = rule.get("detection", {})
    selections = {
        name: _selection(value, warnings)
        for name, value in detection.items()
        if name not in {"condition", "timeframe"}
    }
    body, aggregation = _condition(str(detection.get("condition", "")), selections)
    if aggregation and detection.get("timeframe"):
        warnings.append("timeframe → schedule interval")
    query = f"{source_expr} and {body}"
    if aggregation:
        query += " " + aggregation
    errors = [item for item in lint(query) if item.severity == "error"]
    if errors:
        raise ValueError(f"generated query failed OCL lint: {errors}")
    tags = [tag for tag in rule.get("tags", []) if str(tag).startswith("attack.")]
    return {
        "query": query,
        "log_sources": sources,
        "requires_aggregation": aggregation is not None,
        "mitre_attack": tags,
        "falsepositives": rule.get("falsepositives", []),
        "level": rule.get("level"),
        "warnings": list(dict.fromkeys(warnings)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rule")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rule = yaml.safe_load(Path(args.rule).read_text(encoding="utf-8"))
    result = convert(rule)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["query"])
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
