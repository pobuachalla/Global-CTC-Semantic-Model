# CTC-003 — Document Identity and Commercial Semantics Entity Dictionary

**Version:** Draft 0.2 · **Date:** 2026-10-20 · **Status:** Proposed / not approved  
**Task:** CTC-003 · **Scope:** Document identity, published revisions, party snapshots, line hierarchy, commercial adjustments, references, corrections and supporting value objects. Tax arithmetic, detailed fiscal interpretation, persistence and APIs are deferred.

## 1. Authority, provenance and design status

- **Accepted constraints:** CTC-002 principles P1–P7, D2 nine-concept logical contract and invariants I-01–I-10, as explicitly approved in the project conversation. This document proposes *detailed* structures; it does not change those approvals.
- **Primary source:** `semantic-billing-model(1) (1).md`, v0.3, sections 4–6 and 12.2. Existing concepts and illustrative cardinalities are taken from that draft unless labelled proposed refinement.
- **Comparison source:** `CTC-Semantic-Document-Entity-Model.docx`, v1.0 (7 Sep 2026); older `SemanticDocument`, `SemanticLine`, party and references structures.
- **Known limitation:** Current remote GitHub revision and final CTC-002 approved I-01–I-10 wording were not independently fetched in this session. Use the repository's accepted decision record as authority if wording differs. No regulatory fixture or country-specific legal rule is verified here.
- **Notation:** `1` exactly one, `0..1` optional single, `0..N` optional collection, `1..N` nonempty collection. **Draft** cardinalities apply to a published invoice where specified; draft/incomplete submissions may use different validation states. `Proposed` means not accepted.

## 2. Fundamental identity boundary

| Concept | Semantic responsibility | Authoritative owner | Proposed invariant |
|---|---|---|---|
| `BillingDocument` | Stable platform identity for a logical billing document | Document registry | `documentId` stable, tenant-scoped, not an invoice number |
| `PublishedRevision` | Immutable issued commercial content snapshot | Revision | Document number, series, type, issue date and content facts frozen at publication |
| `DocumentRelationship` | Typed relationship to another legal/business document | Referring revision | Correction/credit is not a mutation of referenced issued invoice |
| `DocumentRepresentation` | Exact source/generated/submitted serialization | Representation record (outside this dictionary) | Not a substitute for semantic revision identity |
| `FiscalIdentity` | Externally assigned fiscal identity | Fiscal identity/evidence domain (deferred) | Not conflated with supplier document number |

**Open:** The term `PublishedRevision` is a logical D2 concept. A working draft may exist before publication, but draft identity and draft-to-published transition are not yet modelled. Do not treat every ERP re-send as a new legal revision.

## 3. Entity dictionary

### DOC-01 BillingDocument — logical identity

| Attribute | Type | Cardinality | Constraint / notes |
|---|---|---|---|
| `documentId` | OpaqueIdentifier | 1 | Platform-assigned; stable within tenant; not a fiscal or submission ID |
| `tenantRef` | TenantReference | 1 | Logical isolation scope; tenancy representation deferred |
| `revisionRefs` | PublishedRevisionRef | 0..N | Only immutable published revisions; draft workflow separately defined |
| `relatedDocumentRefs` | DocumentRelationshipRef | 0..N | Optional index/projection, not a second authoritative relationship store |

**Do not authoritatively duplicate:** `documentNumber`, `documentSeries`, `documentType`, `issueDate`, totals, parties or mutable compliance status on this root. A read model may project current published values.

### DOC-02 PublishedRevision — immutable commercial snapshot

