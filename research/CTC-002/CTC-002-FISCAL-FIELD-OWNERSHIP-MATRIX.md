# CTC-002 — Fiscal Field Ownership Matrix

**Date:** 2026-10-19  
**Status:** Research draft — not approved  
**Scope:** Mexico CFDI 4.0, Italy FatturaPA, France Extended CTC  
**Objective:** Decide where a field's *meaning* is authoritative, independently of XML/JSON syntax, persistence, and transmission.

## 1. Evidence basis and limits

Available: `MASTER-PROMPT.md`, `BACKLOG.md`, `DECISIONS.md` (including the 2026-10-19 CTC-002 checkpoint copy), `MODEL-BASELINE.md`, `semantic-billing-model(1).md` **v0.3**, `relational-data-model(1).md` **v0.3**, `CTC-Semantic-Document-Entity-Model.docx` **v1.0 (2026-09-07)**, `ctc-transformer-complete-reference.md`, and the previously recorded French Extended CTC conceptual stress test. The earlier ERP architecture v2.0 is also available. This matrix uses **existing project source analysis**, not a fresh validation against official schemas or sample repositories. Therefore syntax references are candidate mappings, and compliance requirements, especially France Extended CTC, remain unverified externally. No sample repository files were parsed for this exercise.

Evidence shorthand: **SB** = Global CTC Semantic Billing Model v0.3 (§4, §8, §11, §12.2, §18, Appendix A); **TR** = CTC Transformer Complete Reference (§4, §6); **RM** = Global CTC Relational Data Model v0.3 (§14–15, §22A); **FR** = French Extended CTC stress-test *as documented in SB/RM*, not independently verified fixture. Confidence **H** = strongly supported by the project models for conceptual meaning; **M** = project-supported mapping with ownership still debatable; **L** = illustrative or externally unverified profile-specific behavior.

### Candidate authoritative owners

- **B** — `BillingDocumentRevision`: stable commercial and reusable intrinsic tax meaning.
- **F** — `FiscalContext` / fiscal interpretation: jurisdiction-specific classification, tax-use, local fiscal facts as-of a profile/version.
- **R** — `DocumentRepresentation`: exact source/target serialized artifact, syntax/profile metadata and hashes.
- **C** — `ComplianceTransaction` / attempt / event: routing, submission, processing and outcomes.
- **E** — fiscal identity/evidence: externally conferred legal identity, certification, authorization, receipts, revocation/cancellation proof.
- **P** — jurisdiction profile/rules: constraints, code lists, effective-dated validation; **not** a document fact.

**Ownership rule:** Each fact has one authoritative semantic owner; other aggregates may reference it or hold an explicitly labeled derived projection. Preserve raw representations independently for loss analysis.

## 2. Field ownership matrix

