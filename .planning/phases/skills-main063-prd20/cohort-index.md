# skills-main063-prd20 working index

Prepared 2026-10-09T21:29:10Z (UTC). Working material for the authoritative set in `.planning/prds/`. Author drafts only; no review, implementation or provider acceptance is claimed.

## Reproduction (scratch extracts outside the worktree, offline)

- Current main 6628620: pytest 58 passed; ruff 0.17.0 reports 34 errors; gen_oracle_docs --check, build_chatgpt --check, redaction_check and shellcheck exit 0; `python -m build` fails at package discovery (flat layout).
- Unmerged PR #1 head 7bcd39f: pytest 63 passed (2 setuptools deprecation warnings); ruff clean; the same four checks exit 0.
- Provider reads (read-only): main push run 37930343836 failed at step 'pip install -e .[dev]'; PR #1 runs 37969214474 (pull_request) and 37969210915 (push) at 7bcd39f succeeded on all four test jobs; run 37963585765 at 6229bc9 failed on the gitleaks credential input; repository visibility public, 0 tags, 0 releases.
- Tool versions were installed by this lane and are not project-pinned.
- Not run and not evidenced anywhere: live harness loading, online link check, full-history secret scan, any OCI tenancy action.

## Collisions

- Worktree 2 was allocated on a detached HEAD at 6628620 with no branch. Local branch fm/skills-main063-prd20 was created from that head; nothing was pushed.
- The owner branch fm/skills-packaging-r9 (PR #1, head 7bcd39f) is 4 commits ahead of main. Per the lease, current main is the acceptance baseline; PR #1 results are labelled alternate receipts and are not merged, cherry-picked or rebased.
- The canonical handover docs/agent-handoff.md exists only on the PR #1 branch and is a protected packaging-owner path. It was read through Git only and was not edited or copied; a value-free addendum for its delivery owner is prepared privately.
- An earlier lease (message 002) named docs/prd/. Message 003 superseded it with .planning/prds/ before any docs/prd file was created. Nothing under docs/prd exists.
- Ignored local file .claude/settings.local.json makes the repository's whole-worktree redaction check exit 1 in this worktree. It is not a repository defect and was left untouched.
- The packaging owner's private checkpoint and evidence receipts were not read; only the committed handover and Git/provider reads were used.

## Differences from the Haiku criteria index (support input, not authority)

- Criteria index (6628620): PLAN says 9 skills while 11 ship. Confirmed on main (PRD-001 criterion 1.5); PR #1 fixes it.
- Criteria index: main CI cause unclassified. Classified here: push run 37930343836 failed at step 'pip install -e .[dev]' on ubuntu 3.10 and the other three jobs were cancelled; the build failure reproduces locally (flat-layout package discovery).
- Criteria index R-A7: temporary-HOME round trip not run. It is exercised by test_install_then_uninstall_restores_tree (PRD-006).
- Criteria index: ruff reports 34 errors on main. Reproduced; ruff is clean on the PR #1 head.
- Criteria index: the whole-repository redaction test fails on a local file. Reproduced in this worktree (PRD-005, criterion 5.3).
- Earlier cohort summary counts (38 evidenced / 16 partial) mixed PR #1 and main results and predated the manifest-test correction. All counts are now computed once per revision from this set.

## Considered and not included

- Safety-rule conformance checker for skill examples: Latent: no OCI CLI command examples exist in skills or references, and MUTATES appears only in README setup lines, so the AGENTS.md rules are vacuously satisfied today. Revisit when command examples are added.
- Future Apps SDK or MCP server tools (catalog_query, ocl_lint): Deferred by design in chatgpt/apps-sdk-notes.md and the PLAN non-goals; not an unmet gap.
- Windows installer path: No source states a need.
- One PRD per skill (11): Would duplicate PRD-009 to PRD-014 and inflate the count; skills are grouped by capability.
- docs/agent-handoff.md as a PRD: Handover record, not a product specification.

## Prioritized next tasks

1. P1 PRD-001: Owner decision on the exact-set test (1.6); fold the two later skills into the contract after the source documents settle. Owner: repository owner.
2. P1 PRD-002: Keep this PRD to the catalog and ranking contract; route the reachability finding to PRD-017. Owner: this lane (owned planning paths only).
3. P1 PRD-005: Owner decides the whole-repository test scope; a full-history scan receipt is requested only when scanning is authorized. Owner: repository owner.
4. P1 PRD-007: Define the adapter contract as a table (harness, asset, identity fields, freshness check) bound to the revision it was checked at. Owner: this lane (owned planning paths only).
5. P1 PRD-008: Keep each evidence row labelled by revision; owner decides pinning; do not treat PR-head receipts as main acceptance. Owner: repository owner.
6. P1 PRD-009: Draft the boundary statement and a doc-conformance check task for the example header shape, owned by PRD-016. Owner: this lane (owned planning paths only).
7. P1 PRD-015: Owner reviews the record schema and run-count proposal; no harness run is executed. Owner: repository owner.
8. P1 PRD-016: Owner accepts or rejects the proposal; define the receipt format before any implementation request. Owner: repository owner.
9. P1 PRD-017: Owner accepts the keep-with-boundaries recommendation or chooses consolidation. Owner: repository owner.
10. P2 PRD-003: Propose JSON-shape, exit-code and per-condition sanitizer assertions as tests-to-add for the source owner. Owner: repository owner.
11. P2 PRD-004: Write the normative supported-Sigma subset and list the 'or' and 'all of them' cases to assert. Owner: this lane (owned planning paths only).
12. P2 PRD-006: Specify 6.4 and 6.5 as tests-to-add; defer 6.7 to PRD-015. Owner: repository owner.
13. P2 PRD-010: Define N or mark it operator-chosen; propose a fixture-based CloudEvents example check as a test-to-add. Owner: repository owner.
14. P2 PRD-011: Write scope and acceptance for oci-monitoring-mql and a boundary statement versus oci-monitoring-alarms. Owner: this lane (owned planning paths only).
15. P2 PRD-018: Owner states whether the two unmapped examples are intentional; draft the mapping table from documentation. Owner: repository owner.
16. P2 PRD-019: Extract the grammar from the registered MQL page into this PRD before proposing rule ids. Owner: this lane (owned planning paths only) after owner acceptance.
17. P3 PRD-012: Restate the decision matrix as numbered acceptance criteria. Owner: this lane (owned planning paths only).
18. P3 PRD-013: Review the discovery step wording against the credentials rule and record the outcome. Owner: repository owner.
19. P3 PRD-014: Record how L4 relates to catalog services once the owner decides. Owner: repository owner.
20. P3 PRD-020: Hold until dependencies produce receipts; then draft the disposition table. Owner: repository owner.

## Owner calls (proposals with recommendations; none implemented)

- **O-1** (repository owner): Pin lint and test tool versions (PRD-008). Recommendation: pin.
- **O-2** (repository owner): Whole-repository redaction test scope: tracked files (recommended) or physical worktree (PRD-005). The scanner is not weakened by this set.
- **O-3** (repository owner): Accept an exact-set skill test instead of a lower bound (PRD-001, criterion 1.6).
- **O-4** (repository owner): Keep the two overlapping skill pairs with written boundaries (recommended) or consolidate (PRD-017).
- **O-5** (repository owner): Are the dns and network Sigma examples intentional unmapped negatives (PRD-018)?
- **O-6** (repository owner): Live-smoke run count per harness and authorization for real installs and provider runs (PRD-015, criterion 15.2).
- **O-7** (repository owner): Define or delegate the lag alert threshold N (PRD-010, criterion 10.3).
- **O-8** (repository owner): Should L4 map to catalog services (PRD-002, PRD-014)?
- **O-9** (Firstmate supervisor): Resolved by the supervisor: canonical lease for .planning/prds and the phase directory on current main (message 003).
