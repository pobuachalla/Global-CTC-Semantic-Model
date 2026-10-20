# Global CTC Platform — Master Research and Data Model Definition Prompt

**Version:** 1.0 — Consolidated research brief  
**Date:** 19 October 2026  
**Status:** Working research instruction; not an approved architecture  
**Primary objective:** Define and validate the canonical semantic data model that will form the durable foundation for future development of a global e-invoicing / Continuous Transaction Controls (CTC) application.  
**Secondary objectives:** Establish a compatible logical persistence model, integration boundaries, mandate extensibility approach, test evidence, and phased implementation roadmap.

---

## 0. Executive instruction and priorities

You are acting as a principal enterprise data architect, global e-invoicing/CTC domain specialist, integration architect, and rigorous technical reviewer. Your task is **not** to start a new application implementation, nor to redesign the existing architecture without evidence. Start by critically consolidating the supplied prior work into an implementable, jurisdiction-neutral, versioned **semantic data model**. Make design choices explicit, cite their evidence, preserve useful prior decisions, and document uncertainty.

**Order of priority:**

1. **P0 — Canonical semantic model:** entities, meaning, boundaries, relationships, cardinalities, constraints, identifiers, value types, extensibility, and versioning.
2. **P0 — Reconciliation of competing existing models:** identify contradictions and select/compose the best design with traceability.
3. **P0 — Representative payload validation:** demonstrate that the proposed model can represent materially different global document families without semantic distortion.
4. **P1 — Logical relational model:** derive persistence entities and relationships *from* the accepted semantic model, not vice versa.
5. **P1 — Process and lifecycle boundaries:** define minimal interfaces to submission, response, evidence, routing, and lineage without embedding their mutable state in commercial invoice semantics.
6. **P2 — Mapping/ERP connectors, mandate rule packs, runtime architecture, and delivery roadmap:** describe only to the degree needed to ensure the model will support later implementation.

**Do not start with code, database DDL, or microservices.** The first deliverable is a reviewed, explicit, testable data-model proposal with unresolved decisions clearly highlighted. Do not claim that a draft is production-ready simply because it is comprehensive.

## 1. Supplied source artifacts — read before proposing changes

The following are **existing work products**, not independently verified regulatory sources. Inspect the full content of each available artifact, including diagrams, tables, appendices, ADRs, and examples. If any are unavailable, state the gap and proceed only with evidence actually supplied.

| Artifact | Purpose and required use |
|---|---|
| `ctc-transformer-complete-reference.md` | Existing transformer design, rules, format adapters, mandate packs, technical choices, known gaps, and ADR baseline. |
| `CTC-Semantic-Document-Entity-Model.docx` | Earlier `SemanticDocument` entity model, `TaxRegime`/`TaxApplication`, `FormatNativeBag`, `MandateScope`, validations, and lineage. |
| `CTC-Transformer-Architecture-v2.0-ERP.docx` | Existing Stage 1 ERP normalization / Stage 2 CTC transformation, connector profiles, ERP tax reconstruction, and operational integration design. |
| `ctc-tracker_new.html` | Mandate/deployment tracker UI and its data-loading structure. Do not assume its external `.md`/`.json` dataset is supplied. |
| `CTC-Format-Families-Reference.xlsx` | Country/syntax family taxonomy, clearance models, framework impact, rollout assumptions. Read **all six sheets**: Summary; Country Format Matrix; By Syntax Family; Clearance Models; Framework Impact; Rollout Timeline. Treat regulatory dates and classifications as unverified until checked against official sources. |
| `semantic-billing-model(1) (1).md` | **Newer v0.3 conceptual candidate**: `BillingDocument`, `FiscalContext`, `JurisdictionProfile`, `JurisdictionExtension`, `ComplianceTransaction`, `DocumentRepresentation`, French Extended CTC stress test. |
| `relational-data-model(1) (1).md` | **Newer v0.3 logical persistence candidate**: relational entities, party/line/tax normalization, fiscal and compliance boundaries, provenance, and unresolved design decisions. |
| `relational-model(1) (1).mmd` | Mermaid entity relationship diagram: compare against the logical relational model and detect omissions, contradictions, and incorrect cardinalities. |

