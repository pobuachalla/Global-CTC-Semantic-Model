# Research Findings and Evidence Register

No external repository samples have yet been inventoried or verified as part of this starter pack.

| Finding ID | Task | Finding | Evidence | Confidence | Implications | Status |
|---|---|---|---|---|---|---|
| F-001 | CTC-001 | Earlier SemanticDocument specification treats document control and format-native fields as part of the pivot | CTC-Semantic-Document-Entity-Model.docx, sections 10–12 | High (source-derived) | Compare with separated fiscal/process aggregates | Pending review |
| F-002 | CTC-001 | Newer BillingDocument v0.3 explicitly separates billing semantics, fiscal context and compliance transaction | semantic-billing-model(1) (1).md, sections 3, 8, 11 | High (source-derived) | Model boundary decision needed | Pending review |
| F-003 | CTC-001 | Newer v0.3 includes French grouped/detail lines, signed amounts and line-specific participants | semantic-billing-model(1) (1).md, section 12.2 | High (source-derived) | Compare against earlier line cardinality and tax validation | Pending review |

For new findings, record direct evidence separately from inference. Use `Unknown` when evidence is missing; never silently treat repo examples as legally valid.

## CTC-002 — Instance-level lifecycle simulation (2026-10-19)

The following findings result from a **synthetic, fictional-jurisdiction (XX)** lifecycle simulation covering issuance, clearance, rejection, correction and cancellation. These are architectural inferences, not verified jurisdictional mandates or validated repository fixtures. All are pending review.

| Finding ID | Task | Finding | Evidence | Confidence | Implications | Status |
|---|---|---|---|---|---|---|
| F-002-11 | CTC-002 | Legal document corrections and internal document revisions are distinct operations. | Synthetic lifecycle: original DOC-001/REV-001 retained; corrective credit note DOC-002 with CREDITS relationship. Supported conceptually by Semantic Billing Model v0.3 sections 4.21 and 6.2. | High (conceptual); jurisdiction-specific procedures unverified | Model distinct revision and document-relationship semantics. | Pending review |
| F-002-12 | CTC-002 | Clearance and cancellation can be recorded without mutating original commercial content. | Synthetic lifecycle: REV-001 and original EVD-001 retained while clearance/cancellation events and EVD-002 are added. | High (conceptual); jurisdiction-specific procedures unverified | Preserve historical artifacts and separate legal-state projection from document content. | Pending review |
| F-002-13 | CTC-002 | Compliance operations, submission attempts, processing events and fiscal evidence require distinguishable identities in the candidate design. | Synthetic CT-001, ATT-001, EVT-002 and EVD-001 instances; Semantic Billing Model v0.3 section 11 distinguishes compliance processing. | High (architectural inference) | Define correlation, identity and lifecycle boundaries; do not assume separate physical tables. | Pending review |
| F-002-14 | CTC-002 | A simple clearance lifecycle does not prove FiscalContext must be independent: embedded immutable snapshots and independent/hybrid approaches all accommodate it. | Comparison of embedded A, independent B and hybrid C against the same synthetic lifecycle. | High (within conceptual simulation) | Keep all three options under consideration. | Pending review |
| F-002-15 | CTC-002 | Multi-jurisdiction interpretation and reproducibility of historical profile versions are stronger discriminators among fiscal-context designs. | Conceptual multi-destination scenarios; Relational Model v0.3 section 22 (historical profile linkage). No validated real-world multi-jurisdiction fixtures. | Medium (inference; requires payload validation) | Test actual fiscal attributes and profile versions before selecting aggregate ownership. | Pending evidence |
| F-002-16 | CTC-002 | Each fiscal semantic concept should have one authoritative owner even if other aggregates reference or project it. | Conceptual ownership analysis of BillingDocument, FiscalContext and FiscalEvidence; risk of duplicated inconsistent fiscal facts. | High (design principle, not regulatory fact) | Establish field-level ownership matrix and rules for derived projections. | Pending review |

## CTC-002 — Cross-country evidence and France closeout (2026-10-19)

**Status:** All entries below are proposed/pending review. Mexico and Italy are documentation-based reviews; France is a documented internal example and arithmetic check, not raw fixture validation.

