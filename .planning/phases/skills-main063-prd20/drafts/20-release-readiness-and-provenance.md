> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-020.md`. Statuses and counts in this file are not authoritative.

# Draft position 20: Release readiness and provenance for v0.1.0

Status: AUTHOR DRAFT (New source-backed gap draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Define when the declared 0.1.0 may be called released, how each PLAN §10 item is dispositioned with evidence, and which actions need explicit owner approval.

## Scope

- disposition table for the ten §10 items
- release checklist and receipts
- approval gates for tag, release and visibility

## Non-goals

- performing the release
- any provider write (this lane performs none)

## Source anchors

- PLAN.md §9 T16 (tag v0.1.0; public visibility only after explicit owner approval) and §10 acceptance ledger (all ten items unchecked)
- CHANGELOG.md: version 0.1.0 is source metadata; tag/release pending; no tags or releases observed (owner handover)
- No release workflow exists under .github/workflows (ci.yml only)

## Why this is a new PRD

PLAN T16 and section 10 name the tag and visibility actions in single sentences. No release readiness specification or disposition record exists.

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 20.1 | Each of the ten PLAN §10 items is recorded as met (with evidence reference), waived by the owner with reason, or deferred with a dated reason. | DOC | proposed | all ten boxes are unchecked at both revisions |
| 20.2 | Versions in pyproject and the three manifests agree and match the intended tag. | LS | partial | test_manifests asserts agreement across the three plugin manifests only; pyproject is not compared and the tag intent is not recorded |
| 20.3 | Full-history secret scan, link-liveness and live harness results are attached as receipts (positions 5, 16, 15). | DOC | proposed | none of the three exist yet |
| 20.4 | Tag creation, release publication and visibility change each have recorded explicit owner approval before execution. | DOC | proposed | PLAN requires owner approval for visibility; tag/release approval is implied |
| 20.5 | The CHANGELOG moves Unreleased content under 0.1.0 with its date only after 20.1-20.4. | DOC | proposed | CHANGELOG currently keeps Unreleased |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- Provider read: tag and release listings were empty per owner handover (not re-read here).

## Unresolved tests and prerequisites

- Owner approvals; dependencies on positions 5, 8, 15, 16; PR #1 merge.

## Dependencies

- 5, 8, 15, 16
- downstream: none

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: CHANGELOG/PLAN on PR-branch custody.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P3: Hold until dependencies produce receipts; then draft the disposition table.
