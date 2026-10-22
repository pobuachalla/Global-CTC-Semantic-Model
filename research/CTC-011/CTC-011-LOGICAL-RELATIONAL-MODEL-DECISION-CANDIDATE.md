# CTC-011 — Logical Relational Model, Decision Candidate v1.0

**Status:** REVIEW / PROPOSED. No physical schema or new ADR accepted.
**Source baseline:** CTC-014 approved local Git snapshot (2026-10-21), approved CTC-003 scoped 51-concept dictionary, D2, CTC-005/006/007, CL-01..08 and AR-01..10. Live GitHub HEAD not verified.

## 1. Purpose and non-goals

Translate accepted semantic facts and ownership into a logical relational representation, with explicit identities, reference integrity and conditional cardinalities. This is a logical ER model, **not** a requirement to create 51 tables.

Out of scope: SQL DDL, physical FK/index strategy, partitioning, database selection, storage of encrypted payloads, retention, FiscalContext A/B/C choice, regulatory uniqueness keys, 18 unapproved CTC-003 field proposals.

## 2. Relational principles derived from approved decisions

1. `BillingDocument` provides stable platform identity; `PublishedRevision` owns immutable published assertions. Never update an issued revision in place.
2. Party participation references frozen `PartySnapshot` and retains role and scope; shared mutable ERP master records cannot replace snapshots.
3. Commercial legal identity is namespace/profile-governed; never assume global uniqueness of `documentNumber`.
4. `TaxRegime` identity is distinct from `RevisionTaxRegime` applicability and individual `TaxApplication`; source assertions and computed summaries are not double-counted.
5. `FiscalInterpretation` pins a revision, profile package and resolvable input manifest; derived facts never overwrite source facts.
6. Submission and transport attempts are distinct identities; immutable submission snapshots and envelope manifests pin exact artifacts.
7. `ProcessingEvent` and authority observations are append-only evidence; client status and legal state are separately derived.
8. Ingestion/extraction cardinality permits zero or many documents per source batch; partial batch acceptance remains per member.
9. Cross-tenant references must be rejected; explicit tenant scoping is required where an entity has tenant context. The physical enforcement method is deferred.
10. References with missing external targets are preserved as typed unresolved references; do not invent target documents or authority identities.

## 3. Entity-to-logical-record mapping

The approved dictionary enumerates **51** logical concepts. The mapping register contains every concept and its declared fields. **Do not infer a physical table from a row in this register.**

| Domain | Logical ownership / records |
|---|---|
| Commercial | BillingDocument, PublishedRevision, PartySnapshot, PartyParticipation, BillingLine, DocumentRelationship, DocumentReference, Supply and related value objects |
| Tax/monetary | TaxRegime, RevisionTaxRegime, TaxApplication, TaxSummary, SourceAssertion, monetary values/effects and reconciliation |
| Interpretation | SourceFiscalFact, FiscalInterpretation, InterpretationInputManifest, DerivedFiscalFact, ProfilePackage, provenance and enrichment |
| Operations | DocumentRepresentation, ComplianceTransaction, SubmissionSnapshot, SubmissionAttempt, ProcessingEvent, FiscalIdentity/Evidence, ingestion/extraction, envelope/member/transport and assessments |

## 4. Reference and cardinality register

The following is the reviewable **subset of structural relationships** selected from the accepted logical dictionary and decisions. “Logical association” means the relationship is required by semantics but an exact FK field is not part of the approved declaration. Such cases must not be silently promoted into new canonical fields.

