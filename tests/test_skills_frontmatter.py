from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from scripts.redaction_check import scan_text

SECTIONS = [
    "# ",
    "## When to use",
    "## Key concepts",
    "## Workflow",
    "## Pitfalls",
    "## Examples",
    "## Official docs",
    "## Related skills",
]


def all_skills() -> list[Path]:
    return sorted(Path("skills").glob("*/SKILL.md"))


def test_skills_count_and_expected_skills_exist():
    skill_names = {p.parent.name for p in all_skills()}
    expected_new = {"oci-apm-tracing", "oci-monitoring-mql"}
    assert expected_new <= skill_names
    assert len(skill_names) >= 11


def test_skills_frontmatter_schema_and_metadata():
    for path in all_skills():
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        assert match is not None, f"Missing frontmatter in {path}"
        metadata = yaml.safe_load(match.group(1))
        assert set(metadata) <= {"name", "description", "license"}
        assert metadata["name"] == path.parent.name
        assert re.fullmatch(r"oci-[a-z0-9-]+", metadata["name"])
        assert 60 <= len(metadata["description"]) <= 1024, f"Bad description length in {path}"
        assert "Use when" in metadata["description"], f"Missing 'Use when' in {path}"
        assert metadata.get("license") == "Apache-2.0"


def test_skills_section_order():
    for path in all_skills():
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        assert match is not None
        positions = [text.index(section, match.end()) for section in SECTIONS]
        assert positions == sorted(positions), f"Sections out of order in {path}"


def test_skills_size_limits():
    for path in all_skills():
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count < 500, f"Skill {path} has {line_count} lines (must be < 500)"


def test_skills_reference_links_resolve():
    for path in all_skills():
        text = path.read_text(encoding="utf-8")
        for linked in re.findall(r"\(\.\./\.\./references/([^)]+\.md)\)", text):
            ref_path = Path("references", linked)
            assert ref_path.is_file(), f"Broken reference {linked} in {path}"


def test_skills_official_docs_urls_registered():
    catalog = json.loads(Path("catalog/services.json").read_text(encoding="utf-8"))
    registered = {doc["url"] for service in catalog["services"] for doc in service["docs"]}
    for path in all_skills():
        text = path.read_text(encoding="utf-8")
        official = text.split("## Official docs", 1)[1].split("## Related skills", 1)[0]
        urls = re.findall(r"https://[^\s)>\]]+", official)
        assert urls, f"No URLs found in ## Official docs of {path}"
        unregistered = set(urls) - registered
        assert not unregistered, f"Unregistered official doc URLs in {path}: {unregistered}"


def test_skills_and_references_redaction_clean():
    targets = list(all_skills()) + list(Path("references").glob("*.md"))
    for target in targets:
        findings = scan_text(str(target), target.read_text(encoding="utf-8"))
        assert not findings, f"Redaction findings in {target}: {findings}"


def test_deepened_skills_content_and_concepts():
    lp_skill = Path("skills/oci-logging-pipelines/SKILL.md").read_text(encoding="utf-8")
    assert "Connector Hub" in lp_skill
    assert "CloudEvents" in lp_skill
    assert "Streaming" in lp_skill
    assert "checkpoint" in lp_skill
    assert "dynamic-group" in lp_skill

    db_skill = Path("skills/oci-db-observability/SKILL.md").read_text(encoding="utf-8")
    assert "Database Management" in db_skill
    assert "Operations Insights" in db_skill
    assert "Performance Hub" in db_skill
    assert "ASH" in db_skill
    assert "AWR" in db_skill
    assert "Capacity Planning" in db_skill

    sm_skill = Path("skills/oci-stack-monitoring-agents/SKILL.md").read_text(encoding="utf-8")
    assert "Management Agent" in sm_skill
    assert "Stack Monitoring" in sm_skill
    assert "plugin" in sm_skill
    assert "topology" in sm_skill
    assert "Prometheus" in sm_skill

    sigma_skill = Path("skills/oci-detections-sigma/SKILL.md").read_text(encoding="utf-8")
    assert "Sigma" in sigma_skill
    assert "OCL" in sigma_skill
    assert "requires_aggregation" in sigma_skill
    assert "MITRE" in sigma_skill

    maturity_skill = Path("skills/oci-om-maturity/SKILL.md").read_text(encoding="utf-8")
    assert "L0" in maturity_skill
    assert "L1" in maturity_skill
    assert "L2" in maturity_skill
    assert "L3" in maturity_skill
    assert "L4" in maturity_skill
    assert "AIOps" in maturity_skill
    assert "MCP Safety Pattern" in maturity_skill

    patterns_ref = Path("references/pipelines-patterns.md").read_text(encoding="utf-8")
    assert "Connector Hub Routing Matrix" in patterns_ref
    assert "CloudEvents Normalization" in patterns_ref
    assert "Streaming Lag and Checkpointing" in patterns_ref
    assert "UnconsumedMessages" in patterns_ref

    sigma_ref = Path("references/sigma-field-map.md").read_text(encoding="utf-8")
    assert "Field Translation Table" in sigma_ref
    assert "Event ID" in sigma_ref
    assert "Modifier Translation Table" in sigma_ref

    maturity_ref = Path("references/maturity-l0-l4.md").read_text(encoding="utf-8")
    assert "L0 — Foundations and Governance" in maturity_ref
    assert "L4 — AIOps and AI-Agent Observability" in maturity_ref


def test_all_reference_files_have_headings_and_content():
    for ref_file in Path("references").glob("*.md"):
        content = ref_file.read_text(encoding="utf-8")
        assert content.startswith("# "), f"Reference {ref_file} must start with top-level # heading"
        assert len(content.splitlines()) >= 5, f"Reference {ref_file} is too short"


