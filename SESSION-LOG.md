# Session Log

## Session 000 — Project initiation — 2026-10-19

- Created a portable project starter pack from the consolidated master prompt and supplied artifacts.
- Primary goal: define the semantic data model before designing database implementation or APIs.
- Proposed 18 backlog items, all initially Todo.
- No new architectural decisions approved.
- Next task: CTC-001, reconcile the earlier SemanticDocument and newer BillingDocument drafts.
- Source documents remain external references; attach them to the ChatGPT Project alongside this pack.

## Closeout template

```markdown
### Session NNN — YYYY-MM-DD — CTC-XXX
- Scope:
- Evidence reviewed:
- Findings (IDs):
- Decisions proposed (ADR IDs):
- Decisions explicitly approved (ADR IDs):
- Model changes proposed:
- Backlog changes:
- Open questions:
- Next task:
- Checkpoint file:
```

### Session 001 — 2026-10-19 — CTC-002 instance-level lifecycle simulation
- Scope: Simulate issuance, clearance, rejection, correction and cancellation using explicit before/after instance records for a fictional clearance jurisdiction XX.
- Evidence reviewed: Semantic Billing Model v0.3 (billing/fiscal/process separation; document relationships and correction semantics); Relational Data Model v0.3 (compliance transaction and historical version linkage); previous CTC-002 conceptual scenarios.
- Synthetic instances: DOC-001, REV-001, FC-001, REP-001/002/003, CT-001, ATT-001, EVT-002/003/010, EVD-001/002; corrective DOC-002 with relationship to DOC-001. Branches are illustrative and not a single sequential legal workflow.
- Findings (IDs): F-002-11 through F-002-16, added to FINDINGS.md with evidence limits.
- Decisions proposed: Preserve embedded (A), independently versioned (B) and hybrid (C) FiscalContext options. No preferred option finalized.
- Decisions explicitly approved: None.
- Model changes proposed: Candidate immutable document revisions, submission attempts, append-only events, fiscal evidence and authoritative semantic ownership. No changes accepted into MODEL-BASELINE.md.
- Backlog changes: None made in this update; CTC-002 remains in progress conceptually.
- Open questions: Intrinsic versus jurisdiction-specific fiscal field ownership; multi-jurisdiction interpretation; versioned profile reproducibility; real-world correction/cancellation workflows.
- Next task/activity: Within CTC-002, build a field-ownership matrix using actual Mexico CFDI, Italy FatturaPA and France Extended CTC examples; verify payloads and authority responses before selecting aggregate boundaries.
- Checkpoint file: This SESSION-LOG.md entry and FINDINGS.md rows F-002-11..F-002-16.
- Governance: No authoritative Project copies automatically synchronized; replace them with these reviewed files.

## Session 002 — 2026-10-19 — CTC-002 evening checkpoint

- **Scope:** Compare fiscal-context A/B/C against issuance, clearance, rejection, correction, cancellation; review field ownership for Mexico, Italy and France; perform French documented example stress test.
- **Sources:** Semantic Billing Model v0.3, Relational Model v0.3, SemanticDocument Entity Model v1.0, existing project reviews; documentation-based CFDI/SdI review artifacts.
- **Test performed:** Reconciled French GROUP line 10 (+21,425.59), DETAIL line 11 (+21,425.59, noncontributing), GROUP line 20 (-204.78) to contributing total **EUR 21,220.81**; no raw XML executed.
- **Findings:** F-002-11 through F-002-35 recorded as pending review (F-002-11..16 from earlier synthetic lifecycle; F-002-17..35 from country reviews and French test).
- **Decisions:** A embedded, B independent, C hybrid all remain under investigation. Composed semantic contract is a leading hypothesis only. **No ADR accepted.**
- **Model changes:** None approved; MODEL-BASELINE.md remains unapproved.
- **Backlog:** CTC-002 set to Review / evidence-gated; CTC-003 remains Todo, not started.
- **Evidence gaps:** Real French XML + profile/XSD, genuine paired Mexican certification artifacts, paired Italian SdI notifications, actual multi-interpretation case.
- **Next:** Read PICK-UP-NEXT-SESSION.md; review proposed boundary decisions and evidence gates; only then approve CTC-002 or begin CTC-003.
- **Deliverable:** RESEARCH/CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md and full evening bundle.

