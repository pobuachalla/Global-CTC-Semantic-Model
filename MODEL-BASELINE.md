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

## 2026-10-20 — Backlog realignment note

No model changes in this administrative review. D2 logical contract and T01–T03 policy approvals remain at their exact scopes. Detailed CTC-003 entity dictionary and FiscalContext physical design remain unapproved.

## 2026-10-20 — CTC-001 closure and CTC-003 unified candidate

CTC-001 has explicit **Done (scoped reconciliation)** status; this does not approve its earlier candidate models wholesale. `research/CTC-003/CTC-003-UNIFIED-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.4.md` is the latest **PROPOSED** unified entity dictionary, combining commercial draft 0.2, tax draft 0.3 and approved T01/T02/T03 logical policy. No detailed schema, cardinality or FiscalContext physical aggregate option has been approved. D2, P1–P7 and I-01–I-10 remain accepted at previously approved scope.


## CTC-003 — Unified D2 dictionary Draft 0.5 (2026-10-20)

A detailed **candidate** dictionary now covers all nine approved D2 logical categories and their proposed companion entities, in `research/CTC-003/CTC-003-UNIFIED-D2-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.5.md`. This is **not an accepted detailed semantic schema**. Accepted logical constraints D2/P1–P7/I-01–I-10 and T01/T02/T03 are unchanged; FiscalContext physical A/B/C is deferred. Proposed attributes, nullability and cardinalities require explicit review.

## 2026-10-20 — CTC-003 approved logical ownership directions

D01/D02/D03 and their six paired logical invariants are **Accepted at logical ownership level**. The authoritative published commercial facts and immutable party snapshots are associated with exact revisions; fiscal interpretation derives from pinned inputs without overwriting source facts; submission attempts pin exact submission snapshots and fiscal evidence/identity retain exact attribution. See `DECISIONS.md`.

**Not approved:** candidate entity shapes, cardinalities, concrete fields, physical manifest/snapshot entities, FiscalContext physical A/B/C, or regulatory conformance. Unified dictionary Draft 0.5 and conditional-cardinality Draft 0.7 remain proposed.

## CTC-003 Draft 0.8 proposal (not accepted)

Three-dimensional lifecycle separation, L01–L10 and conditional-cardinality matrix are **proposed**. The approved D2 logical foundation and accepted T01–T03/D01–D03 are unchanged. Detailed entity dictionary remains unapproved. See `research/CTC-003/CTC-003-LIFECYCLE-PUBLICATION-CARDINALITY-REVIEW-DRAFT-0.8.md`.

## 2026-10-20 — Accepted lifecycle policy; Draft 0.9 remains candidate

Three lifecycle dimensions and L01–L10 are **Accepted at logical-policy level** (see DECISIONS.md). No detailed cardinalities, entity shapes, legal issuance rules or physical aggregates were approved. Draft 0.9's conditional relationships and synthetic instances remain proposed. D2, P1–P7, I-01–I-10, T01–T03 and D01–D03 are preserved.

## CTC-003 Draft 1.0 review note

Candidate extraction, submission envelope, envelope member and transport-attempt concepts are **not approved**. Approved D2 logical foundation and scoped decisions remain unchanged; no detailed cardinalities or physical aggregates accepted.

## 2026-10-20 — Accepted batch/container separation (logical only)

`CTC-003-BATCH-01` is Accepted: inbound ingestion and outbound transport containers are semantically distinct from individual `BillingDocument` and `ComplianceTransaction` identities. A container-level processing outcome does not imply individual document legal/fiscal acceptance. **No** candidate batch entities, B01–B10 invariants, C09 cardinalities or physical aggregation have been accepted. The detailed CTC-003 dictionary remains proposed.


## CTC-003 blitz logical constraints — 2026-10-20

**Accepted logical constraints:** C09-02 (0..N extractions per ingestion, 0..1 resolved document per extraction); C09-07 (one immutable payload per submitted transport attempt; multi-member manifest); B01–B10 logical invariants. These supplement previously accepted CTC-003-BATCH-01. **Not an approved detailed schema:** all other C09 cardinalities, physical roots/tables, FiscalContext physical A/B/C and provider-specific legal behavior remain open.

## 2026-10-20 Draft 1.2 cardinality governance note

C09-01 through C09-08 now accepted at qualified **logical relationship** level (C09-02/C09-07 from earlier blitz; remaining six under continuation). This does not approve Draft 1.2 detailed entity shapes, a physical aggregate design, or jurisdiction-specific publication requirements. CTC-003 remains In Progress.


## CTC-003 Draft 1.3 completion candidate
Candidate consolidated dictionary: `research/CTC-003/CTC-003-UNIFIED-SEMANTIC-MODEL-COMPLETION-CANDIDATE-DRAFT-1.3.md`. No detailed schema approval; CTC-003 remains In Progress. Accepted logical principles unchanged.

## 2026-10-20 CTC-003 G2 checkpoint

G2-A..F accepted **only as logical ownership directions**. Integrated dictionary Draft 1.9 is not an accepted detailed schema. FiscalContext physical A/B/C remains deferred.

## 2026-10-20 — CTC-003 detailed logical dictionary accepted at scoped level

The normative **logical** entity dictionary is `research/CTC-003/CTC-003-DETAILED-LOGICAL-DICTIONARY-APPROVED-SCOPED.md` (closure candidate v1.0 approved by user). It defines the scoped 51-entity logical catalogue, identifiers, types, optionality, relationships and qualified cardinalities. This acceptance supersedes the earlier *candidate status* of the detailed dictionary only within the approved scope; it does not approve physical persistence or jurisdiction-specific rules.

The 18 additional Draft 4.2 field contracts remain Proposed, not part of the approved normative field set. FiscalContext A/B/C remains deferred. Historical source specifications and candidate drafts remain reference material, not independently approved alternatives.

## 2026-10-21 — CTC-004 validation disposition

**CTC-004 Done — scoped.** The accepted logical model's T01–T03 tax and monetary policies have focused deterministic validation for multi-regime aggregation, withholding, signed effects, tax inclusion, source assertions, currency safeguards, precision and rounding-policy controls. This is **validation evidence**, not a new schema approval or jurisdictional compliance statement.

D2 and all prior accepted decisions remain unchanged. The 18 proposed CTC-003 field contracts remain unapproved; FiscalContext physical A/B/C remains deferred. The authoritative scoped CTC-003 dictionary remains `research/CTC-003/CTC-003-DETAILED-LOGICAL-DICTIONARY-APPROVED-SCOPED.md`.


## CTC-005 approved logical governance baseline — 2026-10-21

The seven-step reuse-before-extension decision tree and JP-01..JP-10 are **Accepted at logical-governance level**. Applicable profile package identity, effective-date basis, immutable dependency pinning, governed extension ownership, precedence/ambiguity handling, promotion controls and validation/legal-state separation are normative logical rules. See `DECISIONS.md` for exact wording.

This does not add mandatory canonical fields or approve the candidate physical profile contracts. The 18 additional CTC-003 field contracts remain Proposed; physical FiscalContext A/B/C and country-specific regulatory behavior remain deferred. CTC-001..004 scoped approvals and all earlier decisions remain unchanged.


## CTC-006 scoped logical constraints — Accepted 2026-10-21

C006-01: explicit, profile-governed commercial identity namespace; C006-02: immutable published party snapshots; C006-03: typed correction/replacement/credit/cancellation relationships without revision overwrite. These constrain interpretation of the approved CTC-003 logical dictionary without adding physical entities or fields. Jurisdiction-specific validity, 18 proposed field additions and FiscalContext physical A/B/C remain unresolved.
