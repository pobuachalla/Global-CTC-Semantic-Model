# Global CTC — Project Backlog

**Baseline date:** 2026-10-19  
**Primary objective:** Agree an evidence-backed, jurisdiction-neutral semantic data model before application implementation.  
**Authority:** This file is the proposed task register; no task is completed or approved merely by being listed.

## Workflow

Statuses: `Todo`, `In Progress`, `Blocked`, `Review`, `Done`. Only mark `Done` after the acceptance criteria have been reviewed and the deliverable linked. Priority: P0 foundational, P1 validation/persistence, P2 later integration. Preserve task IDs.

| ID | Task | Priority | Workstream | Status | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|---|
| CTC-001 | Reconcile SemanticDocument and BillingDocument | P0 | Semantic foundation | Review | — | Entity-by-entity comparison, conflict register, proposed resolutions with evidence |
| CTC-002 | Agree semantic aggregate boundaries | P0 | Semantic foundation | Done (scoped logical boundary only; P1-P7 + D2 + I-01..I-10 accepted) | CTC-001 | Proposed boundaries for BillingDocument, FiscalContext, ComplianceTransaction, DocumentRepresentation; FiscalContext A/B/C unresolved |
| CTC-003 | Define semantic entity dictionary and cardinalities | P0 | Semantic foundation | In Progress (commercial draft 0.2; tax draft 0.3; T01/T02 accepted; T03 proposed) | CTC-002 | Entity definitions, identifiers, cardinalities, nullability and relationships |
| CTC-004 | Validate tax and monetary semantics | P0 | Semantic foundation | Todo | CTC-003 | Multi-regime tax, withholding, signed values, reconciliation and precision rules |
| CTC-005 | Design jurisdiction profiles and extension governance | P0 | Semantic foundation | Todo | CTC-002 | Extension decision tree, validation, versioning and promotion criteria |
| CTC-006 | Resolve parties, document identity and corrections | P0 | Semantic foundation | Todo | CTC-003 | Party role, identifiers, snapshots, series, correction/reference semantics |
| CTC-007 | Define semantic model versioning and compatibility | P0 | Semantic foundation | Todo | CTC-003 | Versioning rules, breaking-change policy and compatibility test plan |
| CTC-008 | Inventory and score 13 GitHub repositories | P1 | Evidence and validation | Todo | — | File-level inventory, licensing, commit IDs, valid/invalid fixtures and scores |
| CTC-009 | Create semantic coverage and loss matrix | P1 | Evidence and validation | Todo | CTC-003, CTC-008 | Per-field mapping outcomes, unrepresentable concepts, preservation and reversibility |
| CTC-010 | Stress-test French and non-EU payloads | P1 | Evidence and validation | Todo | CTC-004, CTC-008 | Documented tests for grouped lines, signed amounts, multi-regime tax and corrections |
| CTC-011 | Derive logical relational model | P1 | Persistence | Todo | CTC-002, CTC-003 | Logical ER model derived from accepted semantics with explicit cardinalities |
| CTC-012 | Define persistence snapshots and lineage | P1 | Persistence | Todo | CTC-011 | Immutability, source and target representations, lineage and retention decisions |
| CTC-013 | Define compliance transactions and event model | P1 | Compliance lifecycle | Todo | CTC-002 | Submission attempts, destinations, event dimensions and state derivation |
| CTC-014 | Define normalized authority responses | P1 | Compliance lifecycle | Todo | CTC-013 | Response schema, correlation, evidence and client-facing representation |
| CTC-015 | Assess adapters, rule DSL and routing boundaries | P2 | Integration | Todo | CTC-002, CTC-005 | Compatibility analysis for ERP/CTC adapters, rules and multi-destination routing |
| CTC-016 | Define API contracts and client notifications | P2 | Integration | Todo | CTC-013, CTC-014 | Submission, query, status and notification interface contracts |
| CTC-017 | Establish ADR and semantic governance | P0 | Governance | Todo | — | ADR numbering, statuses, approval gates and change review process |
| CTC-018 | Plan proof of concept and regression suite | P2 | Governance | Todo | CTC-009, CTC-010 | Representative fixture suite, pass criteria and phased implementation plan |

## First session

Begin `CTC-001`. First inventory concepts and differences; do not resolve architectural disputes without review. Record all proposed resolutions in `DECISIONS.md` as Proposed.

## Progress note — 2026-10-19

CTC-001 reconciliation deliverable produced and leading hypothesis selected for investigation; acceptance criteria remain under review, so status is Review rather than Done. CTC-002 has started provisionally on the explicitly user-directed hypothesis, without implying CTC-001 acceptance.

## Evening checkpoint — 2026-10-19

