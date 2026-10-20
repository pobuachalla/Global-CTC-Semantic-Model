# Global CTC Semantic Model — Initial Git Baseline

**Prepared:** 2026-10-20
**Purpose:** One self-contained initial repository snapshot.

## Precedence and provenance
- Root governance files `BACKLOG.md`, `DECISIONS.md`, `FINDINGS.md`, `MODEL-BASELINE.md`, `SESSION-LOG.md` are from the **2026-10-20 approved-principles update**, superseding the overlapping 2026-10-19 evening checkpoint copies.
- Root `MASTER-PROMPT.md`, `PROJECT-INSTRUCTIONS.md`, and `README.md` come from the 2026-10-19 evening checkpoint.
- `research/` holds six historical working research reviews, **not accepted ADRs**.
- `checkpoints/` holds historical manifests, pick-up notes, and the 2026-10-20 decision checkpoint; these are archival.
- `references/` contains available source specifications; source drafts are not approved model baselines.

## Approved state
- CTC-002-P1 through P6: **Accepted as architectural principles only**.
- FiscalContext A (embedded), B (independent), C (hybrid): **all deferred/open**.
- CTC-001: Review; CTC-002: Review/evidence-gated; CTC-003: Todo.
- No approved final semantic schema or fiscal-context cardinality.

## Missing evidence
- Verified paired pre/post-certification CFDI samples.
- Paired FatturaPA and SdI response samples.
- Raw French Extended CTC fixture with applicable versioned schema/profile validation.
- Demonstrated need for multiple fiscal interpretations of one immutable billing revision.

## Updating the repository
1. Read root governance files before each task.
2. Produce proposed changes, then obtain explicit approval for ADR acceptance.
3. Commit updated files with task ID and summary.
4. Record new session outcomes in `SESSION-LOG.md`.
5. Never treat research drafts as accepted decisions.

## Initial commit
`git add . && git commit -m "chore: establish CTC semantic model baseline through 2026-10-20" && git push origin main`
