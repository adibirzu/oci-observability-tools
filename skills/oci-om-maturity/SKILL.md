---
name: oci-om-maturity
description: Assess and plan observability maturity on OCI from L0 to L4. Use when designing an observability roadmap, onboarding a workload, or reviewing coverage gaps.
license: Apache-2.0
---
# OCI Observability Maturity Model

## When to use

Use when conducting an observability architecture review, designing an observability adoption roadmap on OCI, benchmarking operational maturity from foundational logging up to autonomous AIOps, or auditing signal coverage gaps.

## Key concepts

The OCI Observability Maturity Model defines five sequential capability tiers:

| Level | Maturity Tier | Core Focus & OCI Services |
|---|---|---|
| **L0** | Foundations | Audit logging, tenancy hierarchy, service logs, retention policies (Logging, IAM) |
| **L1** | Service Health & Alarms | Golden signals, MQL threshold/absence alarms, notification routing (Monitoring, Notifications) |
| **L2** | Analytics & Database Depth | OCL search, custom log parsers, ASH/AWR, capacity forecasting (Log Analytics, DBM, OPSI, SCH) |
| **L3** | User Experience & SLOs | Distributed tracing, OTel collection, synthetic checks, RUM, SLOs (APM, Synthetics) |
| **L4** | AIOps & Agent Observability | Closed-loop remediation, safe AI assistant tooling, autonomous evaluation (O&M Suite) |

### Governance and Operational Interlocks
Maturity is measured not merely by tool installation, but by operational interlocks:
- **Ownership**: Every log group, metric alarm, and dashboard has designated team owners.
- **Actionability**: Every alarm links to an executable runbook with tested notification channels.
- **Feedback Loop**: Incidents trigger review of missing telemetry and threshold tuning.

### Closed-Loop AIOps and Agent Safety
Level 4 introduces autonomous operations following the closed loop:
`Instrument -> Collect -> Analyse -> Evaluate -> Act`
AI coding agents and operational assistants querying OCI must enforce the [MCP Safety Pattern](../../references/mcp-safety.md):
- Sanitizing all query strings before execution.
- Passing time windows, compartment IDs, and row limits as separate structured parameters.
- Restricting assistant privileges to read-only operations unless explicit human approval is granted.

For complete level definitions and checklists, see the [Observability Maturity L0-L4 Reference](../../references/maturity-l0-l4.md).

## Workflow

1. Inventory existing workload telemetry across compute, storage, databases, and microservices.
2. Evaluate current state against the L0 through L4 criteria; require verifiable evidence before awarding a tier level.
3. Identify the highest-priority gap that minimizes operational risk or accelerates mean time to resolution (MTTR).
4. Formulate an actionable remediation plan specifying target services, owner, and deadline.
5. Implement required telemetry pipelines, alarm configurations, and dashboards.
6. Re-evaluate maturity score quarterly and following major service architecture changes.

## Pitfalls

- Deploying tools without operational ownership: enabling APM or Log Analytics without alert response runbooks does not achieve L2 or L3 maturity.
- Jumping tiers prematurely: attempting distributed tracing (L3) without reliable logging foundations (L0) and golden-signal alarms (L1) results in unmanaged alert fatigue.
- Unsanitized automated queries: allowing AI agents or scripts to run unbounded, unindexed log searches inflates costs and degrades analytics performance.
- Stale synthetic tests: failing to update synthetic monitor scripts alongside UI/API deployments causes false-positive alerts.

## Examples

```text
# Maturity Progression Assessment:
# Current: Workload publishes metrics to OCI Monitoring and alerts to Slack -> Tier L1
# Next Objective: Ingest application logs into Log Analytics with automated OCL parsers -> Elevate to Tier L2
```

## Official docs

- [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [APM](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [Connector Hub](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)

## Related skills

Start with `oci-om-router` to map requirements to services, then apply domain-specific skills for implementation.
