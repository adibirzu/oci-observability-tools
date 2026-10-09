import json
from pathlib import Path


def test_manifests_parse_and_agree():
    paths = [
        Path(".claude-plugin/plugin.json"),
        Path(".claude-plugin/marketplace.json"),
        Path(".codex-plugin/plugin.json"),
        Path("gemini-extension.json"),
    ]
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    identity = [documents[0], documents[2], documents[3]]
    assert {item["name"] for item in identity} == {"oci-observability-tools"}
    assert {item["version"] for item in identity} == {"0.1.0"}
    assert {item["license"] for item in identity} == {"Apache-2.0"}
    assert all("Not an Oracle product" in item["description"] for item in identity)
    plugin = documents[1]["plugins"][0]
    assert plugin["name"] == "oci-observability-tools"
    assert "Not an Oracle product" in plugin["description"]
