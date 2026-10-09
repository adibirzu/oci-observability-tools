> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-017.md`. Statuses and counts in this file are not authoritative.

# Draft position 17: Skill routing completeness, overlap boundaries and routing corpus

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Make sure every skill can be selected deterministically, overlaps have written boundaries, and routing quality is measured on a corpus larger than five phrases.

## Scope

- reachability rule and test
- boundary statements
- routing evaluation corpus and thresholds

## Non-goals

- merging or deleting skills (an owner decision this PRD only frames)
- live assistant behavior (position 15)

## Source anchors

- catalog/services.json 'skill' values vs skills/ (computed at 7bcd39f): 5 of 11 skills unreachable via the catalog
- Overlapping skill pairs cite identical documentation sets: oci-apm-otel/oci-apm-tracing and oci-monitoring-alarms/oci-monitoring-mql
- AGENTS.md skill index; PLAN.md §4 'rest map to the skill with the obvious name'; tests/test_catalog_query.py (5 expectations)

## Why this is a new PRD

No document addresses skill reachability or overlap. The catalog contract predates the two later skills and the router relies on an 'obvious name' rule.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 17.1 | A test enumerates skills/ and fails when a skill is neither some catalog service's 'skill' nor declared an entry-point or cross-cutting skill. | LS | proposed | today 5 of 11 are neither mapped nor declared |
| 17.2 | Each overlapping pair carries a boundary sentence in both skills' 'When to use' and in the AGENTS.md index. | DOC | proposed | boundaries are single 'Related skills' clauses today |
| 17.3 | PROPOSED corpus: at least 2 phrasings per skill (22 total) with an expected owning skill; a routing function returns the expected skill first for at least 90 percent (threshold is an owner choice). | LS | proposed | current evidence is 5 phrases and service ids, not skills |
| 17.4 | The catalog or a router table exposes the skill choice (not only the service) for each query in the corpus. | LS | proposed | catalog_query already prints a skill field per service |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Reproduced with a read-only script over catalog/services.json and skills/ at 7bcd39f.

## Unresolved tests and prerequisites

- Owner decision: keep both overlapping skills with boundaries (recommended) or consolidate.
- Choice of threshold in 17.3.

## Dependencies

- 1, 2, 9, 11
- downstream: 15

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: catalog, tests and AGENTS.md; AGENTS.md/tests on PR-branch custody.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Present the reachability finding and the keep-with-boundaries recommendation for source-owner acceptance.