**Confidentiality:** Some supplied material is explicitly labeled internal. Treat it as internal design context; do not upload it to public repositories or external services without authorization. Public GitHub fixtures may be researched separately.

### 1.1 Source precedence and conflicts

Do **not** silently declare either the earlier `SemanticDocument` or newer `BillingDocument` proposal authoritative. The newer v0.3 work introduces important refinements but remains a draft. For each conflicting concept, document: earlier representation, newer representation, trade-offs, proposed canonical representation, migration/compatibility impact, and supporting sample evidence. Explicitly address whether `SemanticDocument` remains a transport wrapper, becomes an alias, is replaced by `BillingDocument`, or is split into multiple domain aggregates.

Distinguish three levels of evidence in every substantive finding: **[A] supplied artifact**, **[B] verified external specification or inspected sample**, **[C] architectural recommendation or inference**. Include artifact section/page or repository path/commit and external source URL where applicable.

## 2. Product and domain goals

The future platform must be capable of accepting invoice and related billing data from ERPs and other clients; normalizing business meaning; evaluating applicable mandates; producing country-specific outputs; exchanging messages with authorities, service providers and networks; interpreting responses; and returning meaningful status to clients. The data model should make these future capabilities feasible without conflating them.

Consider invoices, credit notes, debit notes, self-billed documents, corrections, replacements, cancellations, supporting attachments, relevant fiscal reporting documents, and legally significant acknowledgements. Do not assume that all of these belong to one `BillingDocument` aggregate; determine the right semantic boundaries.

Scope should cover materially different format families, not merely many countries using UBL: UBL/Peppol/EN 16931, UN/CEFACT CII, FatturaPA, Mexico CFDI, Brazil NF-e and NFS-e, Chile DTE, Poland KSeF, India INV-01/GST, Malaysia MyInvois, Saudi ZATCA, UAE PINT-AE, and others where reliable evidence is available. The format-family workbook is a starting hypothesis, not proof of current mandate requirements.

## 3. Non-negotiable modelling principles

1. **Meaning before syntax:** introduce shared concepts for stable business/fiscal meaning, not to mirror source XML/JSON paths.
2. **Semantic versus persistence separation:** define the conceptual contract first; derive relational tables later. A semantic `Money` value does not imply a `MONEY` table.
3. **Separation of concerns:** commercial billing, fiscal/legal context, jurisdiction rules, serialized representations, compliance transactions, authority responses, and operational lineage have different responsibilities and change rates.
4. **Controlled extensibility:** use existing core concepts before proposing profile constraints, reusable fiscal concepts, or namespaced extensions; do not build a universal nullable superset.
5. **Preserve legally relevant meaning:** retain source documents and transformations where required; expose information loss rather than silently dropping fields.
6. **Explicit identity:** separate internal document ID, business document number/series, fiscal identifiers, document revision, source/target representation IDs, compliance transaction ID, submission attempt ID, and authority references.
7. **Signed economics:** do not infer the sign of each amount from document type. Support negative invoice lines and mixed-sign corrections.
8. **Hierarchical line semantics:** support GROUP/DETAIL structures, parent-child lines, line-specific parties, and explicit contribution to totals; avoid double-counting.
9. **Global tax semantics:** model charged versus withheld taxes, multi-regime tax, exemptions, percentage/per-unit/fixed calculations, cascading taxes where evidenced, tax point, and jurisdiction-specific tax classification.
10. **Determinism and auditability:** version semantic models, mappings, jurisdiction profiles, code lists, and validation logic; retain evidence needed to reconstruct historical outcomes.
11. **No fabricated legal data:** missing tax IDs, city names, tax rates, or payment details must not be invented to satisfy schema cardinality. Record missingness and explicit enrichment requirements.
12. **Evidence-based constraints:** separate universal structural invariants from jurisdiction/profile-specific and context-dependent business rules.

