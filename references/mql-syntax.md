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
