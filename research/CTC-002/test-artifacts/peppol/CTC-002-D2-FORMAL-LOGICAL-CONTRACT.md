# CTC-002 — Formal D2 Logical Fiscal Interpretation Contract and Peppol Mapping Validation

**Date:** 2026-10-20  
**Status:** Proposed formal logical contract; D2 direction previously validated by user; detailed schema and FiscalContext A/B/C not approved.  
**Scope:** Semantic contract and focused mapping validation only; no relational schema, API design or production conformance claim.

## 1. Basis and evidence tiers

**Internal sources:** Global Semantic Billing Model v0.3; CTC-002 D2 synthetic replay prototype; approved CTC-002 principles P1–P7; earlier SemanticDocument v1.0. These support the separation of billing meaning, fiscal classifications, representations, compliance state and provenance. Earlier D2 replay showed reproducibility only for fictional profile rules.

**External authoritative source:** OpenPeppol, *Peppol BIS Billing 3.0 — May 2026 release* (https://docs.peppol.eu/poacc/billing/3.0/). The Peppol specification documents UBL business-term mappings, profile identifiers, and arithmetic business rules. We have tested a constructed UBL document against selected published mapping paths and arithmetic checks, not the entire Peppol conformance suite.

## 2. Contract boundaries (implementation-neutral)

| Logical concept | Minimal properties | Cardinality hypothesis | Authoritative owner / invariant |
|---|---|---|---|
| BillingDocument | platform document identity, document family | one per logical document | Stable identity distinct from legal fiscal and transmission IDs (P4) |
| PublishedRevision | revision identity, parent document ID, semantic version, fingerprint, publication marker, intrinsic billing/tax facts | document 1..N revisions | Immutable published values (P2); publication trigger TBD |
| SourceFiscalFact | fact ID, semantic concept, original value, scheme, source artifact/path, origin, source observation | revision 0..N | One authoritative source value (P6); not silently rewritten by interpretation (P7) |
| FiscalInterpretation | interpretation ID, exact revision ID/fingerprint, profile package identity/fingerprint, interpretation purpose, derived facts | revision 0..N candidate; unresolved | Immutable evaluated result; no implicit 'latest' in historical links |
| DerivedFiscalFact | fact ID, semantic concept, normalized/derived value, derivation type, input fact IDs, rule/profile/code-list references | interpretation 0..N | Never masquerades as original fact (P7) |
| ProfilePackage | profile and release, rule/mapping/code-list IDs + versions, immutable package fingerprint, effective-date context | one per interpretation | Historical reproducibility requires preserved package bytes and external inputs, not just version labels |
| DocumentRepresentation | artifact ID, syntax/profile, original bytes reference, content hash, provenance | revision 0..N | Original and generated artifacts independently identifiable (P3) |
| ComplianceTransaction | operation ID, exact revision/interpretation/representation references, obligation/destination | revision 0..N | Processing separate from billing; distinct histories (P1/P5) |
| FiscalIdentity/Evidence | typed authority identity, issuing party, linked certified artifact, evidence bytes/hash | operation 0..N | Never confuse commercial, authority and submission identifiers (P4) |

**Note:** 0..N fiscal interpretations is a logical *capability candidate*, not approval of independent aggregate roots or physical cardinality. The absence of an interpretation does not mean an invoice lacks intrinsic tax facts. All identifiers and relationships are abstract semantic concepts; JSON examples are one test realization.

## 3. Mandatory invariants for the candidate contract

1. **I-01:** An interpretation references a specific published revision and its fingerprint. Re-evaluation never mutates that revision.
2. **I-02:** Each source fact has one authoritative owner and preserves its source representation and source path.
3. **I-03:** Derived facts identify their input fact IDs, rule version, profile release and classification scheme. Enrichment from external lookups additionally requires snapshot/time/source.
4. **I-04:** A submission must pin exact interpretation and representation IDs; a mutable 'current' profile is insufficient for audit.
5. **I-05:** Profile package identity must be content-addressable or otherwise immutable; human-readable versions alone are insufficient for reproducibility.
6. **I-06:** Derived classifications are not permitted to overwrite original source classifications. Contradictions are modeled as distinct assertions with provenance and validation outcomes.
7. **I-07:** Status changes, authority receipts and retry outcomes do not mutate billing or interpretation facts.
8. **I-08:** Target syntax/profile identifiers belong to representation or processing context, not commercial invoice identity.
9. **I-09:** Monetary arithmetic and decimal precision are validated using the selected target profile; no universal assumption of two decimal places is embedded in the global semantic core.
10. **I-10:** Semantic equivalence and legally compliant target representability are separate validation gates.

## 4. Focused jurisdictional mapping: Peppol BIS Billing 3.0 (May 2026)

This test uses **actual published Peppol/UBL paths and rules** and a **locally constructed illustrative XML fixture**. It is not a retrieved official test invoice, nor evidence of Peppol network acceptance. Seller and buyer are fictional.

| UBL path (relative to Invoice) | Meaning | D2 logical target | Ownership | Provenance treatment |
|---|---|---|---|---|
| `cbc:ID` | Invoice number (BT-1) | PublishedRevision.documentNumber | Billing | SOURCE_SUPPLIED |
| `cbc:IssueDate` | Issue date | PublishedRevision.issueDate | Billing | SOURCE_SUPPLIED |
| `cbc:DocumentCurrencyCode` | Invoice currency | PublishedRevision.currency | Billing | SOURCE_SUPPLIED |
| `cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID` | Seller tax ID | PublishedRevision.sellerTaxIdentifier | Billing party snapshot | SOURCE_SUPPLIED |
| `cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:ID` | VAT category code | SourceFiscalFact.sourceTaxCategory | Billing tax/source fiscal fact | SOURCE_SUPPLIED, preserve scheme |
| `cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent` | VAT rate | PublishedRevision.tax.ratePercent | Billing tax | SOURCE_SUPPLIED |
| `cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount` | VAT taxable base | PublishedRevision.tax.base | Billing tax | SOURCE_SUPPLIED |
| `cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount` | VAT amount | PublishedRevision.tax.amount | Billing tax | SOURCE_SUPPLIED |
| `cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount` | Net invoice total | PublishedRevision.totals.taxExclusive | Billing | SOURCE_SUPPLIED; reconcile BR-CO-13 |
| `cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount` | Gross invoice total | PublishedRevision.totals.taxInclusive | Billing | SOURCE_SUPPLIED; reconcile BR-CO-15 |
| `cbc:CustomizationID` | Specification identifier (BT-24) | DocumentRepresentation.customizationId | Representation | SOURCE_SUPPLIED; retain original URI |
| `cbc:ProfileID` | Business process type (BT-23) | DocumentRepresentation.profileId | Representation/process | SOURCE_SUPPLIED; retain original URI |

**Derived mapping example:** The locally authored rule `VAT-CATEGORY-S-MAP` maps source VAT category `S` to normalized `STANDARD_RATE`. The category `S` is an actual Peppol category; the named normalized enum and rule are *our candidate design*, not an official Peppol output. It is stored as DerivedFiscalFact, with a reference to source fact SF-VAT-CATEGORY, mapping/rule version and profile release.

**Important qualification:** The sample's 20% rate is chosen for arithmetic testing only, not asserted as the legally correct rate for the fictional supplier/buyer scenario. Real VAT treatment depends on transaction facts and applicable law.

## 5. Executed test and outputs

Files: `sample-ubl-invoice.xml`, `validate_mapping.py`, `BILLING-REVISION.json`, `FISCAL-INTERPRETATION.json`, `VALIDATION-RESULT.json`.

The script parses UBL XML with namespace-aware XPath, extracts the mapped fields, creates a frozen revision fingerprint and derived interpretation with explicit source provenance. It checks:

1. XML well-formedness.
2. Presence of mapped fields.
3. Tax-exclusive total equals sum of line net amounts in this simple no-adjustment fixture (selected BR-CO-13 case).
4. Tax-inclusive total equals tax-exclusive total plus VAT (BR-CO-15 case).
5. VAT amount agrees with the illustrative rate and base.
6. Specification identifier has the Peppol required prefix.
7. Source fact and derivation provenance are recorded.
8. Revision fingerprint is pinned by the interpretation.

**Execution result: 8 focused checks passed.** Source XML SHA-256: `29972eafe2aa7fa1c343925f2081536a4938bab4741893436624beab5bf890eb`.

**Not executed:** full UBL 2.1 XSD validation; Peppol Schematron/business-rule package; VAT legal correctness; signature checks; real provider submission; exact historical replay with archived immutable mapping/code-list packages. The prototype intentionally sets `codeListVersion` and `packageDigest` to `NOT_ARCHIVED`, so **P7's full historical reproducibility requirement is not yet satisfied by this jurisdictional test**. The earlier fictional two-profile replay is a separate test.

## 6. Findings and architecture decision assessment

- **F-002-45 (proposed):** Real Peppol UBL paths can be mapped to D2's billing, source-fiscal, derived-fiscal and representation concerns without changing a published revision.
- **F-002-46 (proposed):** Peppol VAT category `S` can be preserved as a source fact while a normalized treatment is separately derived; this is a concrete example of P6/P7 semantic ownership.
- **F-002-47 (proposed):** Peppol `CustomizationID`/`ProfileID` must not be confused with the seller-issued invoice number; D2 representation metadata supports this.
- **F-002-48 (proposed):** The tested arithmetic invariants hold for the constructed fixture, but the result does not prove full Peppol compliance or legal VAT correctness.
- **F-002-49 (proposed):** Complete replay under P7 requires immutable profile/mapping/code-list package content and all relevant external enrichment inputs; current Peppol fixture does not establish that archive.

**Recommendation:** D2 is suitable as the *candidate logical fiscal interpretation interface* for CTC-003 planning, but this mapping does not establish independent FiscalContext aggregate roots or prove a case needing multiple interpretations. Keep FiscalContext A/B/C and physical placement deferred. Seek explicit approval of the formal contract before promoting it to MODEL-BASELINE.md. CTC-002 remains Review/evidence-gated pending that approval and any agreed acceptance-gate exceptions.

## 7. Official sources

- Peppol BIS Billing 3.0 May 2026 specification: https://docs.peppol.eu/poacc/billing/3.0/bis/
- Invoice specification/process identifiers: https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cbc-ProfileID/
- Net total and BR-CO-13: https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-TaxExclusiveAmount/
- Gross total and BR-CO-15: https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-TaxInclusiveAmount/
- Peppol specification identifier rule: https://docs.peppol.eu/poacc/billing/3.0/rules/ubl-peppol/PEPPOL-EN16931-R004/

## 8. Checkpoint

**Task:** CTC-002 Review/evidence-gated. **Approved:** P1–P7 at principle level; D2 logical direction confirmed by user. **New ADRs:** none. **Proposed:** Formal contract invariants I-01..I-10 and findings F-002-45..49. **Deferred:** FiscalContext A/B/C physical ownership/cardinality; publication boundary; actual paired authority fixtures; full Peppol validator; full replay package archive. **CTC-003:** not started. **GitHub:** not modified.
