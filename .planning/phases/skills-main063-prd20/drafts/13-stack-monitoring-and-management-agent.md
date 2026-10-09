> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-013.md`. Statuses and counts in this file are not authoritative.

# Draft position 13: Stack Monitoring and Management Agent operations

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Guide agent installation, resource discovery and promotion, topology, baselines and Prometheus collection.

## Scope

- agent plugin model and health
- discovery versus promotion
- topology and baselines
- Prometheus scraping into Monitoring
- agent troubleshooting

## Non-goals

- live discovery runs
- host credential handling (never requested)

## Source anchors

- PLAN.md §3 item 7 (6628620, 7bcd39f)
- skills/oci-stack-monitoring-agents/SKILL.md (75 lines); catalog services stack-monitoring, management-agent
- tests/test_skills_frontmatter.py::test_deepened_skills_content_and_concepts (keyword presence)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 13.1 | The skill names Management Agent, Stack Monitoring, plugin, topology and Prometheus. | LS | evidenced | keyword-presence assertions |
| 13.2 | The skill cites only SM, SMDISC, MA and MAPROM pages. | LS | evidenced | docs registration tests |
| 13.3 | The skill states that discovery does not promote resources and that promotion is needed before telemetry ingestion or alarms. | DOC | evidenced | present at the Pitfalls section by inspection; not asserted by a test |
| 13.4 | The workflow never asks for host credentials; discovery steps refer to credentials only as operator-held. | DOC | partial | workflow step 4 mentions host credentials for a discovery job; no check enforces the 'never request credentials' rule on skill text |
| 13.5 | The guidance is accepted on a live host and stack. | OCI | not_evidenced | out of v1 scope |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: related tests pass.

## Unresolved tests and prerequisites

- 13.4 needs wording review against AGENTS.md safety rules; 13.5 deferred.

## Dependencies

- 1, 2
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P3: Review the discovery step wording against the credentials rule and record the outcome.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Number the PLAN item-7 bullets as criteria; add evidence classes.
