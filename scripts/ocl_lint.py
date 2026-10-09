#!/usr/bin/env python3
"""Lint OCI Log Analytics OCL queries without making network calls."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


STRING_NUMERIC_FIELDS = {"Event ID", "Logon Type", "Response Code", "Status Code"}
NUMBER_FIELDS = {"Source Port", "Destination Port"}
KNOWN_FIELDS = STRING_NUMERIC_FIELDS | NUMBER_FIELDS | {
    "Log Source", "Original Log Content", "Process Name", "Parent Process Name", "Command Line",
    "Principal Name", "Target User", "Source IP", "Destination IP", "Query Name",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    col: int
    message: str
    fix: str


def _finding(rule: str, severity: str, match: re.Match[str] | None, message: str, fix: str) -> Finding:
    return Finding(rule, severity, (match.start() + 1) if match else 1, message, fix)


def _balanced(query: str) -> bool:
    depth = 0
    in_quote = False
    index = 0
    while index < len(query):
        char = query[index]
        if char == "'":
            if in_quote and index + 1 < len(query) and query[index + 1] == "'":
                index += 2
                continue
            in_quote = not in_quote
        elif not in_quote and char == "(":
            depth += 1
        elif not in_quote and char == ")":
            depth -= 1
            if depth < 0:
                return False
        index += 1
    return not in_quote and depth == 0


def lint(query: str) -> list[Finding]:
    findings: list[Finding] = []
    for field in sorted(KNOWN_FIELDS, key=len, reverse=True):
        match = re.search(rf"(?<!['\w]){re.escape(field)}\s*(?:=|!=|>|<|\blike\b|\bin\b)", query, re.I)
        if match:
            findings.append(_finding("OCL001", "error", match, f"Quote multi-word field {field}", f"'{field}'"))
    for field in STRING_NUMERIC_FIELDS:
        match = re.search(rf"'{re.escape(field)}'\s*(?:=|!=|>|<)\s*(\d+)\b", query, re.I)
        if match:
            findings.append(_finding("OCL002", "error", match, f"{field} is string-typed", f"'{match.group(1)}'"))
    for field in NUMBER_FIELDS:
        match = re.search(rf"'{re.escape(field)}'\s*(?:=|!=|>|<)\s*'(\d+)'", query, re.I)
        if match:
            findings.append(_finding("OCL003", "warning", match, f"{field} is number-typed", match.group(1)))
    match = re.search(r"(?:'?Time'?\s*(?:>|<|between\b)|dateRelative\s*\()", query, re.I)
    if match:
        findings.append(_finding("OCL004", "error", match, "Set the time window outside the query", "Use API, CLI, or UI time arguments"))
    match = re.search(r"'Original Log Content'\s+like\s+'\*", query, re.I)
    if match:
        prefix = query[: match.start()]
        if not re.search(r"'(?:Log Source|Event ID|Source IP|Principal Name)'\s*(?:=|in\b)", prefix, re.I):
            findings.append(_finding("OCL005", "warning", match, "Leading wildcard without an indexed filter", "Filter an indexed field first"))
    if not _balanced(query):
        findings.append(_finding("OCL006", "error", None, "Unbalanced quotes or parentheses", "Balance delimiters"))
    match = re.search(r"\blike\s+'[^']*%", query, re.I)
    if match:
        findings.append(_finding("OCL007", "warning", match, "OCL like uses * instead of %", "Replace % with *"))
    match = re.search(r"\|\s*\||\|\s*$", query)
    if match:
        findings.append(_finding("OCL008", "error", match, "Empty pipeline stage", "Remove the empty stage"))
    match = re.search(r"[`;]|[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", query)
    if match:
        findings.append(_finding("OCL009", "error", match, "Unsafe delimiter or control character", "Remove unsafe character"))
    return sorted(findings, key=lambda item: (item.col, item.rule))


def sanitize_for_mcp(query: str) -> str:
    collapsed = re.sub(r"[\n\r\t]+", " ", query).strip()
    collapsed = re.sub(r" {2,}", " ", collapsed)
    if len(collapsed) > 8000:
        raise ValueError("query exceeds 8000 characters")
    unsafe = [item for item in lint(collapsed) if item.rule in {"OCL006", "OCL009"}]
    if unsafe:
        raise ValueError(unsafe[0].message)
    return collapsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="query file or - for stdin")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    query = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    findings = lint(query)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    else:
        for item in findings:
            print(f"{item.severity} {item.rule} col {item.col}: {item.message}; {item.fix}")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
