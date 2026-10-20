# CTC-002 — Semantic Contract Consistency Test

**Date:** 2026-10-20  
**Status:** Completed conceptual consistency test; no architecture option approved  
**Approved constraints:** CTC-002-P1 through P7  
**Candidates:** A embedded; B independent; C hybrid; D2 uniform fiscal semantics with conditional interpretation lifecycle.

## Scope and evidence boundary

This is a deterministic, synthetic semantic-contract comparison. It does not establish tax-law compliance or validate actual XML/XSD fixtures. Source baseline: Global Semantic Billing Model v0.3, earlier SemanticDocument v1.0, CTC-002 ownership research and the 2026-10-20 approved principles. Current remote Git HEAD was not inspected. The original v0.3 model separates BillingDocument, FiscalContext, JurisdictionProfile, DocumentRepresentation and ComplianceTransaction, but does not settle aggregate roots/cardinalities.

## Controlled fixture F0

- Tenant `TEN-01`; document `DOC-001`, immutable revision `REV-001` (issued).
- Invoice `INV-2026-0042`, issue date `2026-10-20`, seller `Alpha Trading Ltd`, buyer `Beta Services Ltd`.
- Fictional `XCU`: net 1000.00, tax 100.00 (10%), payable 1100.00.
- Source XML/JSON artifact `REP-SRC-001`, content hash `HASH-SRC-001` (symbolic, not a computed cryptographic hash).
- Source-supplied classification `LOCAL-TAX-A`, scheme `XX-TAX-SCHEME`, source path `invoice.tax.localCategory`.
- Mapping `MAP-XX-1.0`, jurisdiction profile `XX-CTC-1.0`, code list `XX-TAX-1.0` derives normalized treatment `STANDARD`.
- Derived fact must point to source fact and exact rule/profile/code-list versions.
- A second version `XX-CTC-2.0` hypothetically maps the *same* original source classification to `SPECIAL`. This is a deliberate stress case, not a regulatory assertion.

## Canonical fact ledger (the comparison oracle)

| Fact ID | Meaning | Value | Authority | Provenance |
|---|---|---|---|---|
| BF-01 | Commercial number | INV-2026-0042 | REV-001 | REP-SRC-001 |
| BF-02 | Tax base | XCU 1000.00 | REV-001 | REP-SRC-001 |
| BF-03 | Tax amount | XCU 100.00 | REV-001 | REP-SRC-001 |
| SF-01 | Original local tax code | LOCAL-TAX-A | Frozen source fiscal fact | REP-SRC-001; source path; XX-TAX-SCHEME |
| IF-01 | Interpreted tax treatment | STANDARD | Interpretation under XX-CTC-1.0 | derivedFrom SF-01; MAP-XX-1.0; XX-TAX-1.0 |
| IF-02 | Reinterpreted treatment | SPECIAL | Interpretation under XX-CTC-2.0 | derivedFrom SF-01; distinct profile/rule versions |
| PR-01 | Original payload | REP-SRC-001 | Representation register | exact artifact reference |
| CT-01 | Submission operation | pending | Compliance transaction | references REV-001 + IF-01 + generated representation |

The ledger distinguishes semantic ownership from JSON nesting. `SF-01` must never be silently overwritten by IF-01 or IF-02. `IF-01` and `IF-02` are distinct derived facts, not competing authoritative source values.

## A — Embedded immutable FiscalContext

```yaml
billingDocument:
  id: DOC-001
  revisionId: REV-001
  documentNumber: INV-2026-0042
  tax: {base: '1000.00', amount: '100.00', currency: XCU}
  fiscalContext:
    sourceFacts:
      - {id: SF-01, scheme: XX-TAX-SCHEME, value: LOCAL-TAX-A, sourceRepresentationId: REP-SRC-001}
    derivedFacts:
      - {id: IF-01, treatment: STANDARD, derivedFrom: SF-01, profileVersion: XX-CTC-1.0, mappingVersion: MAP-XX-1.0}
```

**Version-2 test:** To retain IF-01 and add IF-02, A needs either (a) a separate immutable derived interpretation artifact linked to REV-001, which starts resembling B/C/D2, or (b) a new document revision, which wrongly implies changed commercial/source content. A can pass with a separately linked artifact, but pure single-snapshot A does not naturally express independently evolving interpretations. It is not *invalid*, but the extension must be explicit.

