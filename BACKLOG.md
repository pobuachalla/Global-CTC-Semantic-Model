# Global CTC — Project Backlog

**Baseline date:** 2026-10-19  
**Primary objective:** Agree an evidence-backed, jurisdiction-neutral semantic data model before application implementation.  
**Authority:** This file is the proposed task register; no task is completed or approved merely by being listed.

## Workflow

Statuses: `Todo`, `In Progress`, `Blocked`, `Review`, `Done`. Only mark `Done` after the acceptance criteria have been reviewed and the deliverable linked. Priority: P0 foundational, P1 validation/persistence, P2 later integration. Preserve task IDs.

| ID | Task | Priority | Workstream | Status | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|---|
| CTC-001 | Reconcile SemanticDocument and BillingDocument | P0 | Semantic foundation | Done (scoped reconciliation deliverable) | — | Entity-by-entity comparison, conflict register, proposed resolutions with evidence |
| CTC-002 | Agree semantic aggregate boundaries | P0 | Semantic foundation | Done (scoped logical boundary only; P1-P7 + D2 + I-01..I-10 accepted) | CTC-001 | Proposed boundaries for BillingDocument, FiscalContext, ComplianceTransaction, DocumentRepresentation; FiscalContext A/B/C unresolved |
| CTC-003 | Define semantic entity dictionary and cardinalities | P0 | Semantic foundation | Done — scoped (detailed logical dictionary approved 2026-10-20) | CTC-002 | Entity definitions, identifiers, cardinalities, nullability and relationships |
| CTC-004 | Validate tax and monetary semantics | P0 | Semantic foundation | Done — scoped (deterministic logical validation approved 2026-10-21) | CTC-003 | Multi-regime tax, withholding, signed values, reconciliation and precision rules |
| CTC-005 | Design jurisdiction profiles and extension governance | P0 | Semantic foundation | Done — scoped (logical governance approved 2026-10-21) | CTC-002 | Extension decision tree, validation, versioning and promotion criteria |
| CTC-006 | Resolve parties, document identity and corrections | P0 | Semantic foundation | Done — scoped (C006-01..03 approved 2026-10-21) | CTC-003 | Party role, identifiers, snapshots, series, correction/reference semantics |
| CTC-007 | Define semantic model versioning and compatibility | P0 | Semantic foundation | Done — scoped | CTC-003 | Versioning rules, breaking-change policy and compatibility test plan; V-01..V-10 accepted at logical-policy level on 2026-10-21 |
| CTC-008 | Inventory and score 13 GitHub repositories | P1 | Evidence and validation | In Progress | — | File-level inventory, licensing, commit IDs, valid/invalid fixtures and scores |
| CTC-009 | Create semantic coverage and loss matrix | P1 | Evidence and validation | Todo | CTC-003, CTC-008 | Per-field mapping outcomes, unrepresentable concepts, preservation and reversibility |
| CTC-010 | Stress-test French and non-EU payloads | P1 | Evidence and validation | Todo | CTC-004, CTC-008 | Documented tests for grouped lines, signed amounts, multi-regime tax and corrections |
| CTC-011 | Derive logical relational model | P1 | Persistence | Todo | CTC-002, CTC-003 | Logical ER model derived from accepted semantics with explicit cardinalities |
| CTC-012 | Define persistence snapshots and lineage | P1 | Persistence | Todo | CTC-011 | Immutability, source and target representations, lineage and retention decisions |
| CTC-013 | Define compliance transactions and event model | P1 | Compliance lifecycle | Done — scoped | CTC-002 | Submission attempts, destinations, event dimensions and state derivation |
| CTC-014 | Define normalized authority responses | P1 | Compliance lifecycle | Todo — next parallel task | CTC-013 | Response schema, correlation, evidence and client-facing representation |
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

## 2026-10-20 — Backlog realignment review (proposed, no closure approval)

- **CTC-001: Review, not Done.** The 28-row reconciliation and eight conflict analyses exist at `research/CTC-001/CTC-001-RECONCILIATION-REVIEW.md`. D2 and T01/T02/T03 address some earlier conflicts, but full reconciliation disposition, historical ADR namespace inventory, and formal task acceptance remain outstanding. See `reviews/CTC-001-CLOSURE-ASSESSMENT.md`. Request explicit user closure approval before changing status.
- **CTC-002: Done (scoped).** Preserve approved D2 logical contract, P1–P7 and I-01–I-10; physical FiscalContext and evidence gates remain under FU01–FU05.
- **CTC-003: In Progress.** Next output is a unified candidate entity dictionary merging commercial draft 0.2 and tax/monetary draft 0.3, incorporating accepted T01/T02/T03 logical decisions, without pre-approving concrete schema/cardinalities.
- **CTC-004: Todo, with linked preliminary evidence.** Prior CTC-003 tax tests are preparatory evidence only: `research/CTC-003/CTC-003-T03-DECISION-READY-REVIEW.md`, `research/CTC-003/tests/test_t03.py`, and other extended monetary and source-mapping reports where present. No complete official conformance suite or accepted CTC-004 validation matrix.
- **CTC-017: Todo.** Formalize project ADR namespace, approval/closure gates, supersession rules, and GitHub review/commit process; existing approval practice does not imply task closure.
- **Deferred follow-ups:** CTC-002-FU01..FU05 and CTC-003-EV01..EV05 / DES01 remain open as recorded above.

