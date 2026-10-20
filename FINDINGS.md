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