| ID | Semantic fact | Mexico CFDI source / example | Italy FatturaPA source / example | France Extended CTC source / example | Candidate owner | Confidence / evidence | Lifecycle or ambiguity |
|---|---|---|---|---|---|---|---|
| FO-01 | Commercial document number | `Comprobante/@Folio` (and `@Serie` separately) | `DatiGeneraliDocumento/Numero` | UBL `Invoice/ID` | **B** | H: SB App A, §18.3–18.4 | Do not concatenate series and folio irreversibly. |
| FO-02 | Document series | `Comprobante/@Serie` | Numbering/series where distinguishable | Source-specific when present | **B** | M: SB §4.1, TR §6.5 | Series is not authority UUID. |
| FO-03 | Commercial document type | `TipoDeComprobante` maps to business meaning | `TipoDocumento` mapped to invoice/credit/debit | UBL `InvoiceTypeCode` plus profile semantics | **B** for normalized kind; **F** for local fiscal subtype | H/M: SB §4.1, §8, App A | One source code can carry both business and fiscal meaning; keep mapping provenance. |
| FO-04 | Issue date/time | `Comprobante/@Fecha` | `Data` | UBL `IssueDate`/`IssueTime` if supplied | **B** | H: SB §4.1, App A | Avoid dropping time when present. |
| FO-05 | Document currency | `Moneda` | `Divisa` | UBL `DocumentCurrencyCode` | **B** | H: SB §4.1 | Currency is semantic, not target-only. |
| FO-06 | Seller / buyer legal party | `Emisor`, `Receptor` | `CedentePrestatore`, `CessionarioCommittente` | UBL supplier/customer parties | **B** | H: SB §2.1, §4.2 | Party snapshots versus reusable master identity still open. |
| FO-07 | Party tax identifier/registration | `Rfc` | `IdFiscaleIVA`, tax IDs | PartyTaxScheme / registration | **B** for tax registration; **F** for local fiscal party classification | H: SB §4.4–4.5, §8.1 | Identifier scheme and jurisdiction must be explicit. |
| FO-08 | Local seller fiscal regime | `Emisor/@RegimenFiscal` | `RegimeFiscale` | Profile-specific fiscal classification if supplied | **F** | H/M: SB §8.1, §18.3; TR native.sdi | Versioned profile code, not a global Party property. |
| FO-09 | Buyer fiscal use | `Receptor/@UsoCFDI` | No direct generic equivalent established | No direct generic equivalent established | **F** | H: SB §8.1, §18.3 | Explicit local semantic meaning; avoid universal buyer attribute. |
| FO-10 | Tax treatment, rate, base, amount | `Impuestos/Traslados`, line taxes | `AliquotaIVA`, `ImponibileImporto`, `Imposta` | UBL `TaxTotal`/line tax data | **B** | H: SB §4.15–4.17, App A | Regime/type/direction must remain explicit; not every tax is VAT. |
| FO-11 | Withholding | `Retenciones` | `DatiRitenuta` | Only if represented by source/profile | **B** | H: SB §4.15, App A | Preserve withholding direction, not generic negative discount. |
| FO-12 | Tax point / exigibility | Profile-specific if provided | VAT/payment timing where supplied | French stress test: tax-point basis in period structures | **B** for reusable tax-point semantics; **F/P** for local basis-code interpretation | M: SB §4.24a, §12.2; RM §22A | Whether `TaxPoint` is B or F remains a review question. |
| FO-13 | Line structure, group/detail hierarchy | `Conceptos/Concepto` | `DettaglioLinee` | GROUP/DETAIL, parent-child line roles | **B** | H for concept; FR externally unverified: SB §4.8, §12.2 | Contributing-line flag avoids double count. |
| FO-14 | Signed amounts / negative lines | Source signs and mapping rules | Source signs and mapping rules | Negative prices and deduction lines | **B** | H: SB §6.1, §12.2 | Do not derive sign solely from invoice type. |
| FO-15 | Line-specific party | Not established in supplied CFDI mapping | Not established in supplied FatturaPA mapping | French stress test line seller/participant | **B** | M: SB §4.8, §12.2 | Inheritance/override of document seller unresolved. |
| FO-16 | Credit/correction reference | `CfdiRelacionados` | `DatiFattureCollegate` etc. | Billing references | **B** (`DocumentRelationship`) | H: SB §4.21, App A | Separate legal document vs internal revision is profile-dependent. |
| FO-17 | Payment method and terms | `FormaPago`, `CondicionesDePago` | `ModalitaPagamento`, due dates | UBL payment means/terms | **B** | H: SB §4.18–4.20, App A | Distinguish how payment is made from when due. |
| FO-18 | Jurisdictional fiscal document classification | Local CFDI type/classification | `TD01`, `TD04`, etc. | French profile-specific classifications | **F** | H/M: SB §8, §18.4 | Not the same as normalized document type. |
| FO-19 | Export / transaction classification | `Exportacion` | Local export/tax treatment codes | Profile-specific if present | **F** for local classification; **B** for reusable supply facts | M: SB §8, App A | Avoid duplicating core place-of-supply facts. |
| FO-20 | Source format, schema version, profile IDs | CFDI 4.0 source representation | FatturaPA syntax/version | `UBLVersionID`, `CustomizationID`, `ProfileID` | **R** | H: SB §4.24c, §12.2; RM §13A | These identify the serialization, not commercial identity. |
| FO-21 | Source raw payload and generated outbound artifact | Original/pre-certification CFDI | Original FatturaPA, generated outbound | UBL/CII representation(s) | **R** | H: SB §4.24c; RM §13A | Store hashes, artifact references and mapping versions. |
| FO-22 | Fiscal UUID / authority-assigned legal ID | CFDI fiscal UUID (`TimbreFiscalDigital`) | Authority/fiscal ID where applicable; distinguish SdI transmission ID | No generic fiscal UUID established | **E** (linked to fiscal artifact), with typed **F** reference if needed | M: SB §8, §18.3; TR native.sat | Critical ambiguity: SB places UUID in FiscalContext; candidate moves authority-generated identity to evidence. |
| FO-23 | Digital certification, seal, signature | CFDI stamp/seals/certification | Signed fiscal artifact when present | Signed artifact if required by profile | **E** plus **R** for signed bytes | M: SB §8, TR §4.23 | Pre-existing document signature vs post-clearance seal may have different owners. |
| FO-24 | Transmission/submission identifier | Provider/PAC operation ID | SdI transmission / processing ID | PA/platform transmission reference | **C** | H: SB §11, §18.4 | Never conflate with fiscal UUID or commercial invoice number. |
| FO-25 | Acceptance, rejection, validation results | PAC/authority responses | SdI outcomes | PA/platform responses | **C** for events/results; **R** for raw response | H: SB §11, §14 | Outcomes can change without commercial revision. |
| FO-26 | Cancellation decision and receipt | Illustrative authority cancellation result | Illustrative SdI-related cancellation/correction outcome | Applicable correction/response workflow | **C** for state/event; **E** for legal receipt | M/L: conceptual simulation, jurisdiction rules unverified | Preserve prior authorization; do not overwrite original artifact. |
| FO-27 | Mandate profile, rule/code-list versions | MX CFDI profile/version | IT FatturaPA profile/version | FR Extended CTC profile/version | **P** (definitions), referenced by **F/C/R** | H: SB §9, §16 | Historical reproducibility needs exact version IDs. |
| FO-28 | Lineage/source-field derivation | RFC/Serie/Folio mapping | Address / fiscal-code mappings | GROUP/DETAIL and tax-point mappings | **R** or dedicated lineage record | M: TR §4.24; RM §22 | Lineage can cross B/F/E; avoid treating it as commercial data. |

