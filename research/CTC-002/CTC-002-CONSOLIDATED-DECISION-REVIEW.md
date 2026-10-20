# CTC-002 — Consolidated Logical Contract Decision Package

**Date:** 2026-10-20  
**Status:** Decision-ready proposal, **not an approved final architecture**  
**Scope:** Semantic aggregate boundaries, D2 logical contract and cross-format evidence. Database design and application implementation remain out of scope.

## Executive recommendation

**Recommend conditional closure of CTC-002 at the logical-contract level only, subject to explicit user approval of the D2 logical contract and I-01..I-10 invariants.** The physical FiscalContext choice (A embedded, B independent, C hybrid) should remain a documented, explicitly deferred design decision. If CTC-002 acceptance criteria are interpreted as requiring final aggregate-root ownership and cardinalities, keep the task in **Review** rather than Done. The current package does not itself change the task to Done.

This recommendation is based on controlled structural and semantic tests, not full authority conformance. We have not demonstrated a real requirement for multiple independently evolving fiscal interpretations of the same published revision. Absence of a demonstrated example is **not** proof that none exists.

## 1. Governance and exact approvals

The user explicitly accepted **CTC-002-P1..P7** at architectural principle level. Their scope is preserved in `DECISIONS.md`:

| ID | Accepted principle | Exclusion |
|---|---|---|
| P1 | Billing meaning separate from compliance processing | No specific service/table boundary approved |
| P2 | Preserve immutable published revisions | Publication boundary remains unspecified |
| P3 | Preserve original and generated representations | Storage technology and retention policy unresolved |
| P4 | Distinguish fiscal and submission identity | Identifier catalogue/cardinality not approved |
| P5 | Maintain independent compliance histories | Event store implementation not approved |
| P6 | One authoritative semantic owner per concept | Detailed entity/field dictionary not approved |
| P7 | Distinguish source-supplied from inferred/enriched/derived facts with provenance and effective profile versions | Provenance schema and storage not approved |

**D2:** User said "D2 validated" following the controlled replay prototype; previous session treated this as acceptance of D2 *logical design direction*. It is **not** explicit acceptance of the subsequent full I-01..I-10 formal contract or any physical aggregate structure. Those remain proposed for approval.

**Historical ADRs:** unchanged. A/B/C remain deferred. D2 is a logical contract/interface proposal, not a fourth approved physical layout.

## 2. Formal D2 logical semantic contract

Authoritative detailed candidate specification: `CTC-002-D2-FORMAL-LOGICAL-CONTRACT.md` (included).

| Logical concept | Core meaning | Ownership/invariant |
|---|---|---|
| BillingDocument | Stable commercial document identity | Not authority or transmission ID |
| PublishedRevision | Immutable commercial and intrinsic tax facts | Frozen revision and fingerprint |
| SourceFiscalFact | Source value, code scheme, source artifact/path | Source facts never silently replaced |
| FiscalInterpretation | Evaluated meaning under a specific profile package | Pins exact revision and package; cardinality unapproved |
| DerivedFiscalFact | Value plus inputs, derivation type, rules and profile | Distinct from source assertions |
| ProfilePackage | Rule/mapping/code-list identities, versions and fingerprint | Must be immutable for reproducible replay |
| DocumentRepresentation | Source/generated/submitted/certified artifact | Exact bytes and hash traceable |
| ComplianceTransaction | Destination obligation and processing history | Separate from commercial meaning |
| FiscalIdentity/Evidence | Typed externally assigned identities, receipts and seals | References exact artifact/operation |

### Formal candidate invariants I-01 through I-10

1. **I-01:** Every interpretation pins exact published revision and fingerprint; evaluation never mutates it.
2. **I-02:** Each source fact has one authoritative owner and preserves source artifact/path.
3. **I-03:** Derived facts cite input fact IDs, rule/profile/code-list versions; external enrichment needs captured inputs and timing.
4. **I-04:** Submission pins interpretation and representation; mutable `latest` is insufficient.
5. **I-05:** Profile packages must be immutable/content-identifiable; labels alone cannot guarantee replay.
6. **I-06:** Derived classifications never overwrite source classifications; disagreement is explicitly modeled.
7. **I-07:** Status/receipts/retries never mutate billing or interpretation facts.
8. **I-08:** Syntax/profile identifiers belong to representation or processing, not commercial identity.
9. **I-09:** Monetary precision and arithmetic are validated per target profile; avoid a universal two-decimal rule.
10. **I-10:** Semantic validity and legally valid target representability are separate validation gates.

These are **proposed formal invariants**. P1..P7 support their intent but do not constitute prior approval of their exact wording.

## 3. Accumulated test and evidence matrix

