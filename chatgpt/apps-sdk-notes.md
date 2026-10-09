# Future ChatGPT Apps SDK notes

An optional future app could expose two read-only, offline tools:

- `catalog_query(question, top)` returning catalog-ranked services and registered documentation.
- `ocl_lint(query)` returning structured findings and never executing the query.

Version 1 deliberately ships no app or MCP server. Any future query execution integration must apply the controls in the uploaded MCP safety reference.
