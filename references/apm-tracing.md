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
