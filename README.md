# OCI Observability Tools

> Independent community project. Not an Oracle product, not endorsed or supported by Oracle. "Oracle", "OCI", and related marks are trademarks of Oracle and/or its affiliates. Always verify against the official documentation at docs.oracle.com; service capabilities, limits, and pricing change.

Offline-first skills and validation helpers for OCI Observability & Management. The pack helps Claude Code, Codex, Gemini CLI/Antigravity, and ChatGPT choose services and produce safer queries, alarms, pipelines, and detections. Helpers never access an OCI tenancy.

## What is included

| Skill | Purpose |
|---|---|
| `oci-om-router` | Choose an O&M service by job and signal |
| `oci-ocl-queries` | Author and debug Log Analytics OCL |
| `oci-apm-otel` | Instrument APM, OpenTelemetry, RUM, and synthetics |
| `oci-apm-tracing` | Deep distributed tracing, Trace Explorer, and synthetics |
| `oci-monitoring-alarms` | Write MQL and design alarms |
| `oci-monitoring-mql` | Author MQL queries, split metrics, and absence alarms |
| `oci-logging-pipelines` | Route logs, events, and streaming records |
| `oci-db-observability` | Diagnose database performance and capacity |
| `oci-stack-monitoring-agents` | Operate discovery, topology, agents, and Prometheus |
| `oci-detections-sigma` | Convert a supported Sigma subset to OCL |
| `oci-om-maturity` | Assess an L0–L4 observability roadmap |

The `catalog/` directory is the machine-readable capability and documentation registry. The `scripts/` directory contains offline catalog search, OCL linting, Sigma conversion, generation, and public-safety checks.

## Install

Clone or download this repository, enter its directory, and choose a harness. `install.sh` copies a self-contained bundle; it does not download dependencies or contact OCI.

### Claude Code

Install the skills directly:

```sh
./install.sh claude
```

For a Claude Code plugin marketplace, add `adibirzu/oci-observability-tools` with `/plugin marketplace add`, then install `oci-observability-tools`. The local manifest is in `.claude-plugin/`.

### Codex

Install to `~/.codex/skills`, or `~/.agents/skills` when that directory already exists:

```sh
./install.sh codex
```

Set `CODEX_SKILLS_DIR` to override the destination. Codex can also consume the repository-level `AGENTS.md` and `.codex-plugin/plugin.json` directly.

### Gemini CLI and Antigravity

Install the Gemini extension:

```sh
./install.sh gemini
```

This copies `gemini-extension.json`, `GEMINI.md`, skills, references, catalog, and helpers under `~/.gemini/extensions/oci-observability-tools`. Set `GEMINI_EXT_DIR` to override it.

For Antigravity skill discovery:

```sh
./install.sh antigravity
```

Set `AGY_SKILLS_DIR` to override `~/.antigravity/skills`.

### ChatGPT custom GPT

1. Create or edit a custom GPT.
2. Paste `chatgpt/instructions.md` into its instructions.
3. Upload all files in `chatgpt/knowledge/` as knowledge.
4. Optionally use `chatgpt/conversation-starters.md` for starter prompts.

The eleven committed skill bundles and service catalog are generated offline. Run `python scripts/build_chatgpt.py --check` to confirm it matches the skills and references.

### Preview or remove an installation

```sh
./install.sh --dry-run claude codex gemini antigravity
./install.sh --uninstall claude codex gemini antigravity
```

The installer never overwrites an unmanaged path. Each installation has a manifest, and uninstall removes only paths listed in that manifest.

## Use the offline helpers

Python 3.10 or newer is required. For development, create a virtual environment and install the declared packages when available from an approved local package source:

```sh
# MUTATES: creates the local virtual environment.
python3 -m venv .venv
. .venv/bin/activate
# MUTATES: installs development dependencies into the activated environment.
python -m pip install -e ".[dev]"
```

Route a question:

```sh
python scripts/catalog_query.py "Which service traces a slow API?" --top 3 --json
```

The first result is Application Performance Monitoring and links to the registered [APM documentation](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm). The OpenTelemetry setup skill cites the [open-source tracing guide](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html).

A wheel includes the helper modules, catalogs and schemas, all eleven skill bodies, linked references,
generated ChatGPT knowledge, and harness assets. Build it from the development environment:

```sh
# MUTATES: writes local distribution artifacts.
python -m build
# MUTATES: installs into the activated virtual environment.
python -m pip install dist/oci_observability_tools-0.1.0-py3-none-any.whl
oci-catalog-query "slow API traces" --top 1 --json --validate
```

Installed entry points are `oci-catalog-query`, `oci-ocl-lint`, `oci-sigma-to-ocl`, and
`oci-redaction-check`. Modules also run with `python -m oci_observability_tools.scripts.<helper>`.
Direct `python scripts/<helper>.py` commands continue to work from a checkout.

Lint OCL, convert a Sigma rule, and scan public content:

```sh
python scripts/ocl_lint.py query.ocl --json
python scripts/sigma_to_ocl.py examples/sigma/windows-logon.yml --json
python scripts/redaction_check.py .
```

All query time windows and compartment scope belong in separate API, CLI, UI, or tool arguments—not OCL text.

## Maturity map

| Level | Outcome |
|---|---|
| L0 | Audit, logging, compartments, tags, ownership, and retention foundations |
| L1 | Service metrics, actionable alarms, and tested notifications |
| L2 | Log analytics, database depth, governed routing, and data quality |
| L3 | Tracing, RUM, synthetics, correlation, and service-level objectives |
| L4 | Evaluated AIOps and AI-agent observability with controlled actions |

Maturity is demonstrated by operational evidence and interlocks, not by tool deployment alone.

## Develop and verify

```sh
make check
python scripts/gen_oracle_docs.py --check
python scripts/build_chatgpt.py --check
```

`make check` requires shellcheck and includes configured Ruff lint, both generated freshness checks,
shell lint, the complete behavioral suite, and redaction. Packaging regressions build an sdist and
wheel offline and execute installed standard-library helpers and generators in fresh temporary
environments outside the checkout. Runtime dependencies must be installed to use Sigma conversion.

Tests block network sockets. `make linkcheck` is an explicitly manual online task and is not part of offline verification. See `CONTRIBUTING.md` for authoring and leak-response rules and `SECURITY.md` for private reporting.

The declared version is `0.1.0`; published-release and real harness-load acceptance remain pending.
Offline routing and temporary install/uninstall tests do not establish live loaded-agent behavior.
The canonical recovery record is [docs/agent-handoff.md](docs/agent-handoff.md).

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
