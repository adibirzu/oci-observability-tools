import json
import re
from pathlib import Path

from scripts.minivalidate import validate_catalog

EXPECTED_SERVICES = {
    "monitoring",
    "logging",
    "log-analytics",
    "apm",
    "stack-monitoring",
    "database-management",
    "operations-insights",
    "management-agent",
    "notifications",
    "events",
    "service-connector-hub",
    "streaming",
}


def load_catalog() -> dict:
    return json.loads(Path("catalog/services.json").read_text(encoding="utf-8"))


def test_catalog_services_completeness_and_uniqueness():
    catalog = load_catalog()
    services = catalog["services"]
    ids = [s["id"] for s in services]
    assert set(ids) == EXPECTED_SERVICES
    assert len(ids) == len(set(ids)), "Duplicate service IDs in catalog"


def test_catalog_schema_validation():
    catalog = load_catalog()
    schema = json.loads(Path("catalog/services.schema.json").read_text(encoding="utf-8"))
    try:
        import jsonschema

        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        validator.validate(catalog)
    except ImportError:
        pass
    validate_catalog(catalog)


def test_catalog_docs_urls_validity():
    catalog = load_catalog()
    for service in catalog["services"]:
        assert service["docs"], f"Service {service['id']} has no docs"
        keys = [d["key"] for d in service["docs"]]
        assert len(keys) == len(set(keys)), f"Duplicate doc keys in {service['id']}"
        for doc in service["docs"]:
            is_valid_url = doc["url"].startswith("https://docs.oracle.com/") or doc[
                "url"
            ].startswith("https://www.oracle.com/")
            assert is_valid_url, f"Invalid doc URL: {doc['url']}"
            assert doc["key"].isupper(), f"Doc key must be uppercase: {doc['key']}"


def test_catalog_pricing_notes_have_no_currency_amounts():
    catalog = load_catalog()
    currency_pattern = re.compile(r"[$€£]\s?\d|\d+(?:\.\d+)?\s?(?:USD|EUR)")
    for service in catalog["services"]:
        note = service.get("pricingNote", "")
        assert not currency_pattern.search(note), (
            f"Forbidden pricing currency in {service['id']}: {note}"
        )


def test_catalog_skill_mappings_exist_or_valid():
    catalog = load_catalog()
    for service in catalog["services"]:
        skill = service["skill"]
        assert skill.startswith("oci-"), f"Skill name must start with oci-: {skill}"
        assert Path("skills", skill).is_dir(), (
            f"Skill directory missing for service {service['id']}: {skill}"
        )
