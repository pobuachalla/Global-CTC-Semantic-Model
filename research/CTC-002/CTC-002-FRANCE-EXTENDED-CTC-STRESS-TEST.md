# CTC-002 — France Extended CTC Semantic Ownership Stress Test

**Date:** 2026-10-19  
**Status:** Draft for review; no ADR approved  
**Task:** CTC-002 (P0)  
**Evidence level:** Internal documented stress test, **not** a newly executed parsing/validation run against a raw French XML fixture or official French specifications.

## 1. Evidence and source versions

- `semantic-billing-model(1) (1).md` — Global CTC Semantic Billing Model **v0.3**, §§4.8, 4.24a–c, 6.1, 12.2, 18.5 and Appendix A.
- `relational-data-model(1) (1).md` — Global CTC Relational Data Model **v0.3**, §§6, 13A, 22A.
- `CTC-Semantic-Document-Entity-Model.docx` — earlier **v1.0**, dated 2026-09-07, particularly `SemanticLine`, `TaxApplication`, `DocumentControl`.
- `CTC-002-FISCAL-FIELD-OWNERSHIP-MATRIX.md` — prior working matrix, FO-01 through FO-28.

**Not supplied for this execution:** a raw, verifiable French Extended CTC UBL invoice plus matching CII representation, validation report, applicable profile rules and mapping trace. Consequently, this test checks *internal consistency of the documented example* and proposed semantic ownership, not actual French compliance.

## 2. Test specimen from v0.3 §18.5

The existing worked example identifies invoice `AUTOF202600035` with EUR currency:

| Line | Role | Parent | Contributes | Signed net amount (EUR) |
|---|---|---|---|---:|
| 10 | GROUP | — | true | +21,425.59 |
| 11 | DETAIL | 10 | false | +21,425.59 |
| 20 | GROUP | — | true | -204.78 |

**Reconciliation test:** sum of all physical line amounts = 42,646.40 (incorrect for this hierarchy); sum of contributing lines only = **21,220.81**. The DETAIL line explains GROUP 10 and is not added a second time. This test establishes a requirement for line contribution semantics in the proposed canonical model, not an independently verified French mandate rule.

## 3. Field ownership and boundary matrix

| Concept / source clue | Semantic meaning | Candidate authoritative owner | Why | Evidence / unresolved point |
|---|---|---|---|---|
| `Invoice/ID` | Supplier-issued commercial document number | `BillingDocumentRevision` | Business identity, not submission ID | v0.3 Appendix A |
| `InvoiceTypeCode` | Invoice/credit/debit meaning; possibly local fiscal subtype | Core for normalized kind; fiscal interpretation for local subtype | One source code can convey multiple meanings | v0.3 Appendix A; profile mapping not verified |
| `InvoiceLine` GROUP/DETAIL and parent linkage | Hierarchical billing structure | `BillingDocumentRevision` | Represents billed economic structure | v0.3 §§4.8, 12.2, 18.5 |
| `contributesToDocumentTotals` | Which economic lines enter reconciliation | Core semantic line, with profile-derived provenance if derived | Prevents double-counting | v0.3 §§4.8, 6.1 |
| Negative `lineNetAmount` and price | Signed economic values | `BillingDocumentRevision` | Sign is intrinsic; not inferred from document type | v0.3 §§6.1, 12.2 |
| Line-level seller/participant | Actual participant at line scope | `BillingDocumentRevision` party-role association | Source may override document party | v0.3 §§4.8, 12.2; inheritance rules unresolved |
| Group tax summary | Aggregated tax fact on group line | Core line-level `TaxSummary` | Independent of child detail's tax categories | v0.3 §4.8; aggregation semantics need tests |
| Tax point / exigibility date and basis | Taxable event timing and fiscal basis | Shared `TaxPoint` for reusable meaning; fiscal profile for local code interpretation | Avoid treating source placement as semantic ownership | v0.3 §§4.24a, 12.2; boundary still open |
| Structured note prefixes | Business note content plus local qualifiers | Core `Note`; profile for qualifier mapping | Retain original text and qualifier provenance | v0.3 §§4.24b, 12.2 |
| Legal form / company registration | Party legal identity | `Party.LegalRegistration` | Reusable party semantics | v0.3 §§4.4a, 12.2 |
| `UBLVersionID`, `CustomizationID`, `ProfileID` | Source serialization/profile metadata | `DocumentRepresentation` | Identifies format and profile, not billing fact | v0.3 §§4.24c, 12.2 |
| Mapping profile / code-list version | Rules used to interpret source fields | `JurisdictionProfile` definition, referenced by representation and interpretation | Enables reproducible historical mapping | v0.3 §16 |
| PA/platform acknowledgements | Submission/delivery/processing outcomes | `ComplianceTransaction` events and response artifacts | Do not modify commercial meaning | v0.3 §11; actual French responses not tested |
| Authority-issued identifier / receipt (if applicable) | Fiscal legal identity or evidence | Candidate `FiscalEvidence` linked to exact artifact and transaction | Externally generated, separate lifecycle | Conceptual only; no corresponding sample supplied |

