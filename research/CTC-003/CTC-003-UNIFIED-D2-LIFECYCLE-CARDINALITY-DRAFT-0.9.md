# CTC-003 — Unified D2 Lifecycle & Conditional Cardinality Draft 0.9

**Date:** 2026-10-20  
**Status:** Candidate detailed model, not approved.  
**Approved baseline:** D2 nine-concept logical contract; P1–P7; CTC-002 I-01–I-10; T01–T03 logical policies; D01–D03 logical ownership and paired invariants; three lifecycle dimensions and L01–L10 logical invariants.

## 1. Purpose and source precedence

This is a focused refinement of Unified D2 Dictionary 0.5, Ownership Review 0.6, Conditional Cardinality Review 0.7 and Lifecycle Review 0.8. Those source drafts remain available alongside this document. Earlier SemanticDocument v1.0 and BillingDocument v0.3 are reference models, not approved schemas. No new jurisdictional mandate is asserted. All instances below are synthetic.

The **logical D2 concepts are approved**, but the detailed attributes and cardinalities in this document are proposals. The distinction between semantic entity, aggregate root and persistence table remains explicit.

## 2. Lifecycle dimensions (accepted logical policy)

| Dimension | Example states (illustrative only) | Owner | Constraint |
|---|---|---|---|
| Preparation | received, working, validated, published | Ingestion/preparation context | Internal publication is not automatically legal issuance (L02) |
| Legal/fiscal recognition | undetermined, issued, cancelled | Profile-scoped legal-state assessment | Requires jurisdiction, rules and evidence (L04/L09) |
| Compliance processing | pending, submitted, rejected, accepted, unknown | ComplianceTransaction and events | Does not overwrite published revision (L05/L06) |

States are projections, not one universal enum; no state list is mandated for every country.

## 3. Proposed cardinality rules for review

| ID | Relationship | Structural minimum/maximum | Lifecycle/profile condition | Approval |
|---|---|---|---|---|
| C09-01 | IngestionRecord → original DocumentRepresentation | 1..N | Preserve each received artifact and digest | Proposed |
| C09-02 | IngestionRecord → BillingDocument | 0..1 per resolution link (reassess for batch payloads) | May remain unlinked while ingestion fails or awaits resolution | Proposed |
| C09-03 | BillingDocument → PublishedRevision | 0..N | At least one once platform publication has occurred | Proposed |
| C09-04 | PublishedRevision → PartyParticipation / BillingLine | 0..N each at global structural level | Invoice/credit profile imposes minimum roles and line requirements | Proposed |
| C09-05 | PartyParticipation → PartySnapshot | exactly 1 | Snapshot immutable once published; role/scope pinned | Proposed |
| C09-06 | PublishedRevision → FiscalInterpretation | 0..N | Each interpretation pins one revision and one complete input manifest; physical aggregate deferred | Proposed |
| C09-07 | Submitted SubmissionAttempt → SubmissionSnapshot → outbound representation | exactly 1 snapshot and exactly 1 representation per submitted attempt | Snapshot pins revision digest, applicable interpretation/profile and artifact hash | Proposed |
| C09-08 | PublishedRevision → LegalStateAssessment; ComplianceTransaction → ProcessingEvent | 0..N each | Legal assessment profile/evidence scoped; events append-only | Proposed |

These proposals are **not** permission to publish a legally invalid invoice. Global structural permissiveness and profile-specific publication requirements are separate validations (L10).

## 4. Identity and reference rules

1. `IngestionRecord` identifies a reception event and source artifacts; it is not a legal document identity.
2. `BillingDocument.documentId` is stable platform identity; `PublishedRevision` holds issuer-supplied commercial identity as frozen assertions (D01).
3. A revision may be published without a proven legal-state determination (L02).
4. `FiscalInterpretation` pins revision, source facts, enrichment inputs and immutable profile package (D02).
5. `SubmissionSnapshot` pins one exact outbound artifact and all needed interpretation/revision references (D03).
6. `FiscalIdentity` and `FiscalEvidence` identify external legal artifacts/evidence separately from platform submission IDs (P4).
7. A `DocumentRelationship` such as CREDITS/CORRECTS/REPLACES is distinct from an internal revision chain; legal semantics remain profile-dependent.

## 5. Synthetic instance-level cases

### Case A — Ingested but not published

