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
