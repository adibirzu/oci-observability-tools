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