```yaml
ingestion: {id: ING-01, representationRefs: [REP-SRC-01], documentRef: null}
sourceRepresentation: {id: REP-SRC-01, digest: SHA256-EXAMPLE-A}
preparation: {workingId: WORK-01, state: NORMALIZING}
publishedRevision: null
legalState: UNDETERMINED
```

**Expected:** allowed to exist; not treated as issued. Digest is an illustrative placeholder, not a computed hash.

### Case B — Published invoice with uncertain external response

```yaml
document: {documentId: DOC-01}
revision: {revisionId: REV-01, documentRef: DOC-01, published: true, partySnapshotRefs: [PARTY-S1, PARTY-B1]}
representation: {id: REP-OUT-01, revisionRef: REV-01}
submissionSnapshot: {id: SS-01, revisionRef: REV-01, outboundRepresentationRef: REP-OUT-01}
attempt: {id: ATT-01, snapshotRef: SS-01}
event: {id: EVT-UNKNOWN-01, attemptRef: ATT-01, outcome: UNKNOWN}
legalStateAssessment: {revisionRef: REV-01, outcome: UNDETERMINED}
```

**Expected:** source and revision unchanged; UNKNOWN does not imply rejection or issuance.

### Case C — Credit note referencing an earlier invoice

```yaml
original: {documentId: DOC-01, revisionId: REV-01}
creditNote: {documentId: DOC-02, revisionId: REV-02, documentType: CREDIT_NOTE}
relationship: {type: CREDITS, sourceRevisionRef: REV-02, targetRevisionRef: REV-01}
```

**Expected:** new legal-document identity and typed reference; original remains unchanged. The legal validity of the correction is profile-dependent.

### Case D — Cancellation after earlier evidence

```yaml
originalEvidence: {id: EVD-CLEAR-01, revisionRef: REV-01}
cancellationTransaction: {id: CT-CANCEL-01, revisionRef: REV-01}
cancellationEvent: {id: EVT-CANCEL-01, transactionRef: CT-CANCEL-01}
cancellationEvidence: {id: EVD-CANCEL-01, transactionRef: CT-CANCEL-01}
legalStateAssessment: {revisionRef: REV-01, outcome: CANCELLED, evidenceRefs: [EVD-CLEAR-01, EVD-CANCEL-01]}
```

**Expected:** clearance evidence retained; legal-state projection may change without rewriting commercial facts.

## 6. Negative reference assertions (proposed)

| Case | Expected |
|---|---|
| Published party reference resolves only to mutable ERP master | Reject |
| Submitted attempt points to `latest` representation | Reject |
| Submitted attempt has no pinned outbound representation | Reject |
| External timeout automatically marks document rejected | Reject |
| Cancellation deletes earlier fiscal evidence | Reject |
| Source payload with no published revision is labelled legally issued by default | Reject |
| Derived fiscal fact replaces source value without provenance | Reject |
| Credit note silently overwrites original revision | Reject |

These are candidate contract assertions, not an executed conformance suite.

## 7. Unresolved decisions and task mapping

| Question | Task |
|---|---|
| Publication freeze trigger, revision succession and commercial-number uniqueness | CTC-003-R01 / CTC-006 |
| Party and line minimums for document families; credit-note reference requirements | CTC-003-R02 / CTC-005 / CTC-006 |
| Exact semantic shapes of IngestionRecord, WorkingDocument, LegalStateAssessment and SubmissionSnapshot | CTC-003 / CTC-013 |
| Profile rules and immutable package versioning | CTC-005 / CTC-007 |
| Physical FiscalContext A/B/C | CTC-002-FU01 / CTC-011 |
| Real source and authority-response fixture validation | CTC-002-FU02 / CTC-008 / CTC-009 / CTC-010 |
| Authority response/event taxonomy and legal-state projection | CTC-013 / CTC-014 |

## 8. Recommended Draft 0.9 review gate

Review C09-01 through C09-08 individually. In particular, decide whether the ingestion-to-document link can remain 0..1 in the presence of batch payloads, and whether a submitted attempt must always point to exactly one outbound representation. No detailed cardinality is accepted merely by this document.

## 9. Session checkpoint

**Accepted this session:** three lifecycle dimensions and L01–L10 at logical-policy level only, by explicit user approval. **Proposed this session:** C09-01..08, sample record structures and reference assertions. **Status:** CTC-003 In Progress. **No GitHub push performed.**