| Attribute | Type | Cardinality | Constraint / notes |
|---|---|---|---|
| `revisionId` | OpaqueIdentifier | 1 | Stable and unique within tenant |
| `documentRef` | BillingDocumentRef | 1 | Refers to DOC-01 |
| `revisionLabel` | String | 1 | Display/order label; uniqueness within document proposed |
| `documentNumber` | String | 1 | From v0.3 BillingDocument; issuer-facing identifier |
| `documentSeries` | String | 0..1 | Separate only when meaningful in source |
| `documentType` | CodedValue | 1 | INVOICE, CREDIT_NOTE, DEBIT_NOTE, SELF_BILLED_* candidate taxonomy |
| `issueDate` | Date | 1 | Date as stated on document; no automatic substitution with ingestion time |
| `issueTime` | TimeWithOffset? | 0..1 | Timezone semantics need review |
| `documentCurrency` | CurrencyCode | 1 | ISO currency code where applicable |
| `taxCurrency` | CurrencyCode | 0..1 | Distinct reporting currency if stated |
| `partyRoles` | PartyParticipation | 2..N* | Seller and buyer required for standard invoice profile; conditional for other document types |
| `lines` | BillingLine | 1..N* | Published standard invoice; conditional for document family/profile |
| `documentAdjustments` | Adjustment | 0..N | Distinct from price-level/line-level adjustments |
| `monetaryTotals` | MonetaryTotal | 1* | Detailed value definition deferred to CTC-004 |
| `taxFacts` | Tax / TaxApplication | 0..N | Detailed tax model deferred to CTC-004 |
| `documentRelationships` | DocumentRelationship | 0..N | Authoritative outgoing references |
| `notes` | Note | 0..N | Typed text; preserve original note when extracting structure |
| `paymentMeans` | PaymentMeans | 0..N | Payment instruction(s) |
| `paymentTerms` | PaymentTerms | 0..N | Terms and dates |
| `supply` | Supply | 0..1 | Supply/delivery context |
| `accountingPeriod` | Period | 0..1 | Period in source |
| `taxPoint` | TaxPoint | 0..1 | Shared semantic meaning; profile-derived interpretation separately recorded |
| `attachments` | AttachmentReference | 0..N | Link to immutable supporting artifact |
| `sourceFiscalFactRefs` | SourceFiscalFactRef | 0..N | D2 P7 traceability; fact ownership and embedding deferred |
| `publishedAt` | Instant | 1 | Platform publication/freeze event, distinct from `issueDate` |
| `semanticModelVersion` | VersionRef | 1 | Exact version for interpretation/replay |
| `contentFingerprint` | Digest | 1 | Canonicalization algorithm must be versioned; precise digest contract deferred |

`*` Proposed publication-time requirements for ordinary invoices, **not universal requirements for all legal document families**. No separate `status` field is introduced on the revision.

### PARTY-01 PartySnapshot — party as represented on this revision

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `partySnapshotId` | OpaqueIdentifier | 1 | Identity of this frozen snapshot, not a global party master |
| `legalName` | Text | 0..1 | Jurisdiction profile may require |
| `tradingName` | Text | 0..1 | Optional |
| `displayName` | Text | 0..1 | Preserve source naming distinction |
| `identifiers` | Identifier | 0..N | Scheme/authority qualified |
| `taxRegistrations` | TaxRegistration | 0..N | May be several regimes |
| `legalRegistrations` | LegalRegistration | 0..N | v0.3 includes legal registration concept |
| `addresses` | Address | 0..N | Explicitly role-typed where needed |
| `contacts` | Contact | 0..N | May include personal data; retention review later |
| `sourcePartyRef` | ExternalPartyRef | 0..1 | Optional ERP/master-data linkage, not authoritative for published snapshot |

**Proposed invariant:** A later master-data update cannot silently alter the party facts printed or legally represented on an earlier published invoice.

### PARTY-02 PartyParticipation — role at document or line scope

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `role` | CodedValue | 1 | SELLER, BUYER, PAYEE, TAX_REPRESENTATIVE, SHIP_TO, SHIP_FROM, INTERMEDIARY, etc. |
| `partySnapshotRef` | PartySnapshotRef | 1 | Frozen party details |
| `scope` | ScopeRef | 1 | Published revision or specific BillingLine |
| `roleQualifier` | CodedValue | 0..1 | Country/profile nuance without inventing new party class |

**Proposed uniqueness:** one primary SELLER and one primary BUYER for ordinary invoice profiles; multiple other roles allowed. Do not make seller/buyer global cardinalities universal before document-family review. Line-level seller may differ from header seller, as v0.3 stress test notes.

### PARTY-03 Identifier

`value: String (1)`, `type: CodedValue (0..1)`, `scheme: String (0..1)`, `issuingAuthority: String (0..1)`, `country: CountryCode (0..1)`, `jurisdiction: String (0..1)`.

**Proposed:** identifier equivalence is not established by string equality alone; compare scheme, authority and jurisdiction where relevant. Do not conflate fiscal IDs assigned after clearance with party tax registration IDs.

### PARTY-04 TaxRegistration

