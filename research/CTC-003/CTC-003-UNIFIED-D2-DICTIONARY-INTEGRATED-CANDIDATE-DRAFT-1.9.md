# CTC-003 — Unified D2 Entity Dictionary (Normative Candidate Draft 1.9)

**Status:** Integrated detailed candidate; schema NOT approved. **Date:** 2026-10-20. **Backlog:** CTC-003.

**Reading rule:** Field constraints below are integrated into the catalogue. All detailed field shapes remain proposed, including G2-01 through G2-08.

## 1. Source baseline and authority

- Approved: D2 nine-concept logical contract; P1–P7; I-01–I-10; T01–T03; D01–D03; L01–L10; batch separation; B01–B10; C09-01..08 at their explicitly qualified logical scope.
- Source drafts: SemanticDocument v1.0; Semantic Billing Model v0.3; CTC-003 commercial 0.2, tax 0.3, unified 0.5, completion candidate 1.3; G2 reconciliation 1.4.
- Not verified: live GitHub checkout, current regulatory fixtures, final fiscal-context physical aggregation.
- G2 names/merges below are **proposed** and do not imply acceptance of G2-01..08.

## 2. Modelling conventions

- `!` means proposed required field, `?` optional, `[]` collection. These are **candidate detailed field constraints**; conditional publication/profile rules override permissive base shapes only through governed validation.
- `Identifier` is opaque scoped identity; `Digest` includes algorithm and canonicalization context; `Money` is decimal amount plus ISO currency; `Rate` has explicit unit; `Instant` has offset; `CodedValue` includes scheme/version; `TypedValue` is tagged.
- Required references must resolve within the appropriate tenant/identity scope. Published snapshots and submitted artifacts must not be mutated.
- Proposed entity identity is not an assertion of a separate database table or aggregate root.

## 3. Canonical detailed entity catalogue

### Document and commercial

| Entity | Candidate fields (type and nullability) | Logical cardinality | Authoritative responsibility |
|---|---|---|---|
| `BillingDocument` | `documentId: Identifier!; tenantRef: Identifier!` | 0..N PublishedRevision | Stable platform document identity; no mutable legal facts |
| `PublishedRevision` | `revisionId: Identifier!; documentRef: Identifier!; documentType: Code!; documentNumber: Text?; issueDate: LocalDate?; currency: CurrencyCode?; contentDigest: Digest!; publicationProfileRef: Identifier?` | 1 BillingDocument; 0..N lines/parties/taxes | Published commercial assertions immutable; legal issuance separate |
| `PartySnapshot` | `partySnapshotId: Identifier!; legalName: Text?; taxIdentifiers: Identifier[]; address: Address?` | 0..N PartyParticipation | Frozen party facts as represented on document |
| `PartyParticipation` | `participationId: Identifier!; revisionRef: Identifier!; partySnapshotRef: Identifier!; role: Code!; scopeRef: Identifier?` | 1 revision; 1 snapshot | One frozen party reference; line-level role supported |
| `BillingLine` | `lineId: Identifier!; revisionRef: Identifier!; parentLineRef: Identifier?; lineRole: Code!; contributesToTotals: Boolean!; netAmount: Money?` | 1 revision; 0..N child lines | Hierarchical signed lines; noncontributing details excluded from totals |
| `Item` | `itemId: Identifier?; description: MultilingualText?; classifications: CodedValue[]` | 0..N lines | Product/service description and schemes |
| `Price` | `priceAmount: Money!; basisQuantity: Quantity?; inclusion: Code?` | 0..N lines | Price basis and inclusion require explicit meaning |
| `Adjustment` | `adjustmentId: Identifier!; scopeRef: Identifier!; kind: Code!; amount: Money!` | 1 scope | Allowance/charge semantics; no double application |
| `DocumentRelationship` | `relationshipId: Identifier!; sourceDocumentRef: Identifier!; targetDocumentRef: Identifier!; relationType: Code!` | 2 documents | Credit/correction/replacement distinct from revision |
| `DocumentReference` | `referenceId: Identifier!; revisionRef: Identifier!; externalId: Text!; scheme: Code?` | 1 revision | PO/contract/despatch references |
| `Supply` | `supplyId: Identifier!; revisionRef: Identifier!; location: Address?; supplyPeriod: Period?` | 1 revision | Source supply facts separate from derived place-of-supply conclusions |
| `TaxPoint` | `taxPointId: Identifier!; scopeRef: Identifier!; date: LocalDate?; classificationRef: Identifier?` | 1 scope | One reusable tax-point concept |
| `PaymentTerms` | `termsId: Identifier!; revisionRef: Identifier!; dueDate: LocalDate?; terms: Text?` | 1 revision | Payment terms not payment processing |
| `AttachmentReference` | `attachmentId: Identifier!; revisionRef: Identifier?; representationRef: Identifier!; purpose: Code?` | 0..1 revision; 1 representation | Exact referenced attachment artifact |

