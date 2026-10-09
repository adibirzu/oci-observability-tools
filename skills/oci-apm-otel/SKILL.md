---
name: oci-apm-otel
description: Instrument applications for OCI Application Performance Monitoring with OpenTelemetry, APM agents, browser RUM, and synthetics. Use when sending traces/spans to APM, choosing data keys, or debugging missing traces.
license: Apache-2.0
---
# OCI APM and OpenTelemetry

## When to use

Use when instrumenting a service, exporting OTLP spans, enabling browser RUM, adding synthetic monitors, or tracing a slow request.

## Key concepts

Create an APM domain and distinguish `<APM_PRIVATE_DATAKEY>` from `<APM_PUBLIC_DATAKEY>`. Server-side exporters use the private key; browser RUM uses only a public key. Set `OTEL_EXPORTER_OTLP_ENDPOINT=<APM_DOMAIN_UPLOAD_ENDPOINT>`, the documented path/header shape, and a stable `service.name`. Sampling must preserve enough diagnostic traces without assuming current limits.

Correlate trace and span identifiers into application logs, then search those logs in Log Analytics. See [OTel to APM](../../references/otel-to-apm.md).

## Workflow

1. Select the APM domain and data-key type.
2. Configure the OTLP endpoint, authentication header, resource attributes, and sampling.
3. Generate one synthetic request and inspect exporter diagnostics.
4. Allow for ingestion lag, then correlate the trace with logs.
5. Add synthetics for externally observable paths.

## Pitfalls

Never put a private data key in browser code or a repository. Do not invent an upload endpoint. A short delay does not prove data loss; check exporter status, clocks, sampling, and ingestion lag.

## Examples

```text
OTEL_SERVICE_NAME=checkout-api
OTEL_EXPORTER_OTLP_ENDPOINT=<APM_DOMAIN_UPLOAD_ENDPOINT>
APM_DATA_KEY=<APM_PRIVATE_DATAKEY>
```

## Official docs

- [Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [Configure open-source tracing](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/configure-open-source-tracing-systems.html)
- [Synthetic monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/doc/use-synthetic-monitoring.html)

## Related skills

Use `oci-ocl-queries` for trace-log correlation and `oci-om-maturity` for SLO adoption.