**This review does not change accepted architecture decisions, does not close CTC-001, and does not start CTC-004.**

## 2026-10-20 — CTC-001 explicit scoped closure and CTC-003 consolidation

- **CTC-001: Done (scoped)** by explicit user approval of the original reconciliation deliverable. This supersedes earlier Review status snapshots without changing historical entries. Acceptance covers source comparison, conflict identification and proposed resolutions only; does not accept all historic ADRs or detailed entity designs.
- **CTC-003: In Progress.** Unified entity dictionary draft 0.4 now consolidates commercial draft 0.2, tax/monetary draft 0.3 and approved T01–T03 logical policy. Entity field names, cardinalities and new candidate value objects remain proposed.
- **CTC-004: Todo** with prior synthetic and source-derived tests linked as preparatory evidence, not conformance approval.
- **CTC-017: Todo**; historical ADR numbering and supersession still require governance review.
- **CTC-002-FU01..FU05 and CTC-003-EV01..EV05/DES01:** remain open and unaffected.
- **Next:** Review CTC-003 conflict register and publication/identity decisions; develop complete D2 provenance, representation, profile and compliance dictionaries; then seek CTC-003 approval.


## 2026-10-20 — CTC-003 Draft 0.5 checkpoint

- **CTC-003: In Progress / review needed.** Draft 0.5 now proposes detailed logical dictionaries for all nine D2 concepts, with a consolidated reference diagram. Detailed fields, identity rules, conditional cardinalities and physical aggregation are **not accepted**.
- **CTC-003 next gate:** review document/revision/party ownership, fiscal interpretation/provenance references and fiscal identity/evidence correlation; then resolve conditional nullability, complete illustrative instances and v1.0/v0.3 field traceability before closure.
- **CTC-004 remains Todo** with preparatory monetary test evidence only; CTC-002-FU01..FU05, CTC-003-EV01..EV05/DES01 and CTC-017 remain open.


## CTC-003 Draft 0.6 checkpoint — 2026-10-20
Ownership and relationship review drafted for D01–D03; proposals pending explicit review. CTC-003 remains In Progress. See `research/CTC-003/CTC-003-OWNERSHIP-RELATIONSHIP-REVIEW-DRAFT-0.6.md`.

## 2026-10-20 — CTC-003 D01–D03 approval and conditional-cardinality validation

- **CTC-003: In Progress.** D01, D02, D03 logical directions and paired invariants accepted; detailed entity dictionary and cardinalities remain Proposed.
- **CTC-003-R01 (open, CTC-003):** Decide draft-ingestion to publication correlation, legal publication boundary, and document number uniqueness scope.
- **CTC-003-R02 (open, CTC-003/CTC-006):** Decide published party role conditionality, cross-revision snapshot reuse and line-level participant requirements.
- **CTC-003-R03 (open, CTC-003/CTC-007):** Decide interpretation input-manifest completeness, package pinning and idempotency rules.
- **CTC-003-R04 (open, CTC-003/CTC-013):** Decide submitted-attempt snapshot cardinality, response-only correlation and retry versus resubmission semantics.
- **CTC-003-R05 (open, CTC-003/CTC-002-FU02):** Validate candidate conditional cardinalities and references with actual country fixtures.

`research/CTC-003/CTC-003-CONDITIONAL-CARDINALITY-INSTANCE-VALIDATION-DRAFT-0.7.md` is a synthetic logical test, not country conformance.

## 2026-10-20 — CTC-003 Draft 0.8 lifecycle review

- **CTC-003 remains In Progress**. Draft 0.8 proposes three-dimensional lifecycle separation (preparation, legal/fiscal recognition, compliance processing), L01–L10 and conditional cardinality matrix; no new detailed schema approved.
- **CTC-003-R01** remains open: publication/freeze boundary and commercial number uniqueness.
- **CTC-003-R02** remains open: document-type conditional party and line requirements.
- **CTC-003-R04** remains open: retries, snapshots and authority correlation.
- **CTC-013 / CTC-014** to own detailed legal-state and authority-response mapping.
- **CTC-002-FU01 / FU02** remain open; physical aggregation and verified real fixtures deferred.

