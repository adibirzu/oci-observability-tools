from pathlib import Path

from scripts.redaction_check import check_paths, scan_text


def test_whole_repository_is_public_safe():
    assert check_paths([Path(".")], Path.cwd()) == []


def test_constructed_leaks_trigger_every_rule():
    samples = [
        "oci" + "d1.instance.oc1.region.abcdefgh",
        ".".join(["10", "24", "8", "9"]),
        "person@" + "corp.test",
        "-----BEGIN " + "PRIVATE KEY-----",
        "AK" + "IA" + "A" * 16,
        "gh" + "p_" + "a" * 36,
        "xo" + "xb-example",
        ":".join(["ab"] * 16),
        "password=" + "not-a-placeholder",
        "host." + "internal",
        "/home/" + "person/project",
        "https://tenant." + "apm.region.example/upload",
        "https://tenant." + "objectstorage.region.example/bucket",
    ]
    rules = {finding.rule for finding in scan_text("\n".join(samples))}
    assert {
        "OCID",
        "IP_ADDRESS",
        "EMAIL",
        "PEM_PRIVATE_KEY",
        "AWS_ACCESS_KEY",
        "GITHUB_TOKEN",
        "SLACK_TOKEN",
        "KEY_FINGERPRINT",
        "SECRET_VALUE",
        "INTERNAL_HOST",
        "PERSONAL_PATH",
        "APM_ENDPOINT",
        "OBJECT_STORAGE_NAMESPACE",
    } <= rules


def test_clean_fixture_is_clean():
    path = Path("tests/fixtures/redaction/clean.txt")
    assert scan_text(path.read_text(encoding="utf-8"), str(path)) == []


def test_allowlist_requires_reason(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".redaction-allow").write_text("generated/*\n", encoding="utf-8")
    try:
        check_paths([tmp_path], tmp_path)
    except ValueError as exc:
        assert "missing justification" in str(exc)
    else:
        raise AssertionError("invalid allowlist accepted")
