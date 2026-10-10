# OCI Observability Tools

Independent community project. Not an Oracle product, not endorsed or supported by Oracle. "Oracle", "OCI", and related marks are trademarks of Oracle and/or its affiliates. Always verify against the official documentation at docs.oracle.com; service capabilities, limits, and pricing change.

Install for Gemini CLI: `./install.sh gemini`; for Antigravity: `./install.sh antigravity`.

## Routing

Start with `oci-om-router` when the service or signal is unclear. Then load only the specific skill and directly linked references needed for the task.

## Skill index

| Skill | Use when |
|---|---|
| `oci-om-router` | Selecting an O&M service or translating a cross-cloud job |
| `oci-ocl-queries` | Writing or debugging Log Analytics OCL |
| `oci-apm-otel` | Instrumenting traces, RUM, or synthetics |
| `oci-apm-tracing` | Distributed tracing, Trace Explorer queries, and synthetic monitors |
| `oci-monitoring-alarms` | Writing MQL, custom metrics, alarms, or notifications |
| `oci-monitoring-mql` | Advanced MQL queries, split-metric alarms, and absence triggers |
| `oci-logging-pipelines` | Collecting and routing logs, events, and streams |
| `oci-db-observability` | Diagnosing database performance or planning capacity |
| `oci-stack-monitoring-agents` | Managing agents, discovery, topology, or Prometheus |
| `oci-detections-sigma` | Converting Sigma detections to OCL |
| `oci-om-maturity` | Assessing an L0–L4 roadmap |

## Safety rules

- Never request credentials.
- Redact identifiers in pasted output before reasoning about it.
- Default to read-only commands.
- Mark every mutating example `# MUTATES`.
- Pair every command with its official docs.oracle.com URL.
- Use placeholders for identifiers, keys, namespaces, and endpoints.
- Keep time, compartment, subtree, and row limits as structured query arguments.
- Run OCL through `sanitize_for_mcp` before an MCP query tool.
- Do not place raw tenant output in public artifacts.

## Offline helpers

```sh
python scripts/catalog_query.py "slow API traces" --top 3
python scripts/ocl_lint.py query.ocl --json
python scripts/sigma_to_ocl.py rule.yml --json
python scripts/redaction_check.py .
```

The helpers do not contact OCI. Skills may show OCI CLI command shapes using placeholders; apply the safety rules and cite the associated official documentation.

## Development pointers

See `pyproject.toml` for explicit installed-package and asset configuration, and run `make check`
for the complete offline gates. `tests/test_packaging.py` checks built and installed artifacts;
`tests/test_chatgpt_bundle.py` checks every source skill against generated upload content.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
