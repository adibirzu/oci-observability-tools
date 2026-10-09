import json
from pathlib import Path

import pytest
import yaml

from scripts.ocl_lint import lint
from scripts.sigma_to_ocl import UnsupportedSigma, convert


def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_examples_are_deterministic_and_lint_clean():
    for path in sorted(Path("examples/sigma").glob("*.yml")):
        first = convert(load(path))
        second = convert(load(path))
        assert json.dumps(first, ensure_ascii=False) == json.dumps(second, ensure_ascii=False)
        assert not [item for item in lint(first["query"]) if item.severity == "error"]


def test_typing_modifiers_lists_and_all():
    output = convert(load("tests/fixtures/sigma/modifiers.yml"))
    expected = json.loads(Path("tests/fixtures/sigma/expected/modifiers.json").read_text(encoding="utf-8"))
    assert output == expected
    query = output["query"]
    assert "'Event ID' in ('4688', '4689')" in query
    assert "like '*tool*'" in query
    assert "like 'service*'" in query
    assert "like '*flag'" in query
    assert "matches '^example'" in query
    assert "like '*alpha*' and 'Command Line' like '*beta*'" in query


def test_and_not_unknown_field_quote_and_unmapped_logsource():
    rule = {
        "logsource": {"product": "custom", "service": "app"},
        "detection": {
            "a": {"Unknown Field": "O'Brien"},
            "b": {"SourcePort": 443},
            "condition": "a and not b",
        },
        "falsepositives": [],
        "level": "low",
    }
    output = convert(rule)
    assert "'O''Brien'" in output["query"]
    assert "'Source Port' = 443" in output["query"]
    assert "unknown field" in " ".join(output["warnings"])
    assert output["log_sources"] == ["<LOG_SOURCE>"]


def test_aggregation_and_timeframe():
    output = convert(load("examples/sigma/windows-logon.yml"))
    assert output["requires_aggregation"] is True
    assert "| stats count as Count by 'Source IP' | where Count > 5" in output["query"]
    assert "timeframe → schedule interval" in output["warnings"]


def test_unsupported_condition_raises():
    rule = {"logsource": {}, "detection": {"a": {"EventID": 1}, "condition": "2 of them"}}
    with pytest.raises(UnsupportedSigma):
        convert(rule)