## 3. Source-derived facts versus architectural inferences

**Source-derived:** SB v0.3 separates billing, fiscal and compliance concerns; CFDI `RegimenFiscal` and `UsoCFDI` map to `FiscalPartyContext`; Italian `TipoDocumento` is local fiscal classification; `DocumentRepresentation` holds source/target syntax metadata; French stress test exposed line hierarchy, signed values, line-level parties, tax-point semantics and profile identifiers. RM v0.3 models an optional 1:1 `FiscalContext` and 0:N `ComplianceTransaction` records. TR includes `DocumentControl` and format-native bags.

**New architectural proposals:** `FiscalEvidence` as distinct owner of externally conferred identifiers; `BillingDocumentRevision` frozen issuance snapshot; independently versioned fiscal interpretations; separate submission attempts and processing events; strict single-owner rule. These are **not** current approved entities.

**Not yet verified:** actual mandatory fields and schema versions, real CFDI/PAC certification/cancellation response payloads, actual SdI messages, official French Extended CTC structure and production-valid samples. The French stress-test evidence is documented analysis, not an independently inspected fixture in this session.

## 4. The ownership conflicts that matter

| Conflict | Existing model position | Proposed distinction | Validation needed |
|---|---|---|---|
| Authority UUID | SB §8: `FiscalContext.fiscalIdentifiers[]` | Immutable evidence owns issuance; FiscalContext may reference fiscal identity | Certified CFDI and correction/cancellation fixture |
| Signature | SB §8: `FiscalContext.signature` | Distinguish signed source artifact, pre-submission signature, authority seal and receipt | Before/after signed payloads |
| Tax point | SB core `TaxPoint` and fiscal context both mention tax point | One authoritative `TaxPoint` owner; profile-specific interpretation separate | French sample field lineage |
| Document type | Core `documentType` and local `fiscalDocumentType` | Separate normalized business type from local classification | CFDI and FatturaPA code mapping |
| One FiscalContext per document | RM v0.3 optional 1:1 | Candidate 0:N versioned fiscal interpretations per exact billing revision | Two genuinely distinct fiscal interpretations of one revision |
| Native data | TR `FormatNativeBag` | Raw syntax retained in representation; governed extensions only for distinct semantics | Round-trip preservation test |