## 4. Primary assignment: reconcile and define the canonical semantic model

### 4.1 Establish the candidate aggregates

Review the merits of these existing conceptual boundaries:

- `BillingDocument` — commercial billing semantics and document relationships.
- `FiscalContext` — legal/fiscal attributes and classifications that are not universal commercial meaning.
- `JurisdictionProfile` — versioned mandate-specific constraints, code lists, conditional rules, semantic alignments.
- `JurisdictionExtension` — governed, typed, namespaced local concepts.
- `DocumentRepresentation` — immutable source/target serialization metadata and artifact references.
- `ComplianceTransaction` — submission, clearance, delivery, validation and response lifecycle, separate from the billing model.

Assess whether a common document envelope or distinct legal/fiscal document aggregate is required. Specify aggregate ownership, references, mutability, and cardinality. The same billing document may have zero, one, or many jurisdictional processing contexts, representations, and submission attempts.

### 4.2 Produce a complete semantic entity catalogue

For **every proposed entity, value object, relationship, and important attribute**, specify:

- Canonical name and precise business definition.
- Whether it belongs to core billing, fiscal, profile, extension, representation, or process domain.
- Data type and value constraints, including precision, date/timezone, currency and units.
- Required/optional status and cardinality at the *base model* level.
- Identity, ownership, and referential semantics.
- Whether values are supplied, derived, defaulted, or externally enriched.
- Validation and reconciliation invariants.
- Representative source/target field alignments.
- At least one positive and relevant negative/edge-case example.
- Known ambiguity, open decision, and source evidence.

At minimum review: `BillingDocument`, `BillingLine`, `Party`, `PartyRole`, `Identifier`, `TaxRegistration`, `LegalRegistration`, `Address`, `Contact`, `Item`, `ItemClassification`, `Quantity`, `Money`, `Price`, `Adjustment`, `Tax`, `TaxSummary`, `MonetaryTotal`, `PaymentMeans`, `PaymentTerms`, `FinancialAccount`, `DocumentRelationship`, `DocumentReference`, `Supply`, `Period`, `TaxPoint`, `Note`, `Attachment`, `FiscalContext`, `FiscalPartyContext`, `DocumentRepresentation`, and relevant controlled extensions. Explicitly compare each to its earlier `SemanticDocument` counterpart.

### 4.3 Resolve critical open design questions

Provide options, trade-offs and a recommended answer for each:

1. `SemanticDocument` vs `BillingDocument` vs envelope/aggregate decomposition.
2. Document business identity versus fiscal/authority identity and revision/version identity.
3. Immutable party snapshots versus reusable master-party identities; line-specific party snapshots.
4. Money with explicit currency per value versus inherited document currency; decimal precision and rounding.
5. Signed economic amounts, credit/debit note semantics, corrections, and reversals.
6. Hierarchical lines and persisted versus derived `contributesToDocumentTotals`.
7. Generalized `Tax` versus `TaxRegime` + `TaxApplication`: preserve multi-regime strengths without constraining non-VAT taxes to EN 16931 categories.
8. Charged tax, withholding, per-unit/excise tax, compounded/cascading tax, and tax-on-tax bases.
9. Document, line, and adjustment-level tax scope and aggregation/reconciliation.
10. Multiple tax currencies, FX rates, exchange-rate date/source, and currency conversion audit.
11. Party roles, invoice issuer versus seller, line-specific participants, and legal registration.
12. Separate price-level, line-level, and document-level allowances/charges.
13. Payment means versus payment terms; installment plans and payment references.
14. Generic document references versus typed corrections/cancellations and fiscal references.
15. Tax point, delivery, service period, and place-of-supply semantics.
16. Typed multilingual text versus strings with language-tagged variants.
17. `FormatNativeBag` versus typed, validated jurisdiction extensions and preserved raw representations; do not leave legally mandatory native fields unvalidated.
18. Source field fidelity, mapping lineage, original payload retention, and round-trip expectations.
19. Universal base cardinality versus stronger jurisdiction-profile requirements.
20. Multiple destinations and repeated submissions without mutating core document semantics.
21. Schema evolution, semantic compatibility, and historical reproducibility.
22. What belongs in the logical database versus object storage, append-only event history, or configuration registry.

