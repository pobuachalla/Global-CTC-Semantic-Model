# CTC-005 — Approved scoped closure (2026-10-21)

This is a complete repository replacement based on the latest available CTC-005 kickoff snapshot, **not a live GitHub checkout**. All historical source and research files in that snapshot are retained. The five authoritative registers are complete replacement files.

## Status
- CTC-001..005: Done — scoped.
- CTC-005: seven-step extension decision tree and JP-01..JP-10 accepted **only** at logical-governance level.
- 18 additional CTC-003 field contracts remain Proposed. FiscalContext physical A/B/C, country conformance, production package registry, cross-deployment replay and CTC-007 compatibility remain deferred.
- Next: **CTC-006**, party identity, snapshots, commercial identity and correction/reference semantics. Do not reopen D2.

## Apply
1. Back up or commit your existing Git working tree.
2. Extract the ZIP into the repository root (not into a nested folder), preserving paths.
3. Review `git status`, `git diff --check`, and `git diff`. The snapshot is not a live merge; preserve any newer local changes.
4. Run the two CTC-005 tests if desired: `python tests/CTC-005/test_governance.py` and `python tests/CTC-005/test_focused.py`.
5. `git add .`; `git commit -m "docs(ctc-005): approve scoped jurisdiction governance"`; `git push origin main`.

No automatic GitHub push or project synchronization has occurred.
