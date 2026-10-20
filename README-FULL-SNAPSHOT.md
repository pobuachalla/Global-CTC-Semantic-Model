# Global CTC Semantic Model — Full Git-Ready Snapshot

Snapshot assembled 2026-10-20 from locally available baseline and subsequent project checkpoints. **This is not a live GitHub checkout.** Compare against your repository before replacing files.

## Precedence

- Root `BACKLOG.md`, `DECISIONS.md`, `FINDINGS.md`, `MODEL-BASELINE.md`, `SESSION-LOG.md` come from the latest CTC-003 batch-separation approved checkpoint.
- Other root instructions and reference materials come from the original GitHub baseline.
- Research contains cumulative historical drafts, reports and tests. These are evidence, **not automatically accepted designs**.
- `research/historical-variants/` contains differing same-name artifacts where both versions were preserved rather than silently overwritten.

## Governance state

- CTC-001 and CTC-002: Done at approved scoped closure. CTC-003: In Progress.
- Approved: D2 logical contract; P1–P7; I-01–I-10; T01–T03 logical policies; D01–D03 and associated invariants; L01–L10; CTC-003-BATCH-01 logical separation.
- **Not approved:** B01–B10, C09 conditional cardinalities, detailed entity schemas, FiscalContext A/B/C physical design and unverified regulatory fixture conformance.

## Applying to your existing local Git repository

1. Back up or commit any outstanding local changes.
2. Copy the *contents* of this extracted directory into your repository root (not the enclosing directory).
3. Run `git status`, `git diff --check`, `git diff` and inspect changes.
4. Do not overwrite newer GitHub work without reconciling differences.
5. Commit and push only after review.

Example PowerShell commands from repository root:

```powershell
git status
git diff --check
git add .
git commit -m "docs: consolidate full CTC baseline through CTC-003 batch approval"
git push origin main
```

This archive contains source DOCX/XLSX references, but some referenced upstream materials may still be unavailable. It does not contain an actual Git history or remote commits.
