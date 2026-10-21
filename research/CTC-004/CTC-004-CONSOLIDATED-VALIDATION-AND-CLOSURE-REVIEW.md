# CTC-004 — Consolidated Tax and Monetary Validation / Closure Recommendation

**Date:** 2026-10-21  
**Status:** Review — scoped closure recommended; user approval pending  
**Baseline:** End-of-day project baseline dated 2026-10-20; live GitHub not verified.

## Decision guardrails
CTC-001, CTC-002, CTC-003 remain Done — scoped. D2, P1–P7, I-01–I-10, T01–T03 and later accepted logical decisions are unchanged. The 18 proposed CTC-003 field additions are not accepted. FiscalContext physical aggregation remains deferred.

## Consolidated validation matrix

| ID | Capability | Evidence | Assessment | Deferred limitations |
|---|---|---|---|---|
| V01 | Multi-regime tax applications and summary | New MG-004-01 12/12; three synthetic tax regimes, separately grouped, no duplicate inclusion of asserted summaries | Supported — focused | Country-specific tax bases, ordering, compounding and certified fixtures (CTC-008/010) |
| V02 | Withholding | Prior T01–T03 sign and T03 decision suites | Supported — focused | Verified authority withholding payload (CTC-008/010) |
| V03 | Signed values and credit polarity | Prior sign suite and contribution contract | Supported — focused | Jurisdiction-specific credit presentation (CTC-010) |
| V04 | Inclusive/exclusive basis | Prior extended monetary and decision suites | Supported — focused | Complete inclusive unit-price fixture (CTC-008/010) |
| V05 | Source-versus-calculated summaries | Prior extended suite plus new MG-004-01 source assertions | Supported — focused | Country tolerance (CTC-005) |
| V06 | Multi-currency controls | Prior extended suite | Supported — focused | Official FX rule, source and evidence (CTC-005/010) |
| V07 | Precision, rounding and stage | New MG-004-02 11/11: fractional rates, currency quantization, half-up/half-even, line/aggregate difference, per-unit tax | Supported — focused | Effective-dated jurisdiction rules, tolerance (CTC-005/007) |
| V08 | Missing calculation inputs | Prior T03 suite and new MG-004-02 `NOT_EVALUABLE` guards | Supported — focused | Downstream error representation (CTC-014) |
| V09 | Source/derived provenance | D2 logical replay, existing T03 tests | Supported logically | Immutable production profile packages (CTC-007) |

## Executed tests
Existing evidence replayed in previous CTC-004 pass: **66/66 assertions** across four overlapping suites (5, 24, 16, 21). Current execution: **23/23** assertions in `tests/test_remaining_gaps.py`, exact `decimal.Decimal` arithmetic. Total reported: **89 passing assertions across overlapping suites**, not independent legal compliance cases.

The first run of the new test script failed due to an error in the test's `NOT_EVALUABLE` assertion expression; the assertion was corrected, the script rerun and all 23 assertions passed. No semantic implementation code was modified. Test code and results are included for reproducibility.

## Scoped closure recommendation
**Recommend CTC-004 Done — scoped**, after explicit user approval. The original backlog acceptance criteria (multi-regime tax, withholding, signed values, reconciliation and precision) now have focused deterministic test evidence. The approval would establish logical arithmetic and structural validation only; it would not establish tax-authority conformance, complete country profiles, exhaustive semantic coverage, or a new schema decision.

## Open evidence routed to existing backlog
- CTC-005 / CTC-007: jurisdictional rounding, precision, tax ordering, tolerance, versioned effective rules.
- CTC-008 / CTC-010: real, versioned and validated mixed-regime, withholding, inclusive-price, credit and multi-currency payloads.
- CTC-009: semantic loss and end-to-end field coverage.

## Checkpoint
- Findings: MG-004-01 and MG-004-02 pass within stated synthetic scope.
- Proposed ADRs: none.
- New approved decisions: none.
- Authoritative registers changed: none.
- Next: request scoped closure decision for CTC-004; upon approval, prepare complete replacement project records.