### 4.4 Explicit reconciliation of known differences

Do not overlook these known differences between supplied drafts:

- Earlier `SemanticLine` requires quantity, unit code and positive/nonnegative amounts in places; newer `BillingLine` supports optional quantity for group lines, hierarchical structure, signed economic values, and contribution flags.
- Earlier `TaxApplication.categoryCode` is tied to EN 16931 category values even for non-EU taxes; newer `Tax` explicitly models tax type, direction and calculation method.
- Earlier `SemanticParty` requires identifiers and an address; newer `Party` permits more context-sensitive requirements and separates legal/tax registrations.
- Earlier `DocumentControl` combines source metadata, target scope, signing, QR, clearance and lineage; newer design separates representation, fiscal, and compliance process concerns.
- Earlier `FormatNativeBag` holds unvalidated native fields; newer jurisdiction extensions require versioned semantic meaning and validation.
- Earlier totals model assumes line sums in ways that must be checked against French grouped/detail line semantics.
- The newer relational model and `.mmd` ERD are drafts; inspect their completeness, ownership constraints and cardinalities rather than copying them unchanged.

## 5. Evidence and stress-test plan for the model

Build a representative **semantic challenge matrix**, not merely a count of XML files. Include at least: basic invoice; credit note; debit note; self-billing; negative lines; mixed tax rates; exemption and reverse charge; withholding; multi-regime taxes; per-unit excise; line/document/price allowances; multi-currency; tax currency; partial payment; corrections; multiple document references; hierarchical GROUP/DETAIL lines; line-specific sellers; tax point; bilingual parties/lines; complex national IDs; local fiscal extensions; attachments; signed/sealed artifacts; and authority responses. Include deliberately invalid examples and unsupported cases.

For each selected sample: classify each meaningful source concept as **direct mapped / normalized / derived / governed extension / raw-only preserved / intentionally excluded / unmapped**. Distinguish semantic preservation from exact XML byte-level round trip. Validate both source-to-semantic and semantic-to-target feasibility where a reliable target specification exists. Record data-loss severity, test outcome and remediation. Never claim that syntactically valid XML proves regulatory compliance.

### 5.1 Candidate GitHub repository inventory (not yet verified)

| Candidate repository | Proposed coverage |
|---|---|
| https://github.com/OpenPEPPOL/peppol-bis-invoice-3 | Peppol BIS / UBL |
| https://github.com/ConnectingEurope/eInvoicing-EN16931 | EN 16931 UBL/CII validation |
| https://github.com/speedata/einvoice | European invoice fixtures |
| https://github.com/hernaninverso/eu-invoice-fixtures | Peppol, XRechnung, Factur-X |
| https://github.com/amusarra/dontesta-fisco-hub | Italy FatturaPA |
| https://github.com/azuki-beans/fatturapa | Italy FatturaPA |
| https://github.com/CIRFMF/ksef-client-java | Poland KSeF |
| https://github.com/KSeFGuard/ksef-guard | Poland KSeF |
| https://github.com/kreyo-io/facturae-examples | Spain Facturae |
| https://github.com/brasil-fiscal/nfe | Brazil NF-e |
| https://github.com/niclabs/DTE | Chile DTE |
| https://github.com/UblSharp/UblSharp | Generic UBL |
| https://github.com/InvoiceXML/ubl-api-examples | UBL XML/JSON examples |

For every candidate, verify repository availability, owner, license, latest relevant commit, actual fixture file paths, schema versions, number of distinct sample payloads, valid versus invalid fixture intent, jurisdiction, business scenarios, and suitability for reuse. Do not conflate code libraries, schemas, example documentation, and actual test documents. Do not assume that repository names or the supplied descriptions are accurate. Protect private/sensitive data; sanitize or exclude samples that contain personal information or real production credentials.

