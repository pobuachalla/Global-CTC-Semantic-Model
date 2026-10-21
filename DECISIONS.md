# Architecture Decision Register

**Approval policy:** Existing ADRs in supplied references are historical proposals until reviewed. Do not treat them as newly accepted decisions. An ADR is `Accepted` only following explicit user approval.

Statuses: Proposed / Accepted / Rejected / Superseded / Deferred. Retain immutable IDs and record supersession links.

| ADR | Title | Status | Source / evidence | Outcome |
|---|---|---|---|---|
| ADR-09 (historical) | Separate ERP and CTC stages via semantic pivot | To review | Transformer Architecture v2.0, section 9 | Existing proposal; compatibility review pending |
| ADR-10 (historical) | Configuration-driven ERP connector hot reload | To review | Transformer Architecture v2.0, section 9 | Existing proposal; not reapproved |
| ADR-11 (historical) | Customer-specific custom-field registry | To review | Transformer Architecture v2.0, section 9 | Existing proposal; not reapproved |
| ADR-12 (historical) | ERP tax reconstruction via enrichment functions | To review | Transformer Architecture v2.0, section 9 | Existing proposal; not reapproved |
| ADR-13 (historical) | Async handling for party lookup cache misses | To review | Transformer Architecture v2.0, section 9 | Existing proposal; not reapproved |
| ADR-14 (historical) | Source type structural auto-detection | To review | Transformer Architecture v2.0, section 9 | Existing proposal; not reapproved |

**Important:** The complete reference may contain additional ADRs. Inventory and preserve those before assigning any new ADR number.

## New ADR template

```markdown
### ADR-XXX — Decision title
- Status: Proposed
- Date:
- Related task:
- Context and problem:
- Existing design / evidence:
- Options considered:
- Proposed decision:
- Consequences and trade-offs:
- Semantic model impact:
- Compatibility and migration impact:
- Validation / sample evidence:
- Approval / review record:
```

## CTC-002 — FiscalContext ownership alternatives (2026-10-19)

**Status: Proposed / under investigation. No option accepted.** The synthetic instance-level lifecycle simulation does not distinguish a winner. Preserve all three alternatives until validated country payloads and field-level ownership evidence are reviewed.

| Option | Candidate boundary | Strength | Outstanding risk | Status |
|---|---|---|---|---|
| A — Embedded | FiscalContext embedded in an immutable BillingDocument revision, with compliance operations and evidence separate | Simple document snapshot and local consistency | Multiple independently evolving jurisdictional interpretations may force duplication or revision complexity | Under investigation |
| B — Independent | FiscalContext has independent identity/version and references an immutable BillingDocument revision | Supports separate interpretations and historical versions | Risk of splitting intrinsic fiscal meaning or duplicating source facts | Under investigation |
| C — Hybrid | Intrinsic billing/tax meaning stays in BillingDocument revision; independently versioned jurisdictional interpretation and fiscal evidence are separate | Separates stable meaning from processing-specific meaning | Requires rigorous authoritative field ownership to avoid inconsistent copies | Under investigation |

**Decision gates:** (1) validated cross-jurisdiction field ownership matrix, (2) tested correction/cancellation and fiscal identity examples, (3) explicit invariants and historical profile-version references, (4) review of compatibility with SemanticDocument and BillingDocument v0.3. Do not mark any option Accepted without explicit user approval.

## CTC-002 — Evening evidence checkpoint (2026-10-19)

**No new ADR approved.** User previously directed the composed semantic contract as a leading *investigation hypothesis*, and explicitly requested that all FiscalContext alternatives remain open.

- **A — Embedded immutable FiscalContext:** viable for tested single-document lifecycle; requires careful snapshot/interpretation strategy for multiplicity. **Under investigation.**
- **B — Independent versioned FiscalContext:** viable; risks fragmenting intrinsic shared billing/tax facts. **Under investigation.**
- **C — Hybrid shared intrinsic semantics plus independent fiscal interpretation/evidence:** viable; risks duplicated facts and ambiguous authority unless field ownership is enforced. **Under investigation.**

**Evidence considered:** synthetic lifecycle; 28-row Mexico/Italy/France ownership matrix; documentation-backed CFDI stamp review; documentation-backed SdI notification review; internal French Extended CTC worked example with arithmetic reconciliation.