## Session 003 — 2026-10-20 — CTC-002 explicit principle approval

- **Scope:** Decision-ready aggregate ownership/invariant review, following 2026-10-19 evening checkpoint.
- **User approval:** Explicitly approved CTC-002-P1 through P6: separation of billing and processing; immutable published revisions; preserved source/generated representations; distinct fiscal and submission identities; independent compliance histories; single authoritative semantic owner per concept.
- **Approval limitation:** Principle-level only. No specific FiscalContext design, cardinality, schema, database layout or newly numbered global ADR approved.
- **Deferred:** FiscalContext A embedded immutable, B independently versioned, C hybrid. All remain open pending evidence.
- **Task assessment:** CTC-002 is **Review / evidence-gated**, **not Done**, because aggregate boundaries/cardinality and evidence gates remain unresolved. CTC-003 not started.
- **Findings:** Existing F-002-11..35 preserved; no additional sample-validation findings asserted.
- **Model changes:** None. MODEL-BASELINE.md remains an unapproved candidate; principle approval annotated only.
- **Evidence missing:** validated French Extended CTC raw XML/profile, certified CFDI before/after pair, FatturaPA/SdI notification pair, actual multi-interpretation case.
- **Next task within CTC-002:** Resolve ownership of intrinsic versus jurisdictional fiscal facts, and establish whether A/B/C distinction requires additional fixtures; prepare final aggregate boundary approval request.
- **File synchronization:** These are replacement working copies, not automatically synchronized Project documents.

## Session checkpoint — 2026-10-20 — CTC-002 P7 approval

- **Scope:** Distinguish source-supplied facts from inferred, enriched and jurisdiction-derived fiscal facts.
- **Decision explicitly approved:** CTC-002-P7, architectural principle only (exact text recorded in DECISIONS.md).
- **Prior approvals:** CTC-002-P1 through P6 remain Accepted — principle only.
- **Deferred decisions:** FiscalContext A/B/C; no aggregate ownership, cardinality, or implementation selected.
- **Model changes:** None approved. MODEL-BASELINE.md remains a candidate model.
- **Backlog:** CTC-002 remains Review / evidence-gated; CTC-003 remains Todo.
- **Evidence needed:** Versioned, validated real-world fixtures and mapping/profile provenance; demonstration of any need for multiple fiscal interpretations of one billing revision.
- **Next activity:** Within CTC-002, validate provenance classification for source-supplied versus derived fiscal facts against representative fixtures and profile rules.
- **Repository sync:** Prepared as append-only changes; no remote commit performed.


## Session 004 — 2026-10-20 — CTC-002 consolidated decision package

- Scope: Consolidate D2 formal logical contract, P1..P7 approval, synthetic replay, Peppol/CFDI/Malaysia/India tests and earlier Italy/France evidence.
- Decisions approved this session: **None**. P1..P7 remain accepted at principle level; user previously validated D2 logical direction.
- Proposed: D2 nine-concept logical contract and I-01..I-10 invariants for explicit user review.
- Findings proposed: F-002-41..59, pending review. No full authority conformance asserted.
- Unresolved: FiscalContext A/B/C aggregate boundaries, publication boundary, real paired fixtures, complete profile archives, independent-interpretation discriminator.
- Backlog: CTC-002 **Review / evidence-gated, not Done**; CTC-003 Todo.
- Next: User approval of contract/invariants and whether scoped logical-boundary closure is acceptable; record explicit decision before status change.
- Deliverable: `research/CTC-002/CTC-002-CONSOLIDATED-DECISION-REVIEW.md`.
- GitHub: Replacement files generated locally; no remote push.

