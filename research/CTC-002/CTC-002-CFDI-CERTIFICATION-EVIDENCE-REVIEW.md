# CTC-002 — CFDI 4.0 Certification Evidence and Aggregate Ownership

**Date:** 2026-10-19  
**Status:** Research draft — no ADR accepted  
**Task:** CTC-002 (semantic aggregate boundaries)

## 1. Scope and source status

Validate the before/after certification distinction for Mexican CFDI 4.0, with focus on ownership of commercial identity, fiscal classifications, certified representations, and evidence. The original project model sources are `semantic-billing-model(1) (1).md` v0.3, `relational-data-model(1) (1).md` v0.3, and `CTC-002-FISCAL-FIELD-OWNERSHIP-MATRIX.md`. The available project register copies may predate later conversational checkpoints; this report does not overwrite them.

### Evidence sources

- SAT official CFDI 4.0 / Timbre Fiscal Digital 1.1 documentation: https://www.sat.gob.mx/cs/Satellite?blobcol=urldata&blobkey=id&blobtable=MungoBlobs&blobwhere=1461176340698&ssbinary=true
- SAT official explanation of the certification complement: https://wwwmat.sat.gob.mx/consulta/46336/complemento-para-facturas-electronicas
- Public CFDI 4.0 empty XML template (structural example, not a valid completed invoice): https://github.com/facturacionmoderna/Comprobantes/blob/master/CFDI_40/CFDI40_estructuraGral_XML.xml
- Public demonstration CFDI 4.0 example with placeholder signatures (not evidence of genuine certification): https://www.taxten.com/en/samples/mx-cfdi40.xml

**Evidence limitation:** No cryptographically verified pre/post certification pair from the *same* real transaction was established. Consequently, no claim of signature validation, authenticity, or production-valid fiscal compliance is made.

## 2. Before/after field-ownership matrix

