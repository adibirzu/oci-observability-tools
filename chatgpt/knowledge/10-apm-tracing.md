---
name: oci-apm-tracing
description: Instrument applications with OpenTelemetry for OCI APM, query distributed traces in Trace Explorer, and configure synthetic monitors. Use when setting up OTel collectors, tracing distributed requests, diagnosing latency bottlenecks, or creating availability monitors.
license: Apache-2.0
---
# OCI APM Tracing and OpenTelemetry

## When to use

Use when instrumenting applications with OpenTelemetry SDKs, configuring OpenTelemetry Collector pipelines for OCI APM, exploring traces and spans in Trace Explorer, isolating latency bottlenecks across microservices, or authoring synthetic availability monitors.

## Key concepts

An OCI APM domain provides a dedicated telemetry ingestion boundary with a specific endpoint `<APM_DOMAIN_UPLOAD_ENDPOINT>`. Two classes of data keys authenticate telemetry:

- `<APM_PRIVATE_DATAKEY>`: For backend applications, agents, and OpenTelemetry Collectors.
- `<APM_PUBLIC_DATAKEY>`: Exclusively for client-side instrumentation like Browser Real User Monitoring (RUM).

OpenTelemetry spans must follow semantic conventions for resource attributes (`service.name`, `service.version`, `deployment.environment`) and operation attributes (`http.status_code`, `db.system`).

OCI APM Trace Explorer allows interactive querying across spans, service topology visualization, and latency percentiles. Synthetic monitors run automated probes from public or dedicated vantage points to evaluate service reachability and SLA compliance.

For detailed configurations, see the [APM Tracing Reference](../../references/apm-tracing.md) and [OTel to APM Guide](../../references/otel-to-apm.md).

## Workflow

1. Retrieve the APM domain upload endpoint `<APM_DOMAIN_UPLOAD_ENDPOINT>` and generate `<APM_PRIVATE_DATAKEY>` from the OCI Console or CLI.
2. Configure application OpenTelemetry SDKs or the OpenTelemetry Collector to send OTLP spans to the APM endpoint with header `Authorization: DataKey <APM_PRIVATE_DATAKEY>`.
3. Set standard resource attributes, ensuring `service.name` uniquely and consistently identifies each microservice.
4. Verify span ingestion in APM Trace Explorer, querying by service name and inspecting distributed call trees.
5. Create synthetic monitors for critical HTTP/REST endpoints with automated alerts on failure.

## Pitfalls

- Never expose `<APM_PRIVATE_DATAKEY>` in client-side code, mobile applications, or public repositories.
- Allow for standard ingestion buffer latency (typically 1 to 2 minutes) before assuming telemetry ingestion failure.
- Inconsistent `service.name` values fragment service topology maps in APM.
- Avoid attaching high-cardinality values (such as session IDs or full request payloads) as unindexed span tags.

## Examples

```text
# OpenTelemetry environment variables for backend service
OTEL_SERVICE_NAME=order-service
OTEL_EXPORTER_OTLP_ENDPOINT=<APM_DOMAIN_UPLOAD_ENDPOINT>
OTEL_EXPORTER_OTLP_HEADERS="Authorization=DataKey <APM_PRIVATE_DATAKEY>"
OTEL_TRACES_SAMPLER=parentbased_always_on
```

```text
# Trace Explorer query to find slow requests
ServiceName = 'order-service' and SpanDuration > 1500
```

## Official docs

- [Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Configure open-source tracing](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html)
- [Synthetic monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html)

## Related skills

Use `oci-apm-otel` for introductory OTel concepts, `oci-ocl-queries` for log correlation, and `oci-monitoring-mql` for metric-based alarms.


---

# OCI APM Tracing and OpenTelemetry Reference

This reference describes application instrumentation with OpenTelemetry, OpenTelemetry Collector topology, APM domain configuration, trace semantics, and synthetic monitoring for OCI Application Performance Monitoring (APM).

## APM Domain Configuration

An APM domain represents the logical boundary for tracing telemetry in OCI. Each APM domain provides:

- **Data Upload Endpoint**: Configured as `<APM_DOMAIN_UPLOAD_ENDPOINT>`.
- **Private Data Key**: `<APM_PRIVATE_DATAKEY>` used for authenticating server-side instrumentation and OpenTelemetry Collector pipelines.
- **Public Data Key**: `<APM_PUBLIC_DATAKEY>` used exclusively for client-side instrumentation (Browser RUM, mobile clients) where secrets cannot be protected.

