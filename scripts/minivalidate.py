"""Small vendor-free validators used when jsonschema is unavailable."""

from __future__ import annotations

import datetime as dt
import re

SERVICE_FIELDS = {
    "id",
    "name",
    "category",
    "signals",
    "summary",
    "useCases",
    "keywords",
    "pricingNote",
    "skill",
    "relatedServices",
    "maturityLevels",
    "docs",
}
CATEGORIES = {"metrics", "logs", "traces", "database", "agents", "eventing"}
SIGNALS = {"metrics", "logs", "traces", "events", "sql", "topology", "synthetic"}


def validate_catalog(data: dict) -> None:
    if set(data) != {"schemaVersion", "checkedAt", "services"} or data["schemaVersion"] != "1.0":
        raise ValueError("invalid catalog envelope")
    try:
        dt.date.fromisoformat(data["checkedAt"])
    except (TypeError, ValueError) as exc:
        raise ValueError("checkedAt must be an ISO date") from exc
    if not isinstance(data["services"], list) or not data["services"]:
        raise ValueError("services must be a non-empty list")
    ids = {service.get("id") for service in data["services"]}
    for service in data["services"]:
        if set(service) != SERVICE_FIELDS:
            raise ValueError("service fields do not match schema")
        if not re.fullmatch(r"[a-z0-9-]+", service["id"]):
            raise ValueError("invalid service id")
        if service["category"] not in CATEGORIES or not set(service["signals"]) <= SIGNALS:
            raise ValueError("invalid category or signal")
        if (
            len(service["summary"]) > 280
            or len(service["useCases"]) < 2
            or len(service["keywords"]) < 2
        ):
            raise ValueError("invalid catalog content lengths")
        if not set(service["relatedServices"]) <= ids:
            raise ValueError("unknown related service")
        if not service["docs"]:
            raise ValueError("missing docs")
        for doc in service["docs"]:
            if set(doc) != {"key", "title", "url"} or not re.fullmatch(r"[A-Z]+", doc["key"]):
                raise ValueError("invalid doc entry")
            if not re.match(r"https://(?:docs|www)\.oracle\.com/", doc["url"]):
                raise ValueError("invalid doc URL")
