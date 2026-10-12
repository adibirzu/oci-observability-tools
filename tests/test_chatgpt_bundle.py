"""Generated knowledge is an owned upload contract, including every source body."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts import build_chatgpt


def headings(path):
    return [
        line
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if re.match(r"^#{1,6} ", line)
    ]


def skill_name(content):
    return yaml.safe_load(content.split("---", 2)[1])["name"]


def test_generated_bundle_is_fresh_and_complete():
    subprocess.run([sys.executable, "scripts/build_chatgpt.py", "--check"], check=True)
    source = {
        skill_name(path.read_text(encoding="utf-8")): path.read_text(encoding="utf-8")
        for path in Path("skills").glob("*/SKILL.md")
    }
    bundles = list(Path("chatgpt/knowledge").glob("*.md"))
    emitted = [skill_name(path.read_text(encoding="utf-8")) for path in bundles]
    assert len(emitted) == len(set(emitted))
    assert set(emitted) == set(source)
    for path in bundles:
        content = path.read_text(encoding="utf-8")
        body = source[skill_name(content)]
        assert content.startswith(body.rstrip() + "\n")
        links = re.findall(r"\(\.\./\.\./references/([^)]+\.md)\)", body)
        for link in links:
            reference = (Path("references") / link).read_text(encoding="utf-8").rstrip()
            assert reference in content
    assert (
        Path("chatgpt/knowledge/services.json").read_bytes()
        == Path("catalog/services.json").read_bytes()
    )


@pytest.fixture
def generation_root(tmp_path, monkeypatch):
    for directory in ("skills", "references", "catalog", "chatgpt"):
        shutil.copytree(directory, tmp_path / directory)
    for filename in ("AGENTS.md", "GEMINI.md"):
        shutil.copyfile(filename, tmp_path / filename)
    monkeypatch.setattr(build_chatgpt, "ROOT", tmp_path)
    monkeypatch.setattr(build_chatgpt, "KNOWLEDGE", tmp_path / "chatgpt/knowledge")
    return tmp_path


def test_unregistered_source_skill_fails_generation(generation_root, capsys):
    future = generation_root / "skills/oci-future/SKILL.md"
    future.parent.mkdir()
    future.write_text("---\nname: oci-future\n---\n# Future skill\n", encoding="utf-8")
    assert build_chatgpt.main(["--check"]) == 1
    assert "oci-future" in capsys.readouterr().out


def test_generation_is_deterministic_and_rejects_stale_extra_bundle(generation_root):
    assert build_chatgpt.main([]) == 0
    first = {
        path.relative_to(generation_root): path.read_bytes()
        for path in generation_root.rglob("*")
        if path.is_file()
    }
    assert build_chatgpt.main([]) == 0
    second = {
        path.relative_to(generation_root): path.read_bytes()
        for path in generation_root.rglob("*")
        if path.is_file()
    }
    assert first == second
    extra = generation_root / "chatgpt/knowledge/obsolete.md"
    extra.write_text("# Obsolete generated skill\n", encoding="utf-8")
    assert build_chatgpt.main(["--check"]) == 1
    assert build_chatgpt.main([]) == 0
    assert not extra.exists()
    assert build_chatgpt.main(["--check"]) == 0


def test_disclaimer_and_heading_parity():
    assert "Not an Oracle product" in Path("chatgpt/instructions.md").read_text(encoding="utf-8")
    left = [item.replace("OCI Observability Tools", "<TITLE>") for item in headings("AGENTS.md")]
    right = [item.replace("OCI Observability Tools", "<TITLE>") for item in headings("GEMINI.md")]
    assert left == right
