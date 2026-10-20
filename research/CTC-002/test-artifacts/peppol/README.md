# CTC-002 D2 formal contract research package

Place this directory under `research/CTC-002/d2-formal-contract/` in the Git repository. It contains a proposed logical contract, a constructed Peppol BIS Billing 3.0 UBL fixture, a runnable focused mapping script, and generated output JSON. It does not replace authoritative project registers or imply any ADR approval.

Run `python validate_mapping.py` (requires `lxml`) to regenerate JSON and rerun the focused checks. Review report and proposed findings before incorporating into `FINDINGS.md` or `MODEL-BASELINE.md`.