### Tax and monetary

| Entity | Candidate fields (type and nullability) | Logical cardinality | Authoritative responsibility |
|---|---|---|---|
| `TaxRegime` | `regimeId: Identifier!; jurisdiction: Code!; taxScheme: CodedValue!` | 0..N TaxApplication | Scheme identity, not an assessed tax amount |
| `TaxApplication` | `applicationId: Identifier!; revisionRef: Identifier!; regimeRef: Identifier!; scopeType: Code!; scopeRef: Identifier!; magnitude: Money!; direction: Code!; calculationMethod: Code?` (scope and regime must resolve within the same tenant/revision) | 1 revision; 1 regime; 1 economic scope | T01; no summary-as-extra-application |
| `TaxSummary` | `summaryId: Identifier!; revisionRef: Identifier!; groupingKeys: CodedValue[]; computedAmount: Money?` | 0..N applications | T02 derived grouping; never overrides source assertions |
| `SourceAssertion` | `assertionId: Identifier!; representationRef: Identifier!; concept: Code!; assertedValue: TypedValue!` | 1 representation | Preserves source-stated totals/amounts |
| `MonetaryTotal` | `revisionRef: Identifier!; assertedValues: Identifier[]; componentRefs: Identifier[]` | 1 revision | Currency and base explicit |
| `MonetaryBasis` | `basisId: Identifier!; revisionRef: Identifier!; amount: Money!; taxInclusion: Code!` | 1 revision | Candidate T03 basis; not approved entity shape |
| `MonetaryEffect` | `effectId: Identifier!; basisRef: Identifier!; applicationRef: Identifier?; signedContribution: Money!` | 1 basis | Candidate signed effect relative to explicit basis |
| `MonetaryConversion` | `conversionId: Identifier!; sourceMoney: Money!; targetMoney: Money!; rate: Decimal!; effectiveDate: LocalDate?; provenanceRef: Identifier!` | 0..N monetary facts | No implicit cross-currency addition |
| `MonetaryComponent` | `componentId: Identifier!; revisionRef: Identifier!; concept: Code!; amount: Money!; basisRef: Identifier?; sourceAssertionRef: Identifier?; derivationRef: Identifier?; currencyConversionRef: Identifier?` | 1 revision; 0..1 basis | Typed monetary amount; derived and asserted ownership preserved |
| `MonetaryReconciliation` | `evaluationId: Identifier!; revisionRef: Identifier!; basisRef: Identifier?; sourceAssertionRefs: Identifier[]; computedAmount: Money?; outcome: Code!` | 1 revision | G2 proposal; ReconciliationResult compatibility alias only |

### Fiscal and provenance

