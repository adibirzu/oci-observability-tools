# Plan: `oci-observability-tools` (new public GitHub repo)

Status: source plan and acceptance ledger. The current tree contains eleven skills. Source/local tests, live harness acceptance, CI, full-history safety, and published release evidence remain separate; unchecked criteria below are not satisfied by version declarations.
Sources reused:
- `~/dev/oci-skills`: layout, plugin manifests, install.sh, redaction gate, Log Analytics/OCL and Sigma lessons.
- `~/dev/obs`: L0-L4 maturity path and the `governance/external-links.json` doc registry.

Every doc URL below returned HTTP 200 on 2026-10-09 (checked with `curl -L`).
`log-analytics/doc/detection-rules.html` returned 404, so the plan uses `create-alerts-detected-events.html` instead.

## 1. Purpose, audience, non-goals, license, disclaimer

**Purpose.** A vendor-neutral skill pack that works across harnesses: Claude Code, Codex, ChatGPT custom GPTs, and Gemini CLI / Antigravity.
It teaches AI coding assistants three things about OCI Observability & Management (O&M):
- what each service does;
- which service fits which job;
- how to write correct queries, alarms, pipelines, and detections.

It also ships offline helper scripts that check that output.

**Audience.** SREs, platform engineers, DBAs, SOC analysts, and developers who are new to OCI O&M or who work across clouds.
Their assistant should give answers grounded in the official docs.

**Non-goals.**
- No live tenancy access, no OCI SDK/CLI calls in helpers or tests, and no credential handling. Skills may *show* `oci` CLI commands, with placeholders only.
- Not a replacement for Oracle documentation, support, or pricing pages. Skills link to them and never restate prices.
- No non-O&M OCI domains such as IAM authoring, networking, or cost. The router may only point to their docs.
- No MCP server in v1. Skills only teach how to pass arguments safely to existing MCP tools.
- No tenant data, no dashboards exported from real tenancies, and no internal KB entries.

**License: Apache-2.0.** Reasons:
- It includes an explicit patent grant. That matters for a pack that encodes vendor-specific query and detection logic that others will embed.
- Its `NOTICE` file is the standard place for the independence disclaimer and trademark attribution.
- It is the usual license for cloud and observability tooling (for example OpenTelemetry), which eases enterprise adoption.

`oci-skills` is MIT, but this repo copies its structure only. Any adapted snippet is rewritten, so no relicensing question arises.

**Disclaimer.** Use this text verbatim in the README header, `NOTICE`, the suffix of every harness manifest `description`, AGENTS.md, GEMINI.md, and `chatgpt/instructions.md`:
> Independent community project. Not an Oracle product, not endorsed or supported by Oracle. "Oracle", "OCI", and related marks are trademarks of Oracle and/or its affiliates. Always verify against the official documentation at docs.oracle.com; service capabilities, limits, and pricing change.

## 2. Directory tree

```
oci-observability-tools/
├── README.md  LICENSE(Apache-2.0)  NOTICE  SECURITY.md  CONTRIBUTING.md  CHANGELOG.md
├── AGENTS.md                     # Codex/generic entrypoint: skill index, routing, safety rules (<150 lines)
├── GEMINI.md                     # Gemini CLI/Antigravity context (generated from same source as AGENTS.md)
├── CLAUDE.md                     # imports AGENTS.md
├── gemini-extension.json         # {name, version, description, contextFileName:"GEMINI.md"}
├── Makefile                      # check = freshness + shellcheck + ruff + pytest + redaction
├── pyproject.toml                # python>=3.10; explicit setuptools package/assets; runtime/dev deps
├── .redaction-allow              # empty; pathspec + mandatory justification comment per line
├── .gitignore  .gitleaks.toml  .pre-commit-config.yaml
├── .claude-plugin/plugin.json  .claude-plugin/marketplace.json
├── .codex-plugin/plugin.json
├── .github/workflows/ci.yml  .github/PULL_REQUEST_TEMPLATE.md
├── skills/
│   ├── oci-om-router/SKILL.md
│   ├── oci-ocl-queries/SKILL.md
│   ├── oci-apm-otel/SKILL.md
│   ├── oci-apm-tracing/SKILL.md
│   ├── oci-monitoring-alarms/SKILL.md
│   ├── oci-monitoring-mql/SKILL.md
│   ├── oci-logging-pipelines/SKILL.md
│   ├── oci-db-observability/SKILL.md
│   ├── oci-stack-monitoring-agents/SKILL.md
│   ├── oci-detections-sigma/SKILL.md
│   └── oci-om-maturity/SKILL.md
├── references/
│   ├── ocl-field-typing.md   ocl-cookbook.md   sigma-field-map.md   mql-cookbook.md
│   ├── otel-to-apm.md        pipelines-patterns.md (Connector matrix, CloudEvents, lag/checkpoint)
│   ├── mcp-safety.md         maturity-l0-l4.md   portable-deploy.md
│   └── oracle-docs.md        # GENERATED from catalog by scripts/gen_oracle_docs.py
├── catalog/
│   ├── services.json  services.schema.json
│   └── sigma_field_map.json  sigma_field_map.schema.json
├── chatgpt/
│   ├── instructions.md       # custom-GPT instructions (<8000 chars)
│   ├── conversation-starters.md  apps-sdk-notes.md
│   └── knowledge/            # GENERATED by scripts/build_chatgpt.py, committed for direct upload
├── scripts/
│   ├── ocl_lint.py  sigma_to_ocl.py  catalog_query.py  redaction_check.py
│   └── build_chatgpt.py  gen_oracle_docs.py
├── install.sh
├── examples/sigma/*.yml (6 self-authored rules)   examples/cloudevents/*.json (2, placeholder OCIDs)
└── tests/
    ├── conftest.py  (blocks network: monkeypatch socket.socket.connect to raise)
    ├── test_frontmatter.py test_skill_size.py test_doc_urls.py test_catalog_schema.py
    ├── test_redaction.py test_sigma_to_ocl.py test_ocl_lint.py test_catalog_query.py
    ├── test_install_dryrun.py test_chatgpt_bundle.py test_manifests.py
    └── fixtures/ sigma/*.yml sigma/expected/*.json ocl/good/*.ocl ocl/bad/*.ocl redaction/{leaky,clean}.txt
```

