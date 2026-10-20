# CTC-002 — D2 final focused mapping tests: Malaysia MyInvois and India GST IRP

**Date:** 2026-10-20  
**Status:** Executed constructed-fixture tests; findings proposed, not approved.  
**Task:** CTC-002 only. No change to accepted P1–P7 or deferred FiscalContext A/B/C.

## Executive result

Three synthetic input fixtures, **33 of 33 focused assertions passed** in `run_validation.py`. These assertions check fixture parsing, selected arithmetic, source/derived separation, explicit provenance references, immutable revision references and honest disclosure of unarchived profile packages. The script does **not** establish full MyInvois or GST IRP validity, cryptographic correctness, signed responses, legal tax treatment, or true historical replay.

The result supports D2's implementation-neutral logical ownership model across two further format families. It does not settle FiscalContext physical embedding, aggregate cardinality or independent-lifecycle necessity.

## 1. Authoritative sources and scope

### Malaysia

- MyInvois SDK, Invoice v1.1: https://sdk.myinvois.hasil.gov.my/documents/invoice-v1-1/
- MyInvois SDK, Tax Types: https://sdk.myinvois.hasil.gov.my/codes/tax-types/
- MyInvois SDK, Types: https://sdk.myinvois.hasil.gov.my/types/

The official SDK maps invoice type code, version, supplier/buyer, tax type, totals, signature and other elements to a Malaysia-specific UBL 2.1 representation. Invoice v1.1 enables signature validation, distinguishing it from v1.0. The tax-type list identifies `02` as **Service Tax**. These are official field and code-list references, not evidence that the synthetic payload has been accepted by MyInvois.

### India

- IRIS IRP 6, Notified E-invoice Schema: https://einvoice6.gst.gov.in/content/notified-e-invoice-schema/
- IRIS IRP 6, Validation Rules: https://einvoice6.gst.gov.in/content/validation-rules-for-e-invoicing-that-you-must-take-care-to-avoid-errors/
- NIC, GST E-Invoice: https://www.nic.gov.in/project/gst-e-invoice/

The published IRP schema identifies `SupTyp`, `IgstOnIntra`, seller state, buyer place of supply, `HsnCd`, `GstRt`, `IgstAmt`, `CgstAmt`, `SgstAmt`, and invoice totals. The validation guidance describes arithmetic relationships for IGST and split CGST/SGST. It also contains regime-specific exceptions; the synthetic state comparison is **not a substitute for a complete legal tax determination**.

## 2. Test fixtures

| Fixture | Format | Core scenario | Legal validity |
|---|---|---|---|
| `malaysia-constructed.json` | Simplified JSON with MyInvois-named concepts, **not** an official MyInvois UBL JSON submission envelope | Invoice v1.1, type `01`, service tax code `02`, MYR 1,000 + illustrative 8% | Not valid for submission; demo TINs, no signature |
| `india-interstate-constructed.json` | IRP-schema-shaped JSON subset, **not** a complete valid IRP request | Seller state 27, place of supply 07, 18% IGST example | Not valid for submission; demo GSTINs and HSN |
| `india-intrastate-constructed.json` | IRP-schema-shaped JSON subset, **not** a complete valid IRP request | Seller state 27, place of supply 27, 9% CGST + 9% SGST example | Not valid for submission; demo GSTINs and HSN |

**Important:** Unlike earlier Peppol and CFDI tests, the Malaysia fixture deliberately uses a simplified concept-level JSON projection rather than actual UBL JSON paths. This is a semantic ownership test, **not a real MyInvois syntax mapping test**. India uses published schema field names but is likewise incomplete.

## 3. Fiscal field ownership crosswalk

| Country / source field | D2 logical owner | Source or derived? | Why |
|---|---|---|---|
| MY `InvoiceTypeCode` and `listVersionID` | Billing document type + representation version | Source | One syntax location expresses two distinct meanings |
| MY supplier/buyer TIN | Billing party snapshot | Source | Issued-document participant identification |
| MY `TaxCategory/ID` (`02`) | SourceFiscalFact | Source | Preserve local tax scheme/code unchanged |
| MY service-tax semantic family | DerivedFiscalFact | Derived from `02` | Keep local source code authoritative; interpretation cites rule and code list |
| MY tax base, tax amount, totals | Billing tax/monetary facts | Source | Reusable monetary meaning |
| MY signature and v1.1 signature-validation requirement | Representation and jurisdiction profile | Source/profile | Signature is not commercial invoice meaning |
| MY LHDN validation UUID/status (not present) | Fiscal identity/evidence and compliance | External | Do not manufacture authority outcome |
| IN `SellerDtls.Stcd`, `BuyerDtls.Pos` | Billing supply/party context | Source | Original location facts, retained without overwrite |
| IN `SupTyp`, `IgstOnIntra` | SourceFiscalFact / transaction fiscal classification | Source | Legally significant context and exception flags |
| IN `HsnCd` | Billing item classification + original scheme | Source | Preserve native classification |
| IN `GstRt`, `IgstAmt`, `CgstAmt`, `SgstAmt` | Billing tax applications | Source | Explicit multi-component tax values |
| IN illustrative intra/inter state relationship | DerivedFiscalFact | Derived | Only a test interpretation of source state/POS; not a complete tax rule |
| IN IRN / signed QR (not present) | Fiscal identity/evidence | External | Requires actual IRP response to validate |

