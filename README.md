# OCI Observability Tools

> Independent community project. Not an Oracle product, not endorsed or supported by Oracle. "Oracle", "OCI", and related marks are trademarks of Oracle and/or its affiliates. Always verify against the official documentation at docs.oracle.com; service capabilities, limits, and pricing change.

Offline-first skills and validation helpers for OCI Observability & Management. The pack helps Claude Code, Codex, Gemini CLI/Antigravity, and ChatGPT choose services and produce safer queries, alarms, pipelines, and detections. Helpers never access an OCI tenancy.

## See the skills in use

These two comparisons use the same prompt for each pair. Both answers are **illustrative, authored examples**, not captured model runs or a benchmark. An assistant without the pack can also answer correctly and cite documentation. The examples show the guidance the skills are designed to make repeatable; actual output depends on the model, loaded context, and available tools. No live OCI environment was queried.

### Use case 1: Diagnose a slow API and monitor availability

**Ask:**

> Which OCI Observability products should I use to investigate a slow checkout API across microservices, find related application logs, and check availability? Explain the capabilities, prerequisites, and how to validate the setup. Include official references.

**Without the skills — illustrative general answer:**

> Use Application Performance Monitoring (APM) for distributed tracing and synthetic availability monitoring, and Log Analytics to investigate application logs. Instrument your services, collect their logs, and use dashboards to investigate latency and errors. Start with the [APM documentation](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm) and [Log Analytics documentation](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm).

**With the skills — illustrative guided answer:**

> Use **APM** to follow requests across instrumented services and inspect slow spans. Configure OpenTelemetry export and context propagation using Oracle's [tracing ingestion guide](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html); verify the signal-specific endpoint and authentication before using a configuration draft.
>
> Use **Log Analytics** to search the related application logs. Trace-to-log correlation requires your application to emit trace/span identifiers and your log source to parse them. Inspect the existing collection path before adding another; see [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm).
>
> Use **APM synthetic monitoring** for scheduled availability checks. Choose a vantage point that can reach the endpoint; see [synthetic monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html).
>
> **Next step and validation:** First review instrumentation, exporter diagnostics, log fields, and endpoint reachability. In an authorized test, follow a known request through its trace, locate a matching log record in the same time window, and inspect a synthetic result separately. Missing spans may indicate sampling, export, or propagation problems; a successful probe alone does not establish request tracing. Choose sampling and log retention based on diagnostic needs and volume.
>
> **Evidence:** Documentation-backed design guidance; tenant configuration and ingestion are unverified.

**Skills used:** `oci-om-router` → `oci-apm-otel`, `oci-apm-tracing`, and `oci-ocl-queries`.

**What the guidance adds:** Separate signal paths, correlation prerequisites, capability-specific references, and independent validation for traces, logs, and probes.

### Use case 2: Analyze audit logs and detect unhealthy or silent resources

**Ask:**

> How do OCI Logging, Log Analytics, Monitoring, and Notifications differ? I need to investigate audit activity, alert on sustained high CPU per instance, and detect when a custom heartbeat stops arriving. Which capabilities and references should I use, and what should I verify?

**Without the skills — illustrative general answer:**

> Logging collects logs, Log Analytics supports deeper log investigation, Monitoring evaluates metrics and alarms, and Notifications delivers messages to subscribers. Send audit logs to Log Analytics, create CPU and missing-heartbeat alarms, and connect them to a notification topic. See the [Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm), [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm), and [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm) documentation.

**With the skills — illustrative guided answer:**