## 2026-10-20 — CTC-003 Draft 0.9 progress

- **CTC-003: In Progress.** Three lifecycle dimensions and L01–L10 approved at logical-policy level. Conditional cardinalities C09-01..08 remain proposed and require review.
- **CTC-006:** publication/issuance, commercial-number uniqueness, party and correction requirements remain open.
- **CTC-013/014:** legal-state projection and authority response mapping remain open.
- **CTC-002-FU01/FU02:** physical FiscalContext aggregation and validated authority fixtures remain deferred.
- **CTC-004:** remains Todo; earlier tax tests are linked preparatory evidence, not completed regulatory validation.

## CTC-003 Draft 1.0 batch/envelope checkpoint — 2026-10-20

CTC-003 remains **In Progress**. Batch ingestion and outbound submission envelope semantics have been reviewed as **proposals only**. Draft 0.9 C09-02 and C09-07 require reassessment; no cardinality or new logical entity approved. Evidence dependencies: CTC-008/009/010 (real batch fixtures), CTC-013/014 (envelope/member response taxonomy). See `research/CTC-003/CTC-003-BATCH-INGESTION-SUBMISSION-ENVELOPE-DRAFT-1.0.md`.

## 2026-10-20 — CTC-003 batch logical separation approved

- **CTC-003: In Progress.** `CTC-003-BATCH-01` Accepted at logical-principle level: transport/ingestion containers are separate from per-document billing and compliance identities.
- **Pending review:** B01–B10, C09-01..08 (especially C09-02/C09-07), and candidate extraction/envelope/member/transport-attempt entity shapes and cardinalities.
- **Evidence dependency:** CTC-008/009/010 to acquire/validate multi-document batch fixtures and partial-outcome responses; CTC-013/014 to refine transport and member response correlation.
- **Next CTC-003 activity:** Test proposed cardinalities against zero-member, multi-member, duplicate-member, retry and partial-outcome instances before requesting detailed-model approval.


## 2026-10-20 — CTC-003 blitz batch/cardinality checkpoint

- **CTC-003:** In Progress. C09-02, C09-07 and B01–B10 accepted at **logical** level under explicit user authorization to accept default recommendations. C09-01/03..06/08, detailed schema and physical entity shapes remain Proposed.
- **CTC-003-BATCH-EV01:** Todo (P1; CTC-008/009/010). Acquire versioned, licensed multi-document source and provider response fixtures with partial/member outcomes; validate actual correlation and schema.
- **CTC-003-BATCH-EV02:** Todo (P1; CTC-013/014). Resolve ambiguous external identifiers, late/out-of-order callbacks, timeout reconciliation and provider-specific retry/idempotency semantics.
- **CTC-003-BATCH-EV03:** Todo (P1; CTC-011/012). Design immutable envelope manifests, transport attempts and provenance persistence only after logical model approval.
- **Next CTC-003 milestone:** review remaining C09 cardinalities and integrate approved logical constraints into unified dictionary; do not mark CTC-003 Done yet.

## 2026-10-20 CTC-003 blitz continuation

- CTC-003 remains **In Progress**; logical C09-01..08 cardinalities accepted with recorded qualifications.
- Remaining CTC-003 acceptance: complete unified detailed dictionary, conditional constraints, source-model traceability and representative semantic examples.
- CTC-004 tax validation, CTC-005 profiles, CTC-006 parties/corrections and CTC-008..010 real fixtures remain open; do not infer completion from synthetic tests.


## 2026-10-20 CTC-003 completion candidate
Draft 1.3 unified semantic dictionary and review gate prepared. **CTC-003 remains In Progress**, pending G1-G5 and explicit detailed-model approval. Previous logical approvals remain unchanged.

## 2026-10-20 CTC-003 G2 continuation

CTC-003: **Review / evidence-gated, not Done**. Six G2 logical ownership dispositions accepted under standing blitz authorization. Integrated detailed dictionary Draft 1.9 is a **candidate**; G2-01..08 and field-level constraints are not approved. Remaining G1 field review, G3 broad validation, G4 field-level traceability and G5 explicit detailed schema approval.

## 2026-10-20 — CTC-003 scoped closure

- **CTC-003: Done — scoped.** User explicitly approved the CTC-003 final detailed logical dictionary closure candidate v1.0, with entity definitions, logical types, identifiers, qualified cardinalities and relationships.
- The 18 additional typed field contracts remain **Proposed**; do not treat them as accepted normative fields.
- Physical FiscalContext A/B/C, relational design, regulatory conformance, full independent format round trips and exhaustive historical field compatibility remain deferred to existing workstreams (CTC-002-FU01, CTC-004, CTC-008/009/010, CTC-011/012).
- **Next: CTC-004** — formal tax and monetary semantic validation, reusing prior T01–T03 tests; assess multi-regime tax, withholding, signed values, reconciliation and precision.

