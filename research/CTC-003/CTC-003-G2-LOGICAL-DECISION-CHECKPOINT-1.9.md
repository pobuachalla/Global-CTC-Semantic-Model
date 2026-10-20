# CTC-003 — G2 Logical Ownership Decisions and Draft 1.9 Checkpoint

**Date:** 2026-10-20  
**Status:** CTC-003 Review / evidence-gated, **not Done**.

## Authority and evidence

Standing user instruction in this conversation: blitz mode, progress default recommendations. The previous G2 Draft 1.8 recommended six logical dispositions. This checkpoint records those six as **Accepted at logical ownership level only** under that authorization. It does not claim the user individually approved a detailed field schema or G2-01..08.

Available: D2 approved logical contract, P1-P7, I-01..10, T01..03, D01..03, L01..10, B01..10 and qualified C09; Draft 1.8; earlier v1.0 SemanticDocument and v0.3 BillingDocument source designs. Live GitHub and real provider fixtures not verified.

## G2 dispositions (logical only)

| ID | Accepted ownership direction | Deferred detail |
|---|---|---|
| G2-A | `MonetaryReconciliation` is the sole authoritative reconciliation evaluation | Value-object and persistence shape |
| G2-B | One shared scoped `TaxPoint` | Scope-specific fields and profile rules |
| G2-C | `SubmissionAttempt` and `TransportAttempt` identify different operations | Join/cardinality implementation |
| G2-D | Commercial source assertions and local `SourceFiscalFact` have distinct authoritative ownership | Boundary cases and source mappings |
| G2-E | `FiscalIdentity` and `FiscalEvidence` are distinct | Artifact/evidence link schema |
| G2-F | Source-stated assertions remain separate from computed `TaxSummary` | Detailed aggregate schema |

## Candidate dictionary integration

Draft 1.9 integrates the earlier Section 11 corrections directly into field rows: publication profile reference, resolvable interpretation manifest, pinned mapping/profile package references, envelope snapshot consistency, explicit response ambiguity, and typed monetary components. The G2-01..08 invariants remain proposed.

## Evidence gates

G1: Candidate field catalogue integrated; exhaustive field review outstanding.
G2: Six logical ownership resolutions accepted; detailed shapes unapproved.
G3: Earlier focused synthetic positive/negative tests only; not comprehensive schema conformance.
G4: Entity-level source traceability exists; field-level loss matrix deferred to CTC-009.
G5: Detailed dictionary approval not yet given.

**Recommendation:** Keep CTC-003 in Review; conduct field-level approval and scoped closure decision in a separate explicit checkpoint. Do not begin a new backlog ID in this session.
