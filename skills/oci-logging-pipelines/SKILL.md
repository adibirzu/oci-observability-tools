---
name: oci-logging-pipelines
description: Design OCI Logging and Connector Hub pipelines. Use when enabling service, custom, or audit logs, routing logs, events, or metrics to Log Analytics, Streaming, Object Storage, Functions, or Notifications, or handling OCI event payloads.
license: Apache-2.0
---
# OCI logging pipelines

## When to use

Use for service, custom, or audit logging; Connector Hub routes; OCI Events; CloudEvents normalization; and checkpointed stream consumers.

## Key concepts

Logging stores service and custom logs in log groups; audit events are available as audit logs. Connector Hub composes source → optional task → target, subject to supported combinations. Policies grant a placeholder connector group only the required source read and target write abilities.

Normalize event envelopes to `specversion`, `type`, `source`, `id`, `time`, and `data`; fold legacy `eventType` and `cloudEventsVersion` into those fields and deduplicate on `id`. For each stream partition, track offset and last-record time, commit only after durable write, resume from the checkpoint, and alert when lag exceeds the chosen objective. See [pipeline patterns](../../references/pipelines-patterns.md).

## Workflow

1. Identify source signal, volume, transform, target, and failure behavior.
2. Verify the connector matrix and least-privilege policy shape.
3. Normalize and validate example envelopes.
4. Define retry, deduplication, checkpoint, lag, and dead-letter behavior.
5. Test with synthetic events before enabling production flow.

## Pitfalls

Do not assume every source-task-target combination is supported. Acknowledging before durable write loses records. Deduplicating on mutable payload fields creates duplicates. Mark changing commands `# MUTATES`.

## Examples

Connector route: Logging → Functions task → Streaming. A consumer stores a record, then commits its partition offset.

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

Use `oci-ocl-queries` for the analytics destination and `oci-monitoring-alarms` for pipeline health.