| Entity | Candidate fields (type and nullability) | Logical cardinality | Authoritative responsibility |
|---|---|---|---|
| `SourceFiscalFact` | `factId: Identifier!; revisionRef: Identifier!; sourceRepresentationRef: Identifier!; semanticConcept: Code!; value: TypedValue!; sourceLocatorRef: Identifier!` | 1 revision; 1 representation | Original local fiscal code, not duplicate core fact |
| `FiscalInterpretation` | `interpretationId: Identifier!; revisionRef: Identifier!; profilePackageRef: Identifier!; inputManifestRef: Identifier!; inputManifestDigest: Digest!; interpretationDigest: Digest!` | 1 revision; 1 package; 0..N derived facts | Pinned reproducible interpretation; physical placement deferred |
| `DerivedFiscalFact` | `factId: Identifier!; interpretationRef: Identifier!; concept: Code!; value: TypedValue!; provenanceRef: Identifier!` | 1 interpretation; 1 provenance | Never overwrites source facts |
| `SourceLocator` | `locatorId: Identifier!; representationRef: Identifier!; locatorExpression: Text!` | 1 representation | Exact source location in immutable artifact |
| `FactProvenance` | `provenanceId: Identifier!; sourceFactRefs: Identifier[]; sourceRevisionRef: Identifier!; rulePackageRef: Identifier?; enrichmentRefs: Identifier[]` | 1 revision | Closed input manifest; zero source facts allowed only for explicit external derivation |
| `EnrichmentSnapshot` | `enrichmentId: Identifier!; providerRef: Identifier!; capturedAt: Instant!; payloadDigest: Digest!` | 0..N provenance | Pinned external inputs |
| `ProfilePackage` | `profilePackageId: Identifier!; jurisdiction: Code!; version: Text!; contentDigest: Digest!; rulesDigest: Digest!; codeListDigests: Digest[]` | 0..N interpretations | Immutable versioned package |

### Representation, compliance and transport

| Entity | Candidate fields (type and nullability) | Logical cardinality | Authoritative responsibility |
|---|---|---|---|
| `DocumentRepresentation` | `representationId: Identifier!; kind: Code!; format: Code!; contentDigest: Digest!; revisionRef: Identifier?; ingestionRef: Identifier?` | 0..1 revision; 0..1 ingestion | Exact original/generated/submitted/certified bytes |
| `ComplianceTransaction` | `transactionId: Identifier!; revisionRef: Identifier!; obligationRef: Identifier!; destinationRef: Identifier!` | 1 revision; 0..N attempts/events | Distinct per-document operation |
| `SubmissionSnapshot` | `snapshotId: Identifier!; revisionRef: Identifier!; revisionDigest: Digest!; interpretationRef: Identifier?; representationRef: Identifier!; representationDigest: Digest!; profilePackageRef: Identifier?; mappingPackageRef: Identifier?; packageApplicability: Code!` | 1 revision; 1 outbound representation | Immutable pinned submission basis |
| `SubmissionAttempt` | `submissionAttemptId: Identifier!; transactionRef: Identifier!; snapshotRef: Identifier!; transportAttemptRef: Identifier?` | 1 transaction; 1 snapshot | Per-document attempt distinct from transport attempt |
| `ProcessingEvent` | `eventId: Identifier!; subjectType: Code!; subjectRef: Identifier!; eventType: Code!; observedAt: Instant!; evidenceRefs: Identifier[]` | 1 typed subject | Append-only; legal status not inferred from transport receipt |
| `ValidationFinding` | `findingId: Identifier!; subjectRef: Identifier!; ruleRef: Identifier!; severity: Code!; message: Text!` | 1 subject | Non-destructive validation |
| `ResponseCorrelation` | `correlationId: Identifier!; responseRef: Identifier!; candidateSubjectRefs: Identifier[]; resolutionState: Code!; resolvedSubjectRef: Identifier?; reason: Text?` | 0..1 resolved subject | Ambiguous correlation remains unknown |
| `FiscalIdentity` | `fiscalIdentityId: Identifier!; issuerRef: Identifier!; scheme: Code!; value: Text!; artifactRef: Identifier!` | 1 artifact | Typed authority identity, not transport correlation |
| `FiscalEvidence` | `evidenceId: Identifier!; artifactRef: Identifier!; evidenceType: Code!; representationRef: Identifier?` | 1 artifact | Receipt/signature/clearance evidence preserved |
| `IngestionRecord` | `ingestionId: Identifier!; sourceArtifactRefs: Identifier[]; receivedAt: Instant!; tenantRef: Identifier!` | 0..N extractions | Completed external ingestion retains >=1 original artifact |
| `DocumentExtraction` | `extractionId: Identifier!; ingestionRef: Identifier!; sourceMemberLocator: Text!; documentRef: Identifier?` | 1 ingestion; 0..1 document | Batch extraction not automatically legal identity |
| `WorkingDocument` | `workingId: Identifier!; extractionRef: Identifier?; documentRef: Identifier?; state: Code!` | 0..1 extraction; 0..1 document | Pre-publication mutable working state |
| `SubmissionEnvelope` | `envelopeId: Identifier!; destinationRef: Identifier!; payloadRepresentationRef: Identifier?; memberManifestDigest: Digest?` | 0..N members in draft; >=1 submitted | Transport container not billing identity |
| `EnvelopeMember` | `memberId: Identifier!; envelopeRef: Identifier!; transactionRef: Identifier!; snapshotRef: Identifier!; revisionRef: Identifier!; representationRef: Identifier!` (revision/representation must match snapshot) | 1 envelope; 1 transaction | Member-specific processing and correlation |
| `TransportAttempt` | `transportAttemptId: Identifier!; envelopeRef: Identifier!; payloadRepresentationRef: Identifier!; submittedAt: Instant?` | 1 envelope; 1 immutable payload | Transport retry creates new attempt |
| `TransportResponse` | `responseId: Identifier!; attemptRef: Identifier!; representationRef: Identifier!; subjectType: Code!; memberRef: Identifier?` | 1 attempt; optional member | Envelope response != member acceptance |
| `LegalStateAssessment` | `assessmentId: Identifier!; revisionRef: Identifier!; profilePackageRef: Identifier!; evidenceRefs: Identifier[]; result: Code!` | 1 revision | Legal state based on profile/evidence |
| `DuplicateResolution` | `resolutionId: Identifier!; ingestionRefs: Identifier[]; candidateDocumentRefs: Identifier[]; basis: Code!; result: Code!` | 0..N ingestions | Repeated reception != duplicate legal document |

