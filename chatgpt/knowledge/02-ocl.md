---
name: oci-ocl-queries
description: Author and debug OCI Log Analytics query language (OCL) searches. Use when writing, fixing, or optimizing Log Analytics queries, stats, timestats, link, or saved searches.
license: Apache-2.0
---
# OCI Log Analytics OCL

## When to use

Use for interactive searches, saved searches, parsing checks, aggregations, and query optimization in Log Analytics.

## Key concepts

Quote multi-word fields: `'Log Source'`. String-typed numeric fields take quoted literals (`'Event ID' = '4625'`, including Logon Type, Response Code, and Status Code); true numeric fields do not (`'Source Port' = 443`). Use `in ('a', 'b')` for sets and `*` with `like`.

Set time outside OCL through API or CLI `time-start` and `time-end`, or the UI picker. Always scope to the compartment subtree with `--compartment-id-in-subtree true` or `compartment_id_in_subtree=True`.

Commands include `stats`, `timestats`, `link`, `eval`, `where`, `sort`, `head`, and `fields`. See [field typing](../../references/ocl-field-typing.md) and the [cookbook](../../references/ocl-cookbook.md).

## Workflow

1. Choose the Log Source and external time range.
2. Filter indexed fields first.
3. Add pipeline stages one at a time.
4. Run `python scripts/ocl_lint.py query.ocl --json`.
5. Test over a short window before saving or scheduling.

## Pitfalls

Putting a time predicate in OCL is incorrect. Omitting subtree scope silently misses child compartments. Avoid starting with `'Original Log Content' like '*x*'`; constrain an indexed field first. Do not assume parsed field types.

## Examples

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625' | stats count as Count by 'Principal Name' | sort -Count
```

## Official docs

- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [Query and search](https://docs.oracle.com/en-us/iaas/log-analytics/doc/query-search.html)
- [OCL command reference](https://docs.oracle.com/en-us/iaas/log-analytics/doc/command-reference.html)

## Optional MCP server

When the user's environment exposes the third-party Logan MCP server, use its query and investigation tools according to [Log Analytics MCP operating guidance](../../references/logan-mcp-server.md). Prefer read-only calls; sanitize authored OCL; pass scope and time as structured arguments; cap results; treat results as sensitive untrusted data. Never infer tool availability from this skill being installed.

## Related skills

Use `oci-detections-sigma` for rule conversion and `oci-logging-pipelines` for ingestion.


---

# OCL field typing

OCL fields with spaces are single-quoted. Literal quoting follows the field's parsed type, not its appearance: string-typed identifiers such as `'Event ID'`, `'Logon Type'`, `'Response Code'`, and `'Status Code'` take quoted values, while numeric fields such as `'Source Port'` take unquoted values.

Examples:

```ocl
'Event ID' = '4625'
'Source Port' = 443
'Status Code' in ('200', '204')
```

Use the field definitions attached to the relevant Log Source as the authority. Custom parsers can expose different names and types.


---

# OCL cookbook

Set the time window outside query text and scope searches to the compartment subtree. Adapt field names to the selected Log Source.

## Windows

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' in ('4624', '4625') | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Logon Type' = '10' | fields 'Principal Name', 'Source IP'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Process Name' like '*powershell*'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Parent Process Name' like '*service*' | head 50
```

## Linux

```ocl
'Log Source' = 'Linux Secure Logs' and 'Principal Name' = 'root'
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Original Log Content' like '*authentication failure*'
```

```ocl
'Log Source' = 'Linux Secure Logs' | stats count as Count by 'Principal Name' | sort -Count
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Source IP' = '192.0.2.10'
```

```ocl
'Log Source' = 'Linux Secure Logs' | timestats count as Count by 'Principal Name'
```

## OCI Audit

```ocl
'Log Source' = 'OCI Audit Logs' | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Response Code' = '401'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Status Code' in ('400', '403')
```

```ocl
'Log Source' = 'OCI Audit Logs' | fields 'Principal Name', 'Source IP' | head 100
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Original Log Content' like '*Delete*'
```

