> SUPERSEDED preliminary draft (first pass, single status per criterion, not split by revision). Authoritative source: `.planning/prds/PRD-007.md`. Statuses and counts in this file are not authoritative.

# Draft position 07: Cross-harness adapters and generated bundles (Claude, Codex, Gemini/Antigravity, ChatGPT)

Status: AUTHOR DRAFT (Existing-specification promotion draft). Not reviewed, not accepted and not counted toward any review threshold. Nothing here implies implementation, deployment or provider acceptance.

Identifier: none. The cohort position is an index, not a PRD identity; the repository owner assigns identifiers on canonical adoption.

Source revisions: main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b); open PR #1 branch fm/skills-packaging-r9 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788).

Author: skills-main063-prd20 (claude-sonnet-5-5). Any reviewer must differ from the author.

## Purpose

Present the same skill pack, disclaimer and routing rule to each supported harness with generated files that cannot drift.

## Scope

- manifest identity agreement
- generated GEMINI.md and ChatGPT knowledge freshness
- disclaimer parity
- offline routing smoke over shipped assets

## Non-goals

- harness runtime loading (position 15)
- future Apps SDK tools (documented as deferred)

## Source anchors

- PLAN.md §6 (6628620, 7bcd39f)
- .claude-plugin/{plugin,marketplace}.json; .codex-plugin/plugin.json; gemini-extension.json; GEMINI.md; CLAUDE.md
- chatgpt/{instructions,conversation-starters,apps-sdk-notes}.md; chatgpt/knowledge (11 skill bundles + services.json)
- scripts/build_chatgpt.py; tests/test_manifests.py (1), test_chatgpt_bundle.py (4), test_harness_smoke.py (1)

## Acceptance criteria

| ID | Criterion | Class | Status | Evidence |
|---|---|---|---|---|
| 7.1 | All manifests parse; name, version, license and the 'Not an Oracle product' description agree across the Claude plugin, Codex plugin and Gemini extension manifests, and also agree with pyproject (PLAN §7). | LS | partial | test_manifests_parse_and_agree asserts the three manifests (plus repository URLs and the Codex skills directory) but does not read pyproject.toml; pyproject version 0.1.0 matches by inspection only |
| 7.2 | build_chatgpt.py --check exits 0: 11 skill bundles plus services.json match their sources; regeneration is deterministic; an unregistered source skill and a stale extra bundle both fail. | LS | evidenced | test_chatgpt_bundle.py (4 tests); 7bcd39f only (6628620 emits 9 bundles) |
| 7.3 | GEMINI.md and AGENTS.md have heading parity; the disclaimer appears in chatgpt/instructions.md. | LS | evidenced | test_disclaimer_and_heading_parity |
| 7.4 | The common prompt routes to APM and the APMOTEL page is cited in the skill and in the ChatGPT bundle. | LS | evidenced | test_harness_smoke (asset and routing check only) |
| 7.5 | Each harness loads the assets and a live loaded-agent answer routes to APM. | RT | not_evidenced | no loaded-agent result exists; owner handover and CHANGELOG state T16 is open |

Class and status vocabularies are defined in the cohort index.

## Evidence available

- 7bcd39f scratch extract: bundle and manifest tests pass; build_chatgpt.py --check rc 0.
- At 6628620 the ChatGPT bundle omits the two later skills (9 files); fixed on the PR branch only.

## Unresolved tests and prerequisites

- 7.5 -> position 15. Antigravity runtime acceptance is excluded by the owner.
- 7.1: PLAN §7 requires manifests to agree with pyproject; the test does not read pyproject (test-to-add, needs a code lease).

## Dependencies

- 1, 2
- downstream: 15

## Owner and custody

- Product decisions: repository owner (no recorded decision for this PRD).
- Source custody: chatgpt/knowledge, GEMINI.md, manifests, tests on PR-branch custody.
- Draft author: skills-main063-prd20 (claude-sonnet-5-5).

## Prioritized next task

P1: Define the adapter contract as a table (harness, asset, identity fields, freshness check) and bind it to 7bcd39f.

## Revisions needed to make the existing specification reviewable

- No document identifier exists. Identifiers are assigned by the repository owner on canonical adoption; the cohort position is only an index.
- The source is a section of PLAN.md, which mixes plan, task list and acceptance ledger. Extract it into a single-capability document and keep PLAN.md as the ledger.
- Add an explicit problem statement, user and non-goals per capability; PLAN states purpose only at repository level.
- Number every criterion and attach an evidence class. PLAN section 10 has ten coarse checkboxes, all unchecked at both revisions.
- Bind the document to a source revision. Two revisions are in play: main 6628620 and the open PR branch 7bcd39f.
- Describe the four adapters as one numbered requirement list; PLAN §6 is prose bullets.
- Record explicitly that offline asset checks are not harness acceptance.