**Outstanding gate:** validate actual paired source/response fixtures and a case requiring two materially different fiscal interpretations for one immutable document revision.

**Proposed future ADR topics (not assigned new global ADR IDs):** immutable document revisions, representation/evidence identity, compliance transaction versus attempt/event, fiscal interpretation cardinality and versioning, single-authoritative-owner principle. Avoid collision with historical ADR numbering.

## CTC-002 — Approved architectural principles (2026-10-20)

**Approval source:** Explicit user instruction in CTC-002 conversation on 2026-10-20. **Status: Accepted at principle level only.** These IDs are CTC-002 principle IDs, **not newly numbered global ADRs**, avoiding collisions with historical ADR-09 onward. This approval does not accept a specific aggregate schema, entity cardinality, persistence approach or FiscalContext option.

| Principle ID | Approved principle | Exact approval scope | Status |
|---|---|---|---|
| CTC-002-P1 | Separate billing meaning from compliance processing | Commercial billing meaning is not defined by transient submission, clearance or delivery status. | Accepted — principle only |
| CTC-002-P2 | Preserve immutable published document revisions | Published semantic content and its historical references must not be silently overwritten; the precise publication boundary remains to be specified. | Accepted — principle only |
| CTC-002-P3 | Preserve original and generated representations | Source, generated, submitted and certified representations are individually identifiable and traceable; retention implementation remains open. | Accepted — principle only |
| CTC-002-P4 | Separate fiscal identity from submission identity | Commercial document identifiers, fiscal identities, authority references and transmission/submission identifiers are distinct semantic concepts. | Accepted — principle only |
| CTC-002-P5 | Maintain independent compliance histories | Attempts, external responses, validation findings and processing events preserve prior outcomes rather than replacing history. | Accepted — principle only |
| CTC-002-P6 | Assign one authoritative semantic owner per concept | A semantic fact has one authoritative owner; other models may reference or project it without creating competing authoritative versions. | Accepted — principle only |

### Explicit exclusions and unresolved decisions

- **FiscalContext A (embedded immutable), B (independently versioned), C (hybrid): Deferred; all remain available.** No preference or final aggregate-root/cardinality decision approved.
- `BillingDocumentRevision`, `SubmissionAttempt`, `ProcessingEvent`, and `FiscalEvidence` are candidate concepts; approval of principles does not approve their exact names, cardinalities, entity boundaries or physical implementation.
- Unresolved: when publication/issuance freezes a revision; intrinsic versus jurisdiction-specific fiscal attributes; single versus multiple fiscal interpretations; mapping and provenance version references; certified artifact/authority identity ownership; correction and cancellation legal workflows; provider-specific retry and reconciliation rules.
- Evidence gates: verified French Extended CTC XML/profile, paired certified/pre-certification CFDI XML, paired FatturaPA/SdI response XML, and a demonstrable need (or lack thereof) for multiple fiscal interpretations of one immutable revision.
- Historical ADRs are unchanged and not reapproved. CTC-002 remains **Review / evidence-gated**, not Done.

## CTC-002 — Approved principle P7 (2026-10-20)

**CTC-002-P7 — Source facts versus derived fiscal interpretations**

- **Status:** Accepted — architectural principle only.
- **Approval:** Explicit user instruction, 2026-10-20.
- **Exact approved wording:** Source-supplied semantic facts must remain distinguishable from inferred, enriched or jurisdiction-derived facts, with provenance and effective profile versions preserved.
- **Scope:** Semantic provenance and traceability; preserve origin and transformation/derivation context for fiscal meaning.
- **Not approved:** A specific provenance schema, persistence mechanism, aggregate root, cardinality, profile-version implementation, or physical database design.
- **Relationship:** Extends CTC-002-P1 through P6 without modifying their approval status or scope.
- **Deferred:** FiscalContext A (embedded immutable), B (independently versioned), and C (hybrid) remain open. No option preferred or accepted by this approval.
- **Task state:** CTC-002 Review / evidence-gated, not Done. CTC-003 not started.


## CTC-002 — Consolidated D2 decision proposal (2026-10-20)

**Status: Proposed for explicit approval; NOT accepted by creation of this package.** User previously validated D2 logical direction, but the nine-concept formal contract and I-01..I-10 are not yet approved.

