# CTC-003 — Lifecycle, Publication and Conditional Cardinality Review (Draft 0.8)

**Date:** 2026-10-20  
**Status:** Proposed detailed model. No new architecture approval.  
**Task:** CTC-003; associated follow-ups CTC-003-R01/R02/R04, CTC-006 and CTC-013.

## 1. Sources and limitations

This draft builds on Unified D2 Dictionary 0.5, Ownership Review 0.6, Conditional Cardinality Review 0.7, the accepted D2 logical contract, P1–P7, I-01–I-10, T01–T03, and D01–D03 with their six accepted invariants. Older SemanticDocument v1.0 and BillingDocument v0.3 remain reference designs, not approved detailed schemas. All worked instances here use fictional jurisdiction XX. No current mandate rule, authority endpoint, production payload or official legal issuance condition is validated.

## 2. Terminology and lifecycle dimensions

| Term | Candidate meaning | Owner | Not equivalent to |
|---|---|---|---|
| IngestionRecord | Correlation for one received payload and its immutable source representation | Ingestion/representation context | BillingDocument or published revision |
| WorkingDocument | Mutable normalization/validation workspace; not authoritative published semantic content | Preparation workflow | PublishedRevision |
| BillingDocument | Stable logical platform identity for a commercial/legal document | Document registry | Source payload or submission ID |
| PublishedRevision | Frozen semantic snapshot with immutable references and content digest | Billing semantics | Legal issuance or clearance |
| LegalDocumentIdentity | Issuer-assigned number/series and issuer identity captured at publication or issuance, subject to profile | PublishedRevision | Platform document ID or authority fiscal UUID |
| LegalStateAssessment | Profile-scoped assessment of issuance/clearance/cancellation validity based on evidence | Fiscal/compliance projection | Immutable billing facts |
| ComplianceTransaction | One logical compliance operation for an obligation | Compliance domain | Submission attempt |
| SubmissionAttempt | One externally transmitted attempt with pinned submission snapshot | Compliance domain | New legal document |
| FiscalEvidence | Retained authority/provider receipt or certification evidence | Evidence domain | Commercial content |

**Proposed separation:** preparation state (RECEIVED / NORMALIZING / VALIDATED / PUBLISHED / FAILED), legal state (UNDETERMINED / NOT_ISSUED / ISSUED / CANCELLED / etc., as profile-defined), and compliance-operation state (PENDING / SUBMITTED / UNKNOWN / REJECTED / ACCEPTED / etc.) are separate projections. Do not make them a single universal enum.

## 3. Candidate transition rules

1. **Receive:** store exact source `DocumentRepresentation` and `IngestionRecord`, even if no BillingDocument exists. No automatic legal issuance claim.
2. **Normalize:** create/modify `WorkingDocument` and validation findings; preserve source fact provenance. Draft edits need not create `PublishedRevision`.
3. **Publish:** freeze semantic snapshot, party snapshots, source-fact references, exact content digest and revision identity. `PUBLISHED` means internally immutable, not necessarily legally issued.
4. **Determine obligation:** evaluate jurisdiction profile and create a fiscal interpretation or compliance transaction as appropriate. Pin the effective rule/profile versions.
5. **Submit:** create immutable `SubmissionSnapshot` referencing exact published revision, interpretation if used, outbound representation digest and destination. Attempt points to that snapshot.
6. **Receive external outcome:** append processing events, retain original response artifact and correlate to transaction/attempt; derive legal state only through applicable profile rules.
7. **Correct:** before legal issuance, a new published revision *may* be allowed by a profile; after issuance, a distinct corrective document *may* be required. Never mutate a frozen revision or assume a universal correction route.
8. **Cancel:** record separate operation, evidence and legal-state projection; do not delete original invoice or its earlier authorization.

## 4. Conditional cardinality and nullability matrix (all PROPOSED)

| Relationship / field | At ingestion | Working | Published | Submitted | Rule owner / caveat |
|---|---|---|---|---|---|
| IngestionRecord → source representation | 1..N | 1..N | 1..N retained | retained | Platform structural rule |
| IngestionRecord → BillingDocument | 0..1 initially | 0..1 | 0..1 or exception routing | unchanged | Multiple source artifacts may map to one document; dedup policy open |
| BillingDocument → PublishedRevision | 0..N | 0..N | 1..N after first publication | 1..N | Platform; publication is explicit |
| PublishedRevision → commercial number | N/A | 0..1 | 0..1 global | pinned | Invoice/credit profiles may require 1; number scope open |
| PublishedRevision → PartyParticipation | N/A | 0..N | 0..N global | frozen | Profiles impose seller/buyer/recipient minima |
| PartyParticipation → immutable PartySnapshot | N/A | 1 when present | exactly 1 | frozen | D01 accepted logical ownership |
| PublishedRevision → BillingLine | N/A | 0..N | 0..N global | frozen | Published invoice profile may require 1..N |
| PublishedRevision → FiscalInterpretation | N/A | 0..N | 0..N | 0..N | D2 contract; physical aggregation deferred |
| FiscalInterpretation → input manifest | N/A | exactly 1 if interpretation exists | pinned | pinned | D02 approved reproducibility |
| ComplianceTransaction → SubmissionAttempt | 0 | 0 | 0..N | 1..N if transmitted | Some operations have no transmission |
| Submitted attempt → SubmissionSnapshot | N/A | N/A | N/A | exactly 1 | D03 approved logical pinning |
| SubmissionSnapshot → outbound representation | N/A | N/A | N/A | exactly 1 | Immutable digest required |
| PublishedRevision → LegalStateAssessment | 0 | 0 | 0..N | 0..N | Jurisdiction scoped; derived projection, not source fact |
| Corrective document → original reference | 0..N | 0..N | Profile conditional | frozen | Typed CREDITS/CORRECTS/REPLACES; legal meaning profile governed |