## Session 004 — 2026-10-20 — CTC-002 D2 formal contract and scoped approval

- **Scope:** Explicit approval and closure decision after Peppol, CFDI, Malaysia and India focused constructed-fixture tests, two-version synthetic replay, Italy SdI documentation review and France conceptual stress test.
- **User approval:** D2 nine-concept implementation-neutral logical contract **Accepted**; invariants **I-01 through I-10 Accepted**; **CTC-002 scoped logical-boundary closure Approved**. Previously accepted P1..P7 unchanged.
- **Decision record:** `DECISIONS.md` section `CTC-002 — Explicit D2 logical-contract approval and scoped closure`; task-qualified `CTC-002-D2-LOGICAL-APPROVAL`, not a global ADR number.
- **Explicit exclusions:** No acceptance of FiscalContext A/B/C physical design, mandatory independent aggregates, concrete physical cardinalities, full JSON/relational schema or regulatory conformance.
- **Task changes:** CTC-002 marked Done **only for scoped logical boundary**; CTC-003 eligible to start. Follow-ups CTC-002-FU01..FU05 introduced for physical design, paired real fixtures, archived historical replay, multi-interpretation evidence and semantic precision.
- **Evidence:** Test reports remain as documented; synthetic and constructed fixtures do not establish full tax-authority validity. No new external validation performed during approval update.
- **Model baseline:** Accepted logical D2 foundation annotated; detailed model remains unapproved.
- **Next task:** Begin CTC-003 logical entity dictionary and cardinalities, preserving deferred choices as explicit open questions.
- **Synchronization:** Git-ready replacement files generated locally; remote GitHub not modified.


## Session 005 — 2026-10-20 — CTC-003 T01/T02 approval and T03 provisional test

- **Scope:** TaxRegime/TaxApplication ownership, TaxSummary aggregation, sign policy and five synthetic monetary scenarios.
- **Explicit approvals:** T01 and T02 accepted at conceptual level. T03 remains proposed/provisional, not approved.
- **Existing approvals preserved:** CTC-002 P1–P7, D2 logical contract and I-01..I-10. FiscalContext A/B/C physical design deferred.
- **Test:** `tests/test_tax_signs.py` executed with Python Decimal; 5/5 synthetic cases passed (positive invoice, negative line, withholding, credit note, informational tax). No official regulatory validation.
- **Proposed findings:** CTC-003-F01..F05 in FINDINGS.md; evidence limitations explicit.
- **Model changes:** No detailed tax schema accepted. Draft 0.2/0.3 remain unapproved.
- **Backlog:** CTC-003 In Progress; CTC-004 not started.
- **Next:** Resolve whether contribution is a stored assertion or derived projection, and test included taxes, credit/reversal polarity, mixed currencies, rounding and source-asserted tax-summary variances before T03 approval.
- **GitHub:** Full replacement files supplied, not pushed or synchronized.


## Session — 2026-10-20 — CTC-003 T03 logical-policy approval

- **Scope:** Record explicit T03 decision after decision-ready source review and focused tests.
- **Evidence:** `research/CTC-003/CTC-003-T03-DECISION-READY-REVIEW.md` (21 focused assertions; incomplete real-world regulatory fixture validation).
- **Explicitly accepted:** CTC-003-T03 as the ten refined logical monetary invariants transcribed in DECISIONS.md.
- **Preserved approvals:** T01/T02; CTC-002 P1..P7, D2 and I-01..I-10.
- **Not accepted:** Final `MonetaryBasis`/`MonetaryEffect` entity shapes, physical cardinalities, aggregate roots, jurisdictional rules, T03 draft field schema.
- **Open evidence:** E-T03-01..05 and detailed candidate monetary concepts.
- **Backlog:** CTC-003 remains In Progress; evidence and detailed design follow-ups proposed.
- **Next:** Continue CTC-003 detailed entity dictionary and reconcile T03 logical policy with source assertions and summary models.
- **GitHub:** No remote push. Complete replacement files supplied for manual review/commit.