### Authentication Header Format

Telemetry sent to the APM data upload endpoint must include the authentication key in the request headers:

```text
Authorization: DataKey <APM_PRIVATE_DATAKEY>
```

For OpenTelemetry HTTP exporters, the header is configured via exporter options or environment variables.

## OpenTelemetry Collector Configuration

The OpenTelemetry Collector receives telemetry from application services, batches spans, and exports them to OCI APM via OTLP/HTTP:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 512
  memory_limiter:
    check_interval: 1s
    limit_percentage: 75
    spike_limit_percentage: 20

exporters:
  otlphttp/apm:
    endpoint: "<APM_DOMAIN_UPLOAD_ENDPOINT>"
    headers:
      Authorization: "DataKey <APM_PRIVATE_DATAKEY>"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlphttp/apm]
```

## Trace Semantics and Resource Attributes

Spans should adhere to standard [OpenTelemetry](https://opentelemetry.io) semantic conventions to enable correlation and service topology mapping in OCI APM:

### Resource Attributes

| Attribute | Description | Example |
|---|---|---|
| `service.name` | Logical identifier of the microservice | `order-service` |
| `service.version` | Software build or release version | `1.4.2` |
| `service.namespace` | Domain or organizational grouping | `commerce` |
| `deployment.environment` | Runtime stage | `production`, `staging` |

### Span Semantic Attributes

- **HTTP Requests**: `http.method` (`GET`), `http.status_code` (`200`), `http.url` (`<HTTP_REQUEST_URL>`), `http.target` (`/api/v1/orders`).
- **Database Operations**: `db.system` (`oracle`), `db.name` (`sales_pdb`), `db.statement` (`SELECT * FROM orders WHERE id = ?`).
- **RPC Spans**: `rpc.system` (`grpc`), `rpc.service` (`PaymentService`), `rpc.method` (`ProcessPayment`).
- **Error Flagging**: When a span encounters a failure, set span status to `Error` and attach `error = true` with exception details (`exception.type`, `exception.message`).

## Sampling Strategies

- **Head-Based Sampling**: Decisions made at span origination (SDK level). Common ratios include 100% in staging, 5%-20% in high-throughput production services.
- **Tail-Based Sampling**: Decisions evaluated at collector level after spans complete, allowing 100% retention for error traces and high-latency spans while sampling normal traces.

## Trace Explorer Query Patterns

OCI APM Trace Explorer provides querying over indexed span attributes:

```text
# Filter for slow traces across order-service
ServiceName = 'order-service' and SpanDuration > 2000

# Filter for error spans across all services
Error = true

# Correlate spans by trace ID
TraceId = '<TRACE_ID>'
```

## Synthetic Monitoring

Synthetic monitors simulate user transactions and verify availability:

1. **Monitor Types**:
   - **REST / HTTP Monitors**: Single API endpoint checks validating status codes, response headers, and response latency.
   - **Browser Monitors**: Multi-step user journey scripts executing on real browser engines.
2. **Vantage Points**:
   - **Public Vantage Points**: Oracle-managed global locations probing external endpoints.
   - **Dedicated Vantage Points**: Customer-hosted agents deployed inside private VCNs to probe internal services.
3. **Execution Cadence**: Typical schedules range from 1 minute to 15 minutes with automated alarm integration when failures persist.

## Official Oracle Documentation

- [Application Performance Monitoring Overview](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Configure Open-Source Tracing Systems](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html)
- [Synthetic Monitoring Guide](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html)


---

# OpenTelemetry to OCI APM

## Configuration shape

Use `<APM_DOMAIN_UPLOAD_ENDPOINT>` exactly as supplied by the APM domain. Server-side OTLP exporters authenticate with `<APM_PRIVATE_DATAKEY>` using the header and path shape in the official APM OpenTelemetry guide. Browser RUM must use `<APM_PUBLIC_DATAKEY>` only.

Set a stable `service.name`, deployment environment, and service version. Choose sampling deliberately and inspect exporter diagnostics before concluding spans are missing.

## Correlation

Add trace and span identifiers to structured application logs. In Log Analytics, parse those fields and query the same external time window. Allow for ingestion lag in both systems and compare timestamps in a single time zone.

## Debug order

1. Confirm instrumentation creates spans.
2. Confirm the exporter is enabled and the endpoint is a placeholder-derived configured value.
3. Check authentication type, TLS, clocks, and proxy behavior.
4. Check sampling and service-name attributes.
5. Wait for expected ingestion lag, then search by trace identifier.
