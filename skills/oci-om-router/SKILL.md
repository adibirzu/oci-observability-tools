---
name: oci-om-router
description: Capability catalog and router for OCI Observability & Management. Use when a user asks which OCI service fits a monitoring, logging, tracing, database, alerting, or security-analytics job, or compares OCI O&M with other clouds.
license: Apache-2.0
---
# OCI O&M router

## When to use

Start here when the service choice is unclear, the question crosses signal types, or a user wants a cross-cloud conceptual mapping. Run `python scripts/catalog_query.py "<QUESTION>" --top 3` for reproducible ranking.

## Key concepts

| Job | OCI service |
|---|---|
| Metrics | Monitoring |
| Raw logs | Logging |
| Log search, parsing, ML, SIEM-like analysis | Log Analytics |
| Traces, RUM, synthetic monitoring | APM |
| Application-stack topology | Stack Monitoring |
| Database performance | Database Management |
| Capacity and SQL insights | Operations Insights |
| Agent-based collection | Management Agent |
| Routing and fan-out | Events, Connector Hub, Streaming, Notifications |

Conceptual equivalents are not exact product parity: CloudWatch metrics and logs span Monitoring, Logging, and Log Analytics; Azure Monitor and Log Analytics cover similar signals; Google Cloud Monitoring and Logging map by signal. Validate features rather than translating names literally.

## Workflow

1. Identify the signal, workload, required action, and maturity level.
2. Rank catalog services and open the owning skill.
3. Check interlocks: collection, routing, storage, query, alert, and notification.
4. Cite the official page for the recommended capability.
5. Use the [capability answer guide](../../references/capability-answers.md): explain service boundaries, prerequisites, a bounded next step, validation, and evidence status. Keep the answer proportional to the question.

## Pitfalls

Do not route every log question to Log Analytics: use Logging for collection and simple access. Do not use APM for host topology or Operations Insights for live incident triage. Never infer current limits or prices.

Catalog scores are keyword matches, not confidence or proof of capability. For multi-signal questions, route each job separately. A zero-score result is not a recommendation. Verify version-sensitive capabilities against current official documentation when browsing is available; otherwise label them as unverified against current docs. Installed skills do not establish tenancy access or prove telemetry collection.

## Examples

“Trace a slow API” routes to APM and `oci-apm-otel`. “Route audit logs to a SIEM-like search” combines Logging, Connector Hub, and Log Analytics. “Forecast database capacity” routes to Operations Insights.

## Official docs

- [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [APM](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Stack Monitoring](https://docs.oracle.com/en-us/iaas/stack-monitoring/home.htm)
- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [Management Agent](https://docs.oracle.com/en-us/iaas/management-agents/home.htm)
- [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm)
- [Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm)
- [Connector Hub](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)
- [Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)

## Related skills

Continue with the signal-specific skill selected by the catalog, or use `oci-om-maturity` for a roadmap.
