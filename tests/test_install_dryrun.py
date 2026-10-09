import os
import shutil
import subprocess
from pathlib import Path


def run_install(home, *args):
    env = dict(os.environ)
    env["HOME"] = str(home)
    return subprocess.run(["bash", "install.sh", *args], env=env, capture_output=True, text=True)


def snapshot(path):
    return sorted(str(item.relative_to(path)) for item in path.rglob("*"))


def test_dry_run_writes_nothing(tmp_path):
    if shutil.which("bash") is None:
        return
    before = snapshot(tmp_path)
    result = run_install(tmp_path, "--dry-run", "claude", "codex", "gemini", "antigravity")
    assert result.returncode == 0
    assert "WOULD copy" in result.stdout and "WOULD link" in result.stdout
    assert snapshot(tmp_path) == before


def test_unknown_harness_exits_two(tmp_path):
    result = run_install(tmp_path, "unknown")
    assert result.returncode == 2


def test_install_then_uninstall_restores_tree(tmp_path):
    if shutil.which("bash") is None:
        return
    before = snapshot(tmp_path)
    names = ("claude", "codex", "gemini", "antigravity")
    installed = run_install(tmp_path, *names)
    assert installed.returncode == 0, installed.stderr
    assert any(tmp_path.rglob(".oci-observability-tools.manifest"))
    removed = run_install(tmp_path, "--uninstall", *names)
    assert removed.returncode == 0, removed.stderr
    assert snapshot(tmp_path) == before
