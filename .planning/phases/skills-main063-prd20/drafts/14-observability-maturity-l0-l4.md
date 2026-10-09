> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-014.md`. Statuses and counts in this file are not authoritative.

# Draft position 14: Observability maturity model L0-L4

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Let a team assess its current observability level and plan the next, with evidence required before awarding a level.

## Scope

- level definitions and per-level services/interlocks checklists
- MCP safety pattern pointer
- assessment workflow

## Non-goals

- scoring automation
- live tenancy assessment

## Source anchors

- PLAN.md §3 item 9 and level table (6628620, 7bcd39f)
- skills/oci-om-maturity/SKILL.md (75 lines); references/maturity-l0-l4.md (109 lines)
- catalog maturityLevels (values L0-L3 only); tests/test_skills_frontmatter.py (keyword presence)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 14.1 | The skill and reference define L0, L1, L2, L3 and L4 with the headings 'L0 - Foundations and Governance' and 'L4 - AIOps and AI-Agent Observability' and the 'MCP Safety Pattern' section. | LS | evidenced | keyword-presence assertions |
| 14.2 | The skill cites the registered MON, LA, APM, DBM, OPSI and SCH pages only. | LS | evidenced | docs registration tests |
| 14.3 | The workflow requires verifiable evidence before awarding a tier. | DOC | evidenced | workflow step by inspection; not machine-checked |
| 14.4 | Catalog maturityLevels are consistent with the level model, including L4. | LS | not_evidenced | no catalog service lists L4; no test relates the catalog to the level definitions |
| 14.5 | Checklists were rewritten from the originating Atlas source. | DOC | not_evidenced | PLAN cites an external source tree that this lane cannot read; provenance is unverifiable here |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: related tests pass.

## Unresolved tests and prerequisites

- 14.4 needs a source-owner decision about L4 service mapping.
- 14.5 provenance cannot be checked from this lane.

## Dependencies

- 1, 2, 3 (MCP safety pattern)
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills/ and references/ unchanged between revisions.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P3: Decide how L4 relates to catalog services and record it in the PRD.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Replace the provenance statement by a testable requirement or drop it from acceptance.