> For **audit investigation**, inspect the available audit records and use **Log Analytics** for parsed search and analysis. **Connector Hub** can move logs from Logging into Log Analytics; source selection, destination log group, and permissions need configuration. Follow the [service-connector ingestion guide](https://docs.oracle.com/en-us/iaas/log-analytics/doc/ingest-logs-from-other-oci-services-using-service-connector.html).
>
> For **CPU and heartbeat alarms**, use **Monitoring**, not an audit-log query. Confirm the CPU metric namespace and dimensions; group by resource to avoid hiding a busy instance in a fleet average. For a custom heartbeat, confirm the publisher's namespace, cadence, and dimensions. Missing telemetry uses `absent()`; a reported zero is a different condition. See the [MQL reference](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Reference/mql.htm).
>
> Use **Notifications** for delivery to confirmed subscriptions; see [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm). Configure trigger delay and message ownership with the alarm; see [managing alarms](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm).
>
> **Next step and validation:** Review a bounded time window of audit records and metric history before drafting the pipeline or alarms. In an authorized test, verify one known audit event in Log Analytics, evaluate CPU per instance, pause and resume a test heartbeat publisher, and verify alarm firing, notification receipt, and recovery separately. Investigate missing logs as a collection or routing issue before concluding there was no activity. Plan log retention and keep custom metric dimensions bounded.
>
> **Evidence:** Documentation-backed design guidance; pipeline, alarms, and delivery are unverified in your tenancy.

**Skills used:** `oci-om-router` → `oci-logging-pipelines`, `oci-ocl-queries`, `oci-monitoring-mql`, and `oci-monitoring-alarms`.

**What the guidance adds:** Clear collection/analysis/alert/delivery boundaries, absence semantics, prerequisites, and testable outcomes.

### What to look for in the paired answers

These authored examples show the intended contribution in observable terms. In use case 1, check whether the answer separates tracing, log search, and availability probes; names the prerequisites for trace-to-log correlation; and gives each signal its own validation. In use case 2, check whether it separates log collection from metric alerting, distinguishes an absent heartbeat from a reported zero, and validates notification and recovery independently. The skill-guided examples include those distinctions. The short baseline examples do not. These are comparisons of answer content, not proof that a model will produce the same difference in a live run.

| Observable answer evidence | Slow API example | Audit and heartbeat example |
|---|---|---|
| Service boundaries | APM traces, Log Analytics search, and synthetic probes have separate jobs | Logging/Connector Hub collection, Log Analytics analysis, Monitoring alarms, and Notifications delivery are distinct |
| Feasibility prerequisites | Trace context must reach logs and parsed trace/span fields must exist | Metric namespace/dimensions, heartbeat cadence, and notification subscribers must be checked |
| Testable outcome | Validate a known trace, matching log, and synthetic result independently | Validate an audit event, per-instance CPU, heartbeat stop/recovery, and notification separately |
| Failure interpretation | Missing spans can reflect sampling, export, or propagation | Missing telemetry is different from a metric value of zero |

The table is a traceability aid for the authored examples. It describes content present in the skill-guided text; it is not an independently measured model uplift.

### Produce measured comparison evidence

For a publishable model comparison, run each exact prompt in fresh baseline and skill-loaded sessions. Keep the model/version, system instructions outside the pack, tools, browsing access, temperature or other generation settings, and response budget fixed. Change only the skill pack. Do not run the baseline in a workspace that automatically loads this repository's `AGENTS.md`.

Capture the full sanitized responses, run date, model/version, prompt ID, active tools, loaded skills, and sources actually opened. Repeat each pair at least three times. Score each response against the same seven checks: correct service routing; capability boundaries; prerequisites; bounded next step; validation and failure interpretation; official claim-specific references; and honest evidence status. Use `0` (absent/incorrect), `1` (partial), or `2` (complete and supported), then have a domain reviewer check factual accuracy before calculating paired differences. Report per-criterion scores and run count; do not infer improvement from answer length or a single pair.

See the [capability answer guide](references/capability-answers.md) for the scoring sheet and run-record template. The examples above remain illustrative until replaced or supplemented by captured runs. Offline tests validate helpers, guidance structure, and packaging; they do not measure model answer quality or live OCI behavior.

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

For a Claude Code plugin marketplace, add `<OWNER>/oci-observability-tools` with `/plugin marketplace add`, then install `oci-observability-tools`. The local manifest is in `.claude-plugin/`.

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

The committed knowledge bundle is generated offline. Run `python scripts/build_chatgpt.py --check` to confirm it matches the skills and references.

### Preview or remove an installation

```sh
./install.sh --dry-run claude codex gemini antigravity
./install.sh --uninstall claude codex gemini antigravity
```

The installer never overwrites an unmanaged path. Each installation has a manifest, and uninstall removes only paths listed in that manifest.

## Optional Log Analytics MCP integration

This skills pack is offline-first. For live Log Analytics queries, it can be paired with the independent [Log Analytics MCP Server](https://github.com/rishabh-ghosh24/logan-mcp-server). The server is third-party software, not part of this repository or an Oracle product. Review its current code, release, dependencies, permissions, and security posture before installing it.

The server documents query, schema discovery, ingestion-health checks, parser triage, cross-source request-ID pivots, and incident investigations. It also exposes tools that create or change alerts, saved searches, dashboards, parsers, and delivery settings. Start it in read-only mode (`oci-logan-mcp --read-only`) and use a dedicated least-privilege OCI identity. Read-only mode still reads and returns tenant log data; redact results and keep them out of public artifacts. The server's documented query budget does not cover every query entry point, so constrain IAM scope, query time ranges, and result sizes as well.

Follow the server's own setup guide for installation, OCI authentication, and Codex MCP registration. Do not copy its example `StrictHostKeyChecking=no` SSH option into production configuration. Use normal SSH host-key verification. Never put OCI config files, private keys, OCIDs, or tenant data in this repository. This repository does not install or configure the server, and the MCP tools may be unavailable in a given assistant session.

See [Log Analytics MCP operating guidance](references/logan-mcp-server.md) for a safe tool-selection and evidence workflow. A successful tool connection does not prove that logs are complete, current, or correctly parsed.
For coordinator or API proxy integrations, the same guidance covers scope propagation, process-bound identities, fallback visibility, and distinguishing unavailable results from empty query results.

## Use the offline helpers

Python 3.10 or newer is required. For development, create a virtual environment and install the declared packages when available from an approved local package source:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

Route a question:

```sh
python scripts/catalog_query.py "Which service traces a slow API?" --top 3 --json
```

The first result is Application Performance Monitoring and links to the registered [APM documentation](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm). The OpenTelemetry setup skill cites the [open-source tracing guide](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html).

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

Tests block network sockets. `make linkcheck` is an explicitly manual online task and is not part of offline verification. See `CONTRIBUTING.md` for authoring and leak-response rules and `SECURITY.md` for private reporting.

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
