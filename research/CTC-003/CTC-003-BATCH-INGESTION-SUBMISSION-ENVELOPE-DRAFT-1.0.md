# CTC-003 — Batch Ingestion and Submission Envelope Semantics — Draft 1.0

**Status:** Proposed; no new approvals. **Source:** CTC-003 Draft 0.9, approved D2/P1–P7/I-01–I-10, T01–T03, D01–D03, L01–L10. **Date:** 2026-10-20.

## Purpose and boundary

Test C09-01, C09-02 and C09-07 against multi-document inbound and outbound containers. The prior Draft 0.9 explicitly marked ingestion 0..1 document and submitted-attempt exactly-one outbound representation as assumptions requiring review. This document distinguishes **source payload**, **extracted document**, **outbound envelope**, **transport attempt**, **per-document operation** and **per-document response**. These are logical candidates, not tables or mandatory API shapes.

## Findings

1. **An ingestion event is not a billing document.** A received file may contain zero, one or many extractable business documents; one logical document may be referenced by multiple ingestion events (duplicate or corrected transmissions). A single inbound representation can contain multiple document segments.
2. **A transport submission is not necessarily a compliance transaction for one invoice.** A batch can be sent once while producing per-document results. A transport attempt should pin one exact submitted payload/envelope artifact, which can enumerate multiple document members. This preserves D03/L06 without requiring one invoice per payload.
3. **One batch-level acceptance is not proof of every member's fiscal acceptance.** Envelope acknowledgements and document-specific decisions have different subjects. A missing member outcome must remain pending/unknown, not inferred from a successful HTTP or envelope acknowledgement (P1/P5/L09).
4. **Atomicity cannot be presumed.** Some external endpoints may reject an entire envelope, while others may accept a subset. Model outcome granularity explicitly; profile/provider rules determine actual behavior.
5. **One-to-many is not automatically many-to-many ownership.** The same logical invoice may be retransmitted in different envelopes. Immutable membership and correlation are required; a shared transport container must not own or mutate the commercial document.

## Candidate logical concepts

| Concept | Meaning | Candidate required identity/reference |
|---|---|---|
| `IngestionRecord` | One reception event | `ingestionId`, received-at, source context |
| `InboundRepresentation` | Exact received bytes and metadata | `representationId`, digest, format/version |
| `DocumentExtraction` | Extracted member/segment from a source artifact | `extractionId`, source representation, locator/index, resolution state, optional document reference |
| `SubmissionEnvelope` | Exact outbound batch/container artifact and member manifest | `envelopeId`, representation ID/digest, immutable member manifest |
| `EnvelopeMember` | Exact document artifact and semantic references included in an envelope | member ID, revision ID/digest, representation ID/digest, optional interpretation reference |
| `TransportAttempt` | A transmission of an immutable envelope/payload | attempt ID, exact envelope ID/digest, endpoint, correlation |
| `ComplianceTransaction` | Per-document logical compliance operation | transaction ID, revision ID, obligation/destination |
| `ProcessingEvent` | Envelope-level or document-level external event | event ID, subject type and ID, original response reference |

`DocumentExtraction`, `SubmissionEnvelope`, `EnvelopeMember` and `TransportAttempt` are **candidate concepts**; this review does not approve them as new D2 roots or change the nine-concept contract.

## Proposed relationship/cardinality amendments

| ID | Draft 0.9 | Draft 1.0 proposal | Why |
|---|---|---|---|
| C09-01 | IngestionRecord -> original representations 1..N | Retain 1..N | Received event can preserve one or more artifacts |
| C09-02 | IngestionRecord -> BillingDocument 0..1 per resolution link | Replace with IngestionRecord -> DocumentExtraction 0..N; each extraction -> BillingDocument 0..1 | Empty/unparseable, single and batch source all possible; unresolved members allowed |
| C09-07 | Submitted SubmissionAttempt -> exactly one outbound representation | Split: submitted TransportAttempt -> exactly one immutable outbound envelope/payload representation; envelope -> 1..N member references; per-document ComplianceTransaction -> 0..N attempts/associations | Avoid assuming one document per transport attempt while retaining exact artifact pinning |

**Non-batch single document** is a one-member envelope or a single payload with an equivalent immutable membership manifest. Whether a literal envelope object is mandatory is deferred.

## Proposed invariants B01–B10 (NOT APPROVED)

