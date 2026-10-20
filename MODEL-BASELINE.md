# Semantic Model Baseline — Candidate Models, Not Yet Agreed

**Status: OPEN / UNAPPROVED.** This file captures competing drafts; it is not the final schema.

## Earlier candidate: SemanticDocument

Source: `CTC-Semantic-Document-Entity-Model.docx` and `ctc-transformer-complete-reference.md`.

- Root pivot `SemanticDocument` with `DocumentIdentity`, supplier/buyer parties, `TaxRegime`, `TaxApplication`, lines, totals, supporting entities, `DocumentControl` and `FormatNativeBag`.
- Tax regimes and applications designed to support multiple concurrent regimes.
- Format-native bag preserves non-core data; validation of this bag needs review.

## Newer candidate: BillingDocument v0.3

Source: `semantic-billing-model(1) (1).md`.

- `BillingDocument` holds commercial semantics, while `FiscalContext`, `JurisdictionProfile`, `JurisdictionExtension`, `ComplianceTransaction` and `DocumentRepresentation` have distinct responsibilities.
- Supports signed economic values, GROUP/DETAIL line hierarchy, non-additive detail lines, line-specific parties, typed document relationships, price-level adjustments and broader tax calculation types.
- Its logical persistence proposal is in `relational-data-model(1) (1).md`, with diagram in `relational-model(1) (1).mmd`.

## Open boundary decisions

1. Is `SemanticDocument` retained as a transport/envelope type or replaced by separated aggregates?
2. What is the canonical identity of commercial, fiscal and submission objects?
3. How are source fields preserved without using a nonvalidated extension escape hatch?
4. How do multi-destination compliance transactions reference immutable document revisions?
5. How do line hierarchy and signed values change validation and reconciliation?
6. Which source constraints are genuinely universal versus profile-specific?

## Promotion to approved baseline

Only update this file's status to Accepted when the user explicitly approves the resolved entity dictionary and boundaries. Track every decision in DECISIONS.md and source evidence in FINDINGS.md.

## CTC-002 evening review state — 2026-10-19

**Unapproved; no schema changes applied.** Candidate concepts to test: immutable BillingDocumentRevision, FiscalContext/Interpretation (embedded or independent), immutable DocumentRepresentation, ComplianceTransaction, SubmissionAttempt, ProcessingEvent, FiscalEvidence. These are not accepted aggregate roots or database tables.

French documented stress test strengthens shared core BillingLine hierarchy, signed economic amounts, line parties, tax-point semantics and representation provenance. It does **not** decide FiscalContext cardinality.

## 2026-10-20 governance note — principle approval only

CTC-002-P1..P6 are accepted as architecture principles in DECISIONS.md. **No semantic schema, entity dictionary, aggregate cardinality, or FiscalContext A/B/C choice has been accepted.** This candidate baseline remains unapproved; no model structures were changed by this approval.


## CTC-002 — D2 formal logical contract candidate (2026-10-20)

The nine-concept D2 logical contract and I-01..I-10 invariants are **proposed for review**, not accepted as the final semantic schema. User previously validated D2 as logical direction only. FiscalContext A/B/C physical/aggregate cardinalities remain deferred. See `research/CTC-002/CTC-002-CONSOLIDATED-DECISION-REVIEW.md`.

## 2026-10-20 — Accepted D2 logical foundation (not a complete approved schema)

**Accepted by explicit user approval:** D2 implementation-neutral nine-concept logical semantic contract and I-01..I-10; see `DECISIONS.md` and `research/CTC-002/CTC-002-D2-FORMAL-LOGICAL-CONTRACT.md`. P1..P7 remain accepted.

**Logical concepts:** BillingDocument; PublishedRevision; SourceFiscalFact; FiscalInterpretation; DerivedFiscalFact; ProfilePackage; DocumentRepresentation; ComplianceTransaction; FiscalIdentity/Evidence.

**Boundary rules:** immutable published revisions; distinguish source and derived assertions; pin exact revision, interpretation, profile package and representation references; preserve separate compliance history and fiscal evidence; apply profile-specific arithmetic/precision and distinct semantic-vs-target-validity gates.

**Not approved:** full entity dictionary or JSON schema; mandatory physical aggregate roots; FiscalContext A/B/C; database design, physical cardinalities and jurisdictional legal conformance. Earlier sections describing an unapproved *full schema* remain accurate; this section records only the accepted logical foundation. CTC-003 is eligible to begin.


## CTC-003 tax governance note — 2026-10-20

**Accepted at concept level:** T01 separates TaxRegime and TaxApplication with explicit application scope; T02 makes TaxSummary a reconciled aggregate with source summary assertions preserved. **Not accepted:** T03 sign policy (provisional experiment only), exact tax schema/cardinalities, detailed reconciliation rules. Commercial dictionary draft 0.2 and tax/monetary dictionary draft 0.3 remain proposals. Existing D2 logical baseline and P1–P7/I-01..I-10 are unchanged.


## 2026-10-20 — CTC-003 T03 approved policy annotation

CTC-003-T03 is **Accepted at logical monetary policy level only**. The exact ten approved invariants are recorded in `DECISIONS.md` and the decision-ready research report. `MonetaryBasis` and `MonetaryEffect` remain **candidate logical concepts**, not approved entities, fields, aggregate roots or tables. T01 and T02 remain Accepted. The detailed CTC-003 semantic entity dictionary remains a draft and **CTC-003 is In Progress**. No physical FiscalContext A/B/C choice was made.