`identifier: Identifier (1)`, `taxScheme: CodedValue (1)`, `country: CountryCode (0..1)`, `registrationType: CodedValue (0..1)`, `validityPeriod: Period (0..1, proposed)`.

### PARTY-05 LegalRegistration

`registrationIdentifier: Identifier (1)`, `registeredName: Text (0..1)`, `legalForm: CodedValue/Text (0..1)`, `jurisdiction: JurisdictionRef (0..1)`.

### PARTY-06 Address

`addressLines: Text[] (0..N)`, `street: Text (0..1)`, `buildingNumber: String (0..1)`, `city: Text (0..1)`, `postalCode: String (0..1)`, `subdivision: String (0..1)`, `country: CountryCode (0..1)`, `purpose: CodedValue (0..1)`.

Do not fabricate missing country or postal values. Publication requirements depend on profiles.

### PARTY-07 Contact

`name: Text (0..1)`, `department: Text (0..1)`, `telephone: String (0..1)`, `email: String (0..1)`.

### LINE-01 BillingLine

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `lineId` | OpaqueIdentifier | 1 | Stable within revision; distinct from printed `lineNumber` |
| `lineNumber` | String | 1 | Source/business line ID |
| `lineRole` | CodedValue | 1 | STANDARD, GROUP, DETAIL, with profile extensions |
| `parentLineRef` | BillingLineRef | 0..1 | Same revision only |
| `contributesToDocumentTotals` | Boolean | 1 | Must be explicit or reproducibly derived; source/derivation retained |
| `quantity` | Quantity | 0..1 | Optional on GROUP/informational lines |
| `item` | Item | 0..1 | Optional on aggregating lines |
| `price` | Price | 0..1 | Optional where source provides summary only |
| `lineNetAmount` | Money | 1 | Signed economic value; no positivity constraint |
| `parties` | PartyParticipation | 0..N | Line-specific roles |
| `identifiers` | Identifier | 0..N | Source identifiers for item/line |
| `adjustments` | Adjustment | 0..N | Line-level; not price-level |
| `taxes` | Tax / TaxApplication | 0..N | Detailed semantics deferred |
| `taxSummaries` | TaxSummary | 0..N | May exist at GROUP level |
| `period` | Period | 0..1 | Line service period |
| `taxPoint` | TaxPoint | 0..1 | Tax point at line level |
| `documentRelationships` | DocumentRelationship | 0..N | Line-specific external references |

**Invariants (proposed):** parent and child share revision; hierarchy is acyclic; `lineId` unique in revision; `lineNumber` uniqueness by profile; contribution rule must prevent double-counting. Signed amounts retained even in positive invoices. A child DETAIL can be noncontributing while GROUP contributes.

### LINE-02 Item

`name: Text (0..1)`, `descriptions: Note/Text[] (0..N)`, `sellerItemId: Identifier (0..1)`, `buyerItemId: Identifier (0..1)`, `standardIds: Identifier[] (0..N)`, `classifications: ItemClassification[] (0..N)`, `countryOfOrigin: CountryCode (0..1)`.

### LINE-03 ItemClassification

`code: String (1)`, `scheme: String (1)`, `version: String (0..1)`.

### LINE-04 Quantity

`value: Decimal (1)`, `unit: UnitCode (1)`. Negative quantities not universally forbidden; sign and amount reconciliation are profile/document-type constrained.

### LINE-05 Price

`netAmount: Money (1)`, `grossAmount: Money (0..1)`, `baseQuantity: Quantity (0..1)`, `adjustments: Adjustment[] (0..N)`.

**Invariant:** Price-level adjustments must not be counted again as line allowances unless explicitly represented as a distinct economic adjustment.

### LINE-06 Adjustment

`type: Code (1, ALLOWANCE/CHARGE)`, `amount: Money (1)`, `reason: Text (0..1)`, `reasonCode: CodedValue (0..1)`, `percentage: Decimal (0..1)`, `baseAmount: Money (0..1)`, `taxes: Tax[] (0..N)`.

Its scope is determined by owning relationship: document, line or price. **Open:** Whether amount sign is signed or magnitude-plus-type; needs CTC-004 resolution to avoid double negation.

### REL-01 DocumentRelationship

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `relationshipId` | OpaqueIdentifier | 1 | Unique in referring revision |
| `relationshipType` | CodedValue | 1 | ORDER, CONTRACT, DELIVERY, REFERENCES, CREDITS, DEBITS, CORRECTS, REPLACES, CANCELS |
| `relatedDocument` | DocumentReference | 1 | Can refer to external document not in platform |
| `reason` | Text | 0..1 | Optional explanatory reason |
| `sourceFactRefs` | SourceFactRef | 0..N | P7 provenance when relationship derived |

