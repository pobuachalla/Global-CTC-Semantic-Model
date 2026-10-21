# CTC-007 — Semantic Model Versioning and Compatibility — Decision Candidate v0.1

**Date:** 2026-10-21  
**Status:** PROPOSED — not accepted; CTC-007 In Progress  
**Evidence:** Approved CTC-006 full repository snapshot (2026-10-21), `BACKLOG.md`, `DECISIONS.md`, `MODEL-BASELINE.md`, `MASTER-PROMPT.md`, CTC-005 governance and CTC-003 scoped dictionary. Live GitHub HEAD **not verified**.

## Scope and dependencies

CTC-007 original acceptance: versioning rules, breaking-change policy and compatibility test plan. Depends on CTC-003 approved scoped logical dictionary and JP-01..JP-10 immutable profile governance. Does not approve new fields, physical schemas, country rules, API contracts, or alter D2.

## Candidate contract — V-01 through V-10 (all Proposed)

| ID | Proposed rule |
|---|---|
| V-01 | Core semantic contract, jurisdiction profile, source/target mapping, rules, code lists, external API contract and representation format each carry independent version identifiers. |
| V-02 | Semantic meaning, units, ownership and identifier scope are part of a canonical path's compatibility contract; unchanged path spelling does not imply compatibility. |
| V-03 | Adding an optional field without changing existing interpretation is backward compatible; new universal required fields, changed types/units, removed paths or changed cardinality are breaking by default. |
| V-04 | A jurisdiction-specific change is profile-scoped unless it alters canonical semantic meaning; no automatic core version bump. |
| V-05 | Published revisions and fiscal interpretations pin exact contract version and content-addressed applicable dependencies; no implicit latest resolution. |
| V-06 | Historical artifacts and input manifests remain resolvable across migrations; old published revisions are not rewritten to conform to new schema. |
| V-07 | Breaking changes require a new major core contract version, documented migration/dual-read strategy, impact assessment and ADR approval. Version numbers are proposed SemVer-style conventions, not a physical implementation decision. |
| V-08 | Compatible additions require regression tests and documented reader/writer expectations; tolerant readers may preserve unknown fields but must not infer their semantics. |
| V-09 | Release promotion requires evidence, explicit compatibility classification, rollback plan and preserved prior package availability. |
| V-10 | API response/projection compatibility is assessed independently of core model compatibility; legal state remains evidence-governed. |

## Compatibility decision table

| Change | Candidate classification | Consequence |
|---|---|---|
| Optional semantic attribute with unchanged meaning | Compatible | Minor candidate revision; reader tests |
| Required field on all existing published revisions | Breaking | New major; migration/dual-read decision |
| Canonical path rename with no alias | Breaking | Explicit migration/alias policy |
| Tax rate changes from percent to fraction | Breaking | Unit semantics change; new major |
| New jurisdiction extension | Profile-scoped | Govern namespace and effective dating |
| Profile rule/code-list change | Profile-scoped or breaking within profile | Pin old package and evaluate consumers |
| Old code-list value removed | Breaking for affected readers/data | Preserve historical meaning and old list |
| Client status projection change | API/interface review | No automatic core model bump |

## Deterministic test evidence

12 policy classification assertions were executed using a deliberately simple reference classifier. These test the **proposed classification table**, not an independent semantic-schema compatibility checker. All 12 pass. Source-specific country behavior and live registry rollback are not tested.

## Material gaps and disposition

1. A machine-readable canonical path registry and compatibility checker are implementation work; not a blocker to scoped logical policy approval.
2. Core-versus-API version negotiation, mixed-version consumer migration and semantic path aliases require a documented implementation design; track in CTC-016/CTC-018.
3. Historical replay with archived dependency bytes remains CTC-002-FU03; JP-01/02/09 principles already accepted.
4. No regulatory fixture evidence is claimed; CTC-008/009/010 remain open.

## Closure recommendation

**Recommend CTC-007 Done — scoped only after explicit user approval of V-01..V-10**, limited to logical versioning and compatibility governance. Preserve all existing accepted decisions, the 18 proposed CTC-003 fields, and deferred physical FiscalContext A/B/C. Do not close on synthetic checks alone without approval.

## Checkpoint

- Findings: versioned semantic meaning and units are essential; independent version domains avoid unnecessary core churn; old revision replay requires pinned packages.
- Proposed ADR: CTC-007-V01..V10, all Proposed.
- User-approved this session: none.
- Suggested authoritative updates after approval: `BACKLOG.md`, `DECISIONS.md`, `MODEL-BASELINE.md`, `FINDINGS.md`, `SESSION-LOG.md`.
- Next task: approve/refine V-01..V-10; then CTC-008, repository fixture inventory.