## Session — 2026-10-20 — Backlog realignment review

- Scope: assess CTC-001 closure readiness, maintain CTC-003 In Progress, link prior tax test evidence to CTC-004, identify CTC-017 governance work.
- Sources: latest locally available CTC-003 T03 approval package and CTC-001 reconciliation review from baseline archive. Remote GitHub not read.
- Decisions explicitly approved this session: none. Previously accepted D2/P1–P7/I-01–I-10/T01–T03 preserved.
- Backlog: CTC-001 stays Review pending explicit scoped closure approval; CTC-002 Done scoped; CTC-003 In Progress; CTC-004 Todo with evidence links; CTC-017 Todo.
- Next: user review CTC-001 closure assessment; then consolidate unified CTC-003 dictionary.
- Checkpoint: reviews/CTC-001-CLOSURE-ASSESSMENT.md.

## Session — 2026-10-20 — CTC-001 scoped closure and CTC-003 unified draft

- **Scope:** Apply explicit CTC-001 closure approval and reconcile commercial Draft 0.2 with tax Draft 0.3 under D2.
- **User approval:** CTC-001 Done at original reconciliation-deliverable scope only. No additional ADRs or detailed schema accepted.
- **Sources:** 28-row CTC-001 reconciliation, commercial Draft 0.2, tax Draft 0.3, latest available backlog/decisions and T03 accepted ten logical invariants. Remote GitHub HEAD not inspected.
- **Deliverable:** `research/CTC-003/CTC-003-UNIFIED-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.4.md` (proposed).
- **Decisions retained:** CTC-002 D2/P1–P7/I-01–I-10 and CTC-003 T01–T03 at accepted logical scopes. FiscalContext A/B/C physical choice deferred.
- **Findings:** F-003-U01..U04 proposed; no new country conformance evidence.
- **Backlog:** CTC-001 Done scoped, CTC-002 Done scoped, CTC-003 In Progress, CTC-004 Todo with preparatory evidence, CTC-017 Todo. All evidence and aggregate follow-ups open.
- **Next:** Review unified dictionary ownership conflicts, then complete D2 fiscal/provenance and compliance/evidence portions before approving CTC-003.
- **GitHub:** Full replacement files supplied; not pushed automatically.


## 2026-10-20 — CTC-003 Draft 0.5 D2 companion entity consolidation

- **Scope:** Continue CTC-003 only; extend unified Draft 0.4 into an end-to-end implementation-neutral D2 candidate dictionary.
- **Sources:** Existing Commercial 0.2, Tax 0.3, Unified 0.4, approved D2 contract and project decisions, SemanticDocument v1.0, Billing Model v0.3; no new official fixture testing.
- **Output:** `research/CTC-003/CTC-003-UNIFIED-D2-SEMANTIC-ENTITY-DICTIONARY-DRAFT-0.5.md`, including source/derived fiscal facts, provenance, profile packages, representations, compliance events, fiscal identity/evidence, logical references, shared types and unresolved decisions.
- **Accepted decisions:** No new decisions. D2/P1–P7/I-01–I-10/T01–T03 preserved.
- **Status:** CTC-003 In Progress; Draft 0.5 Proposed; FiscalContext A/B/C physical design deferred. CTC-004 not started.
- **Next:** Review candidate ownership and correlation rules, conditional cardinalities and complete example validation before CTC-003 acceptance.
- **GitHub:** Full replacement working files only; no remote push, and remote HEAD not checked.


## CTC-003 — Ownership review Draft 0.6 — 2026-10-20
- Reviewed D01 document/party identity, D02 fiscal provenance, D03 compliance/representation/evidence correlation.
- Proposed immutable party snapshots, closed interpretation input manifest and pinned submission snapshot. No new approvals.
- Next: review D01–D03 and test concrete instance references and conditional cardinalities. CTC-003 remains In Progress.

## Session — 2026-10-20 — CTC-003 D01/D02/D03 approval and conditional-cardinality prototype