**Proposed invariant:** A credit note is an independent `BillingDocument` with a `CREDITS` link, not an overwrite of the credited invoice. A cancellation *process* and a cancellation *document* are distinct and jurisdiction-dependent; `CANCELS` alone does not prove legal cancellation succeeded.

### REL-02 DocumentReference

`documentRef: BillingDocumentRef (0..1)`, `externalNumber: String (0..1)`, `externalSeries: String (0..1)`, `documentType: CodedValue (0..1)`, `issueDate: Date (0..1)`, `identifiers: Identifier[] (0..N)`, `description: Text (0..1)`.

**Constraint:** At least one resolvable identity mechanism must exist (internal reference, external number with suitable context, or typed external identifier). An external document may not exist in the platform.

### COM-01 Supply

`supplyDate: Date (0..1)`, `supplyPeriod: Period (0..1)`, `placeOfSupply: LocationRef (0..1)`, `deliveryLocation: LocationRef (0..1)`, `dispatchLocation: LocationRef (0..1)`, `deliveryParty: PartySnapshotRef (0..1)`, `dispatchParty: PartySnapshotRef (0..1)`, `incoterm: CodedValue (0..1)`, `transportReference: Identifier (0..1)`.

**Open:** Place-of-supply source fact versus legal place-of-supply interpretation (P7) requires later profile mapping review.

### COM-02 Period

`startDate: Date (0..1)`, `startTime: Time (0..1)`, `endDate: Date (0..1)`, `endTime: Time (0..1)`, `description: Text (0..1)`. Validate ordering only when comparable bounds exist.

### COM-03 TaxPoint

`date: Date (0..1)`, `basisCode: CodedValue (0..1)`, `period: Period (0..1)`, `description: Text (0..1)`. Source date and derived exigibility classification must have distinct provenance.

### COM-04 Note

`text: Text (1)`, `code: CodedValue (0..1)`, `subject: Text (0..1)`, `language: LanguageCode (0..1)`. Preserve original text if structured qualifiers are extracted.

### COM-05 PaymentMeans

`meansCode: CodedValue (1)`, `paymentReference: String (0..1)`, `financialAccount: FinancialAccount (0..1)`, `dueDate: Date (0..1)`.

### COM-06 PaymentTerms

`description: Text (0..1)`, `dueDate: Date (0..1)`, `installmentDetails: PaymentInstallment[] (0..N, proposed)`.

### COM-07 FinancialAccount

`accountIdentifier: Identifier (1)`, `financialInstitutionIdentifier: Identifier (0..1)`, `accountName: Text (0..1)`.

### COM-08 AttachmentReference

`attachmentId: OpaqueIdentifier (1)`, `filename: String (0..1)`, `mimeType: String (0..1)`, `description: Text (0..1)`, `artifactRef: ArtifactReference (1)`. Exact bytes, hash and retention belong to representation/evidence architecture.

## 4. Relationship and cardinality register (proposed)

| From | Relationship | To | Cardinality | Constraint |
|---|---|---|---|---|
| BillingDocument | has | PublishedRevision | 0..N | Revision belongs to exactly one document |
| PublishedRevision | participates | PartyParticipation | 2..N* | Standard invoice: seller and buyer |
| PartyParticipation | references | PartySnapshot | 1 | Immutable party snapshot |
| PublishedRevision | contains | BillingLine | 1..N* | Document-type/profile dependent |
| BillingLine | parent | BillingLine | 0..1 | Same revision, no cycles |
| BillingLine | includes | Item | 0..1 | Group may have no item |
| BillingLine | has | Price | 0..1 | Summary may omit price |
| Price | includes | Adjustment | 0..N | Price-level adjustment |
| BillingLine | includes | Adjustment | 0..N | Line-level adjustment |
| PublishedRevision | includes | Adjustment | 0..N | Document-level adjustment |
| PublishedRevision | relates | DocumentRelationship | 0..N | Referring revision owns relationship |
| DocumentRelationship | targets | DocumentReference | 1 | Internal or external target |
| PublishedRevision | has | Supply | 0..1 | Delivery and supply semantics |
| PublishedRevision | has | PaymentMeans | 0..N | Multiple means permitted |
| PublishedRevision | has | PaymentTerms | 0..N | Installments possible |
| PublishedRevision | has | AttachmentReference | 0..N | Bytes stored elsewhere |

