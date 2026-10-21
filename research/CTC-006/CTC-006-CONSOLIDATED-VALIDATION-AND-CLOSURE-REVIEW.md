# CTC-006 — Consolidated Party, Identity and Correction Validation

**Date:** 2026-10-21  
**Status:** Review — scoped closure recommended, not approved  
**Baseline:** Locally available `Global_CTC_CTC005_Approved_Scoped_Closure_Full_Git_2026-10-21.zip`; live GitHub HEAD not verified.  
**Prior approvals preserved:** CTC-001–005 Done — scoped; D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10, accepted batch/C09/G2 logical decisions and JP-01–JP-10.  
**Not approved:** 18 additional field contracts, physical FiscalContext A/B/C, jurisdiction-specific correction rules.

## Scope and evidence

The original CTC-006 backlog scope is party role, identifiers, snapshots, series, and correction/reference semantics. The approved CTC-003 detailed logical dictionary and historical SemanticDocument v1.0 / BillingDocument v0.3 are the design references. This exercise checks ten synthetic logical scenarios; it does not verify a live GitHub revision, real-world authority messages, or legally permitted country workflows.

## Consolidated validation matrix

| ID | Scenario | Expected invariant | Executed outcome | Evidence limit |
|---|---|---|---|---|
| ID-01 | ERP party master changes after publication | Published PartySnapshot remains immutable | PASS | In-memory snapshot comparison |
| ID-02 | Multiple tax registrations for one party | Distinguish scheme, jurisdiction and value | PASS | Synthetic identifiers |
| ID-03 | Same invoice number, different issuers | Commercial identities remain distinct | PASS | Candidate composite identity key |
| ID-04 | Same issuer/number, different series | Series can disambiguate when applicable | PASS | Series applicability profile-governed |
| ID-05 | Draft receives published number | Stable platform identity, publication owns assertion | PASS | Simplified draft/publication instance |
| ID-06 | Credit note references original invoice | Separate documents, typed CREDITS relationship | PASS | No legal workflow validation |
| ID-07 | Corrective replacement | Original retained; typed REPLACES relationship | PASS | Jurisdiction-specific validity unknown |
| ID-08 | Cancellation after clearance | Clearance evidence retained; cancellation appended | PASS | No authority cancellation evidence |
| ID-09 | Reference to external invoice not held locally | Preserve typed unresolved reference | PASS | No cross-system resolution exercised |
| ID-10 | Correction submitted twice | Distinct attempts, same correction identity | PASS | No external idempotency or retry protocol |

**Execution:** `python test_ctc006.py` produced 10/10 PASS; machine-readable output in `results.json`.

## Logical conclusions

1. Stable platform identity and revision-owned published commercial assertions can coexist without conflicting ownership.
2. Immutable party snapshots preserve historical identity information independently of mutable ERP party records.
3. Commercial identity uniqueness is namespace/profile-dependent, not a globally unique invoice number.
4. A credit note or replacement can be a separately identifiable legal document linked by a typed relationship, rather than an overwrite of the original revision.
5. Cancellation is not deletion: historical fiscal evidence and processing history remain available.
6. Unresolved external document references and repeat submission attempts do not require fabricated documents or revised billing content.

## Proposed CTC-006 constraints — not yet accepted

- **C006-01:** A commercial identifier is evaluated in an explicit identity namespace, potentially including issuer, document family, series and jurisdiction/profile; the exact uniqueness key is profile-governed.
- **C006-02:** Published party participation resolves to immutable snapshots; later ERP master changes cannot modify published facts.
- **C006-03:** Credit, replacement, adjustment and cancellation semantics use typed document relationships and/or compliance evidence, never implicit revision overwrites; legal admissibility is profile-governed.

These refine existing approved D2/D01/L principles but are not newly accepted detailed constraints.

## Material gaps and disposition

| Gap | Impact on CTC-006 scoped logical closure | Existing follow-up |
|---|---|---|
| Exact legal uniqueness namespaces by jurisdiction | Nonblocking; must be profile-defined | CTC-005 governance / CTC-010 evidence |
| Legally valid correction, cancellation and replacement workflows | Nonblocking for logical representation; no legal validity claimed | CTC-010, CTC-013 |
| Real source/response fixtures and external references | Nonblocking for structural scope | CTC-008, CTC-009, CTC-010, CTC-014 |
| Full dictionary-wide field/cardinality enforcement | Outside these focused tests | CTC-003 follow-up / CTC-009 |
| Physical keys and relational constraints | Outside logical scope | CTC-011 |

## Closure recommendation

**Recommend CTC-006 Done — scoped, subject to explicit user approval**, for party identity, immutable snapshots, document numbering namespace principles, and typed correction/reference representation. This is supported by 10 focused synthetic tests and accepted D2 architecture. It does **not** approve jurisdictional legal uniqueness rules, correction workflows, physical schema, or new field proposals.

## Session checkpoint

- Findings: Ten synthetic scenarios are structurally representable; no blocking contradiction found at the tested logical scope.
- Proposed decisions: C006-01 to C006-03 (Proposed).
- Decisions newly approved: None.
- Authoritative files changed: None; BACKLOG, DECISIONS, FINDINGS, MODEL-BASELINE, SESSION-LOG remain unchanged.
- Next action: User reviews scoped closure; on approval generate complete replacement Git-ready records. Next original backlog task CTC-007, model versioning and compatibility.