**SKILL.md contract**
- Frontmatter is YAML. Required keys:
  - `name`: equals the directory name and matches `^oci-[a-z0-9-]+$`.
  - `description`: 60-1024 characters, starts with what the skill does, and contains "Use when".
- `license: Apache-2.0` is the only optional key.
- Body sections, in this order:
  1. `# Title`
  2. `## When to use`
  3. `## Key concepts`
  4. `## Workflow`
  5. `## Pitfalls`
  6. `## Examples`
  7. `## Official docs` (catalog URLs only)
  8. `## Related skills`
- Skills link to shared material with `../../references/<file>.md`.

## 3. Skills (11)

Each doc key below maps to a `docs[]` entry in `catalog/services.json`. Every URL has the prefix `https://docs.oracle.com/en-us/iaas/` and returned HTTP 200.

| Key | Path | Key | Path |
|---|---|---|---|
| MON | `Content/Monitoring/home.htm` | APM | `application-performance-monitoring/home.htm` |
| MQL | `Content/Monitoring/Reference/mql.htm` | APMOTEL | `application-performance-monitoring/doc/configure-open-source-tracing-systems.html` |
| ALARM | `Content/Monitoring/Tasks/managingalarms.htm` | APMSYN | `application-performance-monitoring/doc/use-synthetic-monitoring.html` |
| CUSTMET | `Content/Monitoring/Tasks/publishingcustommetrics.htm` | SM | `stack-monitoring/home.htm` |
| LOG | `Content/Logging/home.htm` | SMDISC | `stack-monitoring/doc/promotion-and-discovery.html` |
| CUSTLOG | `Content/Logging/Concepts/custom_logs.htm` | MA | `management-agents/home.htm` |
| LA | `log-analytics/home.htm` | MAPROM | `management-agents/doc/management-agents-collect-prometheus-metrics.html` |
| LAQ | `log-analytics/doc/query-search.html` | DBM | `database-management/home.htm` |
| LACMD | `log-analytics/doc/command-reference.html` | DBMPH | `database-management/doc/performance-hub.html` |
| LASCH | `log-analytics/doc/ingest-logs-from-other-oci-services-using-service-connector.html` | OPSI | `operations-insights/home.htm` |
| LADET | `log-analytics/doc/create-alerts-detected-events.html` | OPSICAP | `operations-insights/doc/capacity-planning.html` |
| NOTIF | `Content/Notification/home.htm` | EVT | `Content/Events/home.htm` |
| SCH | `Content/connector-hub/overview.htm` | EVTENV | `Content/Events/Reference/eventenvelopereference.htm` |
| STRM | `Content/Streaming/home.htm` | | |

1. **oci-om-router**
   - Description: "Capability catalog and router for OCI Observability & Management. Use when a user asks which OCI service fits a monitoring, logging, tracing, database, alerting, or security-analytics job, or compares OCI O&M with other clouds."
   - Job-to-service table:

     | Job | Service |
     |---|---|
     | Metrics | Monitoring |
     | Raw logs | Logging |
     | Log search, parsing, ML, SIEM-like analysis | Log Analytics |
     | Traces, RUM, synthetic monitoring | APM |
     | Application-stack topology | Stack Monitoring |
     | Database performance | Database Management |
     | Capacity and SQL insights | Ops Insights |
     | Agent-based collection | Management Agent |
     | Routing and fan-out | Events, Connector Hub, Streaming, Notifications |

   - Also includes a conceptual cross-cloud equivalence table (CloudWatch, Azure Monitor, Google Cloud Logging) and a "run `scripts/catalog_query.py`" hint.
   - Cites every *home* key.
