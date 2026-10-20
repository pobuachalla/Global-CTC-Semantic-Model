# Pick up tomorrow — Global CTC Semantic Model

**Checkpoint:** 2026-10-20 (end of day)  
**Authoritative status:** Local Git-ready replacement snapshot, not yet pushed to GitHub.

## Approved baseline
- CTC-001: Done — scoped reconciliation.
- CTC-002: Done — scoped D2 logical contract; P1–P7 and I-01–I-10 accepted.
- CTC-003: Done — scoped detailed logical entity dictionary. Its 51-entity closure candidate and approved logical policies form the current accepted logical foundation.
- T01–T03, D01–D03, L01–L10, qualified C09, B01–B10 and G2 logical directions remain accepted within their recorded scopes.

## Explicitly not approved / deferred
- Eighteen additional field contracts from later research are proposals only.
- FiscalContext A/B/C physical aggregation, database/persistence design, provider-specific rules and complete regulatory fixture validation are deferred.
- Historical draft versions in `research/` are evidence, not competing authoritative schemas.

## Next task: CTC-004 — Validate tax and monetary semantics
1. Read `MASTER-PROMPT.md`, `BACKLOG.md`, `DECISIONS.md`, `MODEL-BASELINE.md` and the approved CTC-003 dictionary.
2. Reuse existing T01–T03 evidence and test scripts; do not restart tax design or create unnecessary new drafts.
3. Produce one bounded acceptance matrix for multi-regime tax, withholding, signed amounts, reconciliation, currency and precision.
4. Clearly distinguish existing synthetic passes from unverified real fixtures.
5. Seek scoped approval of CTC-004 only after its backlog acceptance criteria are assessed.

## Restart prompt
> Start CTC-004 using the latest GitHub baseline. Verify accepted CTC-001/002/003 decisions, reuse T01–T03 test evidence, identify only material gaps in multi-regime tax, withholding, signed values, reconciliation and precision. Produce one consolidated validation matrix and a scoped closure recommendation. Do not reopen the approved D2 logical contract or treat proposed field additions as accepted.

## Git update
Extract this ZIP into the local repository root. Review `git status`, `git diff --check` and `git diff` before committing. If your repository has newer changes, reconcile them instead of overwriting blindly. The ChatGPT Project attachments do not automatically synchronize with GitHub.