**Provisional corpus scoring (100 points):** 25 semantic edge-case coverage; 20 authoritative/schema validation quality; 15 jurisdiction and syntax diversity; 15 fixture quantity and scenario diversity; 10 provenance/reproducibility; 10 licensing/reuse suitability; 5 maintenance recency. Record scores with evidence and separate unknown from zero. Weight architectural coverage more heavily than raw file count.

Prioritize a small high-diversity fixture set to validate the initial model; exhaustive collection across all countries is a later workstream.

## 6. Format families, mandates, and coverage

Use the supplied workbook's four-level hierarchy as an organizing hypothesis:

1. **Semantic standard** — meaning and business concepts.
2. **Serialization syntax** — UBL, CII, XML/JSON/EDI, etc.
3. **Profile/CIUS** — constraints, mandatory fields, code lists, validation.
4. **National implementation/mandate** — legal and process obligations.

Evaluate whether the hierarchy fully handles formats that do not align cleanly with a shared international semantic standard. Keep country, jurisdiction, tax regime, format family, syntax version, profile version, mandate version, and delivery/clearance model as distinct dimensions. Do not equate a country with a single syntax or clearance workflow.

Create a crosswalk among (a) earlier 25-country architecture scope, (b) workbook country matrix, (c) actual tracker dataset if provided, (d) verified official regulatory sources, and (e) sample corpus. Highlight scope mismatches. The HTML tracker may require a separate `ctc-tracker-data.md` or JSON snapshot; if absent, say so. Do not silently use its interface as evidence of current client rollout status.

## 7. Logical relational model — after semantic sign-off

Review `relational-data-model(1) (1).md` and `relational-model(1) (1).mmd` **after** deciding the conceptual entities. Produce an updated logical ERD, table/entity catalogue, keys, relationships, cardinalities, uniqueness assumptions, normalization rationale, ownership and integrity constraints, and indexes driven by anticipated queries. Preserve semantic-to-relational traceability.

Specifically review party snapshot strategy, document/line tax ownership, adjustment ownership, line hierarchy integrity, versioned document representations, fiscal context cardinality, multiple compliance transactions, and field-level lineage. Distinguish normalized relational state, JSON extensions, immutable payload storage, and append-only lifecycle events. Avoid prematurely selecting a database vendor or writing production DDL; list any vendor-dependent decisions separately.

## 8. Future application integration boundaries — define interfaces, not the full implementation

Preserve the useful earlier principle that ERP-specific mapping is separate from country-specific transformation. Treat the prior two-stage pipeline as an existing design to assess, not an unquestionable runtime mandate.

Define the minimum data contracts needed for later stages:

- ERP/source ingestion and source representation metadata.
- Source-to-semantic mapping, value normalization, enrichment, and provenance.
- Jurisdiction/profile resolution and deterministic version selection.
- Semantic validation and target representability.
- Semantic-to-target serialization and signing/evidence metadata.
- One-to-many destination routing and independently tracked submissions.
- External authority/provider responses and normalized status/event contracts.
- Client notification and correlation back to original source/business document.

Define response and lifecycle entities as separate aggregates where appropriate, including retry attempts, idempotency, timestamps, original response reference, authority reference, validation findings, and status transitions. Avoid encoding the current mutable compliance status as intrinsic billing semantics. Include high-level security, retention, privacy, and tenant isolation considerations, but defer detailed infrastructure decisions.

## 9. Rule and model governance

Evaluate the existing YAML Rule DSL v2, ERP mapping profiles, configuration hot-reload, and mandate pack design for compatibility with the selected semantic model. Identify where a simple declarative mapping suffices and where tax reconstruction, signing, sequence constraints, or external lookup needs a separately governed executable function. Distinguish schema validation, semantic validation, profile validation, target-format validation, and external authority validation.

Propose independent versioning for core semantic model, fiscal model, profile, mapping, code list, and validation package. Explain historical reproducibility, approval, test promotion, rollback, effective dating, backward compatibility, and extension-to-core promotion. Do not promise that all country onboarding will require no code changes.

