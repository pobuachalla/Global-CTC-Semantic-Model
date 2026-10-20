# CTC-001 — SemanticDocument / BillingDocument Reconciliation

**Date:** 2026-10-19  
**Status:** DRAFT FOR REVIEW — no decisions approved  
**Backlog:** CTC-001 (P0); next dependency CTC-002  
**Evidence classification:** A = supplied design artifact; B = independently verified fixture/specification; C = architectural inference/recommendation. This review contains A and C only; no B validation was performed.

## Scope, sources and limitations

**Goal:** Compare entities, cardinalities, constraints and boundaries of the earlier SemanticDocument and newer BillingDocument v0.3, preserve strengths, expose conflicts, and propose options rather than select a final canonical schema.

**Read:** MASTER-PROMPT.md v1.0 (2026-10-19); BACKLOG.md, DECISIONS.md, MODEL-BASELINE.md (2026-10-19); CTC-Semantic-Document-Entity-Model.docx v1.0 (2026-09-07); ctc-transformation-framework-reference-v1.1.md (architecture revision v1.1); ctc-transformer-complete-reference.md (earlier service-oriented reference); semantic-billing-model(1) (1).md v0.3; relational-data-model(1) (1).md v0.3; available relational-model Mermaid drafts. ERP DOCX, tracker HTML, format workbook and sample ZIP are present but not exhaustively reviewed in this semantic reconciliation. No GitHub repository fixture was independently inspected. Two near-duplicate copies of the v0.3 semantic and relational drafts exist; no equivalence check has been performed.

**Acceptance criteria:** entity-by-entity crosswalk; conflict register; options, migration implications and source anchors; no unapproved architecture decision promoted.

## Executive conclusion

The v0.3 BillingDocument design broadens the semantic expressiveness of the earlier pivot and separates fiscal, representation and process concerns. The earlier design's explicit TaxRegime/TaxApplication references, multilingual SemanticText, mapping lineage and immutable transformation packs remain valuable. The right target is not yet determined: a commercial BillingDocument alone is insufficient as a full transformation result, while an all-in-one SemanticDocument conflates business meaning with operational state. **Proposed hypothesis:** a composed semantic exchange contract referencing separately owned billing, fiscal, representation and compliance objects. **Not approved.**

## Entity and constraint reconciliation matrix