| Finding ID | Task | Finding | Evidence | Confidence | Implications | Status |
|---|---|---|---|---|---|---|
| F-002-17 | CTC-002 | Separate commercial/fiscal/process field ownership is viable as a classification method | CTC-002-FISCAL-FIELD-OWNERSHIP-MATRIX.md | Medium (candidate classification) | Review ownership per field | Pending review |
| F-002-18 | CTC-002 | One source field may express both document kind and local fiscal subtype | Ownership matrix FO-03/FO-18 | Medium (mapping inference) | Map concepts separately without uncontrolled duplication | Pending review |
| F-002-19 | CTC-002 | Representation metadata is distinct from commercial identity | Ownership matrix FO-20/FO-21 | High (source-derived) | Preserve format/profile/version on artifacts | Pending review |
| F-002-20 | CTC-002 | External fiscal identity ownership remains unresolved despite evidence classification | Ownership matrix FO-22/FO-23 | Medium | Test legal identity against certified artifact | Pending review |
| F-002-21 | CTC-002 | Certified CFDI contains fiscal stamp structure in addition to original invoice content | CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md; SAT references therein | High (documentation-backed) | Separate certified representation from original | Pending review |
| F-002-22 | CTC-002 | CFDI fiscal UUID and certification timestamp are not supplier commercial number | CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md | High (documentation-backed) | Typed identity and certification evidence | Pending review |
| F-002-23 | CTC-002 | Preserving both pre- and post-certification representations supports traceability | CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md | High (architecture inference) | Immutable representation identity | Pending review |
| F-002-24 | CTC-002 | Available CFDI demonstration examples are not verified cryptographically valid paired fixtures | CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md | High (evidence gap) | Do not claim actual round-trip validation | Pending review |
| F-002-25 | CTC-002 | CFDI certification evidence alone does not select fiscal-context cardinality | CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md | High (conceptual) | Retain A/B/C | Pending review |
| F-002-26 | CTC-002 | Italian issuance and recipient delivery must be modeled separately | CTC-002-ITALY-SDI-RESPONSE-EVIDENCE.md | High (documentation-backed) | Multidimensional lifecycle | Pending review |
| F-002-27 | CTC-002 | SdI scarto should be recorded without erasing submitted artifact | CTC-002-ITALY-SDI-RESPONSE-EVIDENCE.md | High (documentation-backed) | Preserve rejected representation and response | Pending review |
| F-002-28 | CTC-002 | SdI file/process identity differs from invoice business identity | CTC-002-ITALY-SDI-RESPONSE-EVIDENCE.md | High (documentation-backed) | Separate external identifiers | Pending review |
| F-002-29 | CTC-002 | Recipient response event types depend on SdI workflow (e.g. B2G) | CTC-002-ITALY-SDI-RESPONSE-EVIDENCE.md | High (documentation-backed) | Profile-specific event types | Pending review |
| F-002-30 | CTC-002 | SdI notifications support separate event ownership but not independent fiscal context by themselves | CTC-002-ITALY-SDI-RESPONSE-EVIDENCE.md | High (conceptual) | Retain A/B/C | Pending review |
| F-002-31 | CTC-002 | French documented group/detail example reconciles to EUR 21,220.81 when noncontributing detail is excluded | CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md §2; Semantic Billing v0.3 §18.5 | High (internal example; not mandate verification) | Retain line contribution semantics | Pending review |
| F-002-32 | CTC-002 | Signed values, hierarchy and line parties are reusable billing semantics | CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md §3 | High (conceptual) | Keep in core | Pending review |
| F-002-33 | CTC-002 | Tax-point meaning may be shared while local exigibility mapping remains profile-specific | CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md §3 | Medium (ownership unresolved) | Test actual code and profile mapping | Pending review |
| F-002-34 | CTC-002 | UBL syntax/profile identifiers belong to representation provenance | CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md §3 | High (source-derived) | Keep outside commercial identity | Pending review |
| F-002-35 | CTC-002 | French test does not prove independent FiscalContext versioning | CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md §5 | High within conceptual test | Keep A/B/C under investigation | Pending review |


## CTC-002 — Bounded extended research (2026-10-20)

