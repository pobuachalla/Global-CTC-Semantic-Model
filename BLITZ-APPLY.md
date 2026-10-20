# Apply this full snapshot

This package contains a **full repository working snapshot** assembled from the 2026-10-20 consolidated project archive and the subsequent Draft 1.1 test. It is **not** a live GitHub checkout.

Review the updated root registers (`BACKLOG.md`, `DECISIONS.md`, `FINDINGS.md`, `MODEL-BASELINE.md`, `SESSION-LOG.md`) and new `research/CTC-003/CTC-003-BLITZ-BATCH-DECISION-REVIEW.md` and `tests/validate_batch_edge_cases.py` before copying. Preserve any newer GitHub edits. Do not delete repository files absent from this archive.

From repository root: `git status`, `git diff --check`, `git diff`, `git add -A`, `git commit -m "docs(ctc-003): approve batch logical constraints and record blitz tests"`, `git push origin main`.

Run tests: `python tests/validate_batch_cardinality.py` and `python tests/validate_batch_edge_cases.py`.
