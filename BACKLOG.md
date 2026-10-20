# Global CTC — Project Backlog

**Baseline date:** 2026-10-19  
**Primary objective:** Agree an evidence-backed, jurisdiction-neutral semantic data model before application implementation.  
**Authority:** This file is the proposed task register; no task is completed or approved merely by being listed.

## Workflow

Statuses: `Todo`, `In Progress`, `Blocked`, `Review`, `Done`. Only mark `Done` after the acceptance criteria have been reviewed and the deliverable linked. Priority: P0 foundational, P1 validation/persistence, P2 later integration. Preserve task IDs.

| ID | Task | Priority | Workstream | Status | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|---|
| CTC-001 | Reconcile SemanticDocument and BillingDocument | P0 | Semantic foundation | Review | — | Entity-by-entity comparison, conflict register, proposed resolutions with evidence |
| CTC-002 | Agree semantic aggregate boundaries | P0 | Semantic foundation | Review (evidence-gated; P1-P6 approved) | CTC-001 | Proposed boundaries for BillingDocument, FiscalContext, ComplianceTransaction, DocumentRepresentation; FiscalContext A/B/C unresolved |
| CTC-003 | Define semantic entity dictionary and cardinalities | P0 | Semantic foundation | Todo | CTC-002 | Entity definitions, identifiers, cardinalities, nullability and relationships |
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
