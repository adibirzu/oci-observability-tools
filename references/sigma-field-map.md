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
