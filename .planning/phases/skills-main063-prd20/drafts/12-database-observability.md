> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-012.md`. Statuses and counts in this file are not authoritative.

# Draft position 12: Database observability with Database Management and Operations Insights

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Help choose between Database Management and Operations Insights and diagnose or forecast Oracle Database behavior.

## Scope

- basic versus full Database Management
- enablement prerequisites (private endpoint or management agent)
- Performance Hub with ASH and AWR concepts
- SQL insights and capacity forecasting
- decision matrix

## Non-goals

- live database access
- pricing statements

## Source anchors

- PLAN.md §3 item 6 (6628620, 7bcd39f)
- skills/oci-db-observability/SKILL.md (73 lines); catalog services database-management, operations-insights
- tests/test_skills_frontmatter.py::test_deepened_skills_content_and_concepts (keyword presence)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 12.1 | The skill names Database Management, Operations Insights, Performance Hub, ASH, AWR and Capacity Planning. | LS | evidenced | keyword-presence assertions |
| 12.2 | The skill cites only DBM, DBMPH, OPSI and OPSICAP pages. | LS | evidenced | docs registration tests |
| 12.3 | The skill contains a decision matrix, the enablement prerequisites and a basic-versus-full comparison. | DOC | partial | present by inspection (decision matrix and prerequisites sections); only keyword presence is machine-checked |
| 12.4 | No price or currency amount appears in the skill text. | LS | partial | the pricing test scans catalog pricingNote only; skill text is not scanned for currency amounts |
| 12.5 | The guidance is accepted against a live Database Management or Operations Insights deployment. | OCI | not_evidenced | out of v1 scope |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: related tests pass.

## Unresolved tests and prerequisites

- 12.4 needs a currency scan over skill text (code lease).
- 12.5 deferred.

## Dependencies

- 1, 2
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P3: Restate the decision matrix as numbered acceptance criteria.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Port the item-6 bullet list from PLAN into numbered criteria with evidence classes.
