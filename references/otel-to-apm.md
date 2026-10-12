# OpenTelemetry to OCI APM

## Configuration shape

Use `<APM_DOMAIN_UPLOAD_ENDPOINT>` as the base supplied by the APM domain, then construct the complete signal-specific URL from [Configure Other Tracers](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html). For backend OTLP spans, the documented shape uses `/20200101/observations/private-span` with `dataFormat=otlp-span`, `dataFormatVersion=1`, and `dataKey=<APM_PRIVATE_DATAKEY>` query parameters. Do not assume a generic `Authorization: DataKey` header or a default `/v1/traces` path. Browser RUM uses `<APM_PUBLIC_DATAKEY>`.

Configure the SDK's signal-specific traces endpoint or the Collector's `traces_endpoint` with `<APM_TRACES_UPLOAD_URL>`, representing that complete URL. Verify support in the chosen exporter version. Supply key-bearing URLs through protected runtime configuration and redact them from diagnostics. These examples are documentation-backed drafts; ingestion still requires live validation.

Set a stable `service.name`, deployment environment, and service version. Choose sampling deliberately and inspect exporter diagnostics before concluding spans are missing.

## Correlation

Add trace and span identifiers to structured application logs. In Log Analytics, parse those fields and query the same external time window. Allow for ingestion lag in both systems and compare timestamps in a single time zone.

## Debug order

1. Confirm instrumentation creates spans.
2. Confirm the exporter is enabled and the endpoint is a placeholder-derived configured value.
3. Check authentication type, TLS, clocks, and proxy behavior.
4. Check sampling and service-name attributes.
5. Wait for expected ingestion lag, then search by trace identifier.
