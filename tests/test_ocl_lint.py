import re
from pathlib import Path

import pytest

from scripts.ocl_lint import lint, sanitize_for_mcp


BAD = {
    "OCL001": "Log Source = 'x'",
    "OCL002": "'Event ID' = 4625",
    "OCL003": "'Source Port' = '443'",
    "OCL004": "Time between 'a' and 'b'",
    "OCL005": "'Original Log Content' like '*error*'",
    "OCL006": "('Log Source' = 'x'",
    "OCL007": "'Log Source' like '%Audit%'",
    "OCL008": "'Log Source' = 'x' || stats count",
    "OCL009": "'Log Source' = 'x';",
}


@pytest.mark.parametrize(("rule", "query"), BAD.items())
def test_each_rule_fires(rule, query):
    assert rule in {item.rule for item in lint(query)}


@pytest.mark.parametrize("query", [
    "'Log Source' = 'OCI Audit Logs'",
    "'Event ID' = '4625'",
    "'Source Port' = 443",
    "'Log Source' = 'x' and 'Original Log Content' like '*error*'",
    "('Log Source' = 'x') | stats count as Count",
    "'Log Source' like '*Audit*'",
])
def test_clean_variants(query):
    assert not lint(query)


def test_all_documented_ocl_blocks_lint_clean():
    paths = [Path("references/ocl-cookbook.md"), *Path("skills").glob("*/SKILL.md")]
    for path in paths:
        for block in re.findall(r"```ocl\n(.*?)```", path.read_text(encoding="utf-8"), re.S):
            assert not lint(block), f"{path}: {lint(block)}"


def test_sanitize_for_mcp():
    assert sanitize_for_mcp("  'Log Source' = 'x'\n | stats count  ") == "'Log Source' = 'x' | stats count"
    for unsafe in ["x; y", "`x`", "('x'", "x" * 8001]:
        with pytest.raises(ValueError):
            sanitize_for_mcp(unsafe)
