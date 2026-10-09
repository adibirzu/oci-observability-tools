# OCI Observability Maturity Model (L0–L4)

This framework defines five sequential maturity levels for workloads running on Oracle Cloud Infrastructure (OCI). Each tier establishes required signals, OCI service integrations, governance interlocks, and verification criteria.

## Summary Maturity Matrix

| Level | Tier Focus | Primary OCI Services | Key Capabilities |
|---|---|---|---|
| **L0** | Foundations & Governance | Audit, Logging, IAM | Tenant audit, service logs, log groups, tagging |
| **L1** | Service Health & Alarms | Monitoring, Notifications | Golden signals, MQL thresholds, absence alarms, routing |
| **L2** | Analytics & Database Depth | Log Analytics, DBM, OPSI, SCH | OCL querying, SIEM integration, ASH/AWR, capacity forecasting |
| **L3** | User Experience & SLOs | APM, Synthetics | Distributed tracing, OTel, browser RUM, synthetic probes |
| **L4** | AIOps & Agent Observability | AI Agents, OCI O&M Suite | Closed-loop remediation, MCP safety, automated evaluation |

---

## L0 — Foundations and Governance

**Objective**: Ensure basic auditability, accountability, and baseline log collection across all infrastructure compartments.

- **Signals & Telemetry**:
  - Tenancy-wide OCI Audit logs capturing every API invocation.
  - OCI service logs enabled for boundary resources (VCN flow logs, Load Balancer access logs, Object Storage read/write events).
- **OCI Services**: Logging, Identity and Access Management (IAM).
- **Governance Interlocks**:
  - Defined compartment hierarchy (`<COMPARTMENT_NAME>`) with standardized cost and ownership tags.
  - Dedicated log groups (`<LOG_GROUP_OCID>`) isolating security, audit, and operational logs.
  - Retention policies established for compliance (e.g. 90-day minimum audit retention).
- **Exit Criteria**: All production compartments have audit logs enabled and service logs routed to secured log groups.

---

## L1 — Metrics, Alarms, and Notification Routing

**Objective**: Detect operational anomalies and component failures in real time using metrics and automated alerts.

- **Signals & Telemetry**:
  - Core compute and platform metrics: CPU utilization, memory usage, disk I/O, network throughput.
  - Custom application metrics published to distinct namespaces via OCI Monitoring API.
- **OCI Services**: Monitoring, Notifications.
- **Operational Interlocks**:
  - Actionable MQL alarm rules configured with appropriate trigger delay (pending duration `PT3M`–`PT5M`).
  - Absence alarms configured to detect halted agents and stopped heartbeat streams.
  - Notifications topics configured with verified email, PagerDuty, Slack, or OCI Functions subscribers.
- **Exit Criteria**: Every critical workload has golden-signal alarms with documented runbooks and verified notification delivery.

---

## L2 — Log Analytics, Database Depth, and Pipelines

**Objective**: Centralize log parsing, conduct security analytics, isolate database bottlenecks, and forecast capacity.

- **Signals & Telemetry**:
  - High-volume application, syslog, and database logs ingested into OCI Log Analytics.
  - Active Session History (ASH) and AWR snapshots captured via Database Management.
- **OCI Services**: Log Analytics, Database Management, Operations Insights, Connector Hub.
- **Operational Interlocks**:
  - Log Analytics parsers configured for structured and semi-structured log sources.
  - Connector Hub pipelines reliably moving logs between storage and analytics.
  - Database Management Performance Hub enabled with private endpoint connectivity.
  - Operations Insights providing 90-day predictive capacity forecasts for storage and CPU.
- **Exit Criteria**: Log queries execute via OCL without unindexed scans; database wait events are visible in Performance Hub.

---

## L3 — Distributed Tracing, User Journeys, and SLOs

**Objective**: Track end-to-end request flow across distributed microservices, monitor user journeys, and enforce Service Level Objectives (SLOs).

- **Signals & Telemetry**:
  - OpenTelemetry distributed traces and spans correlated with Log Analytics logs.
  - Browser Real User Monitoring (RUM) measuring Core Web Vitals and client errors.
  - Synthetic HTTP and scripted browser checks testing availability from global vantage points.
- **OCI Services**: Application Performance Monitoring (APM), Synthetics.
- **Operational Interlocks**:
  - OpenTelemetry Collector exporting spans authenticated via `<APM_PRIVATE_DATAKEY>`.
  - Browser RUM configured using `<APM_PUBLIC_DATAKEY>`.
  - Service Level Indicators (SLIs) mapped to user journeys (e.g. 99% of checkouts < 1.5s).
  - Error budget burn rate alarms alerting on SLO degradation.
- **Exit Criteria**: All microservices report standardized `service.name` attributes; synthetic probes alert before customer impact.

---

## L4 — AIOps and AI-Agent Observability

**Objective**: Enable autonomous, closed-loop incident analysis, agentic operations, and machine-learning-assisted remediation within deterministic human guardrails.

- **The Closed-Loop Cycle**:
  1. **Instrument**: Comprehensive OTel telemetry and structured execution traces across agents and tools.
  2. **Collect**: High-throughput ingestion across APM, Log Analytics, and Monitoring.
  3. **Analyse**: Automated correlation of trace anomalies, log clusters, and database wait trees.
  4. **Evaluate**: Safe evaluation of proposed remediation actions against blast-radius models.
  5. **Act**: Execution of bounded, reversible operational workflows (e.g. scaling, restarting, cache invalidation).
- **Agent Tool Safety (MCP Safety Pattern)**:
  - Sanitize all query text through `sanitize_for_mcp` prior to running analytics tools.
  - Pass time ranges, compartments, and limits as separate structured arguments, never concatenated strings.
  - Strictly enforce read-only execution modes by default; require explicit approval for mutating operations.
- **Exit Criteria**: Automated remediation actions are audited, reversible, and accompanied by traceable evaluation evidence.

---

## Official Oracle Documentation

- [OCI Monitoring Service](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [OCI Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [OCI Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/home.htm)
- [OCI Database Management](https://docs.oracle.com/en-us/iaas/database-management/home.htm)
- [OCI Operations Insights](https://docs.oracle.com/en-us/iaas/operations-insights/home.htm)
- [OCI Connector Hub](https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm)
