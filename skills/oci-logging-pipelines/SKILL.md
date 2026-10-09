---
name: oci-logging-pipelines
description: Design OCI Logging and Connector Hub pipelines. Use when enabling service, custom, or audit logs, routing logs, events, or metrics to Log Analytics, Streaming, Object Storage, Functions, or Notifications, or handling OCI event payloads.
license: Apache-2.0
---
# OCI Logging and Connector Hub Pipelines

## When to use

Use when enabling OCI service logs, configuring custom application log collection via management agents, managing audit logs, routing telemetry with Connector Hub, processing OCI Events rules, normalizing CloudEvents payloads, or building checkpointed OCI Streaming consumers.

## Key concepts

OCI Logging centralizes telemetry across three log classes within logical log groups:
- **Service logs**: Pre-integrated telemetry from OCI native services (Load Balancers, VCN Flow Logs, Object Storage access, OKE).
- **Custom logs**: Application and host log files ingested through the Unified Monitoring Agent or Management Agent.
- **Audit logs**: Automatically captured API activity records across all tenancy compartments.

Connector Hub provides serverless data movement across services:
- **Source**: Logging (log groups), Streaming (stream pools), or Monitoring (metrics).
- **Task (Optional)**: In-flight transformation, filtering, and data enrichment using OCI Functions.
- **Target**: Log Analytics, Object Storage, Streaming, Notifications, or Functions.
- **IAM Policies**: Authorization is granted via dynamic groups representing the connector instance (`<CONNECTOR_DYNAMIC_GROUP>`).

OCI Events delivers state-change notifications formatted as CloudEvents:
- Normalization maps incoming payloads into canonical fields: `specversion`, `type`, `source`, `id`, `time`, and `data`.
- Deduplication should rely strictly on the immutable `id` field.

OCI Streaming buffers high-throughput telemetry:
- Consumers must track offsets independently per partition.
- Commit checkpoints only after records are durably persisted to target storage.

See detailed architectures in [Pipeline Patterns](../../references/pipelines-patterns.md).

## Workflow

1. Identify the source telemetry signal (service log category, custom log path, event rule pattern, or stream pool).
2. Create target resources (log group `<LOG_GROUP_OCID>`, Object Storage bucket `<BUCKET_NAME>`, or stream `<STREAM_OCID>`).
3. Author the Connector Hub pipeline linking source, optional OCI Functions transformation task, and destination sink.
4. Apply least-privilege IAM policy statements allowing the connector dynamic group to read the source and write to the target.
5. In downstream event consumers, normalize payloads to CloudEvents v1.0 and deduplicate on the `id` field.
6. For streaming consumers, maintain independent partition cursors, commit offsets only after durable writes, and alert on lag.

## Pitfalls

- Missing IAM permissions: omitting connector dynamic group policies causes silent ingestion failures without pipeline errors.
- Early offset commit: committing partition offsets before downstream write completion risks irrecoverable data loss on crash.
- Deduplicating on mutable body fields rather than CloudEvents `id` causes duplicate processing or dropped messages.
- Over-aggregating log groups: combining diverse retention or security requirements into a single log group complicates governance.
- Unhandled at-least-once delivery: consumers must handle duplicate messages idempotently.

## Examples

```text
# Connector Hub policy pattern
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to read log-content in compartment <COMPARTMENT_NAME>
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to use log-analytics-log-group in compartment <COMPARTMENT_NAME>
```

```text
# Stream consumer lag alarm rule
UnconsumedMessages[5m]{streamId = "<STREAM_OCID>"}.groupBy(partitionId).max() > 5000
```

## Official docs

- [Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [Custom logs](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/custom_logs.htm)
- [Connector Hub](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)
- [Log Analytics ingestion](https://docs.oracle.com/en-us/iaas/log-analytics/doc/ingest-logs-from-other-oci-services-using-service-connector.html)
- [Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm)
- [Event envelope](https://docs.oracle.com/en-us/iaas/Content/Events/Reference/eventenvelopereference.htm)
- [Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)
- [Notifications](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm)

## Related skills

Use `oci-ocl-queries` for Log Analytics search, `oci-monitoring-mql` for pipeline health alarms, and `oci-om-router` for routing decisions.
