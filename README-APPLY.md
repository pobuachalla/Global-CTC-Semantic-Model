# Apply CTC-003 Scoped Closure

This package contains **full replacement versions** of the five root project registers and the approved scoped dictionary under `research/CTC-003/`. It is not an entire repository replacement.

1. Extract at the root of your local GitHub checkout, retaining paths.
2. Review `git diff --check` and `git diff` before staging. The source baseline was the latest available CTC-003 Draft 1.9 full snapshot; merge any newer local changes rather than overwriting them.
3. Run `git add BACKLOG.md DECISIONS.md FINDINGS.md MODEL-BASELINE.md SESSION-LOG.md research/CTC-003/`.
4. Run `git commit -m "docs(ctc-003): approve scoped detailed logical dictionary"` and `git push origin main`.

No remote repository modifications were made here.