**All entries below are proposed, not accepted.** See `research/CTC-002/CTC-002-EXTENDED-FISCAL-OWNERSHIP-REVIEW.md`.

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F-002-36 | Local source code remains source-supplied even if jurisdiction-specific | v0.3 and P7 conceptual analysis | Pending review |
| F-002-37 | Format profile identifiers belong to representation provenance | OpenPeppol May 2026 | Pending review |
| F-002-38 | Brazil multi-tax semantics do not prove FiscalContext multiplicity | Public NF-e XSD/examples; inference | Pending review |
| F-002-39 | French 2026 external specifications require profile-specific fixture checks | impots.gouv.fr v3.2 | Pending review |
| F-002-40 | No verified example yet distinguishes A/B/C cardinality | Bounded cross-format review | Pending review |


## CTC-002 — D2 consistency, mapping and replay evidence (2026-10-20)

**All entries F-002-41..59 are proposed/pending review; synthetic tests are not authority conformance.**

| ID | Finding | Evidence | Status |
|---|---|---|---|
| F-002-41 | D2 reduces semantic-path variability but not versioning/reference complexity | Four-option synthetic consistency test | Pending review |
| F-002-42 | Embedded A needs additional mechanisms for independently evolving interpretations | Four-option synthetic comparison | Pending review |
| F-002-43 | C and D2 support source/derived separation; D2 formalizes a uniform interface | Four-option synthetic comparison | Pending review |
| F-002-44 | Synthetic test does not prove a real mandate needs multiple independent interpretations | Four-option synthetic comparison | Pending review |
| F-002-45 | Published Peppol mappings can be projected into candidate D2 contract | Constructed UBL mapping test, 8 focused checks | Pending review |
| F-002-46 | Peppol specification/process identifiers belong to representation metadata | Published Peppol UBL paths | Pending review |
| F-002-47 | Source VAT category and derived treatment should remain distinguishable | Peppol constructed fixture and P7 | Pending review |
| F-002-48 | Historical replay requires archived rule/code-list inputs, not version strings alone | Formal contract review and synthetic replay | Pending review |
| F-002-49 | Full Peppol XSD/Schematron and legal validity remain untested | Formal contract test limitations | Pending review |
| F-002-50 | CFDI 4.0 source fiscal classifications can be preserved separately from derived interpretations | Constructed CFDI test, 12 focused checks | Pending review |
| F-002-51 | CFDI fractional TasaOCuota must be normalized intentionally | Constructed CFDI tax-rate test | Pending review |
| F-002-52 | Pre-certification CFDI has no authority stamp and should not be assigned invented UUID | Constructed CFDI fixture | Pending review |
| F-002-53 | SAT conformance, PAC certification and signed fiscal evidence remain untested | CFDI test limitations | Pending review |
| F-002-54 | MyInvois tax type `02` is Service Tax; source code remains distinct from derived family | Official MyInvois SDK + simplified JSON test | Pending review |
| F-002-55 | MyInvois type/version/signature dimensions should be represented distinctly | MyInvois SDK + simplified JSON test | Pending review |
| F-002-56 | India IRP exposes distinct IGST, CGST and SGST tax amounts | IRP schema + constructed JSON tests | Pending review |
| F-002-57 | India state/POS/special flags are source facts, not complete legal conclusions | IRP schema + constructed JSON tests | Pending review |
| F-002-58 | D2 handles synthetic Malaysia/India examples without overwriting source facts | Three synthetic cases, 33 focused checks | Pending review |
| F-002-59 | Malaysia/India tests do not establish full schema conformance, authority signatures or historical replay | Test report limitations | Pending review |

## CTC-002 — Decision disposition (2026-10-20)

The user explicitly approved the D2 logical contract and I-01..I-10 and scoped CTC-002 closure. **This is an approval record, not new empirical validation.** Existing F-002-11..59 (and any earlier findings) retain their existing evidence tiers and review statuses; synthetic/constructed-fixture results do not become regulatory-conformance findings. Follow-up evidence gates are tracked as CTC-002-FU02..FU04 in BACKLOG.md. No finding IDs were renumbered or reclassified as verified by virtue of this approval.


## CTC-003 — Tax sign experiment (2026-10-20)