## 5. Comparison of architecture options against observed field ownership

| Criterion | A: embedded immutable FiscalContext | B: independently versioned FiscalContext | C: hybrid intrinsic semantics + interpretation + evidence |
|---|---|---|---|
| CFDI local regime/use known at issue | Good | Good | Good |
| CFDI UUID arrives after certification | Works if evidence is external | Works if evidence is external | Works if evidence is external |
| FatturaPA business type vs fiscal subtype | Works with typed substructure | Works | Works |
| France tax point, signed lines and hierarchy | Works if B keeps intrinsic meaning | Risk of moving reusable facts out of B | Explicitly keeps reusable facts in B |
| Distinct profile interpretations on one revision | Requires separate embedded snapshots or structural extension | Natural | Natural |
| Complexity | Lowest | Higher | Higher; needs strict owner dictionary |
| Proven decisive by the three project-source scenarios? | **No** | **No** | **No** |

**Assessment:** The matrix supports separating *intrinsic billing/tax meaning* from *local fiscal classifications*, *serialized artifacts*, *process state* and *authority evidence*. It **does not prove** that `FiscalContext` must be an independently versioned aggregate root. Option C is a useful leading design experiment, not a justified final selection. Options A/B/C remain open.

## 6. Provisional boundary rule for CTC-003 preparation (not accepted)

1. If the fact describes what was commercially supplied, billed or taxed, prefer **B** even if only one country currently exposes it.
2. If it classifies that same fact under a particular jurisdiction's fiscal vocabulary, prefer **F**, tied to an exact profile version.
3. If it describes the bytes, format or mapping used to exchange the fact, prefer **R**.
4. If it describes an action, attempt, validation or outcome, prefer **C**.
5. If it is an externally conferred identifier, seal or legal receipt, consider **E**, and link it to the precise representation and compliance outcome.
6. If it is a rule rather than a fact, prefer **P**.
7. If a field spans categories, model **two distinct meanings** with explicit provenance, rather than duplicating one mutable value.

## 7. Decision gates and next evidence collection

- **Gate G1:** Obtain a genuine CFDI 4.0 *pre- and post-certification* pair with fiscal UUID, stamp, provider metadata and cancellation outcome. Map FO-22/23/26.
- **Gate G2:** Obtain a FatturaPA payload plus SdI acknowledgement/rejection or related response; map fiscal type vs processing ID.
- **Gate G3:** Obtain the French Extended CTC sample used in v0.3 stress testing; verify GROUP/DETAIL, negative values, line parties and tax point at source paths.
- **Gate G4:** Construct one case where a single immutable revision has two materially different jurisdictional fiscal interpretations (not merely two formats or destinations). If no credible case is found, do not add 0:N fiscal interpretation cardinality solely on speculation.
- **Gate G5:** Run field-by-field loss/reversibility and ownership collision tests, including original, normalized, outbound and response representations.

**CTC-002 disposition:** Keep **In Progress**. The conceptual ownership matrix is ready for review; regulatory and sample-based validation remains open. Do not mark any ADR accepted, or change `MODEL-BASELINE.md`, on this evidence alone.

## 8. Proposed project checkpoint

- **Finding F-002-17 (proposed):** Commercial/fiscal type codes may encode both normalized business kind and local fiscal subtype; they require distinct owned concepts and mapping lineage.
- **Finding F-002-18 (proposed):** Authority-generated identifiers and certification evidence need ownership separate from submission status; precise FiscalContext/Evidence relationship remains unresolved.
- **Finding F-002-19 (proposed):** France Extended CTC line hierarchy, signed amounts and line parties are reusable billing semantics, not justification for a France-specific core schema.
- **Finding F-002-20 (proposed):** Field-ownership evidence supports semantic separation but does not yet justify independently versioned FiscalContext cardinality.
- **Decisions:** All three A/B/C options remain **Proposed / Under investigation**; no approval.
- **Next action:** Validate G1–G4 against authentic, versioned samples, then review the proposed aggregate boundary and start CTC-003 only after CTC-002 sign-off.