- **B01** Each ingestion event identifies immutable original representation(s), regardless of extraction success.
- **B02** Each extracted member has a stable locator within an immutable source representation and its own resolution status.
- **B03** An extraction may resolve to at most one logical BillingDocument at a time; a batch may resolve to many documents.
- **B04** A submitted transport attempt pins exactly one immutable outbound payload/envelope digest.
- **B05** An outbound envelope has a frozen member manifest, including each member's exact submitted representation and revision references.
- **B06** A member may participate in multiple distinct envelope submissions without mutating its billing revision.
- **B07** Envelope-level transport/validation outcomes and per-member compliance outcomes have different typed subjects.
- **B08** Successful envelope transport alone must not imply every member is legally issued, accepted or cleared.
- **B09** Partial success, total rejection and unknown member outcomes are representable without loss of original response and correlation identifiers.
- **B10** Duplicate delivery, retry and idempotency correlation must preserve the exact attempt and member histories; provider-specific deduplication policy remains outside the universal contract.

## Synthetic instance tests

### A. One inbound file containing two invoices

```yaml
ingestion: {id: ING-01, representationRefs: [SRC-01]}
source: {id: SRC-01, digest: HASH-SRC-01}
extractions:
  - {id: EXT-01, sourceRef: SRC-01, locator: 'Invoice[1]', documentRef: DOC-01}
  - {id: EXT-02, sourceRef: SRC-01, locator: 'Invoice[2]', documentRef: DOC-02}
```

**Expected:** two independently identifiable documents from one immutable inbound source.

### B. One envelope with partial results

```yaml
envelope: {id: ENV-01, representationRef: REP-ENV-01, digest: HASH-ENV-01,
  members: [{memberId: M1, revisionRef: REV-01, representationRef: REP-01},
            {memberId: M2, revisionRef: REV-02, representationRef: REP-02}]}
attempt: {id: ATT-01, envelopeRef: ENV-01}
events:
  - {id: EVT-ENV, subject: ENV-01, outcome: RECEIVED}
  - {id: EVT-M1, subject: M1, outcome: ACCEPTED}
  - {id: EVT-M2, subject: M2, outcome: REJECTED}
```

**Expected:** member M1 accepted, M2 rejected; envelope RECEIVED is not universal clearance.

### C. Unknown member and retry

```yaml
firstAttempt: {id: ATT-01, envelopeRef: ENV-01}
memberOutcome: {memberId: M2, state: UNKNOWN}
secondAttempt: {id: ATT-02, envelopeRef: ENV-02, retriesMemberRef: M2}
```

**Expected:** first attempt retained, second artifact and attempt independently pinned; no invented rejection/acceptance.

### D. Negative cases

- Reject a submitted attempt pointing to `latest` representation.
- Reject a member event that cannot resolve to a member or transaction subject.
- Do not infer member acceptance from an envelope-level transport success.
- Do not replace a prior attempt or evidence when retrying.

These are **synthetic structural examples**. No actual provider batch payload or response schema was validated; exact provider atomicity and envelope rules remain evidence gates.

## Interaction with accepted architecture

- **P1/P5:** envelope transport events stay outside billing semantics; member outcomes retain independent history.
- **P2/P3:** revisions and all source/submitted artifacts remain immutable and individually identifiable.
- **P4:** envelope correlation, transport ID, commercial invoice number and fiscal identity are distinct.
- **P6:** member and envelope events have one typed authoritative subject; projections may aggregate but not overwrite.
- **P7/D02:** mapping provenance includes source representation and extraction locator, plus exact rule/profile packages.
- **D03/L06:** exact submitted artifact pinning is preserved, generalized to an immutable envelope and member manifest.

## Decision gate

**Recommend:** Accept *in principle* the distinction between document-level compliance operations and transport envelopes, and amend C09-02/C09-07 only after explicit review. Keep B01–B10, new entity shapes and conditional cardinalities **Proposed**. Obtain at least one actual multi-document inbound fixture and a provider batch response demonstrating per-member correlation before claiming format-specific support.

## Backlog implications

CTC-003 remains In Progress. Add batch/envelope mapping and outcome evidence to CTC-008/009/010; detailed attempt/event taxonomy to CTC-013/014; physical representation choices to CTC-011/012. Do not mark any of those tasks Done.

## Session checkpoint

- **Approved:** None new.
- **Proposed:** C09-02 and C09-07 refinements; B01–B10; candidate extraction/envelope/member concepts.
- **Unchanged:** D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10; physical FiscalContext A/B/C deferred.
- **Next:** Review batch/envelope semantic distinction and B01–B10; then revise Draft 1.1 conditional cardinalities and entity dictionary.