| Finding | Observation | Evidence | Status |
|---|---|---|---|
| CTC-003-F01 | Explicit economic scope and tax-regime reference can avoid treating line applications and document summary assertions as additive duplicate taxes. | Approved T01/T02 conceptual analysis; no official fixture executed | Proposed / design inference |
| CTC-003-F02 | Nonnegative tax magnitude with explicit signed payable contribution models the five constructed cases without double-negation. | `tests/test_tax_signs.py`, `tests/test-results.json` | Tested only on synthetic arithmetic |
| CTC-003-F03 | A credit note can require negative payable contribution even where tax magnitude is positive. | Synthetic credit-note scenario | Proposed; legal convention unverified |
| CTC-003-F04 | An informational tax can have a positive reportable magnitude and zero payable contribution. | Synthetic informational-tax scenario | Proposed; legal convention unverified |
| CTC-003-F05 | Summary asserted-versus-calculated values and source provenance must remain distinct; monetary reconciliation needs separate tests for currency, rounding, adjustments and prepaid amounts. | Approved T02; draft 0.3 | Pending evidence |


## 2026-10-20 — T03 decision disposition (not a new research finding)

The user approved the ten logical T03 policy statements in `research/CTC-003/CTC-003-T03-DECISION-READY-REVIEW.md`. Evidence remains bounded: 21/21 focused checks reported in that review; official worked examples and documentation support selected semantics, but no complete inclusive-unit-price structured invoice, validated certified withholding fixture, or complete jurisdiction-specific conformance suite was executed. Approval does **not** increase evidence confidence or close E-T03-01..05. See DECISIONS.md for exact approval scope.

## 2026-10-20 — Backlog evidence-link note

The prior CTC-003 monetary calculations and source-based reviews are **preparatory inputs** for CTC-004, not newly verified regulatory findings or proof that CTC-004 acceptance criteria are met. See BACKLOG.md and reviews/CTC-001-CLOSURE-ASSESSMENT.md.

## 2026-10-20 — CTC-003 dictionary reconciliation observations (proposed)

- **F-003-U01 (Proposed):** Commercial draft 0.2 and tax draft 0.3 both define `TaxPoint`; use one authoritative semantic concept with document/line applicability and profile interpretation references, not competing owners. Evidence: the two draft dictionaries.
- **F-003-U02 (Proposed):** Draft 0.2 refers to tax facts and monetary totals while draft 0.3 introduces TaxRegime/TaxApplication/TaxSummary; references should converge on those tax concepts, while T01/T02 remain accepted at logical level. Evidence: both drafts and accepted T01/T02.
- **F-003-U03 (Proposed):** The approved T03 monetary policy requires explicit reconciliation basis and monetary effect, but `MonetaryBasis`/`MonetaryEffect` remain candidate logical concepts with no accepted fields/cardinalities. Evidence: T03 approval record and draft 0.3.
- **F-003-U04 (Proposed):** `PublishedRevision` ownership of number/type/date and `BillingDocument` as platform identity is a candidate P6-compliant arrangement, not an approved detailed-schema decision. Evidence: commercial draft 0.2.
- **Evidence limitation:** No new source XML validation or regulatory conformance executed in this consolidation.


## CTC-003 — Draft 0.5 modelling observations (proposed, not evidence-validated)

- **F-003-D05-01 (proposed):** A response artifact can be represented by DocumentRepresentation without requiring an issued BillingDocumentRevision reference; it must correlate to the compliance operation. Source: D2 logical boundary and Italy SdI conceptual review. **Confidence:** design inference.
- **F-003-D05-02 (proposed):** FiscalIdentity and FiscalEvidence need distinct logical roles to prevent authority-issued identity being independently edited in multiple records. Source: D2 P4/P6 and CFDI documentation-based review. **Confidence:** architectural inference.
- **F-003-D05-03 (proposed):** SourceLocator and FactProvenance capture different responsibilities: immutable original position versus derivation history. Source: D2 P7/I-02/I-03. **Confidence:** conceptual.
- **F-003-D05-04 (proposed):** An immutable ProfilePackage requires package/dependency digests, not only a display version, for replay. Source: approved D2 I-05; earlier synthetic replay. **Confidence:** source-derived design implication, not real regulatory validation.

These are *candidate findings* and do not amend earlier findings' evidence classifications.

