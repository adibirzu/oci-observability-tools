import json
import re
from pathlib import Path

import pytest

from scripts.minivalidate import validate_catalog


def test_service_catalog_schema_and_integrity():
    catalog = json.loads(Path("catalog/services.json").read_text(encoding="utf-8"))
    schema = json.loads(Path("catalog/services.schema.json").read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        pytest.skip("jsonschema is unavailable; minimal validator is covered separately")
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(catalog)
    validate_catalog(catalog)
    services = catalog["services"]
    expected = {
        "monitoring", "logging", "log-analytics", "apm", "stack-monitoring",
        "database-management", "operations-insights", "management-agent", "notifications",
        "events", "service-connector-hub", "streaming",
    }
    ids = [service["id"] for service in services]
    assert set(ids) == expected
    assert len(ids) == len(set(ids))
    for service in services:
        keys = [doc["key"] for doc in service["docs"]]
        assert len(keys) == len(set(keys))
        assert Path("skills", service["skill"]).is_dir() or service["skill"].startswith("oci-")
        assert set(service["relatedServices"]) <= expected
        assert not re.search(r"[$€£]\s?\d|\d+(?:\.\d+)?\s?(?:USD|EUR)", service["pricingNote"])


def test_minimal_validator_rejects_bad_catalog():
    with pytest.raises(ValueError):
        validate_catalog({"schemaVersion": "1.0", "checkedAt": "bad", "services": []})


def test_sigma_map_schema():
    data = json.loads(Path("catalog/sigma_field_map.json").read_text(encoding="utf-8"))
    schema = json.loads(Path("catalog/sigma_field_map.schema.json").read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        pytest.skip("jsonschema is unavailable; Sigma map has structural tests in converter tests")
    jsonschema.Draft202012Validator(schema).validate(data)
    assert data["fields"]["EventID"] == {"ocl": "Event ID", "type": "string"}