| # | Earlier SemanticDocument v1.0 | Newer BillingDocument v0.3 | Key difference / issue | Proposed disposition (not approved) |
|---|---|---|---|---|
| 01 | `SemanticDocument` root contains business, control, native | `BillingDocument` business root; associated fiscal/process/representation | Root scope and aggregate ownership differ | **REVIEW** composed contract versus replacement |
| 02 | `DocumentIdentity.id`, `typeCode`, dates, currency, `profileId` | `documentNumber`, `documentSeries`, `documentType`, issue date/time, currencies | Earlier concatenates CFDI Serie/Folio; newer separates; profile ID moves to representation | **REFINE** distinguish business ID, series, format profile, internal ID |
| 03 | `SemanticParty` mandatory name, identifier array >=1, address and city | `Party` optional name/legal name, identifiers, address; roles | Earlier cardinality encourages invented placeholders | **REFINE** base vs profile-specific completeness |
| 04 | `PartyIdentifier` scheme/value | `Identifier`, `TaxRegistration`, `LegalRegistration` | Richer identifier meaning, issuer and legal-form distinction | **RETAIN/EXPAND** identifier semantics; no forced primary-by-array-position |
| 05 | Supplier, buyer, optional payee/tax representative | Seller, buyer, `PartyRole[]` incl intermediary, platform, logistics | More roles; issuer need not equal seller | **REVIEW** role taxonomy and issuer/seller distinction |
| 06 | One address and optional contact per party | Address/contact potentially multiple; separate legal registration | Base multiplicity differs between v0.3 conceptual text and relational draft | **REVIEW** document snapshots and role-specific addresses |
| 07 | `SemanticText` multilingual map | `Note` language-tagged and other text often strings | Earlier multilingual support may be weakened | **RETAIN** multilingual value semantics; clarify BCP-47 keys |
| 08 | `SemanticLine` flat, quantity/unit/price required; net >=0 | `BillingLine` hierarchy, optional quantity/price, signed net, group/detail and contribution flag | Incompatible cardinality and sum invariants | **REFINE** hierarchical line and explicit reconciliation scope |
| 09 | `ItemClassification[]`, seller/buyer item IDs on line | `Item`, `ItemClassification`, multiple identifiers | Item is now a distinct semantic concept | **RETAIN** separate item/line identity |
| 10 | `unitPrice`, `grossUnitPrice` | `Price` + `baseQuantity`, `adjustments[]` | Price allowance differs from line allowance | **REFINE** price-level adjustments and quantity bases |
| 11 | `LineCharge`, `DocumentCharge` separate | `Adjustment` reusable at document, line and price scope | Common meaning, ownership still distinct | **REVIEW** one semantic type with scope via containment |
| 12 | `TaxRegime[]` + `TaxApplication[]`, `regimeRef` | `Tax[]`, `TaxSummary[]` with type/direction/method | Earlier strong regime reference; newer handles per-unit and withholding explicitly | **COMPOSE** regime identity + generalized application; test first |
| 13 | `categoryCode` restricted to EN16931 codes | `Tax.category` scheme-specific | Earlier EU codes incorrectly universalized | **REFINE** qualified category scheme, not global EU enum |
| 14 | Nonnegative taxable/tax amounts and separate withholdingAmount | Tax direction CHARGE/WITHHOLD; signed economics | Need clear sign convention and no double counting | **REVIEW** tax direction, magnitude, withholding arithmetic |
| 15 | `RegimeTaxTotal[]`, totalTaxAmount | `TaxSummary[]`, charged/withheld totals | Summaries need regime, direction, currency and tax base dimensions | **COMPOSE** without assuming 1 row per regime |
| 16 | `MonetaryTotal` sum of all line amounts, fixed tolerances | Totals with contribution-aware reconciliation and separate withholding | Earlier CV-02/CV-05 fail grouped detail; fixed tolerance may be wrong | **REFINE** explicit total basis and profile-specific rounding |
| 17 | `AEDTotals` country-specific nested totals | `Money` with currency; tax currency in header | Country-specific totals should not be universal | **REVIEW** FX and tax reporting currency as reusable concepts |
| 18 | `PaymentMeans` merges means, due date, terms | `PaymentMeans`, `PaymentTerms`, `FinancialAccount` | Separates how versus when | **RETAIN** separation, clarify installments |
| 19 | `SemanticDelivery` | `Supply`, `Period`, `TaxPoint` | Distinguishes delivery, supply, service, tax exigibility | **RETAIN** concepts, resolve tax-point owner |
| 20 | `SemanticReferences` fixed slots (order, contract, preceding) | `DocumentRelationship[]` + `DocumentReference` | Newer supports multiple typed references and corrections | **RETAIN** typed multiplicity and relation direction |
| 21 | `SemanticAttachment` content/URI | `Attachment` metadata and reference | Binary persistence not semantic model | **RETAIN** content metadata; keep raw representations distinct |
| 22 | `DocumentControl` source, target, clearance, lineage; older variants embed signatures and statuses | `DocumentRepresentation`, `FiscalContext`, `ComplianceTransaction` | Stronger separation; target scope can be 1:N | **REVIEW** process boundary and revision links |
| 23 | `FormatNativeBag` by format family, arbitrary unknown entries | Namespaced typed `JurisdictionExtension`, governed validation | Native preservation versus semantically meaningful extensions | **COMPOSE** raw preservation plus validated extensions |
| 24 | `MandateScope` one target on control | `JurisdictionProfile` separate versioned configuration | One document may require multiple target executions | **REVIEW** 0:N compliance contexts and immutable profile pins |
| 25 | `LineageRecord` field-level rule/input/output | `DocumentRepresentation` document-level hash/format/mapping version | Newer model does not fully replace field-level lineage | **RETAIN** lineage outside business aggregate |
| 26 | No first-class normalized response aggregate | `ComplianceTransaction` lifecycle events, validation, authority responses | Response and attempt identity insufficiently detailed | **DEFER** detailed design to CTC-013/014; reserve references |
| 27 | `Decimal` numeric string max 6dp | `Money(amount,currency)`, `Quantity(value,unit)` | Six decimals may be inadequate for some rate/quantity precision; semantic Money independent of DB | **REVIEW** precision by quantity/rate/amount and code-list constraints |
| 28 | Null/default conventions include city empty string and unit C62 | More permissive structural cardinalities | Defaults can manufacture fiscal meaning | **REFINE** explicit missing/enriched/default provenance |

