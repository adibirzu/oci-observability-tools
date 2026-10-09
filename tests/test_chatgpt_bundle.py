import re
import subprocess
import sys
from pathlib import Path


def headings(path):
    return [line for line in Path(path).read_text(encoding="utf-8").splitlines() if re.match(r"^#{1,6} ", line)]


def test_generated_bundle_is_fresh_and_complete():
    subprocess.run([sys.executable, "scripts/build_chatgpt.py", "--check"], check=True)
    assert len(list(Path("chatgpt/knowledge").glob("*.md"))) == 9
    assert Path("chatgpt/knowledge/services.json").is_file()


def test_disclaimer_and_heading_parity():
    assert "Not an Oracle product" in Path("chatgpt/instructions.md").read_text(encoding="utf-8")
    left = [item.replace("OCI Observability Tools", "<TITLE>") for item in headings("AGENTS.md")]
    right = [item.replace("OCI Observability Tools", "<TITLE>") for item in headings("GEMINI.md")]
    assert left == right
