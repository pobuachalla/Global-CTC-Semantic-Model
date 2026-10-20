# CTC-002 — D2 logical fiscal contract validation against Mexico CFDI 4.0

**Date:** 2026-10-20  
**Task:** CTC-002 (Review / evidence-gated)  
**Status:** Focused constructed-fixture validation; **no new ADR accepted**.

## 1. Question and scope

Test whether the previously user-validated D2 logical fiscal interpretation contract (defined in `CTC-002-D2-FORMAL-LOGICAL-CONTRACT.md`) works with a materially non-Peppol XML syntax: Mexico CFDI 4.0. Preserve accepted P1–P7. Test field ownership, source-vs-derived facts, tax-rate representation, document identity, and separation of certification evidence. Do not choose FiscalContext A/B/C or physical aggregate placement.

## 2. Evidence and fixture status

- **Primary authoritative structure:** SAT Anexo 20 CFDI 4.0: https://www.sat.gob.mx/cs/Satellite?blobcol=urldata&blobkey=id&blobtable=MungoBlobs&blobwhere=1461175118249&ssbinary=true
- **SAT XSD location:** http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd ; mirrored for inspection at https://github.com/phpcfdi/resources-sat-xml/blob/master/resources/www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd
- **Previous internal research:** `CTC-002-CFDI-CERTIFICATION-EVIDENCE-REVIEW.md` and `CTC-002-FISCAL-FIELD-OWNERSHIP-MATRIX.md`.
- **Fixture:** `cfdi40-constructed.xml`, created for this test using published CFDI attribute and element names. It has *fictional parties and invalid demonstration signature/certificate values*. It is **not** a real, legally valid, signed or PAC-certified CFDI. It has not been validated against the complete SAT XSD/catalog/conditional rule set.
- The test is based on published official field definitions, but no official completed sample invoice or genuine paired pre-/post-timbrado artifacts were acquired in this run.

## 3. Field-to-contract crosswalk

| CFDI 4.0 XML field | D2 semantic concept | Ownership / provenance | Important distinction |
|---|---|---|---|
| `Comprobante/@Serie`, `@Folio` | `PublishedRevision.commercialIdentity` | Billing; source-supplied | Not a fiscal UUID or submission identifier |
| `Comprobante/@Fecha`, `@Moneda` | Issuance timestamp, currency | Billing; source-supplied | Keep source timezone semantics; do not invent offset |
| `Emisor/@Rfc`, `Receptor/@Rfc` | Party tax registrations | Billing party snapshot; source-supplied | Preserve issuer/recipient role |
| `Emisor/@RegimenFiscal` | `SourceFiscalFact` | Fiscal classification; original code + SAT scheme | Source-supplied, not freely inferred |
| `Receptor/@RegimenFiscalReceptor` | `SourceFiscalFact` | Recipient fiscal classification | Distinct from issuer regime |
| `Receptor/@UsoCFDI` | `SourceFiscalFact` | Recipient document-use classification | Not generic business document type |
| `Concepto/@ObjetoImp` | `SourceFiscalFact` | Tax-object classification | Must not be conflated with `TipoFactor` |
| `Traslado/@Impuesto` | `SourceFiscalFact` and billing tax application | Tax-family code | `002` mapped to `IVA` by **illustrative prototype rule** |
| `Traslado/@TipoFactor`, `@TasaOCuota` | Tax factor and rate | Billing tax + original source attributes | Fraction `0.160000` = 16%, not 0.16% |
| `Traslado/@Base`, `@Importe` | Tax base and tax amount | Billing tax | Reconcile with totals, preserve precision |
| `Comprobante/@SubTotal`, `@Total` | Monetary totals | Billing | Test only simple one-line/no-adjustment case |
| `Comprobante/@Version` | Representation syntax version | Representation | CFDI version is not canonical model version |
| `Comprobante/@Sello`, `@NoCertificado` | Issuer signature metadata | Representation / signature evidence | Test fixture contains nonvalid placeholders |
| `Complemento/TimbreFiscalDigital/@UUID` | Fiscal identity | Fiscal identity/evidence, linked to certified artifact | Absent before certification; not invented in test |
| `TimbreFiscalDigital/@FechaTimbrado`, `@SelloSAT` | Certification evidence | Fiscal evidence / certified representation | Must not be added to billing revision as a status update |

## 4. Executed focused test

