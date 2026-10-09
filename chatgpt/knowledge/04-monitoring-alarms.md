---
name: oci-monitoring-alarms
description: Write OCI Monitoring Query Language (MQL) queries and alarms. Use when querying metrics, publishing custom metrics, or designing alarms with Notifications.
license: Apache-2.0
---
# OCI Monitoring and alarms

## When to use

Use for service or custom metrics, MQL, threshold and absence alarms, and notification routing.

## Key concepts

MQL follows `metric[interval]{dimensions}.grouping().statistic()`. Alarm design includes threshold, absence, pending duration, severity, repeat notification, and a useful message. Route alarm → Notifications topic → email, HTTPS, or Functions. Keep custom namespaces and dimensions stable; link to current limits rather than restating them. See the [MQL cookbook](../../references/mql-cookbook.md).

## Workflow

1. Confirm namespace, metric, dimensions, and resource scope.
2. Graph the MQL query over representative history.
3. Choose threshold or absence semantics and pending duration.
4. Configure severity, message, repeat behavior, and topic subscription.
5. Test both firing and recovery paths.

## Pitfalls

Avoid high-cardinality custom dimensions, instantaneous thresholds, and alarms without owners. Missing data is not always zero. Notification delivery depends on subscription confirmation and endpoint behavior.

## Examples

```text
CpuUtilization[5m]{resourceDisplayName = "example"}.mean()
```

## Official docs

- [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [MQL](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Reference/mql.htm)
- [Managing alarms](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/managingalarms.htm)
- [Publishing custom metrics](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Tasks/publishingcustommetrics.htm)
- [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm)

## Related skills

Use `oci-stack-monitoring-agents` for collection and `oci-logging-pipelines` for routing.


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
