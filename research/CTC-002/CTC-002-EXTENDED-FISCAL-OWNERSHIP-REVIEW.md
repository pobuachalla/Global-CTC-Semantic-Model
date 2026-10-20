# CTC-002 — Extended Fiscal Ownership and Provenance Evidence Review

**Date:** 2026-10-20  
**Status:** Research complete for bounded pass; architecture decision deferred  
**Scope:** CTC-002 only. No new accepted ADR, no CTC-003 schema work.  
**Approved constraints:** CTC-002-P1 through P7.  
**Source precedence:** 2026-10-20 GitHub baseline plus later full P7 DECISIONS.md and SESSION-LOG.md replacements. GitHub remote HEAD not independently inspected.

## Executive assessment

The research strengthens separation of (1) intrinsic billing/tax facts, (2) jurisdictional fiscal classifications, (3) derived fiscal interpretations, (4) representation/profile metadata and (5) compliance events/evidence. It **does not prove** a requirement for an independent FiscalContext aggregate per jurisdiction or per destination. The lowest-regret design is to specify the ownership/provenance contract before committing to embedded A, independent B, or hybrid C. A hybrid conceptual *classification* is useful; this is not approval of hybrid aggregate implementation.

## Evidence taxonomy

- **Official specification/documentation:** authoritative description of syntax/rules at a named publication/version; does not certify any test fixture.
- **Repository sample:** example XML or JSON publicly described/visible, possibly synthetic, test-only or outdated; not authority-validated.
- **Internal v0.3 example:** existing project worked examples; conceptual/arithmetic only.
- **Architecture inference:** proposal extrapolated from documented semantics; explicitly unapproved.

## Field-ownership and P7 provenance matrix

| Concept / source example | Source nature | Candidate authoritative owner | Classification | Required provenance / rule |
|---|---|---|---|---|
| Invoice number, issue date, seller/buyer | Source-supplied | BillingDocumentRevision | Intrinsic | Source path, source representation, snapshot revision |
| Line amount, tax base, tax amount | Source-supplied or derived | BillingDocumentRevision.Tax/Line | Intrinsic economic meaning | Source-vs-calculated flag; arithmetic inputs and transform version |
| Party tax registration / country | Source-supplied | BillingDocumentRevision.Party snapshot | Intrinsic party fact | Identifier scheme and jurisdiction; avoid conflating identity and registration |
| Tax point date | Source or derived | Shared TaxPoint semantic concept; aggregate ownership open | Intrinsic when explicit; derived when computed | Original date vs derived date, calculation/profile provenance |
| Mexico Emisor.RegimenFiscal | Source-supplied jurisdiction code | FiscalContext candidate | Jurisdictional source fact | Exact SAT code, scheme/version, source path |
| Mexico Receptor.UsoCFDI | Source-supplied jurisdiction code | FiscalContext candidate | Jurisdictional source fact | Exact source value, code list version |
| Mexico TFD UUID / FechaTimbrado / SelloSAT | Externally conferred | Fiscal identity/evidence linked to certified representation | Fiscal identity/evidence | Issuer, timestamp, response artifact, hash, certification evidence |
| Italy TipoDocumento | Source-supplied | BillingDocument document type + fiscal subtype (distinct facts) | Shared + local classification | Preserve original TD code and mapping version; no competing owners |
| Italy Natura | Source-supplied local code | Tax treatment + local classification | Shared tax meaning + local code | Original Natura code, mapping, applicable code list |
| Italy SdI scarto/consegna | External response | ProcessingEvent/ValidationResult | Process outcome | SdI response artifact and external correlation |
| France GROUP/DETAIL, signed lines, line party | Source-supplied | BillingDocumentRevision | Intrinsic | Contribution-to-totals semantics; preserve negative signs |
| France tax exigibility code | Source-supplied or derived | TaxPoint plus jurisdictional classification | Mixed | Preserve code, mapped basis, applicable profile |
| France/Peppol UBL CustomizationID, ProfileID | Source-supplied representation metadata | DocumentRepresentation | Serialization/process profile | Exact identifiers, version, payload hash |
| Brazil NFe NCM, CFOP, CRT, CST/CSOSN | Source-supplied local codes | Classification and fiscal/tax-context candidates | Mixed: item classification, operation, regime and tax treatment | Retain exact code + scheme; don't assume all share one fiscal owner |
| Brazil ICMS, PIS, COFINS and IBS/CBS structures | Source-supplied or computed | BillingDocumentRevision.Tax + local classifications | Intrinsic calculation + local regime codes | Tax type, base, rate, direction, code, jurisdiction, mapping provenance |
| India IRN / signed authority response (candidate) | External, not fixture-validated here | FiscalIdentity/Evidence | Fiscal identity/evidence | Need official schema + paired example before field mapping |
| Peppol invoice type / tax categories | Source-supplied | BillingDocumentRevision + representation-specific code alignment | Intrinsic + mapping | Preserve original UNCL code and mapping profile |

