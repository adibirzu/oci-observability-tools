> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-009.md`. Statuses and counts in this file are not authoritative.

# Draft position 09: APM instrumentation and distributed tracing skills

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Teach correct OpenTelemetry/APM instrumentation, key handling, trace querying and synthetics with placeholder-only configuration.

## Scope

- data-key handling
- OTLP configuration shape
- trace-log correlation
- debug order
- Trace Explorer and synthetic guidance

## Non-goals

- live APM domain acceptance
- routing between the two skills (position 17)

## Source anchors

- PLAN.md §3 item 3 (full spec); item 10 at 7bcd39f is pointer-only (6628620 has no item 10)
- skills/oci-apm-otel/SKILL.md (46 lines); skills/oci-apm-tracing/SKILL.md (63 lines)
- references/otel-to-apm.md (19), references/apm-tracing.md (115); catalog service 'apm' (APM, APMOTEL, APMSYN)
- tests/test_harness_smoke.py; tests/test_skills_frontmatter.py

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 9.1 | Both skills cite only the registered APM, APMOTEL and APMSYN pages. | LS | evidenced | test_skills_official_docs_urls_registered, test_each_skill_uses_catalog_official_docs |
| 9.2 | Endpoints and keys appear only as <APM_DOMAIN_UPLOAD_ENDPOINT>, <APM_PRIVATE_DATAKEY>, <APM_PUBLIC_DATAKEY>. | LS | evidenced | redaction rules APM_ENDPOINT and SECRET_VALUE; test_skills_and_references_redaction_clean |
| 9.3 | The skills state that the private key never appears in browser code, that ingestion lag precedes any 'no data' conclusion, and follow the five-step debug order. | DOC | partial | present by inspection in oci-apm-otel, oci-apm-tracing and otel-to-apm.md; no keyword or structure test covers the APM skills (the deepened-content test covers five other skills) |
| 9.4 | The header and path shape in examples matches the APMOTEL page (PLAN §3.3: shape taken only from APMOTEL). | ON | not_evidenced | oci-apm-tracing hard-codes an Authorization header scheme in its workflow and example; it was not compared with the cited page in this lane |
| 9.5 | A boundary between oci-apm-otel and oci-apm-tracing is specified. | DOC | partial | both cite the same three pages; a single 'Related skills' clause is the only boundary |
| 9.6 | Spans from an instrumented sample appear in a live APM domain. | OCI | not_evidenced | out of v1 scope |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: related tests pass.

## Unresolved tests and prerequisites

- 9.4 needs an online doc check (position 16 mechanism).
- 9.6 deferred; 9.5 -> position 17.

## Dependencies

- 1, 2, 16
- downstream: 17

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/ and references/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Add a doc-conformance check task for the example header shape under position 16; draft the boundary statement.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Write the missing PLAN-level spec for oci-apm-tracing (currently pointer-only) so both skills have scope and acceptance.