## 4. G2 reconciliation dispositions (candidate)

| Conflict | Draft 1.5 treatment | Decision status |
|---|---|---|
| ReconciliationResult / MonetaryReconciliation | `MonetaryReconciliation` is the evaluation; former compatibility alias | Proposed |
| TaxPoint duplication | One reusable `TaxPoint`; local exigibility codes live in source/derived fiscal facts | Proposed |
| SubmissionAttempt / TransportAttempt | Distinct document-operation and transport-dispatch identities; membership link by references | Proposed |
| SourceFiscalFact / commercial fact | Original local fiscal code vs authoritative intrinsic commercial assertion; no duplication | Proposed |
| FiscalIdentity / FiscalEvidence | Typed identity separate from immutable proof | Proposed |
| SourceAssertion / TaxSummary | Original asserted value separate from computed summary and reconciliation | T02 accepted policy; fields proposed |

## 5. Conditional cardinality rules and exceptions

| Context | Logical minimum | What is NOT assumed |
|---|---|---|
| Completed external ingestion | >=1 immutable source artifact; 0..N extractions | One artifact != one invoice |
| Pre-publication working document | 0..N working states, no published revision required | Internal publication != legal issuance |
| BillingDocument | 0..N revisions; >=1 once published | Revisions not legal corrective invoices |
| PublishedRevision | 0..N parties/lines in base contract | Invoice profile may require seller, buyer, lines |
| PartyParticipation | Exactly 1 immutable PartySnapshot | Does not prescribe master-data tables |
| FiscalInterpretation | Exactly 1 pinned revision and profile/input manifest | 0..N interpretations per revision |
| Submitted TransportAttempt | Exactly 1 immutable payload | Envelope receipt != member acceptance |
| Submitted multi-member envelope | >=1 frozen members | Member outcome may be unknown |
| Submitted SubmissionAttempt | Exactly 1 immutable SubmissionSnapshot | No mutable latest references |
| Legal assessment | Profile and evidence references where required | Cannot infer from transport status |

## 6. Reference integrity and semantic constraints

1. Tenant-scoped identity uniqueness and reference resolution are mandatory for logical consistency; exact namespace policy is pending.
2. Line parent references must be acyclic, point within the same revision, and never double-count noncontributing explanatory children.
3. TaxApplication regimeRef must resolve to a TaxRegime; scopeRef must resolve to the stated scope. Summaries must not be counted as new applications.
4. Source assertions and computed monetary values remain distinct, with currency, basis and rounding provenance.
5. DerivedFiscalFact must reference a pinned FiscalInterpretation and provenance; no derived value overwrites a source fact.
6. Each submitted member must resolve to an exact revision, compliance operation and immutable representation.
7. A response can be ENVELOPE or MEMBER scoped; unmatched/ambiguous responses remain unresolved.
8. Credit notes are separate documents with typed references, not automatic mutation of the original.
9. Fiscal identity must bind to the exact authorized artifact, distinct from transport correlation IDs.
10. Duplicate ingestion does not establish duplicate legal identity or idempotency without a separately recorded resolution.