`*` For published standard invoices only; not approved universal cardinality.

## 5. Traceability to earlier drafts

| Current proposal | Billing v0.3 source | Earlier SemanticDocument v1.0 | Change rationale |
|---|---|---|---|
| BillingDocument + PublishedRevision | BillingDocument §4.1 | DocumentIdentity | Separates stable platform identity from immutable published facts (P2/P6) |
| PartySnapshot + PartyParticipation | Party, PartyRole §§4.2–4.3 | SemanticParty | Freeze as-issued details, allow line-level roles |
| Identifier, TaxRegistration, LegalRegistration | §§4.4–4.5 | PartyIdentifier and tax identifiers | Typed identifiers with scheme and issuing authority |
| BillingLine | §4.8 | SemanticLine | Preserve GROUP/DETAIL, hierarchy, contribution, signed amounts |
| Price and Adjustment | §§4.13–4.14 | Price, LineCharge, DocumentCharge | Preserve separate adjustment scopes |
| DocumentRelationship + Reference | §§4.21–4.22 | SemanticReferences | Legal correction distinct from internal revision |
| Supply, TaxPoint, Note | §§4.23–4.24b | SemanticDelivery, notes | Shared meaning; local classification separately interpreted |
| AttachmentReference | §4.25 | SemanticAttachment | Preserve artifact without forcing inline bytes |

## 6. Open design questions / decision register candidates

- **Q-003-01:** Exact publication boundary: does a normalized invoice become published at ingestion, client approval, legal issuance or another explicit event?
- **Q-003-02:** Must every published revision have an independently frozen party snapshot, or can equivalent immutable value objects suffice?
- **Q-003-03:** Are document number/type/date authoritative only on revision, with root-level fields projections? Proposed yes, not accepted.
- **Q-003-04:** Which document types legitimately omit billing lines, buyer/seller, totals or issue date?
- **Q-003-05:** What is the canonical allowance/charge sign convention across price, line and document scopes?
- **Q-003-06:** How are corrections after fiscal authorization distinguished from draft amendments and authority cancellation processes?
- **Q-003-07:** Are source-provided party identifiers and inferred/enriched registration values distinct immutable facts with provenance?
- **Q-003-08:** Should party participation reference snapshot identity, embed party value, or both? Logical semantics must remain stable.
- **Q-003-09:** How do multi-line/group tax summaries reconcile without double-counting?
- **Q-003-10:** How are multilingual fields and source text preservation represented as value types?

## 7. Scenario acceptance tests (not yet executed)

1. **Invoice snapshot:** ERP master data changes after issuance; previous seller name/address remains unchanged.
2. **Grouped lines:** GROUP +21,425.59, explanatory DETAIL +21,425.59 (noncontributing), GROUP -204.78 => contributing total 21,220.81.
3. **Credit note:** New DOC-002 / REV-002 credits DOC-001 / REV-001; original remains unchanged.
4. **External predecessor:** DocumentRelationship targets invoice not stored on platform, preserving number/scheme/issuer context.
5. **Multi-role:** Same party appears as seller and ship-from; roles are independent of party identity.
6. **Source/derived:** ERP place-of-supply field and derived jurisdiction interpretation remain separately traceable.
7. **Mixed adjustments:** Gross price adjustment and line allowance are not counted twice.

## 8. CTC-003 checkpoint

- **Task:** CTC-003 In Progress; this is a proposed commercial-domain dictionary only.
- **Accepted decisions unchanged:** P1–P7, D2 logical contract, I-01–I-10.
- **Proposed new detailed schema decisions:** All DOC/PARTY/LINE/REL/COM attributes, publication-time cardinalities and ownership refinements.
- **No new approved ADRs.** FiscalContext A/B/C physical aggregation deferred.
- **Next within CTC-003:** Review DOC-01/DOC-02 authority, PartySnapshot ownership, line contribution and correction relationships; then draft tax/monetary dictionary and cross-domain integrity matrix.
- **Suggested repository path:** `research/CTC-003/CTC-003-DOCUMENT-COMMERCIAL-ENTITY-DICTIONARY-DRAFT-0.2.md`.