2. **oci-ocl-queries**
   - Description: "Author and debug OCI Log Analytics query language (OCL) searches. Use when writing, fixing, or optimizing Log Analytics queries, stats, timestats, link, or saved searches."
   - Field quoting and typing rules:
     - Quote multi-word field names: `'Log Source'`.
     - String-typed numeric fields take quoted literals: `'Event ID' = '4625'`. The same applies to `'Logon Type'`, `'Response Code'`, and `'Status Code'`.
     - True numeric fields take unquoted literals: `'Source Port' = 443`.
     - Use `in ('a','b')` for sets.
     - `like` uses the `*` wildcard.
   - Compartment scope: always query the **subtree** (`--compartment-id-in-subtree true` / `compartment_id_in_subtree=True`). Otherwise data in child compartments silently disappears.
   - **Time window is set outside the query:** pass `time-start`/`time-end` through the API or CLI, or use the UI picker. Never put it in the query text.
   - Pipeline commands covered: `stats`, `timestats`, `link`, `eval`, `where`, `sort`, `head`, `fields`.
   - Performance: filter on indexed fields first. Avoid a leading `'Original Log Content' like '*x*'`.
   - Workflow: run `ocl_lint.py` on every query.
   - Cites LA, LAQ, LACMD.
3. **oci-apm-otel**
   - Description: "Instrument applications for OCI Application Performance Monitoring with OpenTelemetry, APM agents, browser RUM, and synthetics. Use when sending traces/spans to APM, choosing data keys, or debugging missing traces."
   - APM domain setup and public vs private data keys (`<APM_PRIVATE_DATAKEY>`, `<APM_PUBLIC_DATAKEY>`).
   - OTLP exporter configuration (`OTEL_EXPORTER_OTLP_ENDPOINT=<APM_DOMAIN_UPLOAD_ENDPOINT>`, path and header shape taken only from APMOTEL), `service.name`, and sampling.
   - Correlating traces with logs in Log Analytics.
   - Synthetic monitors.
   - Pitfalls: never put the private key in browser code. Allow for ingestion lag before concluding "no data".
   - Cites APM, APMOTEL, APMSYN.
4. **oci-monitoring-alarms**
   - Description: "Write OCI Monitoring Query Language (MQL) queries and alarms. Use when querying metrics, publishing custom metrics, or designing alarms with Notifications."
   - MQL grammar: `metric[interval]{dims}.grouping().statistic()`.
   - Alarms: threshold and absence alarms, pending duration, severity, repeat notification, and message format.
   - Custom metric namespaces and dimensions (link to limits, do not restate them).
   - Alarm routing: alarm → Notifications topic → email, HTTPS, or Functions.
   - Cites MON, MQL, ALARM, CUSTMET, NOTIF.
5. **oci-logging-pipelines**
   - Description: "Design OCI Logging and Connector Hub pipelines. Use when enabling service, custom, or audit logs, routing logs, events, or metrics to Log Analytics, Streaming, Object Storage, Functions, or Notifications, or handling OCI event payloads."
   - Log types (service, custom, audit) and log groups.
   - Connector Hub source → task → target matrix, plus the IAM policy shape for connectors (placeholder groups).
   - Events rules and **CloudEvents normalization**:
     - Map to `specversion`, `type`, `source`, `id`, `time`, `data`.
     - Fold the legacy `eventType`/`cloudEventsVersion` fields into those.
     - Deduplicate on `id`.
   - Streaming **lag and checkpointing**:
     - Track the offset and last record timestamp for each partition.
     - Commit the checkpoint only after the durable write.
     - Resume from the checkpoint.
     - Alert when lag exceeds N minutes.
   - Cites LOG, CUSTLOG, SCH, LASCH, EVT, EVTENV, STRM, NOTIF.
6. **oci-db-observability**
   - Description: "Use OCI Database Management and Operations Insights for Oracle Database performance, fleet health, SQL analysis, and capacity planning. Use when diagnosing database performance or forecasting capacity."
   - Basic vs full Database Management, and enablement prerequisites (management agent or private endpoint).
   - Performance Hub with ASH and AWR concepts.
   - Ops Insights SQL Insights and capacity forecasting.
   - Decision guide: when to use Database Management vs Ops Insights.
   - Cites DBM, DBMPH, OPSI, OPSICAP.
7. **oci-stack-monitoring-agents**
   - Description: "Monitor application stacks and hosts with OCI Stack Monitoring and Management Agent. Use when discovering resources such as WebLogic, hosts, or databases, installing agents, or collecting Prometheus metrics."
   - Management Agent install and plugin model.
   - Stack Monitoring discovery and promotion, topology, and baselines/alarms.
   - Prometheus scraping into Monitoring.
   - Troubleshooting agent health.
   - Cites SM, SMDISC, MA, MAPROM.