- Proposed logical contract: see `research/CTC-002/CTC-002-CONSOLIDATED-DECISION-REVIEW.md` and `CTC-002-D2-FORMAL-LOGICAL-CONTRACT.md`.
- Proposed invariants: I-01..I-10, detailed in the consolidated decision review.
- FiscalContext A embedded / B independent / C hybrid: **Deferred**, no choice approved. D2 is an interface/contract candidate, not a decided physical option.
- Proposed closure: conditional logical-boundary sign-off only if the user explicitly approves the contract, invariants and scoped acceptance criteria; otherwise CTC-002 remains Review.
- Approved CTC-002-P1..P7 remain unchanged. Historical ADRs remain unchanged.

## CTC-002 — Explicit D2 logical-contract approval and scoped closure (2026-10-20)

**Approval source:** Explicit user instruction in the CTC-002 conversation, 2026-10-20. **Status: Accepted — logical semantic contract and invariants only.** This entry supersedes the *pending approval status* in the preceding consolidated D2 proposal; it does not rewrite historical proposals or alter historical ADRs.

### Approved logical contract — nine concepts

The D2 formal implementation-neutral contract is **Accepted at logical level** with these nine concepts and responsibilities, as defined in `research/CTC-002/CTC-002-D2-FORMAL-LOGICAL-CONTRACT.md`:

1. `BillingDocument` — stable logical commercial identity.
2. `PublishedRevision` — immutable published commercial/intrinsic tax content and revision identity.
3. `SourceFiscalFact` — source-supplied value, scheme, origin and provenance.
4. `FiscalInterpretation` — profile-specific interpretation pinned to an exact published revision.
5. `DerivedFiscalFact` — derived assertion and input/rule provenance.
6. `ProfilePackage` — exact versioned rules, mappings, code lists and reproducibility metadata.
7. `DocumentRepresentation` — separately identifiable original/generated/submitted/certified artifacts.
8. `ComplianceTransaction` — compliance operation and independent processing history.
9. `FiscalIdentity/Evidence` — typed external fiscal identities and associated evidence.

**Approval scope:** logical concepts, ownership responsibilities and references; not exact JSON property names, concrete classes, table layouts, service boundaries, storage technology, or all suggested cardinalities. `FiscalInterpretation` is approved as a *logical concept*, not as a mandatory independently persisted aggregate root.

### Approved logical invariants I-01 through I-10

- **I-01:** Interpretation references a specific published revision and fingerprint; re-evaluation never mutates it.
- **I-02:** Each source fact has one authoritative owner and preserves source representation/path.
- **I-03:** Derived facts identify inputs, rule version, profile release and scheme; external enrichment preserves source/time/snapshot.
- **I-04:** Submissions pin exact interpretation and representation references; mutable 'current' profile is insufficient.
- **I-05:** Profile package identity is immutable/content-addressable or equivalent; version labels alone are insufficient for replay.
- **I-06:** Derived classifications do not overwrite original classifications; contradictions remain separately traceable assertions.
- **I-07:** Status, authority receipts and retries do not mutate billing or interpretation facts.
- **I-08:** Target syntax/profile identifiers belong to representation or processing context, not commercial identity.
- **I-09:** Arithmetic and precision are validated under the selected profile; the global core does not universally assume two decimals.
- **I-10:** Semantic equivalence and legally compliant target representability are separate validation gates.

**Previously accepted:** CTC-002-P1 through P7 remain Accepted, unchanged in wording and scope.

### Explicitly deferred / not approved

- FiscalContext **A** embedded immutable, **B** independently versioned, **C** hybrid remain **Deferred** as physical/aggregate designs. D2 logical approval does not select among them or prescribe physical embedding.
- Precise physical cardinalities, persistence layout, JSON schema, APIs, publication trigger, jurisdiction-specific legal correction/cancellation behavior, provider retries and deployment boundaries remain unapproved.
- Cross-format tests are focused constructed-fixture tests, **not** full tax authority or Peppol conformance. Unverified paired production fixtures and archived profile packages remain evidence tasks.

### Scoped task disposition

**CTC-002: Done — scoped logical-boundary deliverable only, by explicit user approval.** The task's physical aggregate implementation and evidence gates are transferred to separately tracked backlog follow-ups. This is not a blanket statement that every aggregate-boundary question is resolved. CTC-003 may start on the approved D2 logical contract, while marking unresolved physical cardinalities as TBD rather than assuming values.

