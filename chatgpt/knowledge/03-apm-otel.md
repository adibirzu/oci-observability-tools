---
name: oci-apm-otel
description: Instrument applications for OCI Application Performance Monitoring with OpenTelemetry, APM agents, browser RUM, and synthetics. Use when sending traces/spans to APM, choosing data keys, or debugging missing traces.
license: Apache-2.0
---
# OCI APM and OpenTelemetry

## When to use

Use when instrumenting a service, exporting OTLP spans, enabling browser RUM, adding synthetic monitors, or tracing a slow request.

## Key concepts

Create an APM domain and distinguish `<APM_PRIVATE_DATAKEY>` from `<APM_PUBLIC_DATAKEY>`. Server-side exporters use the private key; browser RUM uses a public key. Configure the complete signal-specific upload URL from the official guide, rather than only the domain base endpoint, and a stable `service.name`. Sampling must preserve enough diagnostic traces without assuming current limits.

Correlate trace and span identifiers into application logs, then search those logs in Log Analytics. See [OTel to APM](../../references/otel-to-apm.md).

## Workflow

1. Select the APM domain and data-key type.
2. Verify the exporter protocol and configure the documented signal-specific URL, authentication, resource attributes, and sampling.
3. Generate one synthetic request and inspect exporter diagnostics.
4. Allow for ingestion lag, then correlate the trace with logs.
5. Add synthetics for externally observable paths.

## Pitfalls

Never put a private data key in browser code or a repository. Do not invent an upload endpoint. A short delay does not prove data loss; check exporter status, clocks, sampling, and ingestion lag.

## Examples

```text
OTEL_SERVICE_NAME=checkout-api
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=<APM_TRACES_UPLOAD_URL>
```

`<APM_TRACES_UPLOAD_URL>` means the complete authenticated URL described in [Configure Other Tracers](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html), including the private-span path and data-format parameters. Resolve it through protected runtime configuration; do not paste or log the key-bearing URL. This is a configuration draft, not verified ingestion.

## Official docs

- [Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Configure open-source tracing](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html)
- [Synthetic monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html)

## Related skills

Use `oci-ocl-queries` for trace-log correlation and `oci-om-maturity` for SLO adoption.


---

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
