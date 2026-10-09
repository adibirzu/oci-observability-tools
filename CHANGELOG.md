# Changelog

All notable changes follow Keep a Changelog. This project uses Semantic Versioning.

## [Unreleased]

## [0.1.0] - 2026-10-09

### Added

- Nine OCI Observability & Management skills with registered official documentation.
- Offline catalog routing, OCL linting, Sigma conversion, redaction, and generation helpers.
- Claude Code, Codex, Gemini CLI/Antigravity, and ChatGPT adapters and reversible installer.
- Synthetic Sigma and CloudEvents examples, schemas, CI policy, and offline tests.

### Verified

- The common smoke prompt, “Which OCI service should I use to trace a slow API?”, routes to Application Performance Monitoring in each adapter's shared knowledge and cites APMOTEL.
- Adapter smoke verification was performed offline against generated context and knowledge because live harness calls would violate the offline-only release gate.