**P6 ownership nuance:** A source field can map to multiple *distinct semantic facts* (e.g., normalized document type and local fiscal subtype). That is not duplicate ownership of the same fact. Derived projections should carry a `derivedFrom` reference rather than silently becoming second sources of truth.

## Six format families — evidence and limitations

### 1. Mexico CFDI 4.0
Official SAT describes the Timbre Fiscal Digital complement as proof of validation/certification, with fiscal folio and SAT seal assigned following validation. This supports distinct pre-certification and certified representations, and separate fiscal identity. No genuine cryptographically validated matched pair was obtained. The earlier CFDI demonstration was not a valid proof of certification.

### 2. Italy FatturaPA / SdI
Prior project documentation-backed SdI review separates rejection, delivery and failed-delivery outcomes. This supports processing-event ownership, not independent fiscal-context cardinality. A matched submitted FatturaPA XML + original SdI notification pair remains unavailable in this pass.

### 3. France Extended CTC
The project v0.3 worked example has contributing GROUP 10 EUR 21,425.59, explanatory DETAIL 11 EUR 21,425.59 (not contributing), GROUP 20 EUR -204.78; contributing total EUR 21,220.81. This demonstrates line hierarchy and signed-value requirements within the internal example, **not** validation against a current French XSD/profile. The French tax administration publishes v3.2 external specifications dated 30 April 2026 and references AFNOR XP Z12-012 (invoice/status formats), XP Z12-013 (APIs), XP Z12-014 (B2B use cases). Do not equate the older internal French profile with these automatically.

### 4. Brazil NF-e
The `brasil-fiscal/nfe` repository documents an `examples/nfe-exemplo.xml` file and MIT license, while its XSD files include tax classification structures such as IBS/CBS CST. Other publicly visible NF-e XML fixtures expose `NCM`, `CFOP`, `CRT`, `ICMS`, `PIS` and `COFINS` structures. These are evidence of source syntax and test opportunities, not verified production-valid invoices or current authoritative legal interpretations. Multiple tax families do not imply multiple FiscalContext aggregates.

### 5. India GST e-invoicing
The older project's INV-01 scenario distinguishes inter-state IGST versus intra-state CGST/SGST, but that is project-provided conceptual coverage. No authenticated, versioned government schema plus matched IRN response was downloaded and validated in this pass. Do not mark the India evidence gate passed.

### 6. Peppol BIS Billing 3.0 / UBL
The May 2026 OpenPeppol release provides examples, UBL 2.1 invoice/credit note schemas, validation rules and code lists. `CustomizationID`/`ProfileID` identify syntax and business process context; a billing-with-response process is distinct from the commercial invoice. These belong to representation metadata, not billing identity. Official downloadable examples were located but not fetched and run through validators in this environment.

## Architectural options — decision readiness

| Test | A embedded immutable | B independent fiscal context | C hybrid | Outcome |
|---|---|---|---|---|
| Original billing/tax facts preserved | Pass | Pass with discipline | Pass | Non-discriminating |
| Certified artifact and fiscal UUID | Pass with external evidence | Pass | Pass | Non-discriminating |
| SdI rejection vs delivery | Pass with process events | Pass | Pass | Non-discriminating |
| French line hierarchy / signed values | Pass if core is rich | Pass if core is rich | Pass if core is rich | Non-discriminating |
| Multiple tax regimes | Pass | Pass | Pass | Non-discriminating |
| One revision, two incompatible fiscal interpretations | Needs explicit snapshots | Native | Native | **No verified case found** |
| Historical profile re-evaluation | Needs immutable context snapshot | Independent versions | Independent versions | Unresolved requirements |
| Complexity/consistency | Lower | Higher | Higher | A simpler until evidence warrants B/C |