## B — Independent versioned FiscalContext

```yaml
billingDocument: {id: DOC-001, revisionId: REV-001, documentNumber: INV-2026-0042}
fiscalContexts:
  - id: FC-001
    sourceRevisionId: REV-001
    sourceFacts: [{id: SF-01, value: LOCAL-TAX-A, scheme: XX-TAX-SCHEME}]
    derivedFacts: [{id: IF-01, treatment: STANDARD, derivedFrom: SF-01, profileVersion: XX-CTC-1.0}]
  - id: FC-002
    sourceRevisionId: REV-001
    sourceFactsRef: FC-001/SF-01
    derivedFacts: [{id: IF-02, treatment: SPECIAL, derivedFrom: SF-01, profileVersion: XX-CTC-2.0}]
```

**Version-2 test:** Naturally permits multiple interpretations, but requires explicit authoritative ownership of SF-01; copying `sourceFacts` into every fiscal context would breach P6 if independently mutable. References rather than copies are necessary.

## C — Hybrid intrinsic facts + independent fiscal interpretation

```yaml
billingDocument:
  id: DOC-001
  revisionId: REV-001
  sourceFiscalFacts: [{id: SF-01, value: LOCAL-TAX-A, scheme: XX-TAX-SCHEME}]
fiscalInterpretations:
  - {id: FI-001, revisionRef: REV-001, derivedFacts: [{id: IF-01, treatment: STANDARD, derivedFrom: SF-01, profileVersion: XX-CTC-1.0}]}
  - {id: FI-002, revisionRef: REV-001, derivedFacts: [{id: IF-02, treatment: SPECIAL, derivedFrom: SF-01, profileVersion: XX-CTC-2.0}]}
```

**Version-2 test:** Clear source-fact ownership, independent derivations. But the boundary between intrinsic *source fiscal facts* and *jurisdictional source facts* remains ambiguous: is a locally coded source fact always embedded? If not, a governance rule is still required.

## D2 — Uniform interpretation contract, conditional lifecycle

```yaml
billingDocument:
  id: DOC-001
  revisionId: REV-001
  sourceFiscalFacts: [{id: SF-01, value: LOCAL-TAX-A, scheme: XX-TAX-SCHEME, sourceRepresentationId: REP-SRC-001}]
fiscalInterpretations:
  - id: FI-001
    sourceRevisionRef: REV-001
    sourceFactRefs: [SF-01]
    profileRef: XX-CTC-1.0
    derivedFacts: [{id: IF-01, treatment: STANDARD, derivedFrom: SF-01, mappingVersion: MAP-XX-1.0, codeListVersion: XX-TAX-1.0}]
```

**Version-2 test:** Create FI-002 with the same shape, profile XX-CTC-2.0 and IF-02; leave FI-001 and REV-001 untouched. A single interpretation is the default *cardinality in ordinary use*, not a different schema. Independence is a lifecycle capability, not a second JSON type. This means D2 is conceptually very close to C: it improves consistency but does not eliminate independent identity/version complexity.

## Semantic path crosswalk

| Concept | A | B | C | D2 | Uniform resolver target |
|---|---|---|---|---|---|
| Invoice number | billingDocument.documentNumber | billingDocument.documentNumber | billingDocument.documentNumber | billingDocument.documentNumber | billing.documentNumber |
| Source fiscal code | billingDocument.fiscalContext.sourceFacts[id] | fiscalContexts[id].sourceFacts[id] | billingDocument.sourceFiscalFacts[id] | billingDocument.sourceFiscalFacts[id] | fiscal.sourceFact(SF-01) |
| Derived treatment | billingDocument.fiscalContext.derivedFacts[id] | fiscalContexts[id].derivedFacts[id] | fiscalInterpretations[id].derivedFacts[id] | fiscalInterpretations[id].derivedFacts[id] | fiscal.interpretation(FI-001).fact(IF-01) |
| Profile version | embedded fact metadata | context metadata | interpretation metadata | interpretation metadata | fiscal.interpretation.profileRef |
| Source artifact | representation registry | representation registry | representation registry | representation registry | representation(REP-SRC-001) |
| Compliance status | separate transaction | separate transaction | separate transaction | separate transaction | compliance.transaction(CT-01) |

