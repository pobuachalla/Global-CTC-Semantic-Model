# CTC-011 approval and full replacement instructions

- **Approval:** CTC-011 Done — scoped at implementation-neutral logical relational level, explicit user instruction 2026-10-21.
- **New artifact:** `specifications/Global-CTC-Technical-Design-Specification-v0.1-DRAFT.md`. This is a working baseline, **not** a newly accepted schema or an approved CTC-019 task.
- **Source:** latest locally available CTC-014 full repository snapshot plus CTC-011 review ZIP. Live GitHub HEAD was not accessed.
- **Preserved:** all previously accepted decisions, 18 proposed field additions, FiscalContext A/B/C deferred, CTC-008 delegated.
- **Next:** CTC-012 persistence snapshots and lineage. CTC-019 is a proposed future backlog task only.

## Apply

Extract the archive into a separate folder and compare with your local repository before copying. From the repository root, run `git status`, `git diff --check`, `git diff`, then `git add .`, `git commit -m "docs(ctc-011): approve scoped logical relational model and start TDS"`, and `git push origin main`. Do not overwrite newer Git changes without review.
