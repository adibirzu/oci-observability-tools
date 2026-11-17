# HANDOVER: skills-main063-prd20 planning phase

Prepared 2026-10-09T21:29:39Z (UTC). Resume document for this phase. Public-safe: absolute locations are shown as placeholders; exact bindings are in the private checkpoint.

## Identity and binding

| Field | Value |
|---|---|
| Task | skills-main063-prd20 (twenty distinct source-backed PRDs for oci-observability-tools) |
| Host / account | adi2 / adi |
| Author model | claude-sonnet-5-5 |
| Worktree | `<TASK_WORKTREE>` (isolated; binding in the private checkpoint) |
| Branch | fm/skills-main063-prd20 (local; created from the detached base; never pushed) |
| Acceptance baseline | current main 6628620 (662862029babf4acad6352ee5d83f4a79cd0f09b) |
| Alternate receipts only | unmerged PR #1 head 7bcd39f (7bcd39fceb1c4150ad14d8c375b356c5cf94d788) |

## Authority and lease history

1. Message 001: scope and communication rules (status lines only; private paths explicit; source limited to this phase until a lease).
2. Message 002: lease for a new `docs/prd/` directory. Superseded by message 003 before any file was created there; nothing exists under `docs/prd`.
3. Message 003 (authoritative): new `.planning/prds/PRD-001` to `PRD-020` plus `.planning/prds/README.md`, on current main, in this branch. This phase directory is retained with its drafts and provenance and now owns this handover.

Everything else is read-only for this phase: existing PRDs, code, tests, configuration, PLAN.md, AGENTS.md, the Haiku criteria phase and `docs/agent-handoff.md`.

## What exists

| Path | Role |
|---|---|
| `.planning/prds/README.md` | authoritative index, counts, legends, revision binding |
| `.planning/prds/PRD-001.md` to `PRD-020.md` | the 20 PRDs: 14 promotions of existing specifications, 6 documented gaps |
| `.planning/phases/skills-main063-prd20/PINS.json` | exact paths, bytes, SHA-256 and Git blob ids; first-10 and all-20 set digests |
| `.planning/phases/skills-main063-prd20/CHECKS.md` | count and pin verification recorded before the commit |
| `.planning/phases/skills-main063-prd20/cohort-index.md` | working index: reproduction, collisions, differences, next tasks, owner calls |
| `.planning/phases/skills-main063-prd20/drafts/` | superseded first-pass drafts kept as provenance (bannered; not authoritative) |

## Counts (one source of truth: the PRD files)

102 acceptance criteria across 20 PRDs. Current main (evidenced / partial / not evidenced / contradicted / proposed): 33 / 16 / 23 / 5 / 25. Unmerged PR #1 receipts (same order): 38 / 16 / 23 / 0 / 25. The earlier 38/16 and 37/17 figures mixed revisions and predated the manifest-test correction; they are retired. Counted toward the 10 or 20 thresholds: none.

Set digests (definition in PINS.json): first 10 = `c5b7fef73f6d97e09e60320c86eb91e71896962c1a2e2077e13d7f530cd2a9c6`; all 20 = `7bbb851db9e71a5b7d98e80ea73b08549cb67bbfe8109336226c4202c3a11568`.

## Evidence binding

- Current main passes 58 tests and fails ruff (34 errors); its build fails at package discovery; its CI run failed at the install step. These results are the baseline and appear in the Main column.
- PR #1 results (63 tests, ruff clean, four-job CI success) appear only in the PR #1 column as alternate receipts at that exact revision. They are not main acceptance.
- Local static results, provider CI, online documentation checks, authenticated harness runtime and OCI tenancy acceptance are separate evidence classes; none of the last three exists.

## Collisions and protected paths

- The canonical handover `docs/agent-handoff.md` is a protected packaging-owner path that exists only on the PR #1 branch. It was read through Git only. A value-free addendum for its separate delivery owner is prepared in the private records.
- The ignored local file `.claude/settings.local.json` makes the whole-worktree redaction check exit 1 in this worktree (PRD-005, criterion 5.3). It was left untouched and the scanner was not changed.
- The packaging owner's private checkpoint was not read.

## Open decisions (proposals; none implemented)

O-1 pin tool versions; O-2 whole-repository redaction test scope; O-3 exact-set skill test; O-4 keep or consolidate overlapping skills; O-5 intent of the unmapped Sigma examples; O-6 live-smoke run count and authorization; O-7 lag threshold; O-8 L4 service mapping. Owner: repository owner. Details are in the working index and in the proposals sections of the PRDs.

## Commit and receipt

After the final verification, one local commit of exactly the owned paths (`.planning/prds/` and this phase directory) provides the immutable review receipt. A committed file cannot contain its own commit id, so the commit id, tree ids and blob ids are recorded in the private checkpoint and the status file. To verify a commit: check that it touches only those paths, and compare each blob with PINS.json.

## Resume procedure

1. Read the private checkpoint, the status file and this document; run `git status` and `git log` and reconcile with the recorded commit.
2. Do not amend or add commits; the receipt must stay immutable. Changes to the PRDs need a new lease and a new receipt.
3. Wait for the supervisor to admit independent reviewers (Opus 5.5 for the first 10, Fable 5.1 for all 20). This lane creates no agents.
4. Record any review result only from the independent reviewer's own receipt.

## Not done, by design

No push, merge, cherry-pick, rebase or reset; no native or no-mistakes run; no agent creation; no live installation; no OCI or provider write; no scanner, test, contract or configuration change; no edit to the protected handover.

## Checkpoint log (actual UTC)

| UTC | Event |
|---|---|
| 2026-10-09T21:01:45Z | checkpoint 1: git reconciled, cohort designed |
| 2026-10-09T21:06:02Z | checkpoint 2: first private deliverables and preliminary drafts |
| 2026-10-09T21:29:39Z | checkpoint 3: canonical set under `.planning/prds` rebuilt with per-revision statuses; verified; ready for the single local commit |