| Evidence family | Fixture type | Reported focused result | Demonstrated | Not demonstrated |
|---|---|---|---|---|
| D2 fictional two-profile replay | Synthetic JSON/rules | 7 checks reported passed | Stable source revision, two derived interpretations, hashes under a toy rule engine | Actual historical rule archive or real mandate change |
| D2 four-option consistency comparison | Synthetic invoice | 10 logical assertions, comparative | Interface/path tradeoffs of A/B/C/D2 | Runtime/regulatory correctness or mandatory independent fiscal lifecycle |
| Peppol BIS Billing 3.0 May 2026 | Constructed UBL XML with published paths | 8/8 focused checks | XML extraction, selected arithmetic, source/derived separation | Full UBL XSD, Schematron, network acceptance, complete tax correctness |
| Mexico CFDI 4.0 | Constructed XML with published SAT field names | 12/12 focused checks | Source fiscal codes, fractional tax-rate normalization, totals, revision reference | SAT XSD/catalogs, signature validity, PAC timbrado, certified pair |
| Malaysia MyInvois | Simplified JSON **not official UBL submission syntax** | 11/11 focused checks | Concept-level tax type/source/derived separation | Official MyInvois UBL payload conformance, LHDN response/signature |
| India GST IRP interstate | Partial constructed IRP-shaped JSON | 11/11 focused checks | IGST component and illustrative arithmetic, provenance | Full IRP schema, real legal determination, signed IRN/QR |
| India GST IRP intrastate | Partial constructed IRP-shaped JSON | 11/11 focused checks | CGST/SGST component split, provenance | Full IRP schema, real legal determination, signed IRN/QR |
| Italy SdI | Documentation-based response review | No executed paired XML | Separate issuance, delivery and rejection concepts | Matched FatturaPA + SdI response validation |
| France Extended CTC | Internal v0.3 worked example | Contributing sum EUR 21,220.81 | Group/detail non-additivity, signed values, conceptual ownership | Official XML/profile/XSD validation |
| Brazil NF-e | Bounded documentation/example review | No executed full fixture | Need for concurrent taxes and local classification | Real signed authorization sequence and full field mapping |

**Interpretation:** Focused check counts cover different assertions and cannot be summed into a meaningful conformance score. Malaysia/India's 33/33 represents three synthetic cases, not 33 jurisdictional validations. The country sources and scope limitations are documented in the included individual reports.

## 4. FiscalContext option assessment

| Option | Benefit | Unresolved issue | Decision |
|---|---|---|---|
| A embedded immutable | Simpler single-document ownership | Multiple independent interpretations may need extra snapshots/references | Deferred |
| B independently versioned | Strong independent lifecycle | Risk of duplicating intrinsic fiscal facts | Deferred |
| C hybrid | Shared facts + versioned local interpretation | Strict authoritative-owner governance required | Deferred |
| D2 logical contract | Uniform interface, exact provenance/version references | Does not eliminate independent lifecycle complexity or decide physical embedding | Leading logical design, detailed contract pending approval |

**Important:** One invoice sent to two destinations, or two different serialized formats, is not by itself proof of two different fiscal interpretations. Likewise, a new fiscal UUID or SdI notification belongs to evidence/processing rather than automatically requiring a new FiscalContext.

## 5. Remaining decisions and evidence gates

| Gate | Required for | Current evidence | Suggested disposition |
|---|---|---|---|
| G1: Approve I-01..I-10 and logical concept boundaries | Logical CTC-002 closure | Proposed, tested in part | **Ask user to approve** |
| G2: Define publication/freeze boundary | Full invariant and correction semantics | Conceptual only | Carry explicit open question into CTC-003/CTC-006, or keep CTC-002 Review |
| G3: Physical FiscalContext A/B/C, identity/cardinality | Physical aggregate/relational design | No real discriminator | Defer to later model/relational design with stated condition |
| G4: Genuine CFDI pre/post PAC certification pair | Fiscal identity and certified representation proof | Documentation and constructed pre-stamp XML only | Evidence backlog |
| G5: FatturaPA and SdI notification pair | Processing-event fidelity | Documentation only | Evidence backlog |
| G6: Official French Extended CTC XML + profile/XSD | Structural/regulatory representability | Internal worked example only | Evidence backlog |
| G7: Real MyInvois UBL and IRP-complete signed response | Cross-country syntax and evidence | Simplified/partial fixtures | Evidence backlog |
| G8: Two materially different fiscal interpretations for one revision | Justify mandatory independent FiscalContext | Not demonstrated | Explicit design discriminator; avoid mandatory B/C without evidence |
| G9: Archived rule/code-list/profile packages | Production historical reproducibility | Toy replay; unarchived profiles in newer tests | Required before production assurance |

## 6. Recommended decision and closure route

**Recommended route: two-stage closure.**

**Stage 1 (now, subject to explicit user approval):** Accept D2 as the **logical semantic contract** and I-01..I-10 as **logical invariants**, not as a final schema. Record FiscalContext A/B/C as Deferred. CTC-002 can be marked **Done — logical boundaries agreed; physical cardinalities/evidence deferred** *only if* the user explicitly agrees to refine the CTC-002 acceptance criterion to logical boundaries, and the deferred work is assigned named backlog owners/tasks. Otherwise retain **Review / evidence-gated**.

**Stage 2 (future):** Resolve aggregate root/cardinality and physical representation after representative real fixtures, during CTC-003/CTC-011 as appropriate. Do not infer a universal requirement for independent interpretations from synthetic two-profile tests.

**Current status: Review, not Done.** No new ADR is accepted by this package. CTC-003 is not automatically started.

## 7. Explicit approval request

For user review:

1. Do you approve the **D2 formal logical contract**, with the nine concepts above, as the conceptual baseline for CTC-003 (names/cardinalities subject to refinement)?
2. Do you approve proposed **I-01..I-10** as logical invariants, with detailed implementation deferred?
3. May CTC-002 be marked **Done at logical-boundary level**, with physical A/B/C and listed fixture/evidence gates explicitly carried into backlog, or should it remain Review until all gates are met?

Do not interpret silence or prior "D2 validated" as affirmative answers to these three questions.

## 8. GitHub handoff

This package includes **complete replacement versions** of affected project registers, not append fragments. It retains the seven approved principles and marks new findings and invariants as proposed. The GitHub repository has not been modified by this package. Review `git diff` before committing. Original reference artifacts already in GitHub need not be replaced.