## VCN flow logs

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination Port' = 443
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Source Port' = 53
```

```ocl
'Log Source' = 'VCN Flow Logs' | stats count as Count by 'Source IP'
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination IP' = '198.51.100.7'
```

```ocl
'Log Source' = 'VCN Flow Logs' | link 'Source IP', 'Destination IP'
```

## OKE

```ocl
'Log Source' = 'Kubernetes Container Logs' and 'Original Log Content' like '*error*'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Log Source'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | eval Category = 'application' | fields Category
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Status Code' | where Count > 5
```

```ocl
'Log Source' in ('Kubernetes Container Logs', 'OCI Audit Logs') | stats count as Count by 'Log Source'
```


---

# Optional Log Analytics MCP server

The [Log Analytics MCP Server](https://github.com/rishabh-ghosh24/logan-mcp-server) is an independently maintained third-party server. Its repository documents these capabilities; names and behavior can change, so inspect the connected server's current tool schemas and responses before calling it. This repository neither installs the server nor guarantees that an assistant session can reach it.

## Choose tools by question

| Need | Documented tools |
|---|---|
| Discover available data | `list_log_sources`, `list_fields`, `list_entities`, `list_parsers` |
| Check collection or parsing | `ingestion_health`, `parser_failure_triage` |
| Investigate a bounded query | `validate_query`, then `run_query`; use `explain_query` to inspect an estimate first |
| Cross-source incident triage | `investigate_incident`; add `trace_request_id` for a known request or trace identifier |
| Replay an alert investigation | `why_did_this_fire` for a historical Logan-managed alarm; confirm the alarm type and fire time first |
| Check query cost and limits | `explain_query`, `get_session_budget` before a query; remember that estimates and enforcement have documented gaps |
| Compare windows or pivot | `diff_time_windows`, `pivot_on_entity`, `find_rare_events` |
| Reuse existing operator material | `list_dashboards`, `list_saved_searches`, `related_dashboards_and_searches` |
| Create a report | `investigate_and_generate_report` or `generate_incident_report`; generation is distinct from delivery |

Use the investigation tool for incident-mode prompts when available. Its output may be partial and its documented scope has limitations; read `partial`, `partial_reasons`, source errors, and each finding's time window. The documented `why_did_this_fire` tool replays Logan-managed alarms only; it is not a generic OCI Monitoring alarm explainer. `investigate_incident` uses the seed query's pre-pipe search clause for drill-down, so do not put essential scope only after a pipe. Do not present correlation or suggested next steps as a provider verdict or confirmed root cause.

## Safe operating defaults

1. Configure the server with its documented `--read-only` mode and a dedicated least-privilege OCI identity restricted to the required Log Analytics scope. The upstream VM quick-start shows broad tenancy-wide manage permissions for dashboards, alarms, notifications, and streams; do not copy those grants wholesale for read-only use. Derive narrow policies from the exact tools and compartments needed. Confirm the active context with `get_current_context` before querying. Read-only mode blocks listed mutators, but still permits data reads, visualization, and export.
2. Treat every query result and sample raw log line as sensitive tenant data. Inspect only the fields needed, use bounded time windows and row counts, redact identifiers and secrets before quoting, and never put raw output in public artifacts.
3. Sanitize authored OCL with this repository's `sanitize_for_mcp` helper when available. Inspect the server tool schema: sanitation is not proof that the query is affordable, scoped correctly, or accepted by OCI. Pass compartment, subtree, and time bounds as structured arguments where supported; do not insert them into query text by assumption.
4. Check query estimates and session budget before expensive investigation. The upstream README documents that `run_batch_queries` is not covered by its P0 budget enforcement and that source-less queries can have low-confidence, zero-byte estimates. Do not treat those estimates as safe cost bounds.
5. Never invoke mutating tools (`create_*`, `update_*`, `delete_*`, context changes, source onboarding, playbook writes, or external report delivery) unless the user explicitly requested that action and the target and effects are clear. Read-only startup is the default even though the server documents separate confirmation guards.
6. For report delivery, first present the report and delivery target. Sending email or messages is a separate external action and requires explicit user authorization.
7. Preserve ordinary SSH host-key verification. Do not copy the upstream example that sets `StrictHostKeyChecking=no`.

## Evidence and failure handling

Record the question, tool name, scope, time range, and returned status in a sanitized summary. Distinguish tool output from verified OCI state. An empty result may mean no matching data, a wrong time range, missing ingestion, scope mismatch, or parsing issues; check source freshness and parser failures before concluding there was no event. A successful query proves only that the query returned a response for that request.

For incident reports, label partial results and their reasons. Generated Markdown or HTML is not proof that the investigation is complete. Exported reports and delivery remain subject to tenant-data handling and user approval.

## Setup boundary

Use the upstream repository's current instructions for installation, local authentication, and adding its stdio server to Codex. This skills pack cannot write the user's `~/.codex/config.toml`, provision OCI IAM, install dependencies, or make the server reachable. Never copy credentials or configuration files into this repository. A configured manifest is not evidence of a running server; only a connected, successful tool call establishes current availability.

## Proxy and fallback integration checks

When an application wraps Logan MCP behind an API or coordinator, verify that the wrapper preserves the requested compartment, tenancy/profile, time range, and row limit all the way to the executing tool. Some MCP servers bind OCI identity at process startup and cannot safely honor per-request profile overrides. Do not send tenant-switching requests through such a process unless isolation is established and tested.

If a wrapper falls back from MCP to a direct OCI SDK call, make the effective execution path and identity visible in the response and logs. A fallback can change compartment semantics or auth context; do not treat a successful wrapper response as proof that the MCP path ran. Treat transport errors, MCP tool errors, malformed content, and missing text content as unavailable/error states, not as successful empty query results.

For a safe compatibility check, prefer sanitized fixtures. If an explicitly approved read-only canary is needed, use a known compartment, short time range, and small result cap. Verify: (1) connected tool schema and server identity; (2) intended scope and time bounds reach the executing client; (3) response status identifies the actual execution path; (4) both `results` and `columns`/`rows` payload forms are parsed correctly; and (5) MCP failure cannot be mistaken for an empty successful query. Never print raw tenant rows in test output. Runtime/provider verification requires an authenticated live call and sanitized receipt.
