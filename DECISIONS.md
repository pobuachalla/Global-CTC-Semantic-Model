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
