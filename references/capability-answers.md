# Answering OCI observability capability questions

Use this guide after service routing. For a simple question, a recommendation and an official capability reference can be enough. For a multi-service operator question, include the following:

1. **Recommendation and reason**: Name the service for each requested job and explain its signal. Avoid listing the whole portfolio.
2. **Capabilities and boundaries**: Distinguish collection, transport, storage, query, visualization, alerting, and response. Explain manual correlation prerequisites; do not promise automatic correlation.
3. **Prerequisites and assumptions**: Identify instrumentation, agents, source enablement, IAM, connectivity, parsing, subscriptions, or data history as applicable. Ask only for missing details that change the recommendation; never request credentials.
4. **Bounded next step**: Offer a read-only check or an offline draft with placeholders. Keep scope, time window, subtree, and row limits in structured query arguments. Mark mutating examples `# MUTATES` and pair OCI commands with official documentation.
5. **Validation and failure modes**: Define expected evidence and what absent data means. Include notification firing and recovery checks when relevant. Describe retention, volume, and sampling implications without inventing prices or limits.
6. **References and evidence**: Link the official page beside the capability it supports, rather than supplying only a product homepage. Identify whether the answer is code-backed, configured, locally verified, provider verified, release accepted, unverified, or unavailable. Use only the evidence actually observed.

## Selecting references

Start with `catalog/services.json`, then open only the relevant skill and its directly linked references. Treat local references as authoring aids. Check current Oracle documentation for protocols, authentication, query syntax, IAM, supported sources, regional availability, limits, and pricing. A catalog date or successful URL fetch does not establish correctness of every feature claim.

If current documentation cannot be reached, say which claim remains unverified and give the registered official reference. Do not invent an endpoint, field, API, or CLI flag to fill a gap.

## Multi-signal routing

A question about slow requests, related application logs, and availability has three jobs: tracing, log analysis, and probing. Rank focused questions separately rather than treating the top three keyword matches to the whole prompt as an architecture. Reconcile the results against service boundaries and the user's existing collection paths.

For example, APM traces require instrumentation and propagation. Trace-to-log correlation requires emitted identifiers and parsed log fields. An availability probe must reach the target from its selected vantage point. Each path needs its own validation; success in one does not prove the others.

## Comparing answers with and without the pack

README demonstrations are illustrative unless they have captured run evidence. A capable assistant without this pack can still give a correct, well-referenced answer. The pack supplies reusable routing, safety rules, references, and offline checks; it does not guarantee a quality gain.

For a measured comparison:

- Use two fresh sessions with the same model/version, exact prompt, settings, browsing and tool access, and response budget. Change only whether the pack and its repository instructions are loaded. Do not run the baseline inside a workspace that automatically loads this pack.
- Record run date, actual skill loading, full responses, and opened sources. Repeat runs to account for output variation. Redact all receipts before sharing.
- Score both responses against the same criteria: service choice, capability boundaries, prerequisites, actionable next step, validation, claim-specific references, and honest evidence status. Check technical accuracy before crediting detail or length.
- Report observed differences and limitations. Passing offline helper tests is not a model comparison or live OCI acceptance.

### Scoring sheet

Score each criterion independently for both responses. A response earns `2` only when the point is correct and supported by the captured answer; extra detail without support does not increase the score. Use `N/A` only when the criterion truly does not apply, and explain why.

| Criterion | 0 — absent or incorrect | 1 — partial | 2 — complete and supported |
|---|---|---|---|
| Service routing | Wrong service or no useful mapping | Main service named, but a requested signal is missed | Each requested job maps to the right service with a reason |
| Capability boundaries | Blends services or claims unsupported automation | Some distinctions present | Collection, analysis, correlation, alerting, and response are clearly separated as relevant |
| Prerequisites | Omits a prerequisite that changes feasibility | Names some prerequisites | Names the material instrumentation, source, IAM, connectivity, or data requirements |
| Bounded next step | Unsafe, vague, or unbounded | Actionable but missing a key bound | Read-only or offline-first step with explicit scope and limits |
| Validation and failure handling | No test or treats missing data as proof | Validation exists but leaves ambiguous outcomes | Defines expected evidence and plausible failure interpretations |
| Official references | Missing, irrelevant, or mismatched citations | Relevant general reference, but claims lack direct support | Current official reference is attached to each material capability claim |
| Evidence status | Presents assumptions as verified facts | Some uncertainty is labeled | Clearly separates documentation, local, provider, and unavailable evidence |

Sum only comparable numeric criteria (maximum 14 points per answer), but publish the criterion-level paired results too. Have a reviewer check factual correctness before scoring; this rubric measures answer coverage and evidence discipline, not truth by itself. Keep source citations in the score record so reviewers can audit each `2`.

### Run-record template

Copy one record per response. Keep the prompt byte-for-byte identical within a pair. Store the full response and source list in the private evaluation workspace; only publish sanitized material that contains no tenant output, credentials, private topology, or customer identifiers.

```yaml
run_id: <opaque-run-id>
pair_id: <same-id-for-baseline-and-skill-run>
prompt_id: <stable-prompt-name>
condition: baseline | skill
run_date_utc: <timestamp>
model_and_version: <exact-model-version>
generation_settings: <temperature-and-response-budget>
tools_and_browsing: <same-for-both-conditions>
loaded_skills: []
opened_sources: []
response_artifact: <sanitized-path-or-private-reference>
scores:
  service_routing: 0
  capability_boundaries: 0
  prerequisites: 0
  bounded_next_step: 0
  validation_and_failure: 0
  official_references: 0
  evidence_status: 0
reviewer_accuracy_check: pending | pass | fail
notes: <brief, evidence-linked explanation>
```

For each prompt, publish the paired scores, number of repetitions, scoring method, and limitations. Do not claim a measured skill uplift until real paired runs and factual review are complete. Do not include a tenant query or live MCP result unless the test was authorized, sanitized, and clearly labeled as provider-verified evidence.