## 7. Representative logical examples and validation

The machine-readable candidate instances and structural checks are in `tests/CTC-003/`. Five positive fixtures and five negative controls test the proposed contract. The fixture format is a **test projection**, not a normative public API or accepted JSON schema.

## 8. Traceability and semantic-loss follow-up

| Prior source concept | Candidate concept | Disposition | Risk |
|---|---|---|---|
| SemanticDocument/DocumentIdentity | BillingDocument + PublishedRevision | Split | Legal-number timing unresolved |
| SemanticParty | PartySnapshot + PartyParticipation | Refine | Party snapshot profile minima unresolved |
| SemanticLine | BillingLine | Refine | Hierarchical contribution validation |
| TaxRegime / TaxApplication | Same distinct concepts | Retain | Country-specific regime rules deferred |
| RegimeTaxTotal / MonetaryTotal | SourceAssertion + TaxSummary + MonetaryTotal | Split | Precision/rounding evidence pending |
| DocumentControl | Representation + ComplianceTransaction + SubmissionSnapshot | Split | Operational legacy mapping incomplete |
| FormatNativeBag | SourceFiscalFact + governed extensions + original artifact | Replace uncontrolled bag | Field-level loss analysis CTC-009 |
| SignatureData | FiscalIdentity + FiscalEvidence | Split | Authority evidence fixtures pending |
| MandateScope | ProfilePackage / jurisdiction profile | Refine | Version/effective-date policy CTC-005/007 |

## 9. Review gates and open questions

- **G1:** Candidate catalogue, types, optionality and conditional cardinality documented; detailed field review still required.
- **G2:** Six G2 logical ownership directions accepted under standing blitz authorization; detailed fields/invariants proposed.
- **G3:** Synthetic structural instance validation executed; does not demonstrate full semantic or regulatory coverage.
- **G4:** Entity-level traceability available; exhaustive field-level loss matrix remains CTC-009.
- **G5:** Explicit approval of detailed dictionary and scoped closure not yet obtained.
- Open: FiscalContext physical A/B/C; publication/issuance policy by jurisdiction; source fixture evidence; precise relationship nullability for all document families; comprehensive version compatibility; full tax rounding and FX rules.

## 10. Checkpoint

**CTC-003 remains In Progress.** Do not promote this draft to the accepted model baseline. Next: review G1/G2 field constraints, extend G3 fixtures, then G4/G5 approval gate.

---

## 11. Integrated constraint governance and outstanding evidence

The revised fields for `PublishedRevision`, `TaxApplication`, `FiscalInterpretation`, `MonetaryTotal`, `MonetaryComponent`, `SubmissionSnapshot`, `EnvelopeMember`, and `ResponseCorrelation` are now integrated in Section 3. These are **candidate field shapes**, not approved detailed schema.

- Publication-required parties and lines are selected by immutable document-family/profile rules, not universal base minima.
- A fiscal input manifest must be resolvable and content-pinned, including enrichment inputs.
- An ambiguous response cannot have an authoritative resolved subject until disambiguation evidence is retained.
- A submitted envelope must freeze membership and reference exactly the pinned member snapshots.
- Cross-currency comparisons require recorded conversion provenance; calculation and rounding policy remain profile-dependent.
- `ReconciliationResult` is a compatibility alias only, not an independent authoritative evaluation.
- `TaxPoint` has one semantic owner; local exigibility codes remain fiscal source/derived facts.
- `FiscalIdentity` and `FiscalEvidence` have different identities and responsibilities.
- `DuplicateResolution` must distinguish byte equality, business-identity match and transport idempotency.
- `AttachmentReference` may refer to an immutable external locator pre-preservation, subject to later retrieval obligations.

**Open:** G2-01..08 detailed invariants; exhaustive 48-entity validation; field-level source migration/loss matrix (CTC-009); authority fixtures (CTC-008/010); FiscalContext physical A/B/C; detailed cardinalities beyond approved qualified logical rules.
