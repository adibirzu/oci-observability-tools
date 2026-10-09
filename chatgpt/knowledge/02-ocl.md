---
name: oci-ocl-queries
description: Author and debug OCI Log Analytics query language (OCL) searches. Use when writing, fixing, or optimizing Log Analytics queries, stats, timestats, link, or saved searches.
license: Apache-2.0
---
# OCI Log Analytics OCL

## When to use

Use for interactive searches, saved searches, parsing checks, aggregations, and query optimization in Log Analytics.

## Key concepts

Quote multi-word fields: `'Log Source'`. String-typed numeric fields take quoted literals (`'Event ID' = '4625'`, including Logon Type, Response Code, and Status Code); true numeric fields do not (`'Source Port' = 443`). Use `in ('a', 'b')` for sets and `*` with `like`.

Set time outside OCL through API or CLI `time-start` and `time-end`, or the UI picker. Always scope to the compartment subtree with `--compartment-id-in-subtree true` or `compartment_id_in_subtree=True`.

Commands include `stats`, `timestats`, `link`, `eval`, `where`, `sort`, `head`, and `fields`. See [field typing](../../references/ocl-field-typing.md) and the [cookbook](../../references/ocl-cookbook.md).

## Workflow

1. Choose the Log Source and external time range.
2. Filter indexed fields first.
3. Add pipeline stages one at a time.
4. Run `python scripts/ocl_lint.py query.ocl --json`.
5. Test over a short window before saving or scheduling.

## Pitfalls

Putting a time predicate in OCL is incorrect. Omitting subtree scope silently misses child compartments. Avoid starting with `'Original Log Content' like '*x*'`; constrain an indexed field first. Do not assume parsed field types.

## Examples

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625' | stats count as Count by 'Principal Name' | sort -Count
```

## Official docs

- [Log Analytics](https://docs.oracle.com/en-us/iaas/log-analytics/home.htm)
- [Query and search](https://docs.oracle.com/en-us/iaas/log-analytics/doc/query-search.html)
- [OCL command reference](https://docs.oracle.com/en-us/iaas/log-analytics/doc/command-reference.html)

## Related skills

Use `oci-detections-sigma` for rule conversion and `oci-logging-pipelines` for ingestion.


---

# OCL field typing

OCL fields with spaces are single-quoted. Literal quoting follows the field's parsed type, not its appearance: string-typed identifiers such as `'Event ID'`, `'Logon Type'`, `'Response Code'`, and `'Status Code'` take quoted values, while numeric fields such as `'Source Port'` take unquoted values.

Examples:

```ocl
'Event ID' = '4625'
'Source Port' = 443
'Status Code' in ('200', '204')
```

Use the field definitions attached to the relevant Log Source as the authority. Custom parsers can expose different names and types.


---

# OCL cookbook

Set the time window outside query text and scope searches to the compartment subtree. Adapt field names to the selected Log Source.

## Windows

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' = '4625'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Event ID' in ('4624', '4625') | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'Windows Security Events' and 'Logon Type' = '10' | fields 'Principal Name', 'Source IP'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Process Name' like '*powershell*'
```

```ocl
'Log Source' = 'Windows Sysmon Operational Logs' and 'Parent Process Name' like '*service*' | head 50
```

## Linux

```ocl
'Log Source' = 'Linux Secure Logs' and 'Principal Name' = 'root'
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Original Log Content' like '*authentication failure*'
```

```ocl
'Log Source' = 'Linux Secure Logs' | stats count as Count by 'Principal Name' | sort -Count
```

```ocl
'Log Source' = 'Linux Secure Logs' and 'Source IP' = '192.0.2.10'
```

```ocl
'Log Source' = 'Linux Secure Logs' | timestats count as Count by 'Principal Name'
```

## OCI Audit

```ocl
'Log Source' = 'OCI Audit Logs' | stats count as Count by 'Principal Name'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Response Code' = '401'
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Status Code' in ('400', '403')
```

```ocl
'Log Source' = 'OCI Audit Logs' | fields 'Principal Name', 'Source IP' | head 100
```

```ocl
'Log Source' = 'OCI Audit Logs' and 'Original Log Content' like '*Delete*'
```

## VCN flow logs

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination Port' = 443
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Source Port' = 53
```

```ocl
'Log Source' = 'VCN Flow Logs' | stats count as Count by 'Source IP'
```

```ocl
'Log Source' = 'VCN Flow Logs' and 'Destination IP' = '198.51.100.7'
```

```ocl
'Log Source' = 'VCN Flow Logs' | link 'Source IP', 'Destination IP'
```

## OKE

```ocl
'Log Source' = 'Kubernetes Container Logs' and 'Original Log Content' like '*error*'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Log Source'
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | eval Category = 'application' | fields Category
```

```ocl
'Log Source' = 'Kubernetes Container Logs' | stats count as Count by 'Status Code' | where Count > 5
```

```ocl
'Log Source' in ('Kubernetes Container Logs', 'OCI Audit Logs') | stats count as Count by 'Log Source'
```