### Evidence anchors (A)

- Earlier entity specification v1.0: §§4–8 (identity, parties, tax, lines, financials); §10–12 (control/native/constraints). See also `ctc-transformation-framework-reference-v1.1.md` §4.2–4.30.
- Newer semantic model v0.3: §§3–11 (boundaries and entities), §12.2 (French Extended CTC), §§14–17 (validation and governance), §18.5 (hierarchical example).
- Newer relational v0.3: §§4–17 (logical realization), §19 (integrity), §22 and §22A (open decisions/French findings).
- Earlier transformation framework v1.1: §11 ADR-01–ADR-14, §12 known gaps. These ADRs are marked Accepted **inside their historical source**, but project DECISIONS.md explicitly requires fresh review; they are **not project-approved**.

## High-risk conflicts and proposed resolution paths

**C-01 (Critical): root/aggregate identity.** Options: A) retain SemanticDocument as entire domain object; B) replace with BillingDocument; C) define a versioned exchange/envelope that references BillingDocument + FiscalContext + representation(s), with ComplianceTransaction external. **Proposed C for investigation**; requires lifecycle and serialization examples. Migration: old `identity` maps to billing fields; `control` splits; native and lineage move out.

**C-02 (Critical): tax semantics.** A) retain regime/application model but remove EU-only category restriction; B) use generalized Tax alone; C) generalized TaxApplication referencing TaxRegime and separate summary. **Proposed C for investigation**, subject to Brazil, India, Mexico, EU, excise and withholding fixtures. Migration: category and withholding mapping may be breaking.

**C-03 (Critical): line reconciliation.** A) all lines additive; B) derive contribution only from profile; C) explicit line role, hierarchy and frozen contribution semantics with versioned derivation provenance. **Proposed C for investigation**; ensure no circular hierarchy, duplicate count, and signed amounts. Migration: old `sum(all lines)` invariant invalid.

**C-04 (High): party completeness and history.** A) globally required tax ID/address; B) globally optional with profile requirements; C) B plus immutable per-document snapshots. **Proposed B/C investigation**. Migration: remove fabricated `Unknown`/empty city and ungrounded primary ID.

**C-05 (High): fiscal/native extension.** A) preserve arbitrary bag; B) governed extensions only; C) governed typed semantic extensions **plus** immutable original representation/raw field fragments. **Proposed C investigation**. Migration: native fields require triage and validation ownership.

**C-06 (High): document/fiscal/submission identifiers.** A) one ID; B) distinct internal document, business number/series, fiscal ID, revision, representation, transaction, attempt, authority IDs. **Proposed B investigation**. Migration: existing derived `identity.id` may not be reversible.

**C-07 (High): multiple destinations.** A) targetScope embedded on document; B) independent compliance transactions referencing immutable document revision and pinned profile. **Proposed B investigation**. Migration: move `targetScope` off shared billing semantics.

**C-08 (Medium): language and monetary precision.** A) preserve earlier text map/6dp globally; B) explicit localized text, monetary currency, configurable decimal constraints by semantic quantity and profile. **Proposed B investigation**; validate against actual fixtures.

## Source contradictions requiring explicit review

