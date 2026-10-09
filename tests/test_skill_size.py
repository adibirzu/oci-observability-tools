from pathlib import Path


def test_skill_and_context_sizes():
    for path in Path("skills").glob("*/SKILL.md"):
        assert len(path.read_text(encoding="utf-8").splitlines()) < 500, path
    for name in ("AGENTS.md", "GEMINI.md"):
        path = Path(name)
        if path.exists():
            assert len(path.read_text(encoding="utf-8").splitlines()) < 150
    instructions = Path("chatgpt/instructions.md")
    if instructions.exists():
        assert len(instructions.read_text(encoding="utf-8")) < 8000
