import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


SCOPES = [Path("skills"), Path("references"), Path("chatgpt"), Path("README.md"), Path("AGENTS.md"), Path("GEMINI.md")]
ALLOWED_HOSTS = {"docs.oracle.com", "www.oracle.com", "opentelemetry.io", "github.com"}


def markdown_files():
    for scope in SCOPES:
        if scope.is_file():
            yield scope
        elif scope.is_dir():
            yield from scope.rglob("*.md")


def test_document_urls_are_allowed_and_registered():
    catalog = json.loads(Path("catalog/services.json").read_text(encoding="utf-8"))
    registered = {doc["url"] for service in catalog["services"] for doc in service["docs"]}
    for path in markdown_files():
        urls = re.findall(r"https://[^\s)>\]]+", path.read_text(encoding="utf-8"))
        for url in urls:
            assert urlparse(url).hostname in ALLOWED_HOSTS, (path, url)
            if urlparse(url).hostname in {"docs.oracle.com", "www.oracle.com"}:
                assert url in registered, (path, url)


def test_each_skill_uses_catalog_official_docs():
    catalog = json.loads(Path("catalog/services.json").read_text(encoding="utf-8"))
    registered = {doc["url"] for service in catalog["services"] for doc in service["docs"]}
    for path in Path("skills").glob("*/SKILL.md"):
        official = path.read_text(encoding="utf-8").split("## Official docs", 1)[1].split("## Related skills", 1)[0]
        urls = re.findall(r"https://[^\s)>\]]+", official)
        assert urls and set(urls) <= registered


def test_generated_oracle_docs_is_fresh():
    subprocess.run([sys.executable, "scripts/gen_oracle_docs.py", "--check"], check=True)
