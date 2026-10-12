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