| XML path / field | Before timbrado | After timbrado | Semantic meaning | Candidate authoritative owner | Confidence |
|---|---|---|---|---|---|
| `cfdi:Comprobante/@Serie` | Optional, if used | Retained | Supplier document series | BillingDocument | High — schema |
| `cfdi:Comprobante/@Folio` | Optional, if used | Retained | Supplier document number | BillingDocument | High — schema |
| `cfdi:Comprobante/@Fecha` | Present | Retained | Issuance date/time | BillingDocument | High — schema |
| `cfdi:Emisor/@Rfc` | Present | Retained | Seller tax identifier | BillingDocument Party/TaxRegistration | High — schema |
| `cfdi:Emisor/@RegimenFiscal` | Present | Retained | Seller's Mexican fiscal regime classification | FiscalContext / FiscalPartyContext | High — schema |
| `cfdi:Receptor/@UsoCFDI` | Present where required | Retained | Recipient's fiscal use classification | FiscalContext / FiscalPartyContext | High — schema |
| `cfdi:Comprobante/@SubTotal`, `@Total` | Present | Retained | Monetary totals | BillingDocument | High — schema |
| `cfdi:Comprobante/@Sello` | Present on signed input | Retained | Issuer digital signature | DocumentRepresentation + signature evidence | High — schema |
| `cfdi:Comprobante/@NoCertificado` | Present on signed input | Retained | Issuer certificate serial | Representation signature metadata | High — schema |
| `cfdi:Complemento/tfd:TimbreFiscalDigital` | Not yet present | Added after successful certification | Fiscal stamp/certification complement | Certified DocumentRepresentation + FiscalEvidence | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@UUID` | Not yet assigned | Present | Authority fiscal identifier for stamped CFDI | FiscalIdentity linked to certified artifact | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@FechaTimbrado` | Not yet present | Present | Certification timestamp | FiscalEvidence | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@RfcProvCertif` | Not yet present | Present where specified | Certifying provider identity | FiscalEvidence / provider metadata | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@SelloCFD` | Not yet present in stamp | Present | Issuer seal copied into stamp | FiscalEvidence (cryptographic relation to representation) | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@NoCertificadoSAT` | Not yet present | Present | SAT certificate serial | FiscalEvidence | High — SAT official documentation |
| `tfd:TimbreFiscalDigital/@SelloSAT` | Not yet present | Present | SAT digital seal | FiscalEvidence + certified artifact | High — SAT official documentation |
| PAC request/response correlation | External to CFDI XML | External to CFDI XML | Technical submission tracking | ComplianceTransaction / SubmissionAttempt | Architectural inference; provider API evidence pending |

**Important:** 'Retained' describes expected semantic continuity; byte-for-byte preservation and exact signature behavior require a verified pair and should not be assumed from template examples.

## 3. Candidate instance sequence

### Before certification

- `DOC-001` — BillingDocument logical identity, supplier series/folio, parties, amounts.
- `REV-001` — frozen commercial revision, if the revision concept is adopted.
- `FC-001` — fiscal interpretation with Mexican fiscal regime and recipient-use classifications.
- `REP-001` — original source representation.
- `REP-002` — prepared signed CFDI 4.0 representation, no TFD.
- `CT-001` — certification operation; `ATT-001` — transmission attempt (both candidate entities).

### After successful certification

- `DOC-001`, `REV-001` and the commercial meaning remain unchanged.
- `REP-002` remains historically identifiable.
- `REP-003` is the new certified CFDI representation containing the TFD complement, with its own content hash.
- `EVD-001` captures stamp evidence (UUID, timestamp, provider and seals) and links to `REP-003`.
- `CT-001` gains an append-only certification event; its current status is a projection.

**Identity invariant:** `Serie`+`Folio` is not the same identity as `TimbreFiscalDigital/@UUID`; a PAC submission ID is different again.

## 4. Architecture options against the evidence

| Question | A: Embedded immutable FiscalContext | B: Independent FiscalContext | C: Hybrid |
|---|---|---|---|
| Can preserve pre/post XML separately? | Yes, if representations separate | Yes | Yes |
| Can preserve UUID and certification evidence without changing commercial content? | Yes, if evidence separate | Yes | Yes |
| Can preserve fiscal regime as issued? | Yes, embedded snapshot | Yes, referenced interpretation | Yes, intrinsic/context split |
| Does SAT evidence prove multiple FiscalContexts are necessary? | No | No | No |
| Does SAT evidence support separate representation/evidence identity? | Yes | Yes | Yes |

**Interpretation:** The evidence strongly supports independent certified artifact and fiscal-evidence records. It does **not** discriminate decisively between A/B/C for FiscalContext cardinality. Keep all options open.

## 5. Proposed findings (not accepted ADRs)

- **F-002-21:** SAT's TFD 1.1 complement introduces fiscal identity and certification metadata after certification; these are not supplier-issued invoice numbers. Evidence: SAT official TFD documentation. Confidence: high.
- **F-002-22:** A prepared CFDI and certified CFDI are distinct representations of related commercial meaning. Evidence: SAT complement placement and process description. Confidence: high.
- **F-002-23:** Fiscal UUID, certification timestamp, certifier identity and seals should be separately traceable and linked to the exact certified artifact. Evidence: SAT fields; ownership is architectural inference. Confidence: medium-high.
- **F-002-24:** The certification delta alone does not establish whether FiscalContext is embedded or independently versioned. Evidence: comparison of options; confidence: high as a design conclusion.
- **F-002-25:** Public sample evidence is insufficient to claim an authenticated, cryptographically verified pre/post pair. Confidence: high; open evidence gap.

## 6. Evidence gates before CTC-002 approval

1. Obtain an authorized, redacted pre-timbrado and post-timbrado pair from the same transaction, with verifiable cryptographic artifacts, or suitable official test fixtures.
2. Verify exact XML deltas, hashes, certification signatures and the original/complement relationship.
3. Obtain representative PAC response/transport examples to distinguish submission ID, UUID and provider response correlation.
4. Test the same identity/representation/evidence ownership against Italian SdI acknowledgements and a French Extended CTC artifact.
5. Run an independent-fiscal-interpretation scenario that genuinely requires two distinct contextual snapshots; only then decide A/B/C.

## 7. Checkpoint

- Task: CTC-002, in progress.
- ADR approvals: none.
- Proposed architecture: keep embedded, independent and hybrid alternatives.
- Model baseline: unchanged.
- Suggested register update: add F-002-21 through F-002-25 as proposed findings; log this research session. No authoritative files were edited by this report.
