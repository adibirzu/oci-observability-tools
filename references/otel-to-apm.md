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
