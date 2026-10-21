# CTC-005 — Bounded Governance Test and Closure Review

**Date:** 2026-10-21  
**Status:** Tests completed; JP-01..JP-10 proposed, not approved.  
**Source:** `CTC-005-JURISDICTION-PROFILE-GOVERNANCE-DECISION-CANDIDATE.md` (2026-10-21).  
**Baseline:** CTC-001/002/003/004 Done — scoped, based on available local project snapshot; live GitHub HEAD not verified.

## Execution

`python test_governance.py` — **7 of 7 assertions passed**. See `results.json` for expected and actual outcomes.

| Test | Expected | Result | Scope |
|---|---|---|---|
| Overlap without precedence | AMBIGUOUS | Pass | Synthetic date-window selection |
| Missing date basis | NOT_EVALUABLE | Pass | Explicit absence of `issueDate` |
| Profile v2 changes mapping | v1 result unchanged | Pass | Versioned immutable *in-memory* package mapping and digest; no archival replay |
| Existing canonical field extension | Reject redundant extension | Pass | Exact known-field match |
| Unknown local code | Preserve original, unresolved derived | Pass | No implicit code coercion |
| Authority response ID in billing core | Reject wrong owner | Pass | Exact invalid path check |
| Reusable concept proposed for core | ADR/migration required | Pass | Governance routing, not actual ADR execution |

## Coverage against JP proposals

- **Directly exercised in simplified form:** JP-03, JP-04, JP-05, JP-07, JP-10.
- **Partially exercised:** JP-01/02 (content digest and pinned mapping, not durable package/archive/dependency verification); JP-06 (redundancy branch only); JP-08 (ownership rejection, not complete artifact/legal-state preservation).
- **Not directly exercised:** JP-09 (promotion regression suite and rollback). JP-06 namespace/type/provenance completeness also remains untested.

## Material gaps before recommending full scoped closure

1. Test a **published package manifest** with immutable digest and all rule/mapping/code-list dependencies, including tampering rejection (JP-01/02).
2. Test **extension registration completeness** (namespace, owner, type, applicability, provenance, evidence) and explicit rejection of incomplete contracts (JP-06).
3. Test **promotion and rollback metadata**, verifying that existing interpretations remain pinned (JP-09).
4. Test **artifact and legal-state separation** when profile validation succeeds but no authority response exists (JP-08).

These are four tightly bounded governance checks, not new architectural workstreams. No official country fixture validation is required for the *logical governance* closure, but remains a separate evidence task.

## Recommendation

**Move CTC-005 to Review, not Done.** The seven initial scenarios pass and the seven-part decision tree is coherent, but JP-01..JP-10 have not been explicitly approved and four direct logical test gaps remain. Complete the four bounded checks, then request one approval for the decision tree and JP-01..JP-10 at logical-governance scope only.

## Decision preservation

D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10, approved batch/C09/G2 decisions and the scoped CTC-003 dictionary remain unchanged. The 18 supplemental field contracts, physical FiscalContext A/B/C and jurisdictional conformance remain deferred. No authoritative project register or GitHub repository was modified.
