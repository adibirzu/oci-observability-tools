# Changelog

All notable changes follow Keep a Changelog. This project uses Semantic Versioning.
The declared package/adapter version `0.1.0` is source metadata; a tag or published release is pending.

## [Unreleased]

### Changed

- Explicit setuptools package and runtime-asset configuration for wheel and editable installations,
  with installed catalog, OCL, Sigma, and redaction command entry points.
- Complete generated ChatGPT knowledge for all eleven existing source skill bodies, including
  APM tracing and Monitoring MQL; deterministic freshness now detects uncovered source and extras.
- Configured Ruff findings corrected; offline checks include generated freshness and shell lint.
- Distribution pointers aligned to the verified `adibirzu/oci-observability-tools` repository.
- Canonical Skills recovery handover designated at `docs/agent-handoff.md`.

### Source baseline (declared 0.1.0)

- Eleven OCI Observability & Management skills with registered official documentation.
- Offline catalog routing, OCL linting, Sigma conversion, redaction, and generation helpers.
- Claude Code, Codex, Gemini CLI/Antigravity, and ChatGPT adapters and reversible installer.
- Synthetic Sigma and CloudEvents examples, schemas, CI policy, and offline tests.

### Evidence boundaries

- The offline common smoke prompt routes to Application Performance Monitoring and cites the
  registered APM documentation. Shared APM/OpenTelemetry assets include APMOTEL.
- Offline asset checks and temporary installer checks do not establish real harness load or
  loaded-agent answers. T16 live smoke remains open; AGY runtime is excluded from this repair.
- Fresh head-bound CI, independent no-mistakes gates, full-history safety, real installation,
  and a published release require their own evidence. Version text establishes none of those.
