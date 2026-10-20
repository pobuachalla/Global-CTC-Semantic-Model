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
