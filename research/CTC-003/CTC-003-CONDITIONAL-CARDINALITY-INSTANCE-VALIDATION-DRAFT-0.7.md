# CTC-003 — Conditional Cardinalities and Instance-Level Reference Validation (Draft 0.7)

**Status:** Proposed detailed model; D01/D02/D03 logical ownership and their six paired invariants are explicitly Accepted. **Date:** 2026-10-20.

## Evidence basis and scope

Uses approved D2/P1–P7/I-01–I-10/T01–T03, Unified Dictionary Draft 0.5 and Ownership Review Draft 0.6. This is a **synthetic logical consistency test**, not executed authority schema validation. The accepted invariants do **not** approve the following candidate cardinalities.

## Candidate conditional-cardinality matrix

| Source | Target | Draft/ingestion | Published/issued | Submitted | Status / rationale |
|---|---|---|---|---|---|
| BillingDocument | PublishedRevision | 0..N | 1..N after first publication | 1..N | Proposed; revision identities immutable |
| IngestionRecord | DocumentRepresentation | 1..N | 1..N retained | 1..N retained | Proposed logical correlation, no mandatory table |
| PublishedRevision | PartyParticipation | 0..N during construction | 0..N generic, profile may require seller/buyer | Same frozen set | Proposed; not universal 1..N for every document family |
| PartyParticipation | PartySnapshot | exactly 1 | exactly 1 | exactly 1 | D01 ownership approved; exact logical reference candidate |
| PublishedRevision | BillingLine | 0..N | 0..N base contract; invoice profile may require 1..N | frozen | Proposed; corrections/reporting documents differ |
| PublishedRevision | SourceFiscalFact | 0..N | 0..N | frozen | P7, no duplication of core authoritative facts |
| PublishedRevision | FiscalInterpretation | 0..N | 0..N | 0..N | D2 logical interface approved; materialization deferred |
| FiscalInterpretation | InputManifest | 1 complete logical manifest | 1 | 1 pinned | D02 reproducibility approved; physical entity optional |
| FiscalInterpretation | DerivedFiscalFact | 0..N | 0..N | frozen per result | Proposed; zero allowed when no derivations |
| PublishedRevision | DocumentRepresentation | 0..N | 0..N | 1..N if outbound submission exists | Draft source artifact may reference ingestion instead |
| PublishedRevision | ComplianceTransaction | 0..N | 0..N | 1..N for processed revision | Separate lifecycle per P1/P5 |
| ComplianceTransaction | SubmissionAttempt | 0..N | 0..N | 1..N after first transmission | Proposed |
| Submitted SubmissionAttempt | SubmissionSnapshot | N/A | N/A | exactly 1 immutable logical snapshot | D03 approved logical pinning; physical entity optional |
| SubmissionSnapshot | Outbound DocumentRepresentation | N/A | N/A | exactly 1 exact artifact | Proposed: snapshot must not resolve `latest` |
| ComplianceTransaction | ProcessingEvent | 0..N | 0..N | 0..N | Append-only P5 |
| FiscalIdentity | FiscalEvidence | 0..N | 0..N | 0..N | Typed identity; exact evidence attribution, no overwrite |
| DocumentRelationship | Referenced legal document | 0..N | 0..N | 0..N | Correction/credit/cancellation conditional on profile |

### Interpretation of zero minimums

A zero minimum is **not** a claim that a published invoice without a seller, buyer, or line is valid in a given jurisdiction. It means the global structural contract does not impose that minimum across every document family. Publication/profile validators impose specific constraints.

## Instance scenarios and reference checks

### S1 — Draft ingestion, then publication

`ING-001` owns original `REP-SRC-001` before `REV-001` exists. Publication creates immutable `REV-001` with a reference to the source artifact and frozen `PS-SELLER-001`/`PS-BUYER-001`. Changing the ERP master to `PS-SELLER-NEW` must not change the revision's party reference.

### S2 — Legally separate corrective document

`DOC-002` / `REV-002` has a `CREDITS` relationship to `DOC-001` / `REV-001`. It does not mutate the original revision or original fiscal evidence. Whether a particular legal correction requires this relationship is jurisdiction-specific.

### S3 — Two interpretations from one revision

`FI-001` references `REV-001`, manifest `IM-001`, profile package `PP-1` and source fact `SF-001`. `FI-002` references the same revision and source fact but `PP-2` through `IM-002`. Original fact is unchanged; derived facts can differ. This is a technical capability test, not proof two jurisdictions legally require it.

### S4 — Submission timeout, reconciliation and retry

`ATT-001` pins `SS-001` → `REP-OUT-001` and digest. Timeout yields `UNKNOWN` outcome; an external response reconciles it without mutating `SS-001`. A retry can create `ATT-002`, with an explicit snapshot reference. Whether retrying is safe depends on provider idempotency and jurisdictional rules.

### S5 — Certification, identity and cancellation evidence

`EVD-CERT-001` attests `REP-CERT-001` and fiscal identity `FID-001`. A later `EVD-CANCEL-001` references the original fiscal identity and cancellation operation without rewriting the certified representation or earlier evidence.

## Rejected reference patterns

- `SubmissionAttempt.submissionSnapshotRef = latest` — invalid once submitted.
- `FiscalInterpretation.profilePackageRef = current` — invalid for reproducible interpretation.
- `PublishedRevision.partyRef = ERP-master-current` — invalid as an immutable published snapshot.
- Derived fiscal fact overwrites `SourceFiscalFact` — invalid under D02/P6/P7.
- Certified fiscal UUID copied as a second independent authoritative value on `BillingDocument` — invalid under P4/P6.

## Unresolved for review

1. Publication/freeze semantics, document numbering uniqueness and draft revision model.
2. Conditional party and line cardinalities per invoice/credit note/reporting document.
3. Interpretation input manifest completeness, external enrichments and deterministic canonicalization.
4. Snapshot semantics for technical retries with changed payloads.
5. Authority response correlation and evidence revocation/supersession.
6. Whether document/party relationships need immutable link-level versions.

## Decision checkpoint

**Accepted:** D01/D02/D03 logical directions and D01-1/2, D02-1/2, D03-1/2; prior D2, P1–P7, I-01–I-10, T01–T03.

**Proposed:** every cardinality in the table, candidate `IngestionRecord`, `InterpretationInputManifest` and `SubmissionSnapshot` physical entity shapes, any legal publication/correction rules. **CTC-003 remains In Progress.**