**Decision reference:** `CTC-002-D2-LOGICAL-APPROVAL` (task-qualified; not a newly numbered global ADR). No global ADR IDs were reassigned.


## CTC-003 — Tax ownership decisions (2026-10-20)

**Approval evidence:** Explicit user instruction in CTC-003 conversation. These are task-local IDs, not global ADR numbers. No other T03 approval is implied.

| ID | Decision | Status | Exact scope | Exclusions |
|---|---|---|---|---|
| CTC-003-T01 | Separate `TaxRegime` and `TaxApplication` | **Accepted** | A `TaxRegime` identifies a tax scheme/jurisdictional classification; a `TaxApplication` represents a tax applied to one explicitly identified economic scope and references one regime. Multiple applications and regimes are supported. | Exact fields, mandatory jurisdictional constraints, storage cardinality and tax-law applicability remain open. |
| CTC-003-T02 | `TaxSummary` as reconciled aggregate | **Accepted** | Derived grouped summaries are not independent authoritative tax applications; preserve original source-supplied summary assertions and reconcile rather than overwrite or double-count them. | Exact summary entity structure, grouping dimensions and tolerance rules remain open. |
| CTC-003-T03 | Magnitude plus signed contribution sign policy | **Proposed — provisional test hypothesis** | Evaluate nonnegative tax magnitude, explicit signed monetary contribution and separately qualified direction against positive/negative lines, withholding, credit notes and informational taxes. | **Not accepted** as final sign convention; statutory effects, credit polarity, included taxes, rounding and presentation semantics unresolved. |

**Preserved decisions:** CTC-002 P1–P7 and D2 nine-concept logical contract with I-01..I-10 remain accepted; FiscalContext physical A/B/C remains deferred. CTC-003 is In Progress, not Done.


## CTC-003 — Explicit T03 logical monetary policy approval (2026-10-20)

**Decision ID:** CTC-003-T03  
**Status: Accepted — logical policy only.**  
**Approval source:** User explicitly approved T03 with the ten refined invariants in `research/CTC-003/CTC-003-T03-DECISION-READY-REVIEW.md` on 2026-10-20. This supersedes the preceding provisional T03 status, without rewriting its historical record.

### Approved T03 logical invariants (exact decision scope)

1. Preserve original monetary assertions with original sign, currency, scope, representation and provenance.
2. Distinguish fiscal role/direction from the sign and economic effect of a tax.
3. Identify the reconciliation basis, scope, currency and which taxes/adjustments it already includes.
4. Calculate monetary effect relative to the selected basis; never double-count an already-included tax.
5. Preserve legal credit-note presentation independently of perspective-specific economic delta; never automatically negate all credit-note amounts.
6. Keep source tax summary assertions distinct from derived tax summaries; discrepancies are explicit reconciliation findings (T02).
7. Forbid cross-currency arithmetic without an explicit conversion record and provenance.
8. Apply a named rounding policy including stage, precision, method and profile version; preserve source rounded assertions.
9. Retain derivation inputs, source fact references, mapping/profile/code-list versions and calculation rule references (P7).
10. Return `NOT_EVALUABLE` for unknown inclusion, missing conversion, unresolved economic polarity or missing mandatory rounding policy; do not silently invent a payable value.

**Explicitly not approved:** `MonetaryBasis` and `MonetaryEffect` remain **candidate logical concepts**; their final fields, cardinalities, materialization, aggregate-root status and database storage are deferred. `DocumentEconomicEffect` and `MonetaryReconciliation` also remain candidates. The previously proposed T03-I01..I10 field-level invariants are **not** automatically accepted unless identical to the ten statements above. No jurisdictional tax calculation, rounding tolerance or regulatory conformance is approved by this decision.

**Preserved:** CTC-003-T01 and T02 remain Accepted; CTC-002 P1..P7, D2 nine-concept contract and I-01..I-10 remain Accepted; FiscalContext physical A/B/C remain Deferred. CTC-003 remains **In Progress**.

## 2026-10-20 — Backlog realignment (administrative review)

