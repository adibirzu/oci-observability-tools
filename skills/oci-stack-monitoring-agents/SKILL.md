---
name: oci-stack-monitoring-agents
description: Monitor application stacks and hosts with OCI Stack Monitoring and Management Agent. Use when discovering resources such as WebLogic, hosts, or databases, installing agents, or collecting Prometheus metrics.
license: Apache-2.0
---
# OCI Stack Monitoring and Management Agents

## When to use

Use when deploying OCI Management Agents to virtual machines or bare metal hosts, discovering application components (WebLogic domains, Oracle Databases, Apache Tomcat, hosts), managing topology maps, evaluating metric baselines, or scraping Prometheus endpoints into OCI Monitoring.

## Key concepts

OCI Stack Monitoring and Management Agent provide a unified host-and-stack observability framework:

### Management Agent Framework
- **Agent Architecture**: Lightweight, modular Java daemon deployed on hosts or compute instances.
- **Plugin Model**: Dynamically hosts capability plugins (e.g. Stack Monitoring plugin, Database Management plugin, Logging Analytics plugin).
- **Security & Identity**: Authenticates with OCI using an agent install key (`<AGENT_INSTALL_KEY>`) tied to a specific compartment (`<COMPARTMENT_OCID>`).
- **Health & Heartbeat**: Management Agent sends periodic beacons to the control plane; heartbeats indicate daemon liveness and plugin status.

### Stack Monitoring Capabilities
- **Discovery and Promotion**: Discovers components (WebLogic Server clusters, JVMs, database instances, OS hosts) via agent inspection. Discovered candidates must be promoted to monitored resources to begin telemetry ingestion.
- **Topology Mapping**: Automatically generates hierarchical dependency graphs showing relationships between hosts, middleware, and databases.
- **Baselines & Anomaly Detection**: Calculates metric baselines over historical windows (e.g. typical Monday morning CPU load) and detects deviation anomalies without static thresholds.

### Prometheus Metrics Collection
- Management Agents host a dedicated Prometheus collection plugin.
- Scrapes Prometheus-formatted metrics (`/metrics`) from microservices, Kubernetes nodes, or third-party exporters.
- Automatically pushes scraped telemetry into OCI Monitoring under custom metric namespaces.

## Workflow

1. Generate an agent install key in the target compartment (`<COMPARTMENT_OCID>`) with a bounded lifetime and usage limit.
2. Download and install the Management Agent package on the host; configure `input.rsp` with the install key.
3. Verify agent status and confirm that the Stack Monitoring plugin is successfully deployed and active.
4. Initiate a discovery job in Stack Monitoring specifying the target resource type and host credentials.
5. Review discovery results and promote candidate resources into monitored stack assets.
6. Verify topology link rendering and configure baseline alarms for promoted components.
7. To scrape Prometheus metrics, configure the Prometheus plugin scraper target URL (`http://127.0.0.1:9090/metrics`) and destination namespace.

## Pitfalls

- Discovery does not automatically promote: discovered resources do not ingest telemetry or trigger alarms until explicitly promoted.
- Running agent process does not guarantee plugin health: an active `mgmt_agent` process may fail to communicate if firewalls block HTTPS outbound to OCI endpoints.
- Time drift between host OS and NTP servers causes signature verification failures during agent registration.
- High-cardinality Prometheus labels cause metric throttling when pushed into OCI Monitoring; filter labels in the scrape configuration.
- Missing IAM policies preventing the agent dynamic group from uploading metrics.

## Examples

```text
# Agent verification command on target host
sudo systemctl status oracle-cloud-agent || sudo /opt/oracle/mgmt_agent/agent_sys/ManagementAgent/bin/status.sh
```

```text
# Prometheus plugin scrape configuration snippet
scrape_configs:
  - job_name: 'custom_exporter'
    scrape_interval: 1m
    static_configs:
      - targets: ['127.0.0.1:9100']
```

## Official docs

- [Stack Monitoring](https://docs.oracle.com/en-us/iaas/stack-monitoring/home.htm)
- [Promotion and discovery](https://docs.oracle.com/en-us/iaas/stack-monitoring/doc/promotion-and-discovery.html)
- [Management Agent](https://docs.oracle.com/en-us/iaas/management-agents/home.htm)
- [Collect Prometheus metrics](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agents-collect-prometheus-metrics.html)

## Related skills

Use `oci-monitoring-alarms` for metric alarms and notifications, and `oci-db-observability` for database depth.