8. **oci-detections-sigma**
   - Description: "Convert Sigma detection rules into OCI Log Analytics OCL and schedule them as detection alerts. Use when porting SIEM detections, building MITRE-tagged hunts, or validating detection queries."
   - Deterministic mapping from Sigma fields, modifiers, and logsources to OCL.
   - Aggregation tail and the `requires_aggregation` flag. Only aggregating queries are eligible as scheduled searches.
   - Passes MITRE tags and false-positive notes through to the output.
   - Workflow: `sigma_to_ocl.py`, then `ocl_lint.py`, then a test run over a short window.
   - Cites LA, LACMD, LADET.
9. **oci-om-maturity**
   - Description: "Assess and plan observability maturity on OCI from L0 to L4. Use when designing an observability roadmap, onboarding a workload, or reviewing coverage gaps."
   - Levels:

     | Level | Focus |
     |---|---|
     | L0 | Foundations: audit, logging, compartments, tags |
     | L1 | Service metrics and alarms |
     | L2 | Log analytics and database depth |
     | L3 | Tracing, RUM, synthetic monitoring, SLOs |
     | L4 | AIOps and AI-agent observability: instrument → collect → analyse → evaluate → act |

   - Each level has a services and interlocks checklist, rewritten from the obs Atlas.
   - Includes the MCP safety pattern for agent-driven queries.
   - Cites MON, LA, APM, DBM, OPSI, SCH.

10. **oci-apm-tracing**
    - Existing specialized distributed tracing, Trace Explorer, and synthetic-monitor source:
      `skills/oci-apm-tracing/SKILL.md`, with `references/apm-tracing.md`.
11. **oci-monitoring-mql**
    - Existing specialized MQL, split-metric alarm, and absence-trigger source:
      `skills/oci-monitoring-mql/SKILL.md`, with `references/mql-syntax.md`.

See `README.md` for ChatGPT upload usage and section 5 for the generator contract.

## 4. Capability catalog

`catalog/services.json` example entry:
```json
{ "schemaVersion": "1.0", "checkedAt": "2026-10-09",
  "services": [ {
    "id": "log-analytics", "name": "Log Analytics", "category": "logs",
    "signals": ["logs", "events"], "summary": "Search, parse, correlate, and alert on logs (<=280 chars).",
    "useCases": ["search and correlate logs", "parse custom log formats", "scheduled detection alerts"],
    "keywords": ["siem", "ocl", "parser", "search", "detection", "sigma"],
    "pricingNote": "Billed by storage tier; see the official OCI pricing page.",
    "skill": "oci-ocl-queries", "relatedServices": ["logging", "service-connector-hub"],
    "maturityLevels": ["L2"],
    "docs": [ {"key": "LA", "title": "Log Analytics", "url": "https://docs.oracle.com/en-us/iaas/log-analytics/home.htm"} ] } ] }
```
Required service ids (12): `monitoring`, `logging`, `log-analytics`, `apm`, `stack-monitoring`, `database-management`, `operations-insights`, `management-agent`, `notifications`, `events`, `service-connector-hub`, `streaming`.

Skill ownership:
- `notifications` → oci-monitoring-alarms.
- `events`, `service-connector-hub`, `streaming`, `logging` → oci-logging-pipelines.
- `management-agent`, `stack-monitoring` → oci-stack-monitoring-agents.
- The rest map to the skill with the obvious name.

`catalog/services.schema.json` (JSON Schema draft 2020-12, `additionalProperties: false` throughout):
- Top-level `required: [schemaVersion, checkedAt]` plus `services`. `checkedAt` uses `format: date`.
- Each service requires every field in the example.
- `id`: pattern `^[a-z0-9-]+$`.
- `category` enum: `metrics, logs, traces, database, agents, eventing`.
- `signals` items enum: `metrics, logs, traces, events, sql, topology, synthetic`; `minItems: 1`.
- `useCases`, `keywords`: `minItems: 2`.
- `summary`: `maxLength: 280`.
- `pricingNote`: `maxLength: 200`.
- `skill`: pattern `^oci-[a-z0-9-]+$`.
- `maturityLevels` items enum: `L0`-`L4`.
- `docs`: `minItems: 1`; each item `{key: ^[A-Z]+$, title, url}` with url pattern `^https://(docs|www)\.oracle\.com/`.
- Uniqueness of `id` and of doc `key` is enforced in tests, not the schema.

`catalog/sigma_field_map.json`:
- `fields` maps each Sigma field to `{ocl, type: string|number}`:

  | Sigma field | OCL field | Type |
  |---|---|---|
  | EventID | Event ID | string |
  | Image | Process Name | string |
  | ParentImage | Parent Process Name | string |
  | CommandLine | Command Line | string |
  | User, AccountName | Principal Name | string |
  | TargetUserName | Target User | string |
  | SourceIp | Source IP | string |
  | DestinationIp | Destination IP | string |
  | SourcePort | Source Port | number |
  | DestinationPort | Destination Port | number |
  | LogonType | Logon Type | string |
  | QueryName | Query Name | string |