No new architecture decisions approved. CTC-001 closure is proposed, not accepted. CTC-002 scoped closure and CTC-003 T01–T03 remain accepted at their previously recorded scopes. CTC-004 preliminary evidence linkage is not a conformance approval.

## CTC-001 — Explicit scoped task closure (2026-10-20)

**Approval:** User explicitly approved closing CTC-001 at its original reconciliation-deliverable scope. **Task status: Done (scoped).** This is task acceptance, **not** an approval of all earlier candidate entities or historical ADRs. The source comparison, conflict register and proposed resolutions remain the CTC-001 deliverable.

**Carried forward:** detailed entity ownership/cardinalities and corrections into CTC-003/006; tax semantics into CTC-003/004; jurisdiction extensions into CTC-005; historical ADR namespace, review and supersession into CTC-017; evidence gaps into CTC-008/009/010 and CTC-002 follow-ups.

## CTC-003 — Unified entity dictionary draft 0.4 (2026-10-20)

**Status: Proposed, not accepted.** Consolidation of commercial Draft 0.2 and tax Draft 0.3. No new detailed entity definitions, relationships, or cardinalities approved by task continuation. Accepted logical T01/T02/T03 and D2/P1–P7/I-01–I-10 remain in force. FiscalContext physical A/B/C remains deferred. See `research/CTC-003/CTC-003-UNIFIED-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.4.md`.


## 2026-10-20 — CTC-003 unified D2 dictionary Draft 0.5 (no new approvals)

Draft 0.5 extends the previously proposed unified dictionary with detailed **candidate** definitions for SourceFiscalFact, FiscalInterpretation, DerivedFiscalFact, ProfilePackage, DocumentRepresentation, ComplianceTransaction, SubmissionAttempt, ProcessingEvent, FiscalIdentity and FiscalEvidence, plus provenance and shared value types. **Status: Proposed / review required.** No new ADR, entity schema, physical aggregate, cardinality, regulatory rule or CTC-003 closure was approved. D2/P1–P7/I-01–I-10 and T01/T02/T03 retain their exact prior approved logical scope. FiscalContext A/B/C remains deferred. See `research/CTC-003/CTC-003-UNIFIED-D2-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.5.md`.


## CTC-003 Draft 0.6 — Ownership review proposals (2026-10-20)

D01 (document and immutable party snapshots), D02 (closed fiscal interpretation input manifest), and D03 (pinned submission snapshot and evidence correlation) are **Proposed, not Accepted**. See `research/CTC-003/CTC-003-OWNERSHIP-RELATIONSHIP-REVIEW-DRAFT-0.6.md`. All prior approvals remain unchanged.

## CTC-003 — Explicit D01/D02/D03 logical ownership approval (2026-10-20)

**Approval evidence:** User explicitly approved D01, D02 and D03, with their paired logical invariants, in this conversation. **Status: Accepted — logical ownership/invariant level only.** These task-qualified IDs are not global ADR numbers.

| ID | Accepted logical direction and invariants | Scope |
|---|---|---|
| CTC-003-D01 | `BillingDocument` owns stable platform identity; `PublishedRevision` owns immutable published commercial assertions; published party participation pins immutable `PartySnapshot` references (D01-1). Post-issuance changes to legally identifying facts require a governed correction/replacement decision rather than silent replacement (D01-2). | Logical identity and ownership only |
| CTC-003-D02 | `FiscalInterpretation` uses a closed, pinned input manifest to support reproducibility or explicit `NOT_EVALUABLE` when dependencies are unavailable (D02-1). Derived facts cannot overwrite authoritative source facts; conflicts retain both and produce findings (D02-2). | Logical provenance and interpretation ownership only |
| CTC-003-D03 | Every submitted attempt pins an immutable submission snapshot and cannot resolve mutable `latest` references (D03-1). Fiscal identity and evidence refer to the exact artifact or operation they attest without duplicating authoritative identifiers (D03-2). | Logical correlation and evidence ownership only |

**Explicit exclusions:** No approval of detailed fields, mandatory physical `InterpretationInputManifest`/`SubmissionSnapshot` entities, schema/cardinalities, party reuse policy, legal publication boundary, country-specific correction/cancellation rules, FiscalContext A/B/C physical aggregation, storage, API, or regulatory fixture validity. Draft 0.6 remains the design rationale; its unapproved status at time of writing is superseded **only for the six explicitly approved logical invariants and three logical directions above**.

