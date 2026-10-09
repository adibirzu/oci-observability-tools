# OCL field typing

OCL fields with spaces are single-quoted. Literal quoting follows the field's parsed type, not its appearance: string-typed identifiers such as `'Event ID'`, `'Logon Type'`, `'Response Code'`, and `'Status Code'` take quoted values, while numeric fields such as `'Source Port'` take unquoted values.

Examples:

```ocl
'Event ID' = '4625'
'Source Port' = 443
'Status Code' in ('200', '204')
```

Use the field definitions attached to the relevant Log Source as the authority. Custom parsers can expose different names and types.
