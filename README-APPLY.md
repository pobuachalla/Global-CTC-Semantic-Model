# CTC-003 T03 approved-policy update — application instructions

Date: 2026-10-20. Full replacement files, **not append fragments**.

1. In your local `Global-CTC-Semantic-Model` checkout, confirm the latest remote state: `git pull --ff-only`.
2. Compare these replacements with the repository versions before copying. They were composed from the latest local CTC-003 tax-decision baseline available to this session, **not from a live GitHub checkout**. Preserve any newer repository edits.
3. Replace root `BACKLOG.md`, `DECISIONS.md`, `FINDINGS.md`, `MODEL-BASELINE.md`, `SESSION-LOG.md` only after resolving any differences.
4. Copy the research documents under `research/CTC-003/`. Existing research files should not be deleted.
5. Run `git diff --check`, `git diff`, then `git add BACKLOG.md DECISIONS.md FINDINGS.md MODEL-BASELINE.md SESSION-LOG.md research/CTC-003/` and `git commit -m "docs(ctc-003): approve T03 logical monetary policy"`; `git push origin main`.

## Governance

T01/T02/T03 Accepted only within documented scope. D2 and P1-P7 unchanged. MonetaryBasis/MonetaryEffect candidate only. CTC-003 In Progress. No complete regulatory conformance claimed.
