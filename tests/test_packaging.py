"""Distribution contract: real artifacts and installed helpers outside the checkout."""

import email
import json
import os
import subprocess
import sys
import tarfile
import venv
import zipfile
from pathlib import Path

import pytest
from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "oci_observability_tools"
ASSET_PATTERNS = (
    "catalog/*.json",
    "references/*.md",
    "skills/*/SKILL.md",
    "chatgpt/*.md",
    "chatgpt/knowledge/*",
    "examples/sigma/*.yml",
    "examples/cloudevents/*.json",
    ".claude-plugin/*.json",
    ".codex-plugin/*.json",
)
ROOT_ASSETS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "gemini-extension.json",
    "install.sh",
    "LICENSE",
    "NOTICE",
    "README.md",
)


def run(*args, cwd):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["PIP_NO_INDEX"] = "1"
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture(scope="module")
def artifacts(tmp_path_factory):
    output = tmp_path_factory.mktemp("distribution")
    run(sys.executable, "-m", "build", "--no-isolation", "--outdir", str(output), cwd=ROOT)
    return output


def test_wheel_contains_helpers_and_complete_runtime_assets(artifacts):
    wheel = next(artifacts.glob("*.whl"))
    assets = [ROOT / name for name in ROOT_ASSETS]
    for pattern in ASSET_PATTERNS:
        assets.extend(ROOT.glob(pattern))
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        for path in assets:
            target = f"{PACKAGE}/{path.relative_to(ROOT).as_posix()}"
            assert archive.read(target) == path.read_bytes(), target
        for path in (ROOT / "scripts").glob("*.py"):
            assert f"{PACKAGE}/scripts/{path.name}" in names
        assert not any(
            part in {"tests", ".task-private", ".venv", "__pycache__"}
            for name in names
            for part in Path(name).parts
        )
        metadata = email.message_from_bytes(
            archive.read(next(name for name in names if name.endswith(".dist-info/METADATA")))
        )
        runtime = {
            Requirement(value).name.lower()
            for value in metadata.get_all("Requires-Dist", [])
            if Requirement(value).marker is None
        }
        assert {"pyyaml", "jsonschema"} <= runtime
        assert metadata["Requires-Python"] == ">=3.10"
        repository = "https://github.com/adibirzu/oci-observability-tools"
        assert set(metadata.get_all("Project-URL")) == {
            f"Homepage, {repository}",
            f"Repository, {repository}",
        }
        for manifest_path in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            manifest = json.loads(archive.read(f"{PACKAGE}/{manifest_path}"))
            assert manifest["version"] == metadata["Version"]
            assert manifest["repository"] == repository
    with tarfile.open(next(artifacts.glob("*.tar.gz"))) as archive:
        assert not any(
            part in {".task-private", ".venv"}
            for name in archive.getnames()
            for part in Path(name).parts
        )


@pytest.mark.parametrize("editable", [False, True], ids=["wheel", "editable"])
def test_installed_helpers_and_generators_work_outside_source(artifacts, tmp_path, editable):
    wheel = next(artifacts.glob("*.whl"))
    if editable:
        from build import ProjectBuilder

        destination = tmp_path / "editable-artifact"
        destination.mkdir()
        wheel = Path(ProjectBuilder(str(ROOT)).build("editable", str(destination)))
    environment = tmp_path / "environment"
    venv.EnvBuilder(with_pip=True).create(environment)
    binary = environment / "bin"
    python = binary / "python"
    run(str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel), cwd=tmp_path)
    origin = Path(
        run(
            str(python),
            "-I",
            "-c",
            f"import {PACKAGE}; print({PACKAGE}.__file__)",
            cwd=tmp_path,
        ).strip()
    ).resolve()
    assert origin == ROOT / "__init__.py" if editable else origin.is_relative_to(environment)
    routed = json.loads(
        run(
            str(binary / "oci-catalog-query"),
            "slow API traces",
            "--top",
            "1",
            "--json",
            "--validate",
            cwd=tmp_path,
        )
    )
    assert routed[0]["id"] == "apm"
    assert routed[0]["doc"] == (
        "https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm"
    )
    query = tmp_path / "query.ocl"
    query.write_text("'Event ID' = '4625'", encoding="utf-8")
    assert json.loads(run(str(binary / "oci-ocl-lint"), str(query), "--json", cwd=tmp_path)) == []
    clean = tmp_path / "clean.txt"
    clean.write_text("<COMPARTMENT_OCID>", encoding="utf-8")
    run(str(binary / "oci-redaction-check"), str(clean), cwd=tmp_path)
    for generator in ("gen_oracle_docs", "build_chatgpt"):
        run(str(python), "-I", "-m", f"{PACKAGE}.scripts.{generator}", "--check", cwd=tmp_path)
