---
name: oci-detections-sigma
description: Convert Sigma detection rules into OCI Log Analytics OCL and schedule them as detection alerts. Use when porting SIEM detections, building MITRE-tagged hunts, or validating detection queries.
license: Apache-2.0
---
# Sigma Detections for OCI Log Analytics

## When to use

Use when translating open-source Sigma detection rules into OCI Log Analytics Query Language (OCL), authoring MITRE ATT&CK-aligned threat detection rules, porting SIEM rules to OCI, or scheduling recurring automated detection alerts in Log Analytics.

## Key concepts

OCI Log Analytics allows scheduled query-based alerting on detected events:

### Sigma Rule Translation
- **Field & Type Mapping**: Sigma fields translate deterministically to OCL field names using the [Sigma to OCL field map](../../references/sigma-field-map.md).
- **String vs. Numeric Quoting**: String fields with numeric appearance (e.g. `'Event ID' = '4625'`) must use quoted string literals. True numeric fields (e.g. `'Source Port' = 443`) require unquoted literals.
- **Modifiers**: Modifiers like `|contains`, `|startswith`, and `|endswith` convert to OCL `like` expressions with `*` wildcards. `|re` maps to OCL `matches`.
- **Logsource Identification**: Maps to `'Log Source'` filters (such as `'Windows Security Events'`, `'Windows Sysmon Operational Logs'`, `'Linux Secure Logs'`, `'OCI Audit Logs'`).

### Aggregation and Detection Alerts
- **Eligibility Requirement**: In OCI Log Analytics, only queries containing statistical aggregations (`| stats ... | where ...`) can be saved and scheduled as automated detection alerts.
- **Aggregation Tail**: Sigma rules specifying `count() > N` produce a `| stats count as Count by '<Field>' | where Count > N` pipeline. The converter marks these with `requires_aggregation: true`.
- **Non-Aggregating Queries**: Queries lacking aggregation are treated as ad-hoc interactive hunt queries rather than recurring scheduled alerts.

### Metadata Preservation
- **MITRE ATT&CK Tags**: Tags such as `attack.execution` or `attack.t1059` pass through directly to output metadata for SIEM/SOC mapping.
- **False Positives**: Known benign conditions noted in Sigma rules pass through to alert documentation runbooks.

## Workflow

1. Author or acquire a reviewed Sigma YAML detection rule.
2. Run the offline translation tool: `python scripts/sigma_to_ocl.py rule.yml --json`.
3. Inspect output warnings, verifying that all field names, log sources, and types match target Log Analytics definitions.
4. Validate the resulting query with the query linter: `python scripts/ocl_lint.py query.ocl --json`.
5. Execute the query interactively in OCI Log Analytics over a historical test window to assess false positive rates.
6. If the query includes an aggregation tail, save the query and create a scheduled detection alert; map the Sigma `timeframe` to the alert schedule frequency.

## Pitfalls

- Scheduling non-aggregating queries: Log Analytics requires an aggregation stage (`| stats ...`) for automated alert scheduling.
- Misinterpreting timeframe: Sigma `timeframe` specifies the detection window; do not inject relative time filters directly into the OCL query body.
- Schema variance: Sigma field names are conventions; always verify that custom Log Source parsers in your tenancy produce matching field labels.
- Leading wildcard performance: avoid beginning an OCL query with `'Original Log Content' like '*x*'` without preceding indexed filters.

## Examples

```ocl
# Brute-force login detection converted from Sigma
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625' 
| stats count as Count by 'Source IP' 
| where Count > 5
```

```ocl
# Suspicious PowerShell execution with encoded command
'Log Source' = 'Windows Sysmon Operational Logs' and 'Parent Process Name' like '*powershell.exe' and 'Command Line' like '*-enc*'
```

## Official docs

- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [OCL command reference](https://docs.oracle.com/en-us/iaas/log-analytics/doc/command-reference.html)
- [Create alerts for detected events](https://docs.oracle.com/en-us/iaas/log-analytics/doc/create-alerts-detected-events.html)

## Related skills

Use `oci-ocl-queries` for OCL language semantics and `oci-logging-pipelines` for telemetry ingestion paths.
