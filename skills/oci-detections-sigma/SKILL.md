---
name: oci-detections-sigma
description: Convert Sigma detection rules into OCI Log Analytics OCL and schedule them as detection alerts. Use when porting SIEM detections, building MITRE-tagged hunts, or validating detection queries.
license: Apache-2.0
---
# Sigma detections for OCI Log Analytics

## When to use

Use for the supported Sigma subset, deterministic OCL generation, MITRE-tagged hunts, and detection-alert preparation.

## Key concepts

The converter maps Sigma fields, types, modifiers, and logsources using [the shared field map](../../references/sigma-field-map.md). Unknown fields remain quoted and produce warnings. Aggregation tails produce `stats` plus `where` and set `requires_aggregation`; only aggregating queries are eligible as scheduled searches. MITRE tags and false-positive notes pass through to output.

## Workflow

1. Author a synthetic or reviewed Sigma rule.
2. Run `python scripts/sigma_to_ocl.py rule.yml --json`.
3. Review warnings, field names, types, logsource, false positives, and MITRE tags.
4. Run `python scripts/ocl_lint.py query.ocl --json`.
5. Test over a short external time window before scheduling.

## Pitfalls

Sigma fields are conventions, not tenant schemas. A `timeframe` becomes the schedule interval rather than an OCL predicate. Non-aggregating searches are hunts, not scheduled detection searches. Never import unreviewed third-party rules wholesale.

## Examples

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625' | stats count as Count by 'Source IP' | where Count > 5
```

## Official docs

- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [OCL command reference](https://docs.oracle.com/en-us/iaas/log-analytics/doc/command-reference.html)
- [Detected-event alerts](https://docs.oracle.com/en-us/iaas/log-analytics/doc/create-alerts-detected-events.html)

## Related skills

Use `oci-ocl-queries` for query semantics and `oci-logging-pipelines` for source ingestion.
