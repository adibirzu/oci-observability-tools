# Logging pipeline patterns

## Connector matrix

| Source | Optional task | Typical target |
|---|---|---|
| Logging | Functions | Log Analytics, Streaming, Object Storage |
| Streaming | Functions | Logging Analytics or another supported sink |
| Monitoring | Functions | Streaming or Notifications |

Treat this as a design prompt and verify supported combinations in Connector Hub documentation. The IAM shape is: a placeholder dynamic group representing the connector may read only its source and write only its target in `<COMPARTMENT_NAME>`.

## CloudEvents normalization

Map incoming envelopes to `specversion`, `type`, `source`, `id`, `time`, and `data`. Convert legacy `eventType` to `type` and `cloudEventsVersion` to `specversion`. Deduplicate on immutable `id`, preserving the original payload under `data`.

## Streaming lag and checkpoints

Track offset and last-record timestamp independently for every partition. Process and durably store the record before committing its checkpoint. On restart, resume from the committed offset. Measure lag as current time minus last-record time and alert when it exceeds the workload's stated objective.
