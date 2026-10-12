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


---

# OCI Monitoring Query Language (MQL) Reference

This reference covers the syntax, operators, grouping behaviors, and alarm rules for OCI Monitoring Query Language (MQL).

## Grammar and Structure

An MQL expression has the following fundamental structure:

```text
metric[interval]{dimensions}.grouping().statistic()
```

Each component serves a specific role in metric evaluation:

- **`metric`**: The metric name published under an OCI service namespace (for example `CpuUtilization` under `oci_computeagent`) or a custom namespace.
- **`[interval]`**: The aggregation bucket window. Valid intervals include `[1m]`, `[5m]`, `[10m]`, `[1h]`, and `[1d]`.
- **`{dimensions}`**: Dimension filter predicates enclosed in curly braces. Filters restrict data points by resource metadata.
- **`.grouping()`**: Dimension grouping clauses (such as `.groupBy(resourceId)`), separating data streams into distinct time series.
- **`.statistic()`**: The statistical aggregation function applied across data points in each interval bucket.

## Interval Specifications

The interval defines the time window over which raw metric data points are aggregated:

| Interval | Description | Recommended Usage |
|---|---|---|
| `[1m]` | 1-minute aggregation window | Near real-time operational alerts, high-frequency custom metrics |
| `[5m]` | 5-minute aggregation window | Standard service metric alarms, CPU/memory thresholds |
| `[10m]` | 10-minute aggregation window | Trend evaluation, intermediate smoothing |
| `[1h]` | 1-hour aggregation window | Hourly rollups, capacity evaluation |
| `[1d]` | 1-day aggregation window | Long-term trend analysis, baseline reporting |

## Dimension Filtering

Dimension filters restrict metric series based on dimension keys and values:

```text
# Exact equality match
CpuUtilization[5m]{resourceDisplayName = "web-prod-01"}.mean()

# Inequality match
CpuUtilization[5m]{availabilityDomain != "<AVAILABILITY_DOMAIN>"}.mean()

# Set membership match
CpuUtilization[5m]{resourceDisplayName in ("web-prod-01", "web-prod-02")}.mean()

# Regex pattern match
CpuUtilization[5m]{resourceDisplayName =~ "web-prod-.*"}.mean()

# Conjunction of multiple dimensions
DiskBytesRead[5m]{resourceDisplayName = "db-node-01", faultDomain = "FAULT-DOMAIN-1"}.rate()
```

## Grouping and Split Metrics

Grouping divides incoming metric streams into separate time series based on distinct dimension values:

- **`.groupBy(dim1, dim2)`**: Emits one time series per unique tuple of the specified dimensions. When used in an alarm, this produces a **split-metric alarm**, tracking health independently for each resource.
- **`.grouping()`**: Aggregates all matching time series into a single composite series.

```text
# Split metric evaluation per compute instance
CpuUtilization[5m].groupBy(resourceId).mean()

# Grouping by availability domain and region
NetworkBytesIn[5m].groupBy(availabilityDomain, region).sum()
```

## Statistical Functions

Statistical functions aggregate data points within each time bucket:

| Statistic | Description | Common Use Case |
|---|---|---|
| `.mean()` | Average of values in the interval | Resource utilization (CPU, memory, storage) |
| `.max()` | Maximum value observed | Peak load spikes, burst detection |
| `.min()` | Minimum value observed | Free memory floor, baseline availability |
| `.sum()` | Sum of all observed values | Transaction counts, total bytes transferred |
| `.count()` | Total number of data points submitted | Telemetry heartbeat verification |
| `.rate()` | Per-second rate of change | Throughput (IOPS, network bytes/sec) |
| `.percentile(0.95)` | 95th percentile value (`p95`) | Latency SLOs, response time SLA monitoring |
| `.percentile(0.99)` | 99th percentile value (`p99`) | Tail latency monitoring |

## Alarm Rule Types

### 1. Threshold Alarms

Threshold alarms compare metric statistics against numeric bounds:

```text
# CPU utilization above 85% for 5 minutes
CpuUtilization[5m]{resourceDisplayName =~ "app-.*"}.groupBy(resourceId).mean() > 85
```

Configuration parameters:
- **Severity**: `CRITICAL`, `ERROR`, `WARNING`, `INFO`.
- **Trigger delay (pending duration)**: Time the condition must remain true before firing (for example `PT5M`).
- **Evaluation interval**: Frequency of alarm evaluation (typically matching query interval).
- **Split metric alarm**: Set to true when `.groupBy()` is present, generating individual alarm status per dimension value.

### 2. Absence Alarms

Absence alarms trigger when an expected metric stops reporting, signaling host failure or agent outage:

```text
# Metric reporting count falls to zero or ceases
Heartbeat[5m]{appName = "payment-service"}.groupBy(hostId).count() == 0
```

Configuration:
- Set alarm condition to trigger on missing data / absence rather than threshold values.
- Differentiate between a metric value of 0 (normal idle state) and absence of data points (collection pipeline down).

## Official Oracle Documentation

- [Monitoring Service Overview](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [Monitoring Query Language (MQL) Reference](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Reference/mql.htm)
- [Managing Alarms](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm)
- [Publishing Custom Metrics](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/publishingcustommetrics.htm)


---

# MQL cookbook

MQL has the shape `metric[interval]{dimensions}.grouping().statistic()`. Confirm namespaces, metric names, dimensions, and current limits in the official Monitoring documentation.

```text
CpuUtilization[5m]{resourceDisplayName = "example"}.mean()
```

```text
MemoryUtilization[5m]{availabilityDomain = "<AVAILABILITY_DOMAIN>"}.groupBy(resourceId).max()
```

Use a representative graph before creating a threshold. For an absence alarm, model missing telemetry explicitly rather than treating it as a zero value. Keep custom metric dimensions bounded and stable.