**Preserved:** D2 nine-concept logical contract, CTC-002 P1–P7 and I-01–I-10, and CTC-003 T01–T03 remain Accepted at their prior scopes. CTC-003 remains In Progress.

## CTC-003 — Draft 0.8 proposed lifecycle decisions (2026-10-20)

**Status: Proposed, not Accepted.** Candidate separation of preparation, legal/fiscal recognition and compliance-operation lifecycle dimensions; proposed invariants L01–L10. See `research/CTC-003/CTC-003-LIFECYCLE-PUBLICATION-CARDINALITY-REVIEW-DRAFT-0.8.md`. No automatic approval of conditional cardinalities, legal issuance criteria, physical aggregate boundaries or regulatory mandates. Previously accepted D2, P1–P7, I-01–I-10, T01–T03 and D01–D03 remain unchanged.

## 2026-10-20 — CTC-003 lifecycle approval L01–L10

**Approval source:** Explicit user approval in CTC-003 conversation on 2026-10-20. **Status: Accepted at logical-policy level only.**

The following three lifecycle dimensions are independently modelled: **document preparation**, **legal/fiscal recognition**, and **compliance processing**. They must not be collapsed into a single universal status.

| ID | Accepted logical invariant |
|---|---|
| L01 | Ingestion and publication have separate identities; an inbound artifact may exist before a BillingDocument or published revision. |
| L02 | Publication freezes semantic content and immutable references but does not, by itself, establish legal issuance. |
| L03 | Issuer-assigned commercial identity is captured with issuer, series, document type and an applicable uniqueness scope; the scope is not assumed globally. |
| L04 | Legal-state assessments reference jurisdiction, profile/rule version, supporting evidence/events and evaluation time. |
| L05 | Compliance responses do not mutate published commercial content. |
| L06 | Submitted attempts resolve to exact immutable submission snapshots, never mutable `latest` references. |
| L07 | Where an applicable rule requires a separate corrective legal document, it has distinct identity and preserves links to the original. |
| L08 | Cancellation is recorded through separate evidence and legal-state assessment; original clearance history is preserved. |
| L09 | Pending or unknown external outcomes do not automatically establish rejection or legal issuance. |
| L10 | Structural validation and jurisdiction/profile validation are separate stages with recorded outcomes. |

**Explicit exclusions:** The detailed cardinality matrix in Draft 0.8 is **not accepted**; neither are exact publication triggers, jurisdictional issuance/cancellation rules, mandatory physical entities, FiscalContext A/B/C physical aggregation, persistence, or legal validity of fictional examples. Draft 0.8's 'Proposed' label remains historically correct at creation; this entry records subsequent approval of only the above principles and invariants.

**Preserved:** D2, P1–P7, CTC-002 I-01–I-10, T01–T03, D01–D03 and their six invariants remain accepted within previous scopes. CTC-003 remains In Progress.

## CTC-003 — Batch ingestion and submission envelope review (2026-10-20)

**Status: Proposed — no approval requested or recorded yet.** Candidate separation of `IngestionRecord` / `DocumentExtraction` and `SubmissionEnvelope` / `EnvelopeMember` / `TransportAttempt` from individual `BillingDocument` and `ComplianceTransaction` identities. Proposed B01–B10 and amendments to C09-02/C09-07 are documented in Draft 1.0. Preserve all existing approvals (D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10). No global ADR ID assigned.

## CTC-003 — Batch and transport logical separation (2026-10-20)

**Decision ID:** CTC-003-BATCH-01  
**Status:** Accepted — logical principle only  
**Approval evidence:** Explicit user approval in CTC-003 conversation.

**Approved:** Ingestion and transport containers are logically distinct from the individual `BillingDocument` and `ComplianceTransaction` identities they carry. Container-level receipt, submission or success must not, by itself, establish a member document's legal/fiscal acceptance or outcome. Preserve independent document and compliance-operation correlation.

**Not approved:** B01–B10 remain **Proposed**; C09-01 through C09-08, including proposed changes to C09-02/C09-07, remain **Proposed**. `IngestionRecord`, `DocumentExtraction`, `SubmissionEnvelope`, `EnvelopeMember`, and `TransportAttempt` remain candidate entity names/shapes only. No detailed cardinality, physical aggregate/table, jurisdiction-specific batch rule, or real fixture conformance was approved.