## CTC-003 — Draft 0.7 conditional-cardinality findings (2026-10-20)

These are **proposed conceptual findings**, based on synthetic instance tests; not validated country requirements.

| ID | Finding | Evidence | Status |
|---|---|---|
| F-003-07 | Pre-publication representations require ingestion correlation without falsely claiming a published revision exists. | Synthetic draft-to-publication fixture | Pending review |
| F-003-08 | Party master changes do not affect pinned published party snapshots. | Synthetic party-mutation fixture | Pending review |
| F-003-09 | Derived fiscal facts can differ by profile without modifying source facts, provided the input manifest is pinned. | Synthetic two-profile fixture | Pending review |
| F-003-10 | Submitted attempts must reference an immutable exact payload; mutable latest references are invalid. | Synthetic submission and negative control | Pending review |
| F-003-11 | An external fiscal identifier can be associated with certification and later cancellation evidence without overwriting the original identifier or artifact. | Synthetic evidence chain | Pending review |
| F-003-12 | Cardinalities depend on lifecycle phase and document type; universal published seller/buyer or line minimums require profile evidence. | Conditional cardinality analysis | Pending review |

## CTC-003 — Draft 0.8 proposed findings (2026-10-20)

- **F-003-L01 (proposed, conceptual):** Internal publication and legal issuance are different lifecycle dimensions. Evidence: logical model stress test; not a verified jurisdictional mandate.
- **F-003-L02 (proposed, conceptual):** Ingestion/source representation may exist before any published revision. Evidence: Draft 0.7/0.8 synthetic correlation cases.
- **F-003-L03 (proposed, conceptual):** A single universal status conflates preparation, legal-state and external processing. Evidence: earlier CFDI/SdI conceptual reviews and Draft 0.8 synthetic branches.
- **F-003-L04 (proposed, conceptual):** Global structural minima and document-type/profile minima must be separated. Evidence: Draft 0.7/0.8 conditional-cardinality matrix.

These are not newly validated authority facts and remain pending review.

## CTC-003 — Draft 0.9 proposed structural observations (2026-10-20)

- **F-003-D09-01 (Proposed, conceptual):** A source representation can precede a platform document or published revision; ingestion correlation therefore cannot depend on a published revision ID. Evidence: Draft 0.8 synthetic lifecycle; no real authority fixture.
- **F-003-D09-02 (Proposed, conceptual):** Global minimum cardinalities and lifecycle/profile-specific minimums must be expressed separately to avoid treating a partial inbound document as a valid published invoice. Evidence: Draft 0.8 cardinality analysis.
- **F-003-D09-03 (Proposed, conceptual):** An immutable submission snapshot can reference a published revision and outbound representation without forcing legal issuance to coincide with publication. Evidence: synthetic instance checks; no regulatory assertion.
- **F-003-D09-04 (Proposed, conceptual):** Corrective documents and cancellation operations require distinct relationships to the original published revision/evidence; permitted legal paths remain jurisdiction-specific. Evidence: synthetic branches only.

## CTC-003 — Batch/envelope architectural observations (2026-10-20)

**Pending review, synthetic/conceptual evidence only:** One received payload may yield multiple billing documents; one submitted envelope may carry multiple immutable document representations; transport-level success cannot establish member-level fiscal success; partial outcomes require member-specific correlation. See CTC-003 Draft 1.0. No real batch fixture or authority response validated.

## 2026-10-20 — CTC-003 batch review disposition

The earlier batch/envelope observations remain **Pending review** and based on conceptual/synthetic evidence. `CTC-003-BATCH-01` was explicitly accepted as a **logical design principle**, not as new verified jurisdictional evidence. B01–B10 and C09-01..08 remain proposed. Real multi-document submission and partial-outcome fixtures are still required.


## CTC-003 blitz batch validation — 2026-10-20

- **F-003-BLITZ-01 (synthetic):** Existing 22/22 structural assertions passed; 26/26 new edge-case assertions passed locally. Tests exercise logical references, manifest changes, partial outcomes, duplicate receptions, uncertain retries and ambiguous external IDs, not provider/legal conformance.
- **F-003-BLITZ-02 (architectural):** Envelope-level success is insufficient to infer per-member legal outcome. Typed subjects and pinned member manifests are required for safe correlation.
- **F-003-BLITZ-03 (evidence gap):** No verified provider partial-result pair, real-world retry semantics, legally binding duplicate policy or complete concurrency test was executed. Do not upgrade evidence confidence beyond synthetic validation.

