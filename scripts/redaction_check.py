#!/usr/bin/env python3
"""Detect tenant identifiers, secrets, and private topology in text files."""

from __future__ import annotations

import argparse
import fnmatch
import ipaddress
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str


SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    ".tox",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}
SKIP_WALK = {"tests/fixtures/redaction/leaky.txt"}
ALLOWED_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in (
        "192.0.2.0/24",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "127.0.0.0/8",
        "0.0.0.0/32",
        "2001:db8::/32",
        "::1/128",
    )
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.I)
IPV4_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d{1,3}){3})(?![\w.-])")
IPV6_RE = re.compile(r"(?<![\w:])(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}(?![\w:])")


def _rules() -> list[tuple[str, re.Pattern[str]]]:
    # Split sensitive-looking literals so this checker does not flag its own definitions.
    return [
        ("OCID", re.compile("oci" + r"d1\.[a-z0-9]+\.oc[0-9]+\.[a-z0-9-]*\.[a-z0-9]{8,}", re.I)),
        ("PEM_PRIVATE_KEY", re.compile("-----BEGIN " + r"[A-Z ]*PRIVATE KEY-----")),
        ("AWS_ACCESS_KEY", re.compile("AK" + r"IA[0-9A-Z]{16}")),
        ("GITHUB_TOKEN", re.compile("gh" + r"p_[A-Za-z0-9]{36}")),
        ("SLACK_TOKEN", re.compile("xo" + r"x[bp]-")),
        ("KEY_FINGERPRINT", re.compile(r"(?:[0-9a-f]{2}:){15}[0-9a-f]{2}", re.I)),
        (
            "SECRET_VALUE",
            re.compile(
                r"(?:password|token|datakey|secret)\s*[=:]\s*['\"]?(?!<)[^<\s'\"]{8,}",
                re.I,
            ),
        ),
        (
            "INTERNAL_HOST",
            re.compile(
                r"(?:oraclecorp" + r"\.com|us\.oracle\.com|\." + "internal" + r")\b",
                re.I,
            ),
        ),
        ("PERSONAL_PATH", re.compile(r"(?:/Users|/home)/[^/<>\s]+/")),
        (
            "APM_ENDPOINT",
            re.compile(r"https?://(?!<APM_DOMAIN_UPLOAD_ENDPOINT>)[^\s/]*\bapm\b[^\s]*", re.I),
        ),
        (
            "OBJECT_STORAGE_NAMESPACE",
            re.compile(r"https?://(?!<NAMESPACE>)[^.\s]+\.objectstorage\.[^\s]+", re.I),
        ),
    ]


def _is_binary(path: Path) -> bool:
    try:
        return b"\0" in path.read_bytes()[:8192]
    except OSError:
        return True


def _allow_patterns(root: Path) -> list[str]:
    allow = root / ".redaction-allow"
    if not allow.exists():
        return []
    patterns: list[str] = []
    for number, raw in enumerate(allow.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if "#" not in line or not line.split("#", 1)[1].strip():
            raise ValueError(f".redaction-allow:{number}: missing justification comment")
        pattern = line.split("#", 1)[0].strip()
        if pattern:
            patterns.append(pattern)
    return patterns


def _allowed_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return True
    return any(address in network for network in ALLOWED_NETWORKS)


def scan_text(text: str, path: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []
    rules = _rules()
    for line_no, line in enumerate(text.splitlines(), 1):
        for rule, pattern in rules:
            if pattern.search(line):
                findings.append(Finding(path, line_no, rule))
        for match in EMAIL_RE.finditer(line):
            if match.group(1).lower() not in {"example.com", "example.org", "example.net"}:
                findings.append(Finding(path, line_no, "EMAIL"))
        for match in IPV4_RE.finditer(line):
            value = match.group(1)
            prefix = line[max(0, match.start() - 1) : match.start()]
            if prefix.lower() != "v" and not _allowed_ip(value):
                findings.append(Finding(path, line_no, "IP_ADDRESS"))
        for match in IPV6_RE.finditer(line):
            value = match.group(0)
            if ":" in value and not _allowed_ip(value):
                findings.append(Finding(path, line_no, "IP_ADDRESS"))
    return findings


def _staged_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return [root / value for value in result.stdout.splitlines() if value]


def _walk(paths: list[Path], root: Path, staged: bool) -> list[Path]:
    if staged:
        return _staged_files(root)
    output: list[Path] = []
    for path in paths:
        if path.is_file():
            output.append(path)
        elif path.is_dir():
            output.extend(
                item
                for item in path.rglob("*")
                if item.is_file() and not any(part in SKIP_PARTS for part in item.parts)
            )
    return output


def check_paths(paths: list[Path], root: Path, staged: bool = False) -> list[Finding]:
    allow = _allow_patterns(root)
    findings: list[Finding] = []
    for path in _walk(paths, root, staged):
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            relative = str(path)
        if relative in SKIP_WALK and not path.is_file():
            continue
        if any(fnmatch.fnmatch(relative, pattern) for pattern in allow) or _is_binary(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(scan_text(text, relative))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args(argv)
    root = Path.cwd()
    try:
        findings = check_paths([Path(value) for value in args.paths], root, args.staged)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    for finding in findings:
        print(f"{finding.path}:{finding.line}:{finding.rule}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
