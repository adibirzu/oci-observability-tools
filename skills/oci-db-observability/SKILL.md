---
name: oci-db-observability
description: Use OCI Database Management and Operations Insights for Oracle Database performance, fleet health, SQL analysis, and capacity planning. Use when diagnosing database performance or forecasting capacity.
license: Apache-2.0
---
# OCI database observability

## When to use

Use for database performance incidents, fleet health, SQL analysis, and resource-capacity forecasts.

## Key concepts

Database Management basic and full capabilities differ; verify the current feature matrix and enablement prerequisites. Managed databases may connect through a Management Agent or private endpoint. Performance Hub exposes active session history (ASH) and automatic workload repository (AWR) concepts for time-correlated diagnosis.

Operations Insights adds SQL Insights and longer-horizon capacity analysis. Choose Database Management for operational diagnosis and fleet administration; choose Operations Insights for cross-fleet trends and forecasting.

## Workflow

1. Classify the question as current performance, historical SQL, fleet health, or forecast.
2. Confirm database type, management mode, agent/private-endpoint path, and permissions.
3. Correlate load, waits, sessions, and SQL over the same window.
4. Use Operations Insights for trend and capacity questions.

## Pitfalls

A high-load SQL statement may be a symptom rather than a cause. Do not compare mismatched time windows. AWR and ASH availability depends on database configuration and entitlements; verify current documentation.

## Examples

For a recent latency spike, begin in Performance Hub and correlate ASH waits with SQL. For a quarterly storage forecast, use Operations Insights capacity planning.

## Official docs

- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [Performance Hub](https://docs.oracle.com/en-us/iaas/database-management/doc/performance-hub.html)
- [Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [Capacity planning](https://docs.oracle.com/en-us/iaas/operations-insights/doc/capacity-planning.html)

## Related skills

Use `oci-stack-monitoring-agents` for agent health and `oci-om-maturity` for coverage planning.