- CTC-001: **Review** (reconciliation delivered, no final ADR approved).
- CTC-002: **Review / evidence-gated** (French stress test and cross-country ownership reviews completed conceptually; no approved aggregate boundary).
- CTC-003: **Todo / blocked on CTC-002 acceptance**; do not treat entity dictionary as approved.
- Evidence tasks CTC-008 and CTC-009 remain pending; no repository fixtures were validated during this checkpoint.

## 2026-10-20 CTC-002 review status

Six architectural principles (CTC-002-P1 through P6) explicitly accepted at principle level. FiscalContext alternatives A/B/C deferred; task remains Review, not Done. CTC-003 remains Todo pending boundary approval. See DECISIONS.md and SESSION-LOG.md.


## 2026-10-20 CTC-002 consolidated decision review

CTC-002 remains **Review / evidence-gated**, not Done. Pending explicit approval of D2 formal contract I-01..I-10 and scoped logical closure. Outstanding evidence: paired CFDI certification, SdI response, French Extended CTC XSD fixture, real MyInvois/India conformance, archived profile packages, and independent fiscal-interpretation discriminator. CTC-003 remains Todo.

## 2026-10-20 — Explicit CTC-002 scoped closure and follow-up evidence gates

- **CTC-002: Done (scoped logical-boundary deliverable)** following explicit user approval of the D2 nine-concept logical contract and invariants I-01..I-10; accepted P1..P7 unchanged. This supersedes earlier Review status notes; historical entries remain as audit history.
- **CTC-003: Todo / now eligible to start** on the accepted logical contract; do not pre-approve physical aggregate-root choices or concrete cardinalities.
- **CTC-002-FU01: Todo (P1, persistence/aggregate design; dependency CTC-003 and CTC-011)** — Decide FiscalContext A embedded / B independent / C hybrid physical ownership and cardinalities with a documented trade-off and migration plan. Acceptance: explicitly approved ADR after actual design evidence; no default implicit selection.
- **CTC-002-FU02: Todo (P1, evidence; linked to CTC-008/009/010)** — Collect licensed, version-pinned paired CFDI pre/post certification XML; Italian FatturaPA/SdI response pairs; French Extended CTC XML with applicable profile/XSD; authoritative MyInvois and India IRP samples. Acceptance: source/version/license inventory and executed applicable schema/business-rule checks with failure logs.
- **CTC-002-FU03: Todo (P1, reproducibility; dependency CTC-007/009)** — Archive immutable profile/mapping/rule/code-list packages and external enrichment snapshots; demonstrate historical replay and compare exact outputs. Acceptance: content digests, repeatable execution and documented limitations.
- **CTC-002-FU04: Todo (P1, evidence discriminator; dependency CTC-008/009)** — Seek a verified case requiring multiple materially distinct fiscal interpretations of one immutable billing revision. Acceptance: documented scenario and references or explicit negative finding with bounded search; do not assume absence proves impossibility.
- **CTC-002-FU05: Todo (P1, semantic precision; dependency CTC-003)** — Resolve publication/freeze boundary, detailed correction/cancellation semantics and identity/evidence ownership in entity dictionary; distinguish jurisdiction-specific obligations from shared invariants.

These task-qualified follow-up IDs are proposed tracking IDs, not approved global ADRs. Their details can be incorporated into later backlog governance without changing the accepted CTC-002 scope.

## 2026-10-20 CTC-003 tax review

T01 and T02 explicitly Accepted; T03 remains Proposed (provisional). Five synthetic tax-sign cases executed and passed as arithmetic demonstrations, not regulatory tests. Detailed entity schema and monetary reconciliation remain unapproved.


## 2026-10-20 — CTC-003 T03 logical policy approval

- **CTC-003: In Progress.** T01, T02 and T03 are Accepted at their expressly stated logical scopes; detailed tax/monetary entity dictionary, cardinalities, reconciliation implementation and remaining review are not approved.
- **CTC-003-EV01: Todo (P1; evidence, related to CTC-008/009/010)** — Obtain and validate full licensed machine-readable tax-inclusive unit-price invoice with governing calculation/profile.
- **CTC-003-EV02: Todo (P1; evidence)** — Validate full Peppol credit note against applicable XSD/Schematron and compare presentation to economic effect.
- **CTC-003-EV03: Todo (P1; evidence)** — Obtain verified withholding invoice and reconcile source taxes/payable under applicable rules.
- **CTC-003-EV04: Todo (P1; evidence)** — Test source FX rate/date, accounting currency and versioned rounding against a full example.
- **CTC-003-EV05: Todo (P1; evidence)** — Test source subtotal discrepancies and jurisdictional tolerances without overwriting assertions.
- **CTC-003-DES01: Todo (P0; CTC-003)** — Define and review detailed fields/cardinalities for candidate `MonetaryBasis`, `MonetaryEffect`, `DocumentEconomicEffect` and `MonetaryReconciliation` without assuming separate aggregate roots.

These are proposed backlog tracking entries, not accepted regulatory findings.