| Parent / subject | Child / target | Reference | Parent | Child | Field status |
|---|---|---|---|---|---|
| BillingDocument | PublishedRevision | `documentRef` | 1 | 0..N | Declared |
| PublishedRevision | PartyParticipation | `revisionRef` | 1 | 0..N | Declared |
| PartySnapshot | PartyParticipation | `partySnapshotRef` | 1 | 0..N | Declared |
| PublishedRevision | BillingLine | `revisionRef` | 1 | 0..N | Declared |
| BillingLine | BillingLine | `parentLineRef` | 0..1 | 0..N | Declared |
| BillingDocument | DocumentRelationship | `sourceDocumentRef` | 1 | 0..N | Declared |
| BillingDocument | DocumentRelationship | `targetDocumentRef` | 1 | 0..N | Declared |
| PublishedRevision | DocumentReference | `revisionRef` | 1 | 0..N | Declared |
| PublishedRevision | Supply | `revisionRef` | 1 | 0..N | Declared |
| PublishedRevision | TaxApplication | `revisionRef` | 1 | 0..N | Declared |
| PublishedRevision | RevisionTaxRegime | `revisionRef` | 1 | 0..N | Declared |
| TaxRegime | RevisionTaxRegime | `regimeRef` | 1 | 0..N | Declared |
| PublishedRevision | SourceFiscalFact | `revisionRef` | 1 | 0..N | Declared |
| PublishedRevision | FiscalInterpretation | `revisionRef` | 1 | 0..N | Declared |
| ProfilePackage | FiscalInterpretation | `profilePackageRef` | 1 | 0..N | Declared |
| FiscalInterpretation | DerivedFiscalFact | `interpretationRef` | 1 | 0..N | Declared |
| PublishedRevision | ComplianceTransaction | `revisionRef` | 1 | 0..N | Declared |
| ComplianceTransaction | SubmissionAttempt | `transactionRef` | 1 | 0..N | Declared |
| ComplianceTransaction | ProcessingEvent | `transactionRef` | 1 | 0..N | Logical association; no exact approved FK field |
| ComplianceTransaction | LegalStateAssessment | `transactionRef` | 1 | 0..N | Logical association; no exact approved FK field |
| SubmissionEnvelope | EnvelopeMember | `envelopeRef` | 1 | 1..N when submitted | Declared |
| SubmissionEnvelope | TransportAttempt | `envelopeRef` | 1 | 0..N | Declared |
| IngestionRecord | DocumentExtraction | `ingestionRef` | 1 | 0..N | Declared |
| DocumentExtraction | BillingDocument | `documentRef` | 0..1 | 0..N | Declared |

### Qualified rules

- Published revision party/line minimums are document-family/profile-dependent; globally 0..N is permissible at logical ingestion level.
- A submitted transport attempt resolves to one exact immutable payload; that payload can have 1..N member references.
- External document relationship targets may be unresolved. The reference register therefore must not force a fabricated local `BillingDocument` row.
- A `TaxApplication` belongs to exactly one defined economic scope; scope ownership and tax applicability must resolve to the same published revision.
- For source/derived monetary totals, preserve asserted amount, calculated amount and variance separately, with currency and rounding context.
- No compliance or transport acknowledgement implies legal clearance by itself.

## 5. ER diagrams

Four machine-maintainable Mermaid diagrams are included in this directory: `01-commercial.mmd`, `02-fiscal.mmd`, `03-compliance.mmd`, `04-ingestion.mmd`. The diagrams show logical associations, not physical table multiplicity. The detailed qualified cardinalities are governed by `RELATIONSHIP-REGISTER.csv`.

## 6. Identity and reference rules

| Identity class | Logical key | Uniqueness scope |
|---|---|---|
| Platform document | `BillingDocument.documentId` | Tenant-scoped platform identity |
| Published revision | `PublishedRevision.revisionId` and content digest | Immutable revision identity; belongs to exactly one document |
| Commercial/legal number | Issuer, legal namespace, series, number, family, profile context | Conditional profile-governed uniqueness; no universal composite key imposed |
| Fiscal identity | Typed scheme, issuer, jurisdiction, subject, value | Fiscal identity distinct from submission ID |
| Submission attempt | Independent attempt identity, pinned submission snapshot | Separate from envelope transport attempt |
| Envelope member | Envelope-scoped member identity | Correlates per-member outcomes |
| Authority response | Immutable observation ID and typed correlation | External IDs may be ambiguous; unresolved state preserved |

## 7. Logical integrity and immutability tests

The executable checks in `tests/CTC-011/validate_logical_model.py` verify the 51-concept mapping inventory, relationship endpoints, declared reference visibility, diagram coverage, and negative reference scenarios. They do not validate actual SQL, schema migrations or regulator fixtures.

## 8. Explicit unresolved design decisions

1. **FiscalContext A/B/C physical design:** deferred to CTC-002-FU01 and CTC-012; not decided here.
2. **Physical keys and relational decomposition:** CTC-012 / implementation design.
3. **Retention and deletion:** CTC-012, subject to legal and data-protection requirements.
4. **18 additional field contracts:** remain Proposed; do not include as accepted columns.
5. **Profile-specific mandatory roles and legal identity keys:** CTC-005/006 profile validation, not universal relational NOT NULL/UNIQUE constraints.
6. **Authority response detail shapes:** accepted AR logical boundaries; physical response tables deferred.
7. **Full semantic-to-relational reversibility:** depends on CTC-009 and real fixtures.

## 9. Acceptance recommendation

**Recommend CTC-011 Done — scoped, subject to explicit user approval**, for the implementation-neutral logical ER model and mapping/register artifacts only. The acceptance must not imply approval of physical database schema, FiscalContext A/B/C or proposed fields.

## 10. Handoff

CTC-012 should next define immutable persistence snapshots and lineage using this logical model. The development-facing TDS can begin as a separate proposed backlog deliverable after this approval.