**Unchanged accepted baseline:** D2, P1–P7, I-01–I-10, T01–T03, D01–D03 (and paired invariants), three lifecycle dimensions and L01–L10. FiscalContext A/B/C physical design remains deferred. CTC-003 remains In Progress.


## CTC-003 Blitz approval — 2026-10-20 — user-authorized default decisions

**Authority:** User instruction: "lets go into blitz mode. progress with any recommendations and accept default decisions". This authorizes acceptance of recommended logical constraints for the current CTC-003 batch review, **not** unreviewed physical architecture, provider-specific rules, or regulatory claims.

**CTC-003-C09-02 — Accepted, logical cardinality:** An ingestion event may yield 0..N document extractions. An individual extraction resolves to at most one logical BillingDocument at a given resolved state. Multiple receptions and extractions may refer to the same logical document; this does not establish legal identity or idempotency policy.

**CTC-003-C09-07 — Accepted, logical cardinality:** A submitted transport attempt references exactly one immutable outbound payload artifact (which may be a batch/envelope). A multi-document envelope carries 1..N identifiable member references; member-specific compliance operations and outcomes remain independently correlated. This does not mandate a separate envelope database table or one fixed transport protocol.

**CTC-003-B01..B10 — Accepted, logical invariants only:**

| ID | Accepted logical invariant | Exclusions / deferred |
|---|---|---|
| B01 | Preserve immutable original source representation reference(s) per reception. | Retention duration/storage. |
| B02 | Each extracted member has a stable source locator and distinct resolution history. | Provider-specific locator syntax. |
| B03 | A resolved extraction identifies at most one BillingDocument at a time; ambiguous matches remain unresolved and auditable. | Dedup/identity algorithms. |
| B04 | Submitted transport attempts pin one exact immutable outbound payload/digest. | Physical storage/envelope requirement. |
| B05 | Submitted multi-member payloads have immutable member manifests with exact revision/representation references. | Manifest encoding, ordering rules. |
| B06 | A revision can be referenced by distinct transport submissions without modifying the revision. | Whether retry is legally permitted. |
| B07 | Envelope and member outcomes carry typed, independently correlated subjects. | Provider correlation fields. |
| B08 | Transport/envelope success alone does not imply legal acceptance/clearance of each member. | Country-specific legal-state mapping. |
| B09 | Partial, total and unknown member outcomes are expressible with original response provenance. | Provider atomicity assumptions. |
| B10 | Retry, duplicate reception and idempotency histories remain distinct and auditable. | Dedup keys, external idempotency semantics, retry safety. |

**Not approved:** C09-01, C09-03..06, C09-08; full detailed cardinality schema; named physical entity roots/tables; country-specific batch behavior; real-fixture conformance. Existing D2/P1–P7/I-01–I-10/T01–T03/D01–D03/L01–L10/CTC-003-BATCH-01 approvals unchanged. FiscalContext A/B/C physical choice deferred. CTC-003 remains In Progress.

## CTC-003 Blitz continuation — 2026-10-20 — C09 remaining logical cardinalities

**Approval basis:** User instructed the project to proceed in blitz mode and accept default recommendations. Applied only to the recommended logical cardinality constraints below; no physical schema or legal mandate decisions.

- **CTC-003-C09-01 Accepted (qualified):** A completed external ingestion/reception preserves 1..N immutable original source artifact references. This does not impose an external artifact on purely internal document creation.
- **CTC-003-C09-03 Accepted (logical):** A BillingDocument may have 0..N published revisions, with at least one after the platform's first publication; the legal issuance boundary remains separately governed.
- **CTC-003-C09-04 Accepted (logical):** PublishedRevision may structurally reference 0..N PartyParticipations and BillingLines; mandatory roles/lines are enforced by document-family and jurisdiction profile. This does not authorize publication of invalid invoices.
- **CTC-003-C09-05 Accepted (logical):** Each PartyParticipation resolves to exactly one PartySnapshot; published references must resolve to immutable snapshots.
- **CTC-003-C09-06 Accepted (logical):** A PublishedRevision may have 0..N FiscalInterpretations; each interpretation pins exactly one revision and a complete immutable profile/input manifest. Physical FiscalContext design remains deferred.
- **CTC-003-C09-08 Accepted (logical):** A PublishedRevision may have 0..N legal-state assessments and a ComplianceTransaction 0..N typed processing events. Legal assessments require applicable evidence/basis, which need not be an authority response in every regime.