- `logsources` maps `"<product>/<service>"` to a list of Log Source names:
  - `windows/security` → `Windows Security Events`
  - `windows/sysmon` → `Windows Sysmon Operational Logs`
  - `linux/auth` → `Linux Secure Logs`
  - `oci/audit` → `OCI Audit Logs`
- `references/sigma-field-map.md` renders the map and states that it is a convention: verify field names against your own Log Source definitions.

## 5. Offline helper scripts

All scripts use the stdlib plus pyyaml/jsonschema, expose `main(argv) -> int`, support `--help`, and support `--json` where they emit results.

- **ocl_lint.py** `[FILE|-] [--json]`
  - Emits findings as `{rule, severity, col, message, fix}`. Exits 1 if any finding is an error.
  - Rules:

    | Rule | Severity | Triggers on |
    |---|---|---|
    | OCL001 | error | Unquoted multi-word field (known map field, or `Word Word` before an operator) |
    | OCL002 | error | String-typed numeric field compared with an unquoted number. Fix: `'4625'` |
    | OCL003 | warning | Number-typed field compared with a quoted number |
    | OCL004 | error | Time filter in the query text (`Time >`, `Time between`, `dateRelative(`). Message: set the window outside the query |
    | OCL005 | warning | Leading-wildcard `'Original Log Content' like` with no earlier indexed filter |
    | OCL006 | error | Unbalanced quotes or parentheses |
    | OCL007 | warning | `%` used in `like` (OCL uses `*`) |
    | OCL008 | error | Empty pipeline stage (`\|\|` or a trailing `\|`) |
    | OCL009 | error | Backtick, `;`, or control character |

  - Also exports `sanitize_for_mcp(q) -> str`:
    - collapses newlines and tabs to single spaces, then strips;
    - raises `ValueError(reason)` on `;`, backticks, control characters, length over 8000, or any OCL006 error.
- **sigma_to_ocl.py** `RULE.yml [--json]`
  - Outputs `{query, log_sources, requires_aggregation, mitre_attack, falsepositives, level, warnings}` with stable key order and selection fields in YAML order.
  - Modifier mapping:

    | Sigma | OCL |
    |---|---|
    | (none) | `=` |
    | `\|contains` | `like '*v*'` |
    | `\|startswith` | `like 'v*'` |
    | `\|endswith` | `like '*v'` |
    | `\|re` | `matches 'v'` |
    | `\|contains\|all` | AND of `like` terms |
    | list value with `=` | `in (...)` |
    | list value with `like` | OR of `like` terms |

  - Supported conditions: `X`, `a and b`, `a or b`, `a and not b`, `1 of sel*`, `all of them`. Anything else raises `UnsupportedSigma`.
  - Keyword-list selections become `('Original Log Content' like '*v*')`.
  - `count() [by F] > N` with `timeframe` adds `| stats count as Count by 'F' | where Count > N`, sets `requires_aggregation: true`, and adds the warning "timeframe → schedule interval".
  - Logsource becomes an OR of `'Log Source' = '...'`. An unmapped logsource produces `'<LOG_SOURCE>'` plus a warning.
  - Unknown fields are quoted as-is and produce a warning.
  - Values are quoted by type, and `'` is escaped as `''`.
  - The final query must pass `ocl_lint` with zero errors. Otherwise the script raises.
- **catalog_query.py** `"<question>" [--top 3] [--json] [--list] [--validate]`
  - Lowercases and tokenizes the question, then expands synonyms:
    - `trace`, `span`, `latency`, `slow` → traces
    - `alarm`, `threshold`, `cpu` → metrics
    - `sql`, `awr`, `ash` → sql
    - `siem`, `detection` → logs
    - `prometheus`, `agent` → agents
  - Scores each service: keywords ×3, useCases token overlap ×2, signals ×1.
  - Sorts by score descending, then id.
  - Prints `{id, name, score, skill, doc, why}`.
  - `--validate` checks the catalog against the schema.
- **redaction_check.py** `[PATHS...] [--staged]`
  - Walks text files, skipping `.git`, binaries, and `.redaction-allow` entries.
  - Prints `path:line:RULE`. Exits 1 on any finding.
  - Rules are listed in section 8.
- **build_chatgpt.py** `[--check]`
  - Bundle registration is owned by `BUNDLES` in `scripts/build_chatgpt.py`; each output includes its source skill and linked references. The service catalog is copied to `chatgpt/knowledge/services.json`.
  - Renders GEMINI.md from AGENTS.md: same body, Gemini-specific install line.
  - `--check` exits 1 on stale outputs, obsolete Markdown bundles, duplicate registrations, or a mismatch between registered bundles and source skills. Generation removes obsolete Markdown bundles.
