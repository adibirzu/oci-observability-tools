import json
import subprocess
import sys

from scripts.catalog_query import search


def ids(question):
    return [item["id"] for item in search(question)]


def test_expected_routing():
    assert ids("slow API traces")[0] == "apm"
    assert ids("cpu alarm")[0] == "monitoring"
    assert set(ids("AWR SQL regression")[:2]) & {"database-management", "operations-insights"}
    assert set(ids("route audit logs to SIEM")[:2]) & {"service-connector-hub", "log-analytics"}
    assert "management-agent" in ids("prometheus scrape")[:2]


def test_order_is_deterministic():
    assert search("logs and metrics", 12) == search("logs and metrics", 12)


def test_cli_json_and_validation():
    run = subprocess.run(
        [sys.executable, "scripts/catalog_query.py", "slow API", "--json", "--validate"],
        check=True, capture_output=True, text=True,
    )
    assert json.loads(run.stdout)[0]["id"] == "apm"
