---
name: oci-stack-monitoring-agents
description: Monitor application stacks and hosts with OCI Stack Monitoring and Management Agent. Use when discovering resources such as WebLogic, hosts, or databases, installing agents, or collecting Prometheus metrics.
license: Apache-2.0
---
# OCI Stack Monitoring and agents

## When to use

Use for Management Agent installation and plugins, Stack Monitoring discovery/promotion, topology, baselines, and Prometheus scraping.

## Key concepts

Management Agent hosts service plugins and requires healthy connectivity, current plugins, and suitable permissions. Stack Monitoring discovers candidate resources, then promotes them into monitored resources and relationships. Topology connects application components; metrics support baselines and alarms. The Prometheus collection plugin can scrape configured endpoints and publish metrics to Monitoring.

## Workflow

1. Confirm supported platform, connectivity path, and least-privilege prerequisites.
2. Install the agent using placeholders and verify agent health.
3. Deploy required plugins, discover resources, inspect results, and promote deliberately.
4. Verify topology and metric freshness; add alarms for collection gaps.

## Pitfalls

Discovery does not imply promotion. A running process does not prove a healthy plugin. Check clock, certificates, endpoint reachability, plugin state, and ingestion lag before reinstalling.

## Examples

For a missing host, verify agent heartbeat and plugin status before repeating discovery. For Prometheus, start with one low-cardinality scrape target and confirm metrics in Monitoring.

## Official docs

- [Stack Monitoring](https://docs.oracle.com/en-us/iaas/stack-monitoring/home.htm)
- [Promotion and discovery](https://docs.oracle.com/en-us/iaas/stack-monitoring/doc/promotion-and-discovery.html)
- [Management Agent](https://docs.oracle.com/en-us/iaas/management-agents/home.htm)
- [Collect Prometheus metrics](https://docs.oracle.com/en-us/iaas/management-agents/doc/management-agents-collect-prometheus-metrics.html)

## Related skills

Use `oci-monitoring-alarms` for metrics and `oci-db-observability` for database depth.