- **Scope:** Accept logical ownership directions D01/D02/D03 and six paired invariants; evaluate conditional cardinalities and instance-level references without approving schema.
- **Explicit approvals:** CTC-003-D01/D02/D03, D01-1/2, D02-1/2, D03-1/2 (logical level only).
- **Preserved approvals:** D2, P1–P7, I-01–I-10, T01–T03.
- **New deliverables:** Draft 0.7 relationship/cardinality matrix, synthetic instance scenarios and executable structural assertion script.
- **Not approved:** field-level shapes, cardinalities, publication boundaries, physical FiscalContext A/B/C, country fixtures.
- **Backlog:** CTC-003 In Progress; CTC-003-R01..R05 tracked as open.
- **Next:** Review proposed conditional cardinalities and exception handling; then integrate approved details into Draft 0.8.
- **Sync:** Git-ready replacement files only; no remote push.

## 2026-10-20 — CTC-003 lifecycle/publication Draft 0.8

- Scope: distinguish ingestion, mutable normalization, immutable publication, legal/fiscal issuance and external compliance operations.
- Output: lifecycle state dimensions, candidate transitions, conditional cardinality matrix, synthetic instance/reference validation cases, proposed L01–L10.
- Decisions approved: None new. Prior D2, P1–P7, I-01–I-10, T01–T03, D01–D03 retained.
- Unresolved: publication boundary, legal identity uniqueness, document-type minima, retry/reconciliation and legal-state rules.
- Task status: CTC-003 In Progress; detailed model not approved.
- Next: review L01–L10 and lifecycle separation, then refine unified dictionary with approved outcomes.

## Session — 2026-10-20 — CTC-003 L01–L10 approval and Draft 0.9

- **User explicitly approved:** three-dimensional separation of preparation, legal/fiscal recognition, and compliance processing; L01–L10 at logical-policy level only.
- **Not approved:** detailed cardinalities, legal publication/issuance triggers, country-specific rules, physical FiscalContext A/B/C, entity materialization or regulatory validity.
- **Draft 0.9:** proposes a phase-aware cardinality contract and synthetic reference fixtures for invoice, credit note, cancellation and pre-publication ingestion. These are design proposals, not regulatory assertions.
- **Task:** CTC-003 remains In Progress; CTC-004 remains Todo with linked preparatory evidence.
- **Next:** review C09-01 through C09-08 cardinality proposals and resolve conditional profile requirements before detailed entity schema approval.

## Session — 2026-10-20 — CTC-003 batch and envelope review

- Scope: Reassess Draft 0.9 C09-02 and C09-07 for multi-document inbound payloads and outbound batch envelopes.
- Findings: Transport container identity and per-document identity/outcome need separate correlation; partial outcomes must not be inferred from envelope acceptance. Synthetic cases only.
- Proposed: B01–B10 and candidate extraction/envelope/member entities. No new approvals.
- Existing approvals: D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10 preserved.
- Task: CTC-003 In Progress. Next: review proposed cardinality changes and obtain real batch/response fixtures.
- GitHub: replacement files prepared; no push.

## Session — 2026-10-20 — CTC-003 batch separation approval

- **Scope:** Review the Draft 1.0 batch ingestion/submission envelope separation proposal.
- **Explicit user approval:** Logical separation of ingestion/transport containers from individual `BillingDocument` and `ComplianceTransaction` identities (`CTC-003-BATCH-01`).
- **Explicit exclusions:** B01–B10, candidate entity shapes and C09 cardinalities remain Proposed; no physical model or jurisdiction-specific batch semantics approved.
- **Preserved:** D2, P1–P7, I-01–I-10, T01–T03, D01–D03 and L01–L10 unchanged.
- **Evidence:** Previous Draft 1.0 conceptual analysis and synthetic examples; no newly validated real batch fixtures.
- **Task status:** CTC-003 In Progress.
- **Next:** Instance-level batch and member correlation tests, then conditional cardinality review.
- **GitHub:** Complete replacement files prepared; remote repository not modified.
