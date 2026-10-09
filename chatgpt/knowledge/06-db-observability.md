---
name: oci-db-observability
description: Use OCI Database Management and Operations Insights for Oracle Database performance, fleet health, SQL analysis, and capacity planning. Use when diagnosing database performance or forecasting capacity.
license: Apache-2.0
---
# OCI Database Observability

## When to use

Use when diagnosing active database performance incidents, investigating SQL plan regressions, reviewing Active Session History (ASH) and AWR snapshots, analyzing database fleet health, or forecasting long-term CPU, storage, and I/O capacity requirements.

## Key concepts

OCI provides two complementary services for database observability:

### Database Management (DBM)
Focused on real-time operational diagnostics, performance tuning, and fleet administration:
- **Service Tiers**:
  - *Basic Management*: High-level metrics, fleet overview, and basic Performance Hub (included with Oracle Cloud databases).
  - *Full Management*: Advanced Performance Hub, interactive ASH analytics, AWR explorer, SQL tuning sets, and database jobs.
- **Enablement Prerequisites**: Connectivity established via OCI Private Endpoint (for databases in private subnets) or Management Agent (for on-premise and external databases), plus monitoring database credentials.
- **Performance Hub**: Correlates ASH session load, wait events (`User I/O`, `CPU`, `Concurrency`, `Commit`), and historical AWR metrics over unified time windows.

### Operations Insights (OPSI)
Focused on historical analytics, cross-fleet patterns, and predictive machine learning:
- **SQL Insights**: Fleet-wide SQL inventory, execution degradation detection, plan change classification, and outlier detection across months of history.
- **Capacity Planning**: Predictive forecasting (30 to 365 days) for database CPU, memory, storage, and I/O utilization with linear and seasonal trend projection.

### Decision Matrix: DBM vs. OPSI
- Choose **Database Management** for real-time incident triage, active wait state diagnosis, blocking session resolution, and short-term performance troubleshooting.
- Choose **Operations Insights** for quarterly capacity forecasting, fleet-wide SQL plan regression analysis, and resource exhaustion prediction.

## Workflow

1. Classify the inquiry as active operational troubleshooting (DBM) or analytical fleet trend/capacity forecasting (OPSI).
2. Verify database enablement prerequisites (private endpoint security lists, agent status, and monitoring user privileges).
3. For active degradation: open Performance Hub in Database Management, evaluate average active sessions against CPU thread count, and isolate top wait classes.
4. Drill down from wait classes into specific SQL IDs, plan hash values, and blocking session trees.
5. For capacity planning: navigate to Operations Insights, inspect fleet utilization trends, and review projected exhaustion dates for storage and compute.

## Pitfalls

- Diagnosing symptoms instead of root causes: a high-CPU SQL statement may be waiting on lock contention or unindexed lookups caused by another transaction.
- Network port blocking: forgetting to allow ingress on database listener port 1521 from the private endpoint subnet prevents metric collection.
- Mismatched time ranges: when correlating application APM traces with database ASH, ensure time windows and time zones match precisely.
- Insufficient AWR history: standard database AWR retention is typically 8 days; use Operations Insights for extended historical retention (up to 25 months).

## Examples

```text
# Performance Hub triage sequence
1. Check Average Active Sessions (AAS) against CPU cores.
2. Filter ASH by Wait Class = "User I/O" or "Concurrency".
3. Identify top SQL ID contributing to wait events.
4. Review Execution Plan hash history for recent plan changes.
```

```text
# Decision Rule:
# If investigating current latency spike -> Database Management Performance Hub
# If forecasting storage growth for next 6 months -> Operations Insights Capacity Planning
```

## Official docs

- [Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [Performance Hub](https://docs.oracle.com/en-us/iaas/database-management/doc/performance-hub.html)
- [Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [Capacity planning](https://docs.oracle.com/en-us/iaas/operations-insights/doc/capacity-planning.html)

## Related skills

Use `oci-stack-monitoring-agents` for host and agent health, `oci-monitoring-mql` for metric-based alerts, and `oci-om-maturity` for database observability roadmaps.
