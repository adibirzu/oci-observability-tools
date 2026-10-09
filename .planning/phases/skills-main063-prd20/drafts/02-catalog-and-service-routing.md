> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-002.md`. Statuses and counts in this file are not authoritative.

# Draft position 02: Capability catalog and deterministic service routing

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Map a natural-language observability job offline to the owning OCI O&M service, its owning skill and its registered official documentation.

## Scope

- catalog schema and the 12 required service ids
- ranking and ordering rules
- catalog_query CLI contract (--top, --json, --list, --validate)
- router skill content

## Non-goals

- skill reachability and overlap (position 17)
- live URL reachability (position 16)
- pricing (catalog stores a pointer note only)

## Source anchors

- PLAN.md §3 item 1 and job-to-service table; §4 catalog; §5 catalog_query (6628620, 7bcd39f)
- catalog/services.json (12 services, 27 doc entries, checkedAt 2026-10-09) and services.schema.json
- scripts/catalog_query.py; skills/oci-om-router/SKILL.md
- tests/test_catalog.py (5), tests/test_catalog_schema.py (3), tests/test_catalog_query.py (3), tests/test_doc_urls.py (3)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 2.1 | services.json validates against the schema; the 12 required ids are present and unique; doc keys are unique per service; skill directories exist; relatedServices resolve; pricingNote contains no currency amount. | LS | evidenced | test_catalog*, test_catalog_schema* |
| 2.2 | Five routing expectations hold: 'slow API traces' -> apm first; 'cpu alarm' -> monitoring first; 'AWR SQL regression' -> database-management or operations-insights in the top 2; 'route audit logs to SIEM' -> service-connector-hub or log-analytics in the top 2; 'prometheus scrape' -> management-agent in the top 2. | LS | evidenced | test_expected_routing |
| 2.3 | Ranking is deterministic and the CLI emits valid JSON with --json --validate. | LS | evidenced | test_order_is_deterministic, test_cli_json_and_validation |
| 2.4 | Every shipped skill is reachable from at least one catalog service 'skill' value or is declared an entry-point skill. | LS | not_evidenced | computed at 7bcd39f: 5 of 11 skills are no service's 'skill' value (oci-om-router, oci-apm-tracing, oci-monitoring-mql, oci-detections-sigma, oci-om-maturity); no test enforces reachability |
| 2.5 | All catalog documentation URLs return HTTP 200 on a dated check. | ON | not_evidenced | PLAN records a one-time curl check on 2026-10-09 with no receipt; Makefile linkcheck is an echo stub |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: catalog and routing tests pass.
- Catalog maturityLevels use only L0-L3; no service maps to L4.

## Unresolved tests and prerequisites

- 2.4 -> position 17.
- 2.5 -> position 16.
- Whether L4 (AIOps and agent observability) needs a service mapping is undecided.

## Dependencies

- 1 (skill contract)
- downstream: 15, 16, 17

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: no active writer observed on these paths (main 6628620 and branch 7bcd39f identical); PLAN.md and tests are on the PR-branch custody.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Fold the reachability finding into position 17 and keep this draft limited to the catalog and ranking contract.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- PLAN says remaining services 'map to the skill with the obvious name'; define an explicit rule now that eleven skills exist.
- State the ranking weights (keywords x3, use cases x2, signals x1) as normative, with the five expectations as the acceptance corpus.
