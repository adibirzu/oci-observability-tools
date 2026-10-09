---
name: oci-monitoring-mql
description: Author and optimize OCI Monitoring Query Language (MQL) queries, split-metric alarms, threshold rules, and absence triggers. Use when querying OCI service or custom metrics, configuring fine-grained alarms, splitting alerts across dimensions, or routing notifications.
license: Apache-2.0
---
# OCI Monitoring and MQL Querying

## When to use

Use when authoring MQL metric queries, designing threshold alarms, creating split-metric alarms per compute or database resource, implementing heartbeat absence alarms, or tuning evaluation intervals and pending durations.

## Key concepts

MQL queries adhere to the standard grammar: `metric[interval]{dimensions}.grouping().statistic()`.

- **Interval**: Aggregation bucket window (`[1m]`, `[5m]`, `[1h]`).
- **Dimensions**: Resource filter predicates enclosed in curly braces.
- **Grouping**: Grouping expressions such as `.groupBy(resourceId)` to produce split metrics per individual resource.
- **Statistics**: Functions such as `.mean()`, `.max()`, `.min()`, `.sum()`, `.count()`, `.rate()`, and `.percentile()`.

Threshold alarms compare statistical aggregations against defined values. Absence alarms detect when expected telemetry stops arriving (such as agent failure or instance termination). Notifications topics route firing and resolution messages to subscribed email, HTTPS, Slack, or OCI Functions endpoints.

For complete grammar details, see the [MQL Syntax Reference](../../references/mql-syntax.md) and [MQL Cookbook](../../references/mql-cookbook.md).

## Workflow

1. Identify the target metric namespace (such as `oci_computeagent`) and metric name in OCI Metric Explorer.
2. Formulate the MQL expression with appropriate interval and dimension filters.
3. Add `.groupBy()` if individual resource tracking is desired for split-metric alarms.
4. Establish threshold bounds, operator (`>`, `>=`, `<`, `<=`), trigger delay (pending duration), and severity level (`CRITICAL`, `ERROR`, `WARNING`, `INFO`).
5. Route notifications to an OCI Notifications topic and verify subscriber confirmation.
6. Verify alarm behavior under both firing and recovery conditions.

## Pitfalls

- Aggregating without `.groupBy()` produces fleet-wide averages that conceal individual instance failures.
- Conflating zero-value metrics with absence of data; absence indicates reporting failures requiring absence alarms.
- Setting pending duration too short leads to alert flapping on transient spikes; 3 to 5 minutes is typical for infrastructure metrics.
- Overusing high-cardinality custom dimensions leads to metric throttling.

## Examples

```text
# Compute CPU utilization threshold with resource grouping
CpuUtilization[5m]{availabilityDomain = "<AVAILABILITY_DOMAIN>"}.groupBy(resourceId).mean() > 85
```

```text
# Service heartbeat absence alarm
CustomHeartbeat[5m]{appName = "payment-api"}.groupBy(instanceId).count() == 0
```

## Official docs

- [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [MQL](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Reference/mql.htm)
- [Managing alarms](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm)
- [Publishing custom metrics](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/publishingcustommetrics.htm)
- [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm)

## Related skills

Use `oci-monitoring-alarms` for foundational alarm setups, `oci-stack-monitoring-agents` for agent-based metric collection, and `oci-logging-pipelines` for notification routing.