**Already accepted and unchanged:** C09-02/C09-07; B01–B10; CTC-003-BATCH-01; D2/P1–P7/I-01–I-10/T01–T03/D01–D03/L01–L10.
**Still proposed:** Detailed entity shapes and cross-profile validation requirements. No physical aggregate/table or universal legal-state transition approved.
**Evidence:** 22 synthetic positive/negative structural assertions in tests/validate_ctc003_draft12.py; not official source fixtures.

## CTC-003 G2 logical ownership — 2026-10-20 blitz continuation

**Status: Accepted at logical ownership level only** under the user's standing blitz-mode authorization to accept default recommendations. G2-A through G2-F: one authoritative MonetaryReconciliation; one scoped TaxPoint; separate SubmissionAttempt and TransportAttempt; distinct commercial and source fiscal fact ownership; separate FiscalIdentity and FiscalEvidence; preserved SourceAssertion distinct from computed TaxSummary. **G2-01..08, detailed fields, nullability, cardinalities and physical schema remain Proposed.** No change to D2, P1-P7, I-01..10, T01..03, D01..03, L01..10, B01..10, C09 or FiscalContext A/B/C deferral.

## CTC-003 — Detailed logical dictionary scoped approval — 2026-10-20

**Status: Accepted — scoped. Approval authority:** User explicitly stated: “I explicitly approve the CTC-003 detailed logical entity dictionary at the scoped closure-candidate level. Mark CTC-003 Done — scoped. Preserve the 18 additional field contracts as proposals, all deferred physical and regulatory work, and existing accepted decisions.”

**Normative approved artifact:** `research/CTC-003/CTC-003-DETAILED-LOGICAL-DICTIONARY-APPROVED-SCOPED.md`, based on `CTC-003-DETAILED-LOGICAL-DICTIONARY-CLOSURE-CANDIDATE.md` v1.0.

**Approval includes:** 51 candidate logical entity definitions promoted as the approved scoped logical dictionary, the documented logical field types and optionality, stable identities, typed fiscal identities/authority references, controlled signature alias convention, logical relationships and qualified cardinalities. The approved logical rules D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10, B01–B10, C09 and G2 ownership remain unchanged.

**Not approved:** The 18 Draft 4.2 additional field contracts (remain Proposed); physical FiscalContext A/B/C; tables and aggregate-root implementation; country-specific publication/issuance rules; full regulatory conformance; full independent format round trips; exhaustive historical field compatibility; unresolved jurisdictional mappings. No historical ADR is silently superseded.

**Disposition:** CTC-003 Done — scoped. Deferred items retain their existing backlog ownership; this is not an assertion that all 51 entities have been proven across all countries.

## CTC-004 — Scoped tax and monetary validation closure — 2026-10-21

**Status: Accepted — scoped task closure. Authority:** User explicitly stated: “I explicitly approve CTC-004 Done — scoped, limited to deterministic logical tax and monetary validation. Preserve all existing approved decisions and proposed fields, defer jurisdictional evidence to existing backlog tasks, and prepare complete replacement Git-ready project records.”

**Approval includes:** Closure of CTC-004's original logical validation criteria for multi-regime tax, withholding, signed amounts/credit polarity, source-vs-derived reconciliation, inclusive/exclusive basis, currency arithmetic safeguards, precision and rounding-policy behavior. Evidence comprises 66 previously replayed focused assertions and 23 newly executed assertions, all passing, with overlapping suites and synthetic test assumptions.

**Not approved:** New schema fields or entities; the 18 additional CTC-003 field contracts (still Proposed); tax-authority or jurisdictional conformance; country-specific tax ordering/rounding/tolerances; production FX policy; exhaustive semantic-loss coverage; physical FiscalContext A/B/C. No earlier ADR superseded.

**Evidence:** `research/CTC-004/CTC-004-CONSOLIDATED-VALIDATION-AND-CLOSURE-REVIEW.md`; `tests/CTC-004/test_remaining_gaps.py`; `tests/CTC-004/results.json`.
