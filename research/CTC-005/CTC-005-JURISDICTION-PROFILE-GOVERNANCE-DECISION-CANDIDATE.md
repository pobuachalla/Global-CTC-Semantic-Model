# CTC-005 — Jurisdiction Profiles and Extension Governance

**Date:** 2026-10-21  
**Status:** Proposed for review; CTC-005 In Progress  
**Basis:** 2026-10-21 CTC-004 approved scoped snapshot; `semantic-billing-model(1).md` §§2, 9–10; approved D2 and CTC-003 logical dictionary. No live GitHub checkout verified.

## Scope and acceptance
Design a reusable extension decision tree, applicability and validation policy, versioning boundaries and promotion criteria. Do **not** reopen D2, approve Draft 4.2's 18 candidate fields, define physical FiscalContext storage, or certify national tax rules. CTC-007 owns global model compatibility policy; CTC-009/010 own broad sample coverage.

## Proposed logical profile contract

| Concept | Proposed mandatory identity/metadata | Semantics and constraints |
|---|---|---|
| JurisdictionProfile | profileId, profileVersion, jurisdiction, regime, effectiveFrom, packageDigest | Defines scope and applicable constraints; `effectiveTo` optional, exclusive when present; lifecycle status draft/review/published/retired |
| ApplicabilityPredicate | document family, seller/buyer role/location, transaction date basis, scope dimensions | Evaluated against pinned source facts and rule version; unresolved inputs return INDETERMINATE rather than guessing |
| RulePackage | ruleId, version, digest, dependencies | Immutable once published; semantic, profile and cross-field rules distinct from syntax checks |
| CodeListBinding | scheme, issuer, version/digest, effective interval | Preserve original local code and scheme; no undocumented coercion |
| MappingPackage | mappingId, version, digest, input/output family | Explicitly pin mapping and source/target format version; source facts not overwritten |
| JurisdictionExtension | namespace, conceptId, meaning, type, cardinality, owner, version | Only for genuine local meaning; must include validation, provenance, source representation references |
| ProfileEvaluation | exact document revision, profile package digest, evaluatedAt, rule outcomes | Derived evaluation; never legal issuance merely from validation success |

These are **contract candidates**, not newly approved entities or attributes. They may be realized as value objects or references in the existing D2 model.

## Decision tree — apply in order

1. **Existing canonical fact?** Map to approved D2 field and preserve source provenance.
2. **Only tighter requirement or local code-list?** Put constraint in the profile, not the core.
3. **Reusable new semantic meaning across jurisdictions?** Propose core enhancement through separate review; do not silently change accepted dictionary.
4. **Genuinely local semantic fact?** Add governed namespaced extension with typed contract and owner.
5. **Representation/serialization metadata?** Own in DocumentRepresentation/MappingPackage.
6. **Submission, routing, fiscal evidence or status?** Own in compliance/representation/evidence domains, never in billing core.
7. **Ambiguous or insufficient evidence?** Preserve source artifact and flag UNRESOLVED; do not infer compliance.

## Proposed governance invariants

- **JP-01** A published profile package is immutable and content-addressable.
- **JP-02** Every interpretation pins an exact applicable profile package, mapping/rule/code-list dependencies and input manifest.
- **JP-03** Profile effective date evaluation names the date basis (issue, tax point, supply or other), with no universal default.
- **JP-04** Overlapping applicable profiles require explicit precedence or produce AMBIGUOUS, never silent latest-version selection.
- **JP-05** Profile rules may constrain but not overwrite authoritative source facts.
- **JP-06** Extensions require namespace, owner, typed meaning, applicability, provenance and test evidence.
- **JP-07** Extension-to-core promotion requires cross-jurisdiction reuse evidence, semantic equivalence, migration mapping and explicit ADR approval.
- **JP-08** Original and outbound artifacts remain preserved; validation and legal-state assessments remain distinct.
- **JP-09** Profile release promotion requires regression evidence and a documented rollback path; past interpretations remain pinned.
- **JP-10** Unavailable or conflicting applicability inputs produce explicit NOT_EVALUABLE / AMBIGUOUS outcomes, not acceptance.

All JP-01..JP-10 are **Proposed**.

## Decision examples (illustrative; no legal validation)

| Scenario | Expected classification | Why |
|---|---|---|
| Mexico CFDI source `UsoCFDI` | Source fiscal fact / governed local code | Preserve original code and scheme; profile validates applicability |
| Italy FatturaPA `Natura` | Source code + derived treatment | Local classification retained; normalized meaning derived with pinned rule |
| France profile requires a field conditionally | Profile constraint | Does not require a new core entity |
| Malaysia MyInvois UBL syntax | Distinct profile and mapping package | UBL serialization alone does not imply Peppol rules |
| India GST IGST vs CGST/SGST | Source tax applications + profile interpretation | Source tax amounts remain authoritative; tax-rule inference requires evidence |
| Authority-issued UUID or response ID | Fiscal identity/evidence or compliance reference | Never use unqualified invoice identifier |

## Proposed validation levels

1. Source syntax/schema validation.
2. Canonical semantic structural validation.
3. Jurisdiction-profile applicability and semantic constraints.
4. Target-format serialization validation.
5. External authority response and legal-state assessment (separate lifecycle).

Validation findings must preserve level, rule/version, subject, severity, source reference and evaluation outcome.

## Bounded acceptance test plan

| Test | Expected outcome |
|---|---|
| Two published profiles overlap without precedence | AMBIGUOUS |
| Applicable date-basis missing | NOT_EVALUABLE |
| Profile v2 changes code mapping | Historical v1 interpretation unchanged |
| Local requirement already supported in core | Extension request rejected as unnecessary |
| Local source code unknown to mapping | Source code preserved, derived value unresolved |
| Response/authority identifier offered as billing field | Ownership validation rejects |
| New reusable concept proposed for core | ADR and migration review required |

## Decision request and closure

**Recommended default:** Accept the seven-part decision tree and JP-01..JP-10 at logical-governance level *after review*, without accepting physical implementation or country rules. CTC-005 should remain **In Progress** until these rules are reviewed and the bounded tests run. No approval is inferred from this document.

## Dependencies / deferred evidence

- CTC-007: model/profile version compatibility and breaking-change policy.
- CTC-008/009/010: verified fixture corpus, mapping coverage and jurisdictional evidence.
- CTC-002-FU01..05: physical aggregation, full profile replay and country-specific legal states.
- CTC-003: 18 proposed additional field contracts remain proposed.

## Session checkpoint

**Findings:** Existing source supports profile constraints, reuse-before-extension and namespace governance. Proposed package identity, precedence, effective-date basis and validation-level rules need approval.  
**Approved decisions this session:** None.  
**Files:** BACKLOG, SESSION-LOG updated to record start only; DECISIONS, MODEL-BASELINE and FINDINGS unchanged.  
**Next:** Review proposed JP rules and run seven bounded tests; seek scoped CTC-005 closure only afterward.
