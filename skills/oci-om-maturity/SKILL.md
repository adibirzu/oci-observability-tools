---
name: oci-om-maturity
description: Assess and plan observability maturity on OCI from L0 to L4. Use when designing an observability roadmap, onboarding a workload, or reviewing coverage gaps.
license: Apache-2.0
---
# OCI observability maturity

## When to use

Use to assess a workload, sequence an observability roadmap, or find missing signal and governance interlocks.

## Key concepts

| Level | Focus |
|---|---|
| L0 | Foundations: audit, logging, compartments, tags |
| L1 | Service metrics and alarms |
| L2 | Log analytics and database depth |
| L3 | Tracing, RUM, synthetic monitoring, SLOs |
| L4 | AIOps and AI-agent observability: instrument → collect → analyse → evaluate → act |

Each level needs services plus ownership, retention, routing, access, quality, and response interlocks. See [the L0-L4 checklist](../../references/maturity-l0-l4.md) and [MCP safety](../../references/mcp-safety.md).

## Workflow

1. Inventory workloads, owners, critical user journeys, and current signals.
2. Score each level only when its evidence and interlocks exist.
3. Select the smallest next-level gap that reduces operational risk.
4. Define success measures, owner, deadline, and validation exercise.
5. Reassess after incidents and architecture changes.

## Pitfalls

Tool deployment alone is not maturity. Do not skip signal ownership, alert response, data quality, or SLO validation. Agent-driven queries remain read-only by default and must sanitize query text and structure scope separately.

## Examples

A workload with logs but no actionable alarms remains below L1. Traces without service naming, log correlation, and user-journey SLOs do not establish L3.

## Official docs

- [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [APM](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [Connector Hub](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)

## Related skills

Start with `oci-om-router`, then use each level's signal-specific skills.
