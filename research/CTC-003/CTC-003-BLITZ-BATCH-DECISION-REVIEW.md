# CTC-003 — Blitz Batch Cardinality Decision & Evidence Review

**Date:** 2026-10-20  
**Status:** Logical decisions accepted under explicit user instruction; detailed model still draft.  
**Sources:** Consolidated full project snapshot through CTC-003-BATCH-01; Draft 1.0 batch review; Draft 1.1 instance test; approved D2 logical baseline.

## Test execution

- Existing `tests/validate_batch_cardinality.py`: **22/22** synthetic checks passed.
- New `tests/validate_batch_edge_cases.py`: **26/26** synthetic checks passed.
- Total **48 focused checks**, not 48 independent regulatory assertions. No actual authority/provider conformance.

## Scenarios

| Scenario | Evidence | Outcome | Caveat |
|---|---|---|---|
| Multi-document ingestion | ING1 -> EX1, EX2 | Supports 0..N extractions | Batch source fixture synthetic |
| Partial acceptance | ENV1 -> M1 accepted, M2 rejected | Member outcomes independent | Provider partial processing unverified |
| Retries/timeout | ATT1 unknown, ATT2 distinct | History preserved | Safe retry/idempotency unverified |
| Duplicate documents | Distinct receptions, same bytes | Reception != legal identity | Duplicate classification requires jurisdiction/client policy |
| Per-member correlation | Typed member subjects, out-of-order responses | Correct member projection | Ambiguous external IDs need mapping policy |
| Manifest immutability | SHA-256 canonical JSON digest change | Mutation detected | Canonicalization contract not finalized |

## Accepted logical constraints

- **C09-02:** 0..N extractions per ingestion, each extraction resolves to 0..1 BillingDocument at a given resolution state.
- **C09-07:** submitted transport attempt pins exactly one immutable payload; multi-member payload has identifiable member references.
- **B01–B10:** logical invariants accepted, with exact wording and exclusions in root DECISIONS.md.

## Non-approvals

C09-01/03..06/08, detailed entity shapes, provider-specific retry rules, real-world atomicity, legal issuance and physical persistence remain proposed/deferred. No automatic conversion of envelope success into member clearance.

## Recommended next CTC-003 work

1. Reconcile Draft 1.0/1.1 accepted constraints into a unified Draft 1.2 dictionary.
2. Review remaining C09 conditional cardinalities with invoice, credit-note and draft instances.
3. Link actual provider fixtures to CTC-008/009/010 and response-correlation behavior to CTC-013/014.
4. Keep CTC-003 In Progress pending complete entity dictionary, traceability and schema review.