- **gen_oracle_docs.py** `[--check]`: renders `references/oracle-docs.md` from the catalog, grouped by service.
- **install.sh**: bash 3.2-compatible, `set -euo pipefail`, shellcheck-clean.
  - Usage: `install.sh [--dry-run] [--uninstall] [--list] [claude|codex|gemini|antigravity ...]`.
  - With no harness named, it installs only into harnesses whose home directory exists (`~/.claude`, `~/.codex`, `~/.gemini`, `~/.antigravity`).
  - Targets, each overridable by an env var:

    | Harness | Env var | Default |
    |---|---|---|
    | Claude | `CLAUDE_SKILLS_DIR` | `~/.claude/skills` |
    | Codex | `CODEX_SKILLS_DIR` | `~/.codex/skills`, or `~/.agents/skills` if that exists |
    | Antigravity | `AGY_SKILLS_DIR` | `~/.antigravity/skills` |
    | Gemini | `GEMINI_EXT_DIR` | `~/.gemini/extensions/oci-observability-tools` |

  - Skills-dir harnesses (claude, codex, antigravity):
    - Copy the bundle to `<target>/oci-observability-tools/`, containing `skills/`, `references/`, `catalog/`, `scripts/`, and `AGENTS.md`.
    - Then create a symlink `<target>/<skill-name>` → `<target>/oci-observability-tools/skills/<skill-name>` for each skill, so `../../references` links resolve.
  - Gemini: copy `gemini-extension.json`, `GEMINI.md`, and the same bundle dirs into the extension dir.
  - Each install writes `<target>/.oci-observability-tools.manifest` listing created paths. `--uninstall` removes only those paths.
  - It never overwrites a path it did not create: it warns and skips.
  - `--dry-run` prints `WOULD copy|link SRC -> DST` and touches nothing.
  - Exits 2 on an unknown harness. All paths derive from `$HOME`.

## 6. Harness adapters

- **Claude Code**
  - `.claude-plugin/plugin.json`: `{name: "oci-observability-tools", description (+disclaimer), version: "0.1.0", author{name,url}, homepage, repository, license: "Apache-2.0", keywords}`.
  - `marketplace.json`: `{$schema: "https://anthropic.com/claude-code/marketplace.schema.json", name, owner, plugins: [{name, description, version, source: "./", category: "observability"}]}`.
  - See `README.md` for the current marketplace installation instructions.
- **Codex**
  - `.codex-plugin/plugin.json` has the same identity fields plus `"skills": "skills/"`.
  - AGENTS.md contains the disclaimer, a skill index (name → when to use), the routing rule ("start with oci-om-router when unsure"), the safety rules (section 8, item 9), and copy-paste helper commands.
- **Gemini CLI / Antigravity**
  - `gemini-extension.json` plus GEMINI.md (generated, heading parity with AGENTS.md).
  - Antigravity loads the skills dirs installed by install.sh.
- **ChatGPT**
  - `instructions.md` contains:
    - role and disclaimer;
    - "cite docs.oracle.com URLs only from knowledge files";
    - "never invent OCIDs or endpoints; use `<PLACEHOLDER>`s";
    - the OCL typing rules inline;
    - "redact OCIDs, IPs, and emails from pasted output before analysis; never ask for credentials".
  - Users upload `knowledge/*` as GPT knowledge.
  - `apps-sdk-notes.md` sketches future Apps SDK tools for `catalog_query` and `ocl_lint` (out of scope for v1).

## 7. Test strategy (pytest, offline only)

`tests/test_packaging.py` builds actual sdist/wheel and editable artifacts, checks tools/assets and
runtime dependency metadata, excludes private recovery files, and runs installed helpers and
generator freshness outside the source tree. `tests/test_chatgpt_bundle.py` compares emitted names,
complete source bodies, and linked references against every source skill, and verifies deterministic
regeneration and rejection of unregistered skills and obsolete generated bundles.