## 4. Before/after instance simulation

### Before normalization

- `SRC-FR-001`: raw source UBL representation, containing profile identifiers, line hierarchy and tax-point encoding.
- No canonical line-contribution semantics yet established.

### After semantic mapping

- `DOC-FR-001` / `REV-FR-001`: commercial invoice with signed GROUP and DETAIL lines, party roles, tax point, notes and tax summaries.
- `REP-FR-001`: original source representation and immutable hash (proposed).
- `MAP-FR-001`: exact mapping/profile version and lineage explaining how the source hierarchy and encoded tax-point were interpreted (proposed).
- `FC-FR-001` (optional): local fiscal classification, if the source actually contains one that is not reducible to shared tax/billing semantics.
- **No new `ComplianceTransaction` is required merely to normalize the invoice.**

### After hypothetical outbound transformation

- `REP-FR-002`: distinct target representation, if required, linked to the same `REV-FR-001` and mapping version.
- `CT-FR-001`: created only if a submission/delivery/reporting operation is initiated.
- Any subsequent response is linked to `CT-FR-001` and the relevant submitted artifact, not written into line/party/tax semantics.

These are **illustrative records**, not artifacts produced by executing a transformer.

## 5. Candidate comparison

| Test | A: embedded immutable FiscalContext | B: independent versioned FiscalContext | C: hybrid intrinsic + independent interpretation |
|---|---|---|---|
| Group/detail hierarchy | Pass if represented in core | Pass if represented in core | Pass if represented in core |
| Signed negative lines | Pass | Pass | Pass |
| Line parties and tax summaries | Pass | Pass | Pass |
| Profile-encoded tax point | Pass if mapping into core + profile evidence | Pass if interpretation preserves source meaning | Pass if shared TaxPoint + local qualifier |
| Profile metadata | Separate representation required | Separate representation required | Separate representation required |
| Several independently evolving fiscal interpretations | Not tested here | Can support | Can support |

**Outcome:** The French test **does not select B or C over A**. It supports a rich, jurisdiction-neutral billing core and separate representation/profile metadata. It argues against moving reusable semantics into a generic country-specific fiscal bag. An independently versioned fiscal interpretation is still an *option*, not a demonstrated necessity.

## 6. Proposed findings — pending review

- **F-002-31:** The documented French grouped/detail example requires explicit contribution semantics to prevent double-counting; demonstrated contributing net total = EUR 21,220.81. Evidence: v0.3 §18.5; arithmetic independently checked. Confidence: high for example, not mandate verification.
- **F-002-32:** Signed values, hierarchical lines and line-level parties are reusable billing semantics, not necessarily French-only fiscal extensions. Evidence: v0.3 §§4.8, 6.1, 12.2. Confidence: high conceptual.
- **F-002-33:** Tax-point meaning can be shared while local exigibility code interpretation belongs to profile rules; exact ownership of tax-point basis remains unresolved. Evidence: v0.3 §§4.24a, 12.2. Confidence: medium.
- **F-002-34:** UBLVersionID, CustomizationID and ProfileID belong to representation provenance, not the core invoice identity. Evidence: v0.3 §4.24c and §12.2. Confidence: high conceptual.
- **F-002-35:** The French example does not prove a need for independent FiscalContext versioning; all A/B/C remain viable if core semantic facts and external processing are separated. Evidence: conceptual A/B/C comparison. Confidence: high within test scope.

## 7. Evidence gates still open

1. Obtain raw French Extended CTC UBL sample with license/source/version and verify source hierarchy, group totals and signed amounts.
2. Verify official profile documentation, tax-point/exigibility code mapping and legal-form/line-party requirements.
3. Execute source → canonical → target round-trip and record field-level losses, including line-contribution and tax-point mapping.
4. Capture applicable actual platform/authority responses and correlate their identifiers to the exact submitted artifact.
5. Find a real case with two **materially different fiscal interpretations of the same immutable commercial revision**. This is the decisive remaining test for FiscalContext independence.

## 8. CTC-002 decision impact

**No ADR accepted.** A, B and C remain under investigation. The composed contract remains the user-selected *leading investigation hypothesis*, not an approved model. Recommend moving CTC-002 to **Review / evidence-gated**, not Done, pending explicit review of the boundary matrix and unresolved fiscal interpretation multiplicity.