**Recommendation for user review, not acceptance:** Treat the semantic classification as stable and keep A/B/C deferred. A versioned *interpretation record* may be supported as an optional extension without requiring every invoice to create an independent FiscalContext aggregate. This is a design hypothesis; it needs invariants and counterexamples before approval.

## Minimal conceptual provenance contract (candidate, not approved schema)

Each derived fact should be able to answer: `value`, `semanticConcept`, `originKind` (SOURCE/DERIVED/ENRICHED/EXTERNAL), `sourceRepresentationRef`, `sourcePath`, `derivationRuleRef`, `mappingVersion`, `profileVersion`, `codeListVersion`, `effectiveAt`, `derivedAt`, `evidenceRef`, and `confidence/validationOutcome` when applicable. Not every field must be physically repeated; lineage may be held as linked records. Never fabricate missing fiscal source values.

## Evidence gates and acceptance tests

1. Download official French v3.2 package and independently obtain applicable AFNOR profile; parse a licensed representative Extended CTC fixture; compare tax point, lines, parties, profile metadata.
2. Obtain matched, permitted pre/post-certification CFDI XML with certificate/TFD and test field deltas and original artifact hashes.
3. Obtain matched FatturaPA XML and SdI notification XML (NS, RC, MC); test correlation and status dimensions.
4. Obtain Brazil NF-e current-version fixture and XSD; test multiple taxes and local fiscal classifications; distinguish homologation fixture from legally valid payload.
5. Obtain official India schema and signed IRN response pair; validate authority identity and provenance.
6. Obtain a real scenario where *one immutable billing revision* has two independently versioned fiscal interpretations, not just two formats or delivery destinations. If no case is found, document the absence rather than claiming impossibility.
7. For each fixture, record URL, license, commit/release, format/schema/profile version, parser result, XSD result, business-rule result, semantic field coverage, losses, and source-vs-derived provenance.

## Candidate new findings (pending review)

- **F-002-36:** A jurisdiction-specific source code is still a source-supplied fact; it must not be labelled as derived solely because it is local. Evidence: project v0.3 examples + P7; inference, high conceptual confidence.
- **F-002-37:** Format profile identifiers are representation provenance, not business invoice identity. Evidence: OpenPeppol May 2026 specification; high documentation confidence.
- **F-002-38:** Brazil's simultaneous tax/classification structures stress the Tax semantic core but do not prove FiscalContext multiplicity. Evidence: public NF-e schema and examples; medium inference.
- **F-002-39:** France's current 2026 external specification/profile ecosystem needs version-specific fixture validation before earlier Extended CTC assumptions are treated as compliant. Evidence: French tax authority v3.2 index; high documentation confidence.
- **F-002-40:** The researched country examples do not yet discriminate A/B/C aggregate cardinality. Evidence: reviewed documentation and unvalidated samples; high within bounded research, not proof of nonexistence.

## Source register (accessed 2026-10-20)

- SAT, TFD complement: https://wwwmat.sat.gob.mx/consulta/46336/complemento-para-facturas-electronicas
- French tax authority, external specifications v3.2 (30 April 2026): https://www.impots.gouv.fr/specifications-externes-b2b
- OpenPeppol BIS Billing May 2026: https://docs.peppol.eu/poacc/billing/3.0/
- OpenPeppol BIS profile identifiers: https://docs.peppol.eu/poacc/billing/3.0/bis/
- OpenPeppol preceding invoice reference: https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/cac-BillingReference/cac-InvoiceDocumentReference/
- Brasil Fiscal NF-e repo (MIT; examples): https://github.com/brasil-fiscal/nfe
- Brasil Fiscal NF-e tax XSD: https://github.com/brasil-fiscal/nfe/blob/main/schemas/DFeTiposBasicos_v1.00.xsd
- Public NF-e test fixture, explicitly homologation: https://github.com/nfephp-org/sped-nfe/blob/master/tests/fixtures/xml/exemplo_xml_envia_lote_modelo_65.xml

**Execution limitation:** Web-accessible specifications and source excerpts were inspected. Direct raw GitHub downloads from the analysis container were unavailable, so this is *not* a machine-executed XSD validation or full field-by-field fixture parse. This limitation is reflected in every evidence gate.
