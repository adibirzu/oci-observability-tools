> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-003.md`. Statuses and counts in this file are not authoritative.

# Draft position 03: OCL authoring skill and offline linter with MCP query sanitizer

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Let assistants write OCL that follows documented Log Analytics conventions and make agent-driven query calls safe to forward to an MCP query tool.

## Scope

- OCL001-OCL009 rule table and severities
- lint JSON output shape
- sanitize_for_mcp rejections
- cookbook and skill example hygiene

## Non-goals

- live execution against Log Analytics
- Sigma conversion (position 4)

## Source anchors

- PLAN.md §3 item 2; §5 ocl_lint and sanitize_for_mcp; §8 item 10 (6628620, 7bcd39f)
- skills/oci-ocl-queries/SKILL.md (46 lines); references/ocl-cookbook.md (25 ocl blocks), ocl-field-typing.md, mcp-safety.md
- scripts/ocl_lint.py (rules OCL001-OCL009); tests/test_ocl_lint.py; tests/fixtures/ocl/{good,bad}

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 3.1 | Each rule OCL001-OCL009 fires on at least one failing fixture and is silent on at least one passing fixture. | LS | evidenced | test_each_rule_fires, test_clean_variants |
| 3.2 | All 25 ocl blocks in references/ocl-cookbook.md and all ocl blocks in skills lint with zero errors. | LS | evidenced | test_all_documented_ocl_blocks_lint_clean |
| 3.3 | sanitize_for_mcp collapses whitespace and raises ValueError on ';', backticks, control characters, length over 8000 and unbalanced quotes or parentheses. | LS | partial | test_sanitize_for_mcp passes; per-condition case coverage was not enumerated in this lane |
| 3.4 | The CLI exits 1 on any error finding and --json emits {rule, severity, col, message, fix}. | LS | partial | owner handover reports a negative-exit check on installed artifacts; the JSON field set is not asserted by a test read here |
| 3.5 | Cookbook queries and typing rules are accepted by a live Log Analytics service. | OCI | not_evidenced | out of v1 scope (PLAN §1 non-goals: no live tenancy access); the rules encode documented conventions |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: all OCL lint and sanitizer tests pass.

## Unresolved tests and prerequisites

- 3.3 and 3.4 need explicit assertions (code lease).
- 3.5 requires an authenticated OCI tenancy and is deferred by design.

## Dependencies

- 1
- downstream: 4, 18

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: PLAN.md/scripts/tests on PR-branch custody; skills/ and references/ unchanged.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P2: Specify the lint output contract and rule-id stability policy; propose JSON-shape and per-condition sanitizer assertions.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Define what 'correct OCL' means: convention conformance (testable offline) versus service acceptance (not testable here).
- Move the rule table out of PLAN §5 into this document and version it.
