# CTC-003 — Batch Cardinality and Response Correlation Validation — Draft 1.1

**Date:** 2026-10-20  
**Status:** Evidence for review; B01–B10 and C09-01..08 remain Proposed.  
**Approved foundation:** D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10 and CTC-003-BATCH-01 logical separation.  
**Source basis:** CTC-003 Batch Ingestion and Submission Envelope Draft 1.0 and Unified D2 Lifecycle/Cardinality Draft 0.9, supplied in the consolidated project archive.

## Scope and method

Executed `tests/validate_batch_cardinality.py` against constructed JSON instances. The test asserts selected reference and digest constraints, not tax-authority legality, provider-specific atomicity, actual deduplication, transport semantics or complete validation of all ten B-invariants. SHA-256 values are computed from synthetic strings for internal consistency.

**Result: 22/22 focused assertions passed.** These checks are not 22 separate regulatory rules and are not full formal verification of the model.

## Scenario results

| Scenario | Constructed instances | Finding |
|---|---|---|
| Multi-document ingestion | ING1 -> SRC1 -> EX1/D1 and EX2/D2 | 1:N extraction is necessary; no direct single-document limit on ingestion. |
| Partial acceptance | ENV1 includes M1/V1 and M2/V2; E1 RECEIVED envelope, E2 ACCEPTED M1, E3 REJECTED M2 | Envelope receipt and member decisions have separate subjects. |
| Unknown member outcome | Envelope received; only M1 response exists | M2 remains unconfirmed; absence of an outcome cannot imply acceptance/rejection. |
| Retry | A1/ENV1 preserved; A2/ENV2 references V2 and new payload digest | Retry requires its own immutable attempt identity and pinned payload; legal retry permission not established. |
| Duplicate reception | ING1 and ING2 reference same SRC1; EX3 resolves to D1 | Receptions remain distinct even if resolution reuses a logical document. Identity/dedup policy unresolved. |
| Response correlation | Member outcome before envelope receipt; M2 pending, M1 accepted | Arrival order does not determine legal status; typed member references prevent cross-member attribution. |
| Negative controls | Mutable `latest` attempt reference, orphan member event, wrong revision digest, extraction resolving to two documents, wrong envelope digest | Validator rejects these structural inconsistencies. |
| Zero-document source | Ingestion with preserved source but no extractions | 0 extraction is structurally necessary for invalid/unparseable inputs. |

## Cardinality recommendations for review (NOT APPROVED)

| Rule | Proposed cardinality | Assessment |
|---|---|---|
| C09-01 Ingestion -> original representations | 1..N | Retain; one or more immutable received artifacts per ingestion. |
| C09-02 Ingestion -> DocumentExtraction | 0..N | Replace prior 0..1 direct document assumption; each extraction -> 0..1 resolved BillingDocument. |
| C09-03 BillingDocument -> PublishedRevision | 0..N, with lifecycle condition | Not exercised in this focused test; remains proposed. |
| C09-04 PublishedRevision -> PartyParticipation/BillingLine | 0..N structurally | Not exercised; jurisdiction/profile minimums deferred. |
| C09-05 PartyParticipation -> PartySnapshot | 1 | Not exercised; retains prior proposal. |
| C09-06 PublishedRevision -> FiscalInterpretation | 0..N | Not exercised; physical independence deferred. |
| C09-07 TransportAttempt -> submitted payload | Exactly 1 immutable payload/envelope artifact; envelope -> 1..N member refs | Strong synthetic structural support; keep per-document transaction associations distinct. |
| C09-08 Revision -> LegalStateAssessment; Transaction -> ProcessingEvent | 0..N | Partially exercises typed processing events; legal assessment cardinality untested. |

## B01–B10 evidence disposition

| ID | Test coverage | Status |
|---|---|---|
| B01 | Source representation reference present | Supported by synthetic checks; Proposed |
| B02 | Extraction locator/source association | Supported by synthetic checks; Proposed |
| B03 | Extraction resolves to at most one logical document | Supported by synthetic checks; Proposed |
| B04 | Attempt pins immutable envelope/payload digest | Supported by positive/negative checks; Proposed |
| B05 | Member manifest exact revision/representation refs | Partially supported; manifest immutability over time not tested; Proposed |
| B06 | Same revision may be resubmitted without mutation | Supported synthetically; provider rules not tested; Proposed |
| B07 | Typed envelope/member response subjects | Supported by positive/negative checks; Proposed |
| B08 | No automatic member clearance from envelope receipt | Supported as a projection rule, not provider law; Proposed |
| B09 | Partial/unknown outcomes representable | Supported structurally; Proposed |
| B10 | Duplicate/retry histories preserved | Partially supported; actual idempotency policy untested; Proposed |

## Gaps and counterexamples to investigate

1. **Duplicate classification:** byte-identical receipts, semantically identical documents with different serialization, and legitimately reused business identifiers need separate tests. Define idempotency keys and identity scope only with evidence.
2. **Response correlation:** real providers may return file-level IDs, document-level IDs, index-only references or asynchronous callbacks. A mapping/correlation strategy must preserve original identifiers and ambiguity.
3. **Partial rejection:** an envelope-level failure might prevent any member-level processing; never invent member outcomes.
4. **Retries:** retry after unknown outcome may create duplicates externally. A safe retry policy depends on provider idempotency/reconciliation.
5. **Manifest changes:** member order, extraction offsets and changed envelope encoding may affect digests and correlation. Preserve source and generated artifact hashes.
6. **Validation coverage:** test runner does not check uniqueness of all IDs, full temporal transitions, profile-specific legal rules, or concurrency.
7. **Evidence gate:** no actual multi-document inbound fixture paired with authority/provider partial-result response was executed.

## Recommended disposition

- Keep **CTC-003-BATCH-01 Accepted** at logical principle level.
- Advance **C09-02** and **C09-07** to **Review-ready proposals**, not Accepted.
- Keep **B01–B10 Proposed**; individual approval should follow review of their exact language and remaining gaps.
- Do not approve C09-03..06 or the legal-state portion of C09-08 on the strength of these tests.
- Maintain CTC-003 **In Progress**. Link actual fixture acquisition to CTC-008/009/010 and detailed response mapping to CTC-013/014.

## Session checkpoint

**Approved this session:** None.  
**Proposed findings:** F-003-BATCH-01 through F-003-BATCH-05 (synthetic structural evidence only).  
**Proposed decisions:** C09-02 and C09-07 refinements remain Proposed.  
**Next:** Review B01–B10 individually; define explicit correlation keys, duplicate resolution and retry invariants; seek genuine paired batch fixture evidence.
