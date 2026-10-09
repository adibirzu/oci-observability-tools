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


---

# Sigma to OCI Log Analytics (OCL) Field Mapping Reference

This reference documents the deterministic translation from Sigma detection rule specifications to OCI Log Analytics Query Language (OCL).

## Field Translation Table

Sigma fields map to canonical OCL fields and their corresponding data types:

| Sigma Field | Canonical OCL Field | OCL Data Type | Quoting & Literal Syntax |
|---|---|---|---|
| `EventID` | `'Event ID'` | string | Quoted literal: `'Event ID' = '4625'` |
| `Image` | `'Process Name'` | string | Wildcard search: `'Process Name' like '*cmd.exe'` |
| `ParentImage` | `'Parent Process Name'` | string | Wildcard search: `'Parent Process Name' like '*powershell.exe'` |
| `CommandLine` | `'Command Line'` | string | Substring search: `'Command Line' like '*-enc*'` |
| `User`, `AccountName` | `'Principal Name'` | string | Exact match: `'Principal Name' = 'SYSTEM'` |
| `TargetUserName` | `'Target User'` | string | Exact match: `'Target User' = 'admin'` |
| `SourceIp` | `'Source IP'` | string | String IP match: `'Source IP' = '198.51.100.10'` |
| `DestinationIp` | `'Destination IP'` | string | String IP match: `'Destination IP' = '203.0.113.5'` |
| `SourcePort` | `'Source Port'` | number | Unquoted number: `'Source Port' = 443` |
| `DestinationPort` | `'Destination Port'` | number | Unquoted number: `'Destination Port' = 8080` |
| `LogonType` | `'Logon Type'` | string | Quoted literal: `'Logon Type' = '3'` |
| `QueryName` | `'Query Name'` | string | Regex match: `'Query Name' matches '^cdn\\.'` |

> [!NOTE]
> Field names in OCL that contain spaces must always be single-quoted. String-typed numeric identifiers such as `'Event ID'`, `'Logon Type'`, and `'Response Code'` must be compared against single-quoted string literals. Numeric fields such as `'Source Port'` take unquoted numeric literals.

## Modifier Translation Table

Sigma value modifiers translate to specific OCL comparison operators:

| Sigma Modifier | Example Sigma Syntax | Generated OCL Expression |
|---|---|---|
| *(none / exact)* | `Image: 'malware.exe'` | `'Process Name' = 'malware.exe'` |
| `\|contains` | `CommandLine\|contains: 'download'` | `'Command Line' like '*download*'` |
| `\|startswith` | `Image\|startswith: 'C:\\Users\\'` | `'Process Name' like 'C:\\Users\\*'` |
| `\|endswith` | `Image\|endswith: '.ps1'` | `'Process Name' like '*.ps1'` |
| `\|re` | `CommandLine\|re: 'regex_pattern'` | `'Command Line' matches 'regex_pattern'` |
| `\|contains\|all` | `CommandLine\|contains\|all: ['-enc', 'bypass']` | `('Command Line' like '*-enc*' and 'Command Line' like '*bypass*')` |
| List with exact match | `EventID: ['4624', '4625']` | `'Event ID' in ('4624', '4625')` |
| List with wildcards | `Image\|contains: ['mimikatz', 'procdump']` | `('Process Name' like '*mimikatz*' or 'Process Name' like '*procdump*')` |

## Logsource Mappings

The rule logsource determines the generated `'Log Source'` clause:

| Sigma Product / Service | Target OCI Log Source | Generated OCL Filter |
|---|---|---|
| `windows/security` | Windows Security Events | `'Log Source' = 'Windows Security Events'` |
| `windows/sysmon` | Windows Sysmon Operational Logs | `'Log Source' = 'Windows Sysmon Operational Logs'` |
| `linux/auth` | Linux Secure Logs | `'Log Source' = 'Linux Secure Logs'` |
| `oci/audit` | OCI Audit Logs | `'Log Source' = 'OCI Audit Logs'` |

If an unmapped logsource is specified, the converter outputs `'Log Source' = '<LOG_SOURCE>'` and emits a warning.

## Aggregation and Scheduled Searches

Sigma rules utilizing `count() [by Field] > Threshold` with a `timeframe` specification produce an aggregation tail:

```ocl
# Example: Detect brute-force login attempts
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625'
| stats count as Count by 'Source IP'
| where Count > 5
```

- **`requires_aggregation: true`**: In OCI Log Analytics, only aggregating searches (queries containing `| stats ... | where ...`) are eligible to be scheduled as automated detection alerts.
- **Timeframe Mapping**: The Sigma `timeframe` parameter (e.g. `15m`, `1h`) maps directly to the scheduled alert execution frequency and evaluation window in OCI Log Analytics, rather than being injected into query text.

## Offline Conversion Workflow

Convert and validate detection rules using the offline repository tooling:

```bash
# 1. Convert Sigma YAML rule to OCL JSON structure
python scripts/sigma_to_ocl.py path/to/rule.yml --json

# 2. Validate OCL query syntax and typing rules
python scripts/ocl_lint.py path/to/query.ocl --json
```