| File | Asserts |
|---|---|
| test_frontmatter.py | Every skill starts with a `---` YAML block. Keys ⊆ {name, description, license}. `name` equals the dir name. Description length and "Use when" checks pass. Required sections appear in order. Every `../../references/*.md` link exists. |
| test_skill_size.py | Each SKILL.md is under 500 lines. AGENTS.md and GEMINI.md are under 150 lines. `chatgpt/instructions.md` is under 8000 chars. |
| test_doc_urls.py | Collects all URLs in skills/, references/, chatgpt/, README, AGENTS.md, GEMINI.md. Allowed hosts are only docs.oracle.com, www.oracle.com, opentelemetry.io, github.com/SigmaHQ, and this repo's GitHub URL. Every docs.oracle.com or oracle.com URL is registered in catalog `docs`. Each skill's `## Official docs` URLs come from services it owns, or from any service in the router's case. `oracle-docs.md` matches `gen_oracle_docs.py --check`. |
| test_catalog_schema.py | Both catalogs validate against their schemas. All 12 ids are present and unique. Doc keys are unique per service. `skill` dirs exist. `relatedServices` resolve. `pricingNote` contains no currency amount (regex `[$€£]\s?\d\|\d+(\.\d+)?\s?(USD\|EUR)`). |
| test_redaction.py | The whole repo has 0 findings. `leaky.txt` triggers every rule. `clean.txt` triggers none. It contains 192.0.2.10, 198.51.100.7, 203.0.113.9, 127.0.0.1, 2001:db8::1, `user@example.com`, and `<TENANCY_OCID>`. |
| test_sigma_to_ocl.py | Golden JSON for each fixture: EventID → `'Event ID' = '4688'`; each modifier; list → `in`; `and not`; `1 of sel*`; keyword fallback; count/timeframe tail with `requires_aggregation`; unmapped logsource warning; unknown field warning; `O'Brien` → `'O''Brien'`; unsupported condition raises; two runs are byte-identical; every output passes lint. |
| test_ocl_lint.py | Each rule OCL001-009 has at least one failing and one passing fixture. Every ```` ```ocl ```` block in `ocl-cookbook.md` and in the skills lints clean. `sanitize_for_mcp` cases pass. |
| test_catalog_query.py | "slow API traces" → apm is #1. "cpu alarm" → monitoring is #1. "AWR SQL regression" → database-management or operations-insights is in the top 2. "route audit logs to SIEM" → service-connector-hub or log-analytics is in the top 2. "prometheus scrape" → management-agent is in the top 2. Ordering is deterministic. |
| test_install_dryrun.py | `HOME=tmp_path bash install.sh --dry-run claude codex gemini antigravity` exits 0, prints WOULD lines, and creates no files. An unknown harness exits 2. A real install followed by `--uninstall` restores the tmp tree snapshot. Skips if bash is absent. |
| test_chatgpt_bundle.py | `build_chatgpt.py --check` passes. The disclaimer is in `instructions.md`. AGENTS.md and GEMINI.md have heading parity. |
| test_manifests.py | All three manifests plus `gemini-extension.json` parse. name, version, and license agree with each other and with pyproject. Every description contains "Not an Oracle product". |

**CI** (`.github/workflows/ci.yml`):
- Runs on push and pull_request, with `permissions: contents: read` and no secrets.
- Matrix: ubuntu-latest and macos-latest, Python 3.10 and 3.12.
- Steps:
  1. checkout with `fetch-depth: 0`
  2. setup-python
  3. `pip install -e .[dev]`
  4. `ruff check .` plus both generators with `--check`
  5. `shellcheck install.sh` (ubuntu only)
  6. `python scripts/redaction_check.py .`
  7. `pytest -q`
  8. `gitleaks/gitleaks-action` over full history (ubuntu only)

## 8. Security and redaction rules

1. **OCIDs:** `ocid1\.[a-z0-9]+\.oc[0-9]+\.[a-z0-9-]*\.[a-z0-9]{8,}` is forbidden. Use placeholders such as `<TENANCY_OCID>`, `<COMPARTMENT_OCID>`, `<LOG_GROUP_OCID>`, `<APM_DOMAIN_OCID>`.
2. **IPv4/IPv6:** the check parses candidates with `ipaddress`. Allowed ranges:
   - 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 (RFC 5737)
   - 127.0.0.0/8 and 0.0.0.0
   - 2001:db8::/32 and ::1

   Ignore dotted version strings preceded by `v` or followed by `-`.
3. **Emails:** only `@example.(com|org|net)` addresses are allowed.
4. **Secrets:**
   - PEM `-----BEGIN [A-Z ]*PRIVATE KEY-----`
   - `AKIA[0-9A-Z]{16}`
   - `ghp_[A-Za-z0-9]{36}`
   - `xox[bp]-`
   - key fingerprints `([0-9a-f]{2}:){15}[0-9a-f]{2}`
   - `(password|token|datakey|secret)\s*[=:]\s*['"]?[^<\s'"]{8,}`, where values that start with `<` count as placeholders
5. **Internal topology:**
   - No internal hostnames (`oraclecorp[.]com`, `us[.]oracle[.]com`, `internal` suffixes). `localhost` is allowed.
   - No personal paths (`/Users/<x>/`, `/home/<x>/`; use `~`).
   - No real APM or ingestion endpoints. Use `<APM_DOMAIN_UPLOAD_ENDPOINT>`.
   - No Object Storage namespaces in URLs. Use `<NAMESPACE>`.
6. **Examples are synthetic:**
   - Events use placeholder OCIDs and RFC 5737 IPs.
   - Sigma rules are self-authored. Link to SigmaHQ, never vendor its rules.
7. **Allowlist:** every `.redaction-allow` line needs a `# reason` comment, and a test enforces this. The file starts empty.
8. **Gates:**
   - The pre-commit local hook runs `redaction_check.py --staged` plus gitleaks. CI repeats both.
   - CONTRIBUTING documents the leak response: stop, do not push a "fix" commit, rewrite history with `git filter-repo --replace-text`, then push.
9. **Assistant behavior** (text in AGENTS.md, GEMINI.md, and instructions.md):
   - Never request credentials.
   - Redact identifiers in pasted output before reasoning about it.
   - Default to read-only commands.
   - Mark mutating examples `# MUTATES`.
   - Pair every command with its doc URL.
10. **MCP safety** (`references/mcp-safety.md`):
    - Run queries through `sanitize_for_mcp` before calling `execute_query`-style tools.
    - Pass time range, compartment, and subtree as separate structured arguments, never concatenated into the query.
    - Cap the row count.
    - Never paste raw results that contain identifiers into public artifacts.
11. **Local demos** (`references/portable-deploy.md`, guidance only):
    - Bind to 127.0.0.1.
    - Probe with `nc -z 127.0.0.1 $port`.
    - On collision, increment the port, up to +20.
    - Print the chosen port.
    - No deploy script ships.

## 9. Ordered implementation tasks

- **T1** Scaffold: LICENSE, NOTICE, README skeleton with disclaimer, SECURITY, CONTRIBUTING, CHANGELOG, .gitignore, pyproject, Makefile, empty `.redaction-allow`.
- **T2** `redaction_check.py`, `test_redaction.py`, fixtures, pre-commit and gitleaks config. The gate comes first so every later commit is checked.
- **T3** `services.schema.json` and `services.json` (12 services, verified URLs from section 3), plus `test_catalog_schema.py`.
- **T4** `catalog_query.py` and `test_catalog_query.py`.
- **T5** `sigma_field_map.json` and its schema; `ocl-field-typing.md`; `sigma-field-map.md`.
- **T6** `ocl_lint.py` (including `sanitize_for_mcp`), `test_ocl_lint.py`, fixtures, `ocl-cookbook.md` (25 generic queries covering Windows, Linux, OCI Audit, VCN flow logs, and OKE).
- **T7** `sigma_to_ocl.py`, `examples/sigma/*.yml`, golden files, `test_sigma_to_ocl.py`.
- **T8** Skills 1-2 (router, OCL), then `test_frontmatter.py` and `test_skill_size.py`.
- **T9** Skills 3-11 and the remaining references: mql-cookbook, otel-to-apm, pipelines-patterns, mcp-safety, maturity-l0-l4, portable-deploy. Plus `examples/cloudevents/*.json`.
- **T10** `gen_oracle_docs.py`, `oracle-docs.md`, `test_doc_urls.py`.
- **T11** Manifests (Claude, Codex, Gemini), AGENTS.md, CLAUDE.md, `test_manifests.py`.
- **T12** `build_chatgpt.py`, GEMINI.md generation, chatgpt/ files, generated knowledge, `test_chatgpt_bundle.py`.
- **T13** `install.sh` and `test_install_dryrun.py`; shellcheck-clean.
- **T14** CI workflow and PR template (checklist: redaction, catalog URLs, under 500 lines). Require local `make check` success and separate CI matrix evidence; an offline Linux pass does not establish macOS acceptance.
- **T15** Final README with per-harness install, skill table, `catalog_query` demo, and maturity map. Run `make linkcheck` (online, manual). Run gitleaks over the full history.
- **T16** Manual smoke test in each harness with the prompt "Which OCI service should I use to trace a slow API?". The answer must route to APM and cite APMOTEL. Record real loaded-agent results separately from offline asset checks before any authorized v0.1.0 tag. Live harness smoke and release publication remain pending; the packaging repair does not authorize them, and AGY runtime is excluded. Repo visibility switches to public only after explicit owner approval.

## 10. Acceptance criteria

- [ ] The tree matches section 2, and generated files are fresh (`--check` passes).
- [ ] 11 skills, each with valid frontmatter, required sections, under 500 lines, and Official-docs URLs that are all registered in the catalog.
- [ ] `services.json` validates, has 12 services, and every URL is on docs.oracle.com or oracle.com. `make linkcheck` returns 200 for all of them.
- [ ] The four helpers run offline with `--help`, are unit-tested, and Sigma output is deterministic and lint-clean.
- [ ] `pytest -q` passes offline on macOS and Ubuntu with Python 3.10 and 3.12. ruff and shellcheck are clean, and CI is green.
- [ ] `redaction_check.py .` and gitleaks report zero findings, including full history.
- [ ] `install.sh --dry-run` writes nothing. Install and uninstall into a temp HOME is reversible for all four harnesses.
- [ ] The disclaimer and Apache-2.0 license are consistent across README, NOTICE, manifests, AGENTS.md, GEMINI.md, and chatgpt/instructions.md.
- [ ] The T16 smoke test passes in Claude Code, Codex, Gemini CLI/Antigravity, and ChatGPT.
- [ ] No OCIDs, non-documentation IPs, real emails, internal hostnames, personal paths, or secrets anywhere in the repo or its history.
