> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-001.md`. Statuses and counts in this file are not authoritative.

# Draft position 01: Skill authoring contract and bundle integrity

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Give every shipped skill one validated shape so each harness loads a small, predictable body and linked references never dangle.

## Scope

- frontmatter keys and name rules
- body section order
- size limits
- reference-link and official-docs URL resolution
- enumeration of the shipped skill set

## Non-goals

- correctness of a skill's subject matter (positions 3, 4, 9-14)
- routing between skills (position 17)

## Source anchors

- PLAN.md §2 'SKILL.md contract' (6628620, 7bcd39f)
- PLAN.md §3 intro and §10 item 2 (skill count: 9 at 6628620, 11 at 7bcd39f)
- tests/test_frontmatter.py, tests/test_skills_frontmatter.py (9 tests), tests/test_skill_size.py

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 1.1 | All 11 skills/*/SKILL.md have frontmatter keys within {name, description, license}; name equals the directory and matches ^oci-[a-z0-9-]+$; description is 60-1024 characters and contains 'Use when'. | LS | evidenced | tests pass at 7bcd39f (63 passed, scratch reproduction) |
| 1.2 | Each body keeps the PLAN section order: When to use, Key concepts, Workflow, Pitfalls, Examples, Official docs, Related skills. | LS | evidenced | test_skills_section_order, test_frontmatter |
| 1.3 | Every SKILL.md is under 500 lines (observed maximum 78); AGENTS.md and GEMINI.md under 150 lines (observed 61); chatgpt/instructions.md under 8000 characters (observed 1457). | LS | evidenced | test_skill_size, test_skills_size_limits |
| 1.4 | Every ../../references/*.md link resolves and every Official-docs URL is registered in catalog/services.json. | LS | evidenced | test_skills_reference_links_resolve, test_skills_official_docs_urls_registered |
| 1.5 | The specification's stated skill count equals the shipped count. | DOC | partial | PLAN says 9 at 6628620 (stale; 11 shipped); PLAN says 11 at 7bcd39f. Correct on the unmerged PR branch only. |
| 1.6 | PROPOSED: the skill-set test asserts the exact expected set rather than a lower bound. | LS | proposed | current test asserts len >= 11 plus two required names; an unregistered 12th skill or a silent rename would pass |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: pytest 63 passed; ruff 0.17.0 clean.
- 6628620 scratch extract: pytest 58 passed.

## Unresolved tests and prerequisites

- Criterion 1.6 needs a source-owner decision and a code lease (tests are read-only here).
- PLAN section 3 items 10-11 (oci-apm-tracing, oci-monitoring-mql) are pointer-only: no description, scope or citation spec.

## Dependencies

- none upstream
- downstream: 2, 7, 17

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: skills-packaging-r9 (open PR #1, head 7bcd39f) for paths that branch changed.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Request the canonical-placement lease; promote this draft; ask the source owner whether 1.6 is accepted.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Replace the stale '9 skills' acceptance line on main by the PR-branch '11' wording (PLAN.md is read-only here).
- Add specification content for the two pointer-only skills so the contract covers all eleven.