## 4. Executed assertions

Run `python run_validation.py`. Three fixture-specific result files and `results/summary.json` are produced.

- Malaysia: 7 fixture assertions + 4 common ownership/provenance assertions = **11 passed**.
- India interstate: 7 fixture assertions + 4 common assertions = **11 passed**.
- India intrastate: 7 fixture assertions + 4 common assertions = **11 passed**.
- **Total: 33/33**.

The common assertions verify: interpretation references a revision fingerprint; source facts have paths; derived facts cite input fact IDs; profile package is explicitly flagged `NOT_ARCHIVED` rather than falsely treated as reproducible.

The India cases check arithmetic for the illustrative supplied tax allocations and preserve `IgstOnIntra=N`; they do not infer legally correct tax solely from state comparison. The Malaysia case checks its simplified fields and numeric reconciliation; it does not parse or validate official UBL XML/JSON.

## 5. D2 principle evaluation

| Principle | Malaysia | India | Limitations |
|---|---|---|---|
| P1 Separate billing and processing | Structurally supported | Structurally supported | No authority response fixtures |
| P2 Immutable revisions | Revision fingerprint pinned | Revision fingerprint pinned | Publication lifecycle not executed |
| P3 Preserve representations | Source JSON hashed | Source JSON hashed | No generated official-format payload or signed response |
| P4 Distinct identities | No LHDN UUID invented | No IRN invented | External identity linkage not tested |
| P5 Independent histories | Not exercised | Not exercised | No attempts, callbacks or retries |
| P6 Single authoritative owner | Local tax type source distinct from derived family | Source GST components distinct from derived supply relation | Complete ownership dictionary remains unapproved |
| P7 Provenance | Source paths, rule reference, profile label | Source paths, rule reference, profile label | No archived immutable rules/code lists, so historical replay **not demonstrated** |

## 6. Findings proposed for review

- **F-002-54:** Malaysian MyInvois tax-type codes remain source fiscal facts even though their syntax is UBL-derived; code `02` maps to Service Tax in the official SDK. Focused test only.
- **F-002-55:** Malaysia document type and version share an interchange location but represent distinct semantic dimensions; signature validation differs by document version.
- **F-002-56:** India IRP explicitly represents GST as separate IGST, CGST and SGST components, reinforcing the need for a multi-application tax model and exact source-value preservation.
- **F-002-57:** India seller state, place of supply and special flags must be preserved separately from derived tax-jurisdiction conclusions; state comparison alone is not authoritative legal classification.
- **F-002-58:** D2's logical contract handles these constructed fixtures without revising the original source facts or conflating process identities; neither test establishes independent FiscalContext lifecycle necessity.
- **F-002-59:** Current tests are insufficient for authority compliance, true historical replay or complete MyInvois UBL/IRP-schema conformance; full package and real signed response evidence remain necessary.

All are **proposed**, not accepted research findings.

## 7. Architecture recommendation

D2 is a reasonable **logical semantic interface candidate** across Peppol, CFDI, MyInvois and India IRP. The latest tests strengthen the case for typed tax applications, typed local code schemes, source/derived provenance and separate fiscal evidence. They do **not** establish that the independent FiscalInterpretation is a mandatory aggregate for all documents. Keep A/B/C physical boundaries deferred.

Before CTC-002 Done, agree the D2 logical invariants and explicitly document the evidence exception or remaining gates. For future confidence, validate real MyInvois UBL 2.1 XML/JSON and IRP-complete JSON against published validators, and obtain signed authority response fixtures.

## 8. Session checkpoint

**Task:** CTC-002, Review/evidence-gated. **Approved:** P1–P7, D2 logical direction validated by user. **Proposed:** F-002-54..59; this mapping report. **Unapproved:** Formal D2 I-01..I-10 invariants, FiscalContext A/B/C physical ownership/cardinality, complete entity dictionary. **CTC-003:** Not started. **GitHub:** Not modified.

**Suggested updates after review:** add F-002-54..59 to FINDINGS.md, link this report in SESSION-LOG.md, retain existing DECISIONS.md approvals and deferrals, keep BACKLOG.md at Review and MODEL-BASELINE.md unapproved.
