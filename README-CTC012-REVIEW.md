# CTC-012 review baseline

CTC-012 is **Review**, not Done. PS-01..PS-12 remain **Proposed** pending explicit approval. All prior accepted decisions are preserved. `MODEL-BASELINE.md` is intentionally not amended with unapproved rules. No physical database, retention period or FiscalContext A/B/C option is selected.

Review `research/CTC-012/CTC-012-PERSISTENCE-SNAPSHOTS-AND-LINEAGE-DECISION-CANDIDATE.md`, `CTC-012-CLOSURE-REVIEW.md` and the test matrix. Run `python tests/CTC-012/validate_persistence_contract.py`.

Extract this complete snapshot into a clean Git worktree, compare to your local HEAD with `git diff`, and commit only after reviewing differences. This is a local baseline, not a live GitHub checkout.