## 10. Deliverables and acceptance criteria

### Phase 1 — mandatory, highest priority: semantic model foundation

1. **Baseline and conflict assessment:** artifact-by-artifact inventory, existing decisions and terminology, differences between earlier/newer models, unresolved assumptions, and a retain/refine/replace register.
2. **Recommended domain boundaries:** conceptual context diagram and explicit aggregate ownership for commercial, fiscal, representation, profile, extension, and compliance/process data.
3. **Canonical semantic model specification vNext (draft):** complete entity/attribute catalogue, types, relationships, cardinalities, invariants, identity and signed-value conventions, with a clear distinction between base and profile requirements.
4. **Semantic ERD / class diagram:** readable, machine-maintainable Mermaid (or equivalent) reflecting the actual specification.
5. **Example canonical documents:** machine-readable examples for a standard invoice, credit note, multi-regime tax, and French hierarchical/grouped invoice; include fiscal context and representations only where appropriate.
6. **Compatibility/migration map:** prior `SemanticDocument` fields to proposed concepts, indicating lossless, derived, split, deprecated, and unmappable fields.
7. **Risk and decision register:** high-impact open questions with options, recommendation, evidence and confidence.
8. **Focused validation matrix:** a small, high-diversity fixture set and test results or a clearly labeled unexecuted test plan where execution is unavailable.

**Phase 1 exit gate:** Do not call the model approved until every required base entity is defined, all major contradictions are adjudicated, critical sample scenarios are represented without silent data loss, core/profile separation is explicit, and all remaining high-risk decisions have owners and resolution plans.

### Phase 2 — logical persistence model

9. Updated logical relational model and Mermaid ERD derived from Phase 1.
10. Semantic-to-relational mapping, integrity constraints, snapshots/immutability, versioning and provenance strategy.

### Phase 3 — architecture and validation expansion

11. Verified GitHub fixture inventory and reusable test-corpus scoring.
12. Country/syntax/profile coverage and regulatory evidence matrix.
13. Forward/reverse integration contracts and compliance lifecycle model.
14. Architecture decision register, phased proof-of-concept plan, and implementation roadmap.

**Do not substitute Phase 2 or 3 deliverables for Phase 1.** A polished technical architecture without a validated semantic contract does not satisfy the assignment.

## 11. Required response format for the first research iteration

Return results in this order:

1. **Executive summary** (what can be retained, what must change, and key uncertainties).
2. **Existing model comparison** (`SemanticDocument` versus `BillingDocument`/`FiscalContext`/related aggregates).
3. **Recommended canonical boundaries** and reasoned alternatives.
4. **Entity inventory and highest-risk semantic decisions**, with evidence.
5. **Proposed first-cut semantic ERD and data dictionary** (not physical SQL).
6. **Minimal representative payload test matrix** and sample selection rationale.
7. **Decision log and unresolved questions** ranked by architectural impact.
8. **Recommended next iteration**, explicitly stating what evidence or approval is needed.

When a source is unverified, mark it **UNVERIFIED**. When a recommendation is provisional, mark it **PROPOSED**. When a test has not run, mark it **NOT TESTED**. Do not present speculative field mappings or country rules as confirmed facts.

## 12. Stop conditions and scope control

Stop and request architectural input if a decision would materially change the domain boundaries (for example, canonical root choice, snapshot semantics, tax representation, or document identity) and available evidence cannot distinguish options. Do not spend the initial iteration implementing API endpoints, deployment architecture, signing services, production schemas, or UI components. Present options rather than making irreversible choices without support.

---

## Immediate instruction to execute

**Begin with Phase 1.** Read and compare the supplied prior artifacts, with special attention to the newer v0.3 semantic and relational proposals and the earlier `SemanticDocument` tax and control structures. Produce a defensible consolidated semantic data-model recommendation suitable for architectural review. Use representative sample payloads to test assumptions when available. The objective is to establish the data contract that future development can safely build upon, not to build the entire CTC platform in this iteration.