Run: `python validate_cfdi_d2.py` in this directory. Script uses Python standard-library XML parsing, `decimal.Decimal`, JSON and SHA-256. Outputs: `BILLING-REVISION.json`, `FISCAL-INTERPRETATION.json`, `VALIDATION-RESULT.json`.

**Result: 12/12 focused assertions passed**:

1. XML well-formed.
2. CFDI 4.0 namespace/version recognized.
3. Required fixture nodes present.
4. Line amount reconciles to document subtotal.
5. Line tax = base × fractional rate.
6. Document total = subtotal + transferred tax (simple fixture).
7. Line tax agrees with document tax summary.
8. No `TimbreFiscalDigital` in constructed pre-certification artifact.
9. Source fiscal codes preserved with source paths.
10. Derived IVA classification linked to its input fact and rule/profile metadata.
11. Interpretation pins the exact immutable revision fingerprint.
12. Missing archived profile/code-list package explicitly flagged.

Source XML SHA-256: `8ce9b5c28029391079700053ebe18f74a9a3c2d5595becb8ea6e79942b0c6a08`.

**Not tested:** SAT XSD/catalog conformance, real-world conditional rules, cryptographic issuer seal, PAC certification, signed post-certification XML, SAT fiscal status, cancellation/credit note, legal tax treatment, real dual interpretations, archived rule-package replay. **This is not an end-to-end CTC conformance test.**

## 5. P1–P7 evaluation

| Principle | Focused result | Caveat |
|---|---|---|
| P1 billing/processing separation | Pass conceptually | No real processing response used |
| P2 immutable revisions | Pass (revision hash pinned) | Publication lifecycle not exercised |
| P3 original/generated representations | Partial (source hashed) | No certified representation generated |
| P4 fiscal vs submission identity | Pass structurally | No real UUID/submission ID in fixture |
| P5 independent compliance histories | Not tested | No actual PAC response/attempt |
| P6 authoritative ownership | Pass for selected source/derived tax classification | Not a complete field dictionary |
| P7 provenance/versioned derivation | Partial: source paths and mapping/rule identifiers recorded | Profile package digest and SAT code-list version NOT_ARCHIVED |

## 6. Architectural implications

1. **D2 supports non-UBL native fiscal concepts** without forcing them into generic tax category fields: `RegimenFiscal`, `RegimenFiscalReceptor`, `UsoCFDI`, and `ObjetoImp` remain typed source fiscal facts.
2. **A source fact can be local and still authoritative.** Its local code scheme is preserved even when a normalized classification is derived separately.
3. **Tax rates need typed representation.** CFDI's fractional `TasaOCuota` should not silently become a percentage with incorrect scale; model both original and normalized value with provenance.
4. **Certification is a new artifact/evidence relationship, not a billing mutation.** This is structurally supported by the published TFD complement but is not proven through a genuine matched pair in this test.
5. **No result discriminates A vs B vs C vs D2 physical aggregation.** D2 remains a logical interface discipline; its optional independent interpretation lifecycle is still a design hypothesis.

## 7. Proposed findings, not yet registered or approved

- **F-002-50:** Published CFDI 4.0 XML fields can map to D2 billing, source fiscal fact and representation domains while preserving local code values (constructed-fixture test).
- **F-002-51:** CFDI `TasaOCuota` fractional scale requires explicit semantic normalization; selected arithmetic reconciled with `Decimal`.
- **F-002-52:** A normalized IVA tax-family fact can be derived from `Impuesto=002` without overwriting the source code, with rule provenance (prototype rule only).
- **F-002-53:** The test does not establish PAC certification, fiscal UUID authenticity, full P7 historical replay or independently versioned FiscalContext necessity.

## 8. Decision checkpoint

**Previously accepted:** CTC-002 P1–P7 (principles); D2 logical direction user-validated. **Still proposed:** D2 formal logical contract invariants I-01..I-10, including publication boundary details. **Still deferred:** FiscalContext A/B/C and physical/cardinality implementation. **CTC-002:** Review/evidence-gated. **CTC-003:** Not started.

**Next discriminating test:** obtain a genuine licensed and verifiable before/after PAC-certified CFDI pair and validate the TFD evidence-to-representation link; separately seek a real use case requiring two distinct fiscal interpretations for one immutable billing revision. Do not mark this test as full SAT compliance.

**GitHub:** No repository files changed. Add this report and fixtures under `research/CTC-002/cfdi-d2/` after review.
