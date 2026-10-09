import re
from pathlib import Path

import yaml


SECTIONS = [
    "# ", "## When to use", "## Key concepts", "## Workflow", "## Pitfalls",
    "## Examples", "## Official docs", "## Related skills",
]


def skills():
    return sorted(Path("skills").glob("*/SKILL.md"))


def test_all_nine_skills_have_valid_frontmatter_and_sections():
    assert len(skills()) == 9
    for path in skills():
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        assert match, path
        metadata = yaml.safe_load(match.group(1))
        assert set(metadata) <= {"name", "description", "license"}
        assert metadata["name"] == path.parent.name
        assert re.fullmatch(r"oci-[a-z0-9-]+", metadata["name"])
        assert 60 <= len(metadata["description"]) <= 1024
        assert "Use when" in metadata["description"]
        assert metadata.get("license") == "Apache-2.0"
        positions = [text.index(section, match.end()) for section in SECTIONS]
        assert positions == sorted(positions)
        for linked in re.findall(r"\(\.\./\.\./references/([^)]+\.md)\)", text):
            assert Path("references", linked).is_file(), (path, linked)
