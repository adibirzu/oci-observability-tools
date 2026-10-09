# OCI Logging Pipeline Patterns and Reference Architectures

This reference details production patterns for OCI Logging, Connector Hub routing matrices, IAM policy templates, CloudEvents envelope normalization, and OCI Streaming checkpointing and consumer lag monitoring.

## Connector Hub Routing Matrix

Connector Hub orchestrates data movement between OCI services. It connects a telemetry source to an optional transformation task and delivers records to a destination sink:

| Source | Optional Task | Target Sink | Primary Use Case |
|---|---|---|---|
| Logging (Service, Custom, Audit) | Functions | Log Analytics | Ingesting and parsing logs into OCL-searchable indexes |
| Logging (Service, Custom, Audit) | None | Object Storage | Archival, compliance retention, and cold storage |
| Logging (Service, Custom, Audit) | Functions | Streaming | Decoupled streaming fan-out to external SIEM/data lakes |
| Logging (Audit) | Functions | Notifications | Critical security event alerts (e.g. IAM policy changes) |
| Streaming (Stream Pool) | Functions | Log Analytics | Routing streaming message logs to search clusters |
| Streaming (Stream Pool) | None | Object Storage | Bulk stream persistence and backup |
| Monitoring (Metric Namespace) | Functions | Streaming | Forwarding high-frequency metric data to stream processing |
| Monitoring (Metric Namespace) | None | Notifications | High-cardinality metric alerts fan-out |

## Connector Hub IAM Policy Patterns

Connector Hub requires authorization to read from source resources and write to target destinations. Model access using dynamic groups representing the connector instance:

```text
# Define a dynamic group for the connector
# Matching rule: resource.id = '<CONNECTOR_OCID>'
# Dynamic group name: <CONNECTOR_DYNAMIC_GROUP>

# 1. Read access from source log groups in the source compartment
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to read log-content in compartment <COMPARTMENT_NAME>

# 2. Write access to target Log Analytics in destination compartment
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to use log-analytics-log-group in compartment <COMPARTMENT_NAME>

# 3. Write access to target Object Storage bucket
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to manage objects in compartment <COMPARTMENT_NAME> where target.bucket.name = '<BUCKET_NAME>'

# 4. Write access to target Streaming pool
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to use stream-pull in compartment <COMPARTMENT_NAME>
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to use stream-push in compartment <COMPARTMENT_NAME>

# 5. Invoke permission if an OCI Functions task is configured
allow dynamic-group <CONNECTOR_DYNAMIC_GROUP> to use fn-invocation in compartment <COMPARTMENT_NAME>
```

## CloudEvents Normalization

OCI Events generates JSON envelopes conforming to CloudEvents standards. When building ingestion pipelines or consumer services, normalize heterogeneous event payloads to the canonical CloudEvents v1.0 specification:

### Normalization Field Mapping

| Canonical Field | OCI Event Field | Description | Type |
|---|---|---|---|
| `specversion` | `cloudEventsVersion` / `specversion` | CloudEvents specification version (e.g. `1.0`) | String |
| `type` | `eventType` / `type` | Distinct event identifier (e.g. `com.oraclecloud.objectstorage.createbucket`) | String |
| `source` | `source` | Context URI identifying the emitting resource or service | String |
| `id` | `eventID` / `id` | Unique identifier for deduplication | String |
| `time` | `eventTime` / `time` | Timestamp of event occurrence in RFC 3339 format | String |
| `data` | `data` | Service-specific event payload details | Object |

### Canonical Normalization Logic

```json
{
  "specversion": "1.0",
  "type": "com.oraclecloud.computeagent.sendinstancecrashedaction",
  "source": "ComputeInstance",
  "id": "<EVENT_ID>",
  "time": "2026-10-09T12:00:00.000Z",
  "data": {
    "compartmentId": "<COMPARTMENT_OCID>",
    "compartmentName": "<COMPARTMENT_NAME>",
    "resourceId": "<RESOURCE_OCID>",
    "resourceName": "app-server-01",
    "availabilityDomain": "<AVAILABILITY_DOMAIN>"
  }
}
```

### Deduplication Strategy

1. Extract the canonical `id` attribute from the normalized envelope.
2. Store processed event IDs in a high-speed key-value cache or database table with a configured TTL (for example 24 to 72 hours).
3. If an incoming event ID exists in the cache, acknowledge and discard the duplicate.
4. Never deduplicate on payload fields (`data.*`) because payload mutations can produce false deduplication collisions.

## Streaming Lag and Checkpointing

OCI Streaming provides partitioned message logs. Safe stream processing requires partition-level state tracking and durable checkpointing:

### Two-Phase Processing and Checkpoint Flow

```text
[Partition Message Buffer] 
         │
         ▼
[1. Read Batch at Current Offset]
         │
         ▼
[2. Process and Durably Store Record in Target Sink]
         │
         ▼
[3. Commit New Offset to Checkpoint Store]
         │
         ▼
[Acknowledge Next Batch]
```

### Guarantees and Invariants

1. **Commit After Durable Write**: Never commit a partition offset before the processed batch is durably written to downstream storage. Committing prematurely causes data loss during consumer crashes.
2. **Independent Partition Tracking**: Track offsets independently per partition. Avoid global stream-level cursors.
3. **Idempotent Sinks**: Because consumers provide at-least-once delivery, downstream persistence must be idempotent or rely on unique transaction IDs.

### Stream Consumer Lag Monitoring

Consumer lag measures how far behind the consumer is relative to the latest record published to the stream:

- **Offset Lag**: `latest_partition_offset - committed_partition_offset`
- **Time Lag**: `current_timestamp - last_processed_record_timestamp`

### MQL Alarm for Consumer Lag

Monitor stream partition health and consumer lag using OCI Monitoring:

```text
# Alert when unconsumed message count exceeds 5000 records
UnconsumedMessages[5m]{streamId = "<STREAM_OCID>"}.groupBy(partitionId).max() > 5000
```

## Official Oracle Documentation

- [OCI Logging Overview](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [Custom Logs in OCI Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/custom_logs.htm)
- [Connector Hub Overview](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)
- [Ingest Logs into Log Analytics with Connector Hub](https://docs.oracle.com/en-us/iaas/log-analytics/doc/ingest-logs-from-other-oci-services-using-service-connector.html)
- [OCI Events Overview](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm)
- [Event Envelope Reference](https://docs.oracle.com/en-us/iaas/Content/Events/Reference/eventenvelopereference.htm)
- [OCI Streaming Overview](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)
- [OCI Notifications Overview](https://docs.oracle.com/en-us/iaas/Content/Notification/home.htm)
