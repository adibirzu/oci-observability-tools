from pathlib import Path

from scripts.catalog_query import search


PROMPT = "Which OCI service should I use to trace a slow API?"
APMOTEL = "https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html"


def test_shared_router_and_every_harness_asset_route_to_apm_with_otel_docs():
    assert search(PROMPT, top=1)[0]["id"] == "apm"
    skill = Path("skills/oci-apm-otel/SKILL.md").read_text(encoding="utf-8")
    chatgpt = Path("chatgpt/knowledge/03-apm-otel.md").read_text(encoding="utf-8")
    assert APMOTEL in skill
    assert APMOTEL in chatgpt
    for adapter in ("AGENTS.md", "GEMINI.md", "CLAUDE.md", ".codex-plugin/plugin.json"):
        assert Path(adapter).is_file()
