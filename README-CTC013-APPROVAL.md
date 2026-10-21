# CTC-013 approved scoped closure — 2026-10-21

This is a **full repository replacement** assembled from the latest locally available full CTC-008 kickoff snapshot plus the explicitly approved CTC-013 logical lifecycle decision and its bounded test evidence. It is **not a live GitHub checkout**.

## Approved
- CTC-013 Done — scoped; CL-01–CL-08 Accepted at logical-policy level.
- All earlier accepted decisions remain accepted and unchanged.
- CTC-008 remains In Progress with delegated fixture collection.

## Not approved
- Detailed authority response schemas, physical event storage, legal-status rules, provider-specific correlation/precedence, API contracts.
- Eighteen proposed CTC-003 field contracts; FiscalContext A/B/C physical design.

## Apply safely
1. Back up the local repository or create a branch.
2. Extract the archive into the repository root (preserve directories).
3. Review `git status`, `git diff --check`, and `git diff`; merge any newer local changes rather than overwriting them.
4. Run `python tests/CTC-013/test_lifecycle.py` and verify the result.
5. Commit and push only after review.

Suggested commit: `docs(ctc-013): approve scoped compliance lifecycle policy`.

## Next
Start CTC-014: normalize authority responses and correlation/evidence for client consumption, building on accepted CL-01–CL-08.
