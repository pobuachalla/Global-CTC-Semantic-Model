# CTC-006 approved Git replacement — 2026-10-21

This is a **full repository snapshot** based on the locally available CTC-005 approved archive, overlaid with CTC-006 closure records and evidence. It is not a live GitHub checkout.

## Application
1. Extract into a temporary folder and compare against your local Git repository before replacing files.
2. Preserve any newer local or remote changes; merge conflicts deliberately.
3. Run `python tests/CTC-006/test_ctc006.py`, `git diff --check`, and review `git diff`.
4. Commit and push after review: `git add .`, `git commit -m "docs(ctc-006): approve scoped identity and correction constraints"`, `git push origin main`.

## Approved
CTC-001 through CTC-006 Done — scoped; C006-01..03 logical constraints accepted. CTC-007 is next. All previous approvals remain unchanged. Eighteen additional fields remain Proposed and FiscalContext A/B/C physical aggregation remains Deferred.