## CTC-003 Draft 1.2 findings — synthetic structural review

See `research/CTC-003/CTC-003-UNIFIED-CARDINALITY-REFERENCE-REVIEW-DRAFT-1.2.md` for F-003-C12-01 through F-003-C12-05. These are candidate research findings supported by synthetic checks only; no regulatory conformance asserted.

## 2026-10-20 G2 checkpoint

The six ownership overlaps are resolved at logical level under standing blitz authorization. Draft 1.9 integrates earlier candidate constraint corrections; no new regulatory fixture validation or exhaustive 48-entity conformance is claimed.

## 2026-10-20 — CTC-003 closure evidence disposition

The user approved the scoped detailed logical dictionary. Earlier synthetic structural validations and partial UBL/CFDI selected-field tests remain evidence of *focused* consistency only; they do not demonstrate full country regulatory conformance, complete source-to-D2-to-target round-trip preservation, or exhaustive historical field-level coverage. The 18 additional typed field contracts remain proposals. No existing finding confidence is upgraded by the closure decision.

## CTC-004 — Validated logical findings — 2026-10-21

- **F-004-01 (focused synthetic):** Three concurrent tax regimes with charge/withhold directions were aggregated independently without double-counting source-asserted summaries (MG-004-01: 12/12).
- **F-004-02 (focused synthetic):** Explicit quantization, rounding mode and calculation stage yield reproducible monetary results; missing essential policy inputs produce `NOT_EVALUABLE` (MG-004-02: 11/11).
- **F-004-03 (evidence boundary):** Earlier four overlapping suites replayed 66/66 assertions. Combined 89/89 assertions support logical behavior, not 89 independent real-world cases or authority compliance.
- **Deferred:** Country profiles and precision rules CTC-005/007; validated authority samples CTC-008/010; semantic-loss analysis CTC-009.


## 2026-10-21 — CTC-005 scoped closure evidence disposition

- Seven original synthetic governance scenarios passed; four remaining logical coverage areas passed twenty additional deterministic assertions (package/dependency integrity 4, extension registration 7, legal-state separation 3, promotion/rollback/history 6).
- These results support logical contract consistency only. No production registry durability, cryptographic verification, actual jurisdictional rule correctness, authority response conformance or cross-deployment replay is established.
- JP-01..JP-10 and the seven-step decision tree are accepted by explicit user approval, not inferred from tests.


## CTC-006 validation evidence — 2026-10-21

Ten synthetic focused scenarios passed, covering immutable party snapshots, multiple registrations, issuer/series numbering, draft-to-publication continuity, credit and replacement references, cancellation history, unresolved external references and repeat submissions. These tests establish selected logical representability only, not full 51-entity schema coverage or country-specific regulatory validity. See `research/CTC-006/CTC-006-CONSOLIDATED-VALIDATION-AND-CLOSURE-REVIEW.md`.

## CTC-007 scoped closure evidence — 2026-10-21

- The 12/12 deterministic classification assertions support consistency of the V-01..V-10 policy decision table, not full implementation compatibility or historical replay.
- Semantically breaking changes can occur without a canonical path rename (units, ownership, identifier scope). Independent version domains avoid unnecessary core model revisions.
- Open evidence: machine-readable compatibility checker, dual-read/API negotiation, archived dependency replay and jurisdictional fixtures. These remain assigned to existing backlog work, not treated as failed CTC-007 acceptance criteria.

## CTC-013 logical validation findings (2026-10-21)

Ten synthetic lifecycle scenarios passed. They support independent member outcomes, timeout/unknown treatment, duplicate/late callback preservation, ambiguity handling and deterministic replay in a bounded projection. Limitations: not a production event engine; no actual provider response payloads, cryptographic validation, jurisdictional legal rules or physical persistence validation. See `research/CTC-013/CTC-013-CONSOLIDATED-VALIDATION-AND-CLOSURE-REVIEW.md`.
