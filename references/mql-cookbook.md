# MQL cookbook

MQL has the shape `metric[interval]{dimensions}.grouping().statistic()`. Confirm namespaces, metric names, dimensions, and current limits in the official Monitoring documentation.

```text
CpuUtilization[5m]{resourceDisplayName = "example"}.mean()
```

```text
MemoryUtilization[5m]{availabilityDomain = "<AVAILABILITY_DOMAIN>"}.groupBy(resourceId).max()
```

Use a representative graph before creating a threshold. For an absence alarm, model missing telemetry explicitly rather than treating it as a zero value. Keep custom metric dimensions bounded and stable.