**Finding:** The first three architectures require an adapter/resolver if mappings must use the same logical path across all. D2 standardizes that resolver contract natively, but its underlying reference-resolution cost remains.

## Test assertions and results

Legend: **PASS** = represented without violating an approved principle in the illustrated contract; **CONDITIONAL** = requires an extra rule or extension; **NOT PROVEN** = cannot be established from a synthetic fixture.

| Assertion | A | B | C | D2 |
|---|---|---|---|---|
| T01 Same billing values and totals | PASS | PASS | PASS | PASS |
| T02 Preserve original local code | PASS | PASS | PASS | PASS |
| T03 P7 derivation and profile lineage | PASS | PASS | PASS | PASS |
| T04 P2 immutable issued revision | PASS | PASS | PASS | PASS |
| T05 P6 one owner for SF-01 | PASS | CONDITIONAL (avoid copies) | PASS | PASS |
| T06 Add FI-02 without changing REV-001 | CONDITIONAL | PASS | PASS | PASS |
| T07 Historical submission references FI-001 | CONDITIONAL | PASS | PASS | PASS |
| T08 Single common mapping path | CONDITIONAL (resolver) | CONDITIONAL (resolver) | CONDITIONAL (resolver) | PASS by design |
| T09 Multiple destinations sharing FI-001 | CONDITIONAL (explicit references) | PASS | PASS | PASS |
| T10 Real-world requirement for FI-02 | NOT PROVEN | NOT PROVEN | NOT PROVEN | NOT PROVEN |

**Important:** PASS is logical expressibility, not runtime or regulatory conformance. The D2 pass for T08 is definitional: uniformity is imposed by its proposed contract, not empirically demonstrated.

## Complexity assessment (qualitative)

- **A:** lowest conceptual footprint for one fixed interpretation; adding independent interpretations or historical re-evaluation forces extensions.
- **B:** most flexible but greatest risk of duplicated authoritative source facts and extra reference governance.
- **C:** clear separation of source facts from derived interpretations; ownership taxonomy remains necessary.
- **D2:** similar conceptual complexity to C; lowers mapping-contract variability by mandating one interpretation shape and stable resolvers. Does not remove versioning, identifiers, or reference resolution.

## Proposed boundary rules for review (not accepted)

1. Every fiscal source fact has one authoritative owner and immutable provenance at publication.
2. Every derived fiscal fact references one or more source facts and exact mapping/profile/code-list versions; external enrichment sources are explicit.
3. Each compliance transaction references the exact billing revision, interpretation version (if used), and submitted representation.
4. No new fiscal interpretation is created solely for a different serialization, transport channel, or retry.
5. An independent interpretation is created only for materially different semantic derivation or separately reproducible interpretation history.
6. A shared resolver path must never obscure whether a value is original or derived.

## Decision recommendation

**Keep C and D2 as the most promising candidates, with D2 preferred for further contract prototyping, not accepted.** A remains viable with additional history/interpretation machinery; B remains viable with strict no-duplication governance. D2 does **not** eliminate aggregate complexity; it constrains it behind a uniform semantic interface. Its added value is consistency of semantic paths, provenance, and version references, rather than reduced entity count.

The key unresolved discriminator is an independently verified real-world case where one immutable source billing revision requires more than one materially different fiscal interpretation. No such fixture was validated in this test. Do not mark CTC-002 Done or begin approved CTC-003 entity cardinalities.

## Checkpoint and Git update recommendation

- **CTC-002:** Review/evidence-gated; P1–P7 accepted, no new ADR.
- **F-002-41 (proposed):** D2 uniform resolver contract reduces path variability but not reference/version complexity; conceptual test only.
- **F-002-42 (proposed):** A cannot naturally preserve independent re-interpretations without additional artifact/history mechanism.
- **F-002-43 (proposed):** C and D2 express source/derived separation consistently; D2 is a more explicit interface discipline than a materially new domain partition.
- **F-002-44 (proposed):** No country requirement for multiple interpretations was proven by synthetic fixture.
- **Files:** Add this report under `research/CTC-002/`; do not modify accepted decisions or MODEL-BASELINE until reviewed. Proposed findings may be incorporated into full replacement files at next approved checkpoint.