A global 0 minimum is not permission to publish an invalid invoice: conditional profile validation imposes required content.

## 5. Identity and publication invariants proposed for review

- **L01** Ingestion and publication are separately identified; source payload can predate a BillingDocument or revision.
- **L02** Publication freezes semantic content and immutable references; it does not imply legal issuance.
- **L03** Issuer-assigned commercial identity is captured with its issuer, series, document type and applicable uniqueness scope; scope must be profile-defined, not globally guessed.
- **L04** A legal-state projection must identify jurisdiction, profile/rule version, supporting events/evidence and evaluation time.
- **L05** A compliance response does not mutate published commercial content.
- **L06** A submitted attempt resolves to an exact immutable snapshot, never `latest`.
- **L07** A corrective legal document is separately identified where the applicable rule requires it; source original remains traceable.
- **L08** A cancellation outcome is append-only evidence with a separate legal-state projection, not deletion or replacement of certification history.
- **L09** Unknown or pending external outcome cannot be treated as rejected or legally issued without evidence.
- **L10** Structural minima and jurisdiction/profile minima must be evaluated separately, with a recorded validation stage.

L01–L10 are candidate detailed invariants; none is newly accepted by this draft. They are consistent with existing accepted principles but should not be confused with approved CTC-002 I-01–I-10.

## 6. Instance-level simulation (synthetic XX)

| Stage | Before | New records / after | Must remain unchanged |
|---|---|---|---|
| Source received | none | ING-01 + REP-SRC-01 | raw source bytes |
| Normalized working document | ING-01 | WORK-01, validation findings | REP-SRC-01 |
| Published | WORK-01 | DOC-01 + REV-01 + frozen PARTY-S1/PARTY-B1 | source and published digest |
| Submitted | REV-01 | CT-01, FI-01, REP-OUT-01, SS-01, ATT-01 | REV-01 and SS-01 |
| Timeout | ATT-01 pending | EVT-UNKNOWN-01, legal status UNDETERMINED | submitted artifact and snapshot |
| Reconciled as cleared | unknown | EVT-ACCEPT-02 + REP-CERT-01 + EVD-CERT-01 + FID-01 | earlier timeout event, REV-01 |
| Corrective credit note | DOC-01 cleared | DOC-02 + REV-02 + REL-CREDITS-01 | DOC-01, REV-01, EVD-CERT-01 |
| Cancellation accepted | CT-CANCEL-01 pending | EVT-CANCEL-01 + EVD-CANCEL-01, projected legal state CANCELLED | original clearance event and certified artifact |

**Branching note:** Correction and cancellation are independent test branches, not asserted as one legally permitted sequence. `XX` is fictional.

## 7. Reference-validation cases

| Test | Expected |
|---|---|
| Inbound representation before revision exists | Allowed, with IngestionRecord correlation |
| Published revision references mutable ERP party master | Rejected |
| Attempt points to `latest` outbound representation | Rejected |
| Authority timeout maps automatically to rejection | Rejected |
| Authority cancellation overwrites original evidence | Rejected |
| Credit note mutates original revision | Rejected |
| Different source and commercial identifiers coexist | Allowed |
| Legal state asserted without jurisdiction/profile/evidence | Rejected or NOT_EVALUABLE |

## 8. Open decisions and ownership

| Open question | Suggested owner/task |
|---|---|
| Exactly when a working document becomes published; whether publication precedes legal issuance | CTC-003-R01 / CTC-006 |
| Commercial number uniqueness tuple and legally permitted renumbering | CTC-006 |
| Required parties/lines by invoice, credit, correction and other document types | CTC-003-R02 / CTC-005 |
| Legal state dimensions and authority-response normalization | CTC-013 / CTC-014 |
| Retry versus resubmission and artifact regeneration | CTC-003-R04 / CTC-013 |
| Source-fixture proof for selected jurisdictions | CTC-002-FU02 / CTC-008 / CTC-010 |
| Physical FiscalContext and snapshots | CTC-002-FU01 / CTC-011 |

## 9. Recommended decision gate

Approve, refine or defer L01–L10 and the **three-dimensional lifecycle separation** as a logical modelling policy. Do **not** approve the full conditional cardinality matrix by implication. After this review, update Unified Dictionary to Draft 0.9 with approved definitions, resolve profile-specific constraints and produce representative canonical instances before CTC-003 closure.

## 10. Session checkpoint

- **CTC-003:** In Progress; Draft 0.8 proposed.
- **Accepted unchanged:** D2, P1–P7, CTC-002 I-01–I-10, T01–T03, D01–D03 and their six invariants.
- **New approvals:** None.
- **FiscalContext A/B/C physical design:** Deferred.
- **Evidence:** Synthetic only; no authority conformance claim.