1. Earlier service-oriented reference owns signing/delivery, while framework v1.1 delegates them to host. Treat as **historical architecture evolution**, not simultaneous approved requirements.
2. Earlier and later references reuse ADR-09–ADR-14 IDs for **different titles**. Preserve IDs with source namespace (`Framework-v1.1:ADR-10` versus `ERP-v2.0:ADR-10`) until an authoritative migration map is approved; do not overwrite either.
3. v0.3 conceptual Party mentions singular optional address/contact in §4.2, while its hierarchy/relational draft permit arrays. Cardinality is not yet settled.
4. v0.3 conceptual BillingDocument lists `notes` as strings, but §4.24b defines a typed Note and hierarchy uses `notes[] -> Note`; resolve at dictionary stage.
5. v0.3 FiscalContext has one jurisdiction but platform goals allow multiple destinations; decide whether fiscal contexts are per legal artifact, per regime, or per submission.
6. v0.3 relational FISCAL_CONTEXT is 0..1 per document; this may contradict multi-jurisdiction fiscal processing.
7. Earlier default city `""` or `"Unknown"` and unit `C62` can fabricate meaning; do not treat as safe canonical rules.
8. No independently executed regression suite accompanies the conceptual French stress-test narrative in this review.

## ADR proposals — IDs intentionally unassigned

The existing ADR namespaces collide. Until CTC-017 resolves governance, use task-scoped proposal keys rather than inventing a global ADR number:

| Proposal key | Decision question | Proposed direction | Status |
|---|---|---|---|
| CTC-001-P01 | Canonical root and boundary | Explore composed exchange contract | Proposed, not approved |
| CTC-001-P02 | Tax abstraction | Compose regime identity with generalized tax application | Proposed, not approved |
| CTC-001-P03 | Line hierarchy/reconciliation | Preserve signed values, hierarchy, explicit contribution | Proposed, not approved |
| CTC-001-P04 | Parties and snapshots | Profile-required fields, no invented values, snapshot policy | Proposed, not approved |
| CTC-001-P05 | Native extensions | Governed semantics plus immutable raw preservation | Proposed, not approved |
| CTC-001-P06 | Identity and multi-destination | Separate IDs, immutable revision references | Proposed, not approved |

## Minimal evidence challenge plan (NOT TESTED)

| Test | Candidate family | Expected challenge |
|---|---|---|
| T01 | Peppol UBL invoice and credit note | Base cardinality, taxes, notes, payment, references |
| T02 | French Extended CTC UBL | GROUP/DETAIL, signed lines, line sellers, tax point |
| T03 | Italian FatturaPA | Fiscal document type, Natura, address components, references |
| T04 | Mexican CFDI | Serie/Folio, RFC, fiscal UUID, retenciones, signed economics |
| T05 | Brazilian NF-e | Multiple tax regimes, tax bases, tax summary fidelity |
| T06 | India INV-01 | CGST/SGST versus IGST, party IDs, supply context |
| T07 | Per-unit excise / compound tax synthetic challenge | Calculation method and dependent bases; requires verified real example |
| T08 | Authority rejection/clearance response | Correlation and boundary between fiscal identity and lifecycle |

Fixtures and licenses must be verified in CTC-008. This is a test plan, not evidence that these cases pass.

## Decision questions for user review

1. Should we proceed to CTC-002 with **composed exchange contract** as the leading *hypothesis* (not approved architecture), or examine an alternative first?
2. Is the canonical internal representation expected to persist **each immutable normalized revision**, or is persistence strategy still open?
3. Should the initial semantic scope include **non-billing fiscal documents** or keep them as future distinct aggregates under a common envelope?

## Session checkpoint (proposed only)

- **Task:** CTC-001 — propose move Todo -> Review once this report is reviewed; not Done.
- **Findings:** 28 entity/constraint reconciliation rows; 8 ranked conflicts; 8 source inconsistencies; 6 decision proposals.
- **Approved decisions:** None.
- **Model changes:** None applied.
- **Suggested BACKLOG.md update:** CTC-001 to Review after user assessment; keep CTC-002 blocked on acceptance of CTC-001 deliverable.
- **Suggested DECISIONS.md update:** Add proposal keys CTC-001-P01..P06 and source-qualified historical ADR inventory; do not mark Accepted.
- **Suggested FINDINGS.md update:** Record entity reconciliation and source contradictions, with evidence anchors.
- **Suggested MODEL-BASELINE.md update:** Add candidate composed-boundary hypothesis, explicitly OPEN.
- **Suggested SESSION-LOG.md update:** Link this review, list unapproved proposals and next review questions.
- **Next task:** CTC-002 — agree aggregate boundaries, after review.

**No authoritative project files were modified by this review.**