## 2026-10-21 — CTC-004 scoped closure

- **CTC-004: Done — scoped**, explicitly approved by the user on 2026-10-21. Scope is deterministic logical tax and monetary validation only.
- Evidence: 66/66 assertions replayed across four overlapping T01–T03 suites, plus 23/23 new focused assertions (12 multi-regime, 11 precision/rounding), 89/89 total assertions, not independent regulatory scenarios.
- Preserve accepted T01–T03, D2, P1–P7, I-01–I-10 and all other previously accepted logical decisions. The 18 CTC-003 additional field contracts remain Proposed.
- Jurisdictional tax ordering, profile rounding and tolerance policies: CTC-005/007. Real licensed authority fixtures: CTC-008/010. Semantic-loss and field coverage: CTC-009. Physical FiscalContext A/B/C: CTC-002-FU01/CTC-011.
- **Recommended next P0 task:** CTC-005 jurisdiction profiles and extension governance, bounded to logical applicability/versioning and extension ownership; do not reopen D2.

## 2026-10-21 — CTC-005 kickoff

CTC-005 In Progress. One bounded decision candidate created at `research/CTC-005/CTC-005-JURISDICTION-PROFILE-GOVERNANCE-DECISION-CANDIDATE.md`; JP-01..JP-10 and candidate contract remain Proposed. CTC-001..004 scoped approvals unchanged.


## 2026-10-21 — CTC-005 approved scoped closure

- **CTC-005: Done — scoped.** Seven-part extension decision tree and JP-01..JP-10 approved at logical-governance level by explicit user instruction.
- Validation: seven original deterministic scenarios and twenty focused governance assertions passed; tests are synthetic and not country-regulatory conformance.
- Deferred: production profile registry, archival/replay implementation, real jurisdiction profiles, semantic model compatibility (CTC-007), fixture evidence (CTC-008/009/010), FiscalContext physical A/B/C, and 18 proposed CTC-003 field additions.
- **Next P0 task: CTC-006** — parties, document identity and correction semantics; reuse the accepted CTC-003 logical dictionary.


## CTC-006 — Approved scoped closure — 2026-10-21

- **CTC-006: Done — scoped.** Explicit user approval of C006-01 through C006-03 at logical level, after ten focused synthetic scenarios passed.
- **CTC-007: Todo; next priority.** Define semantic model versioning and compatibility, breaking-change policy and compatibility test plan.
- Country-specific identity uniqueness, correction/cancellation legal validity, authority fixtures and relational keys remain deferred to existing backlog workstreams.
- Approved D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10, B01–B10, qualified C09, G2 and JP-01–JP-10 remain unchanged. Eighteen supplemental field contracts remain Proposed; FiscalContext physical A/B/C remains Deferred.

## 2026-10-21 — CTC-007 approved scoped closure

- **CTC-007: Done — scoped.** User explicitly accepted V-01 through V-10 at logical-policy level. The versioning decision candidate and 12/12 deterministic classification checks are the supporting evidence, not proof of a production compatibility engine.
- **CTC-008: Todo — next.** Inventory and score the 13 candidate public repositories: verify repo availability, license, pinned commit, actual invoice/response fixture paths, schema/profile validity, jurisdiction coverage, and reuse suitability. Do not treat example payloads as authoritative without validation.
- **Deferred:** machine-readable compatibility engine, API negotiation and consumer migration (CTC-016/018); historical replay package archiving (CTC-002-FU03); real jurisdiction fixtures (CTC-008/009/010); physical FiscalContext A/B/C (CTC-002-FU01/CTC-011); 18 proposed CTC-003 field contracts remain Proposed.
- Earlier CTC-001..006 Done — scoped statuses and approved D2, P1..P7, I-01..I-10, T01..T03, D01..D03, L01..L10, B01..B10, C09, G2, JP-01..JP-10, and C006-01..03 remain unchanged.


## CTC-008 kickoff — 2026-10-21

Initial public-source inventory started. 13 candidates retained; commit pins, license checks, full fixture enumeration and validation remain open. See `research/CTC-008/`.

## CTC-013 scoped closure — 2026-10-21

CTC-013 **Done — scoped** following explicit user approval of CL-01 through CL-08 at logical-policy level. Ten bounded synthetic lifecycle scenarios passed. CTC-008 remains In Progress (delegated fixture inventory). CTC-014 is the next parallel task. Provider-specific authority response schemas, response precedence, cryptographic validation, physical event storage and API contracts remain with CTC-014/016/011/012 and evidence tasks.
