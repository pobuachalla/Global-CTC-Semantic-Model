# CTC-003 — T03 Monetary Contribution Contract and Source-Based Test

**Version:** Draft 0.4 | **Date:** 2026-10-20 | **Task:** CTC-003 | **Decision status:** T03 PROPOSED (not accepted)

## 1. Scope and authority

Approved and unchanged: D2 logical contract, I-01..I-10, P1..P7; T01 distinct TaxRegime/TaxApplication and T02 TaxSummary derived grouping with separately preserved source assertions. This report proposes a refinement of T03, not a new approval or a revision to T01/T02. Current GitHub HEAD was not read. The earlier Draft 0.3 and 24-assertion synthetic stress test are source inputs.

## 2. Formal conceptual contract (candidate)

**TaxApplication:** `applicationId`, `regimeRef`, `economicScopeRef`, `fiscalRole` (e.g. CHARGE, WITHHOLD, INFORMATIONAL, RECOVER), `taxAmountAssertion` (Money with source sign, currency and provenance), `taxMagnitude` (nonnegative Money, derivation trace), `calculationBasis` (base/rate/method as available), `sourceClassificationRefs`, `factProvenanceRefs`.

**MonetaryBasis:** `basisId`, `scopeRef`, `currency`, `basisType` (TAX_EXCLUSIVE_NET | TAX_INCLUSIVE_GROSS | OTHER_EXPLICIT), `includedTaxApplicationRefs`, `includedAdjustmentRefs`, `basisAmount` (source asserted or derived), `basisProvenance`. The inclusion list must be explicit or provably derived. Unknown inclusion means contribution cannot be safely inferred.

**MonetaryEffect:** `effectId`, `applicationRef`, `basisRef`, `effectAmount` (signed Money), `effectKind` (ADD | DEDUCT | INCLUDED_ALREADY | REPORT_ONLY | UNDETERMINED), `calculationRuleRef`, `profilePackageRef`, `inputFactRefs`, `origin` (SOURCE_ASSERTED | DERIVED), `evaluatedAt`. `effectAmount` is relative to the named `MonetaryBasis`, **not** a universal property of TaxApplication. It must not become a second authoritative source tax amount.

**DocumentEconomicEffect:** `documentRef`, `documentType`, `presentationAmount` (Money), `effectPerspective` (seller receivable, buyer payable, ledger posting, etc.), `economicDelta` (Money), `polarityRuleRef`, `sourceDocumentRelationshipRef`. Do not infer polarity from document type alone; a credit note may include negative lines.

**TaxSummaryAssertion:** `sourceRepresentationRef`, `sourcePath`, `groupingDimensions`, `assertedTaxAmount` (Money), `provenanceRef`.

**TaxSummaryCalculation:** `groupingDimensions`, `applicationRefs`, `computedTaxAmount` (Money), `formulaVersion`, `roundingPolicyRef`, `provenanceRefs`. Source assertions and calculations remain distinct under T02.

**MonetaryReconciliation:** `basisRef`, `effectRefs`, `computedAmount`, `sourceAssertedAmount`, `difference`, `toleranceRuleRef`, `roundingPolicyRef`, `status` (PASS | FAIL | NOT_EVALUABLE), `profilePackageRef`. A missing necessary basis or policy yields NOT_EVALUABLE, not a guessed value.

## 3. Proposed invariants (T03-I01..I10; all unapproved)

1. Preserve source amount, sign, currency, scheme and original representation (P3/P7).
2. Tax magnitude is nonnegative, but the source asserted tax amount may be signed.
3. Fiscal role is not an arithmetic operator; effect requires an explicit basis and rule.
4. A tax already included in the selected reconciliation basis is not added again.
5. One economic effect is counted at most once per reconciliation path; no line/document aggregate duplication.
6. Credit-note presentation values are not automatically negated; economic polarity is perspective- and profile-specific.
7. Monetary additions require matching currency, or an explicitly versioned conversion.
8. Rounding stage, precision and mode must be specified by a versioned policy before a derived amount is authoritative.
9. Source-stated totals/summaries are never overwritten by derived totals; discrepancies become reconciliation findings.
10. Missing basis, conversion or interpretation provenance must yield NOT_EVALUABLE instead of silent defaulting.

## 4. Source-based validation: Peppol BIS Billing 3.0 May 2026

**Published example:** Peppol BIS Billing credit-note example shows `CreditNoteLine` line extension amounts **2800** and **-1500**, `ChargeTotalAmount` **25**, `TaxExclusiveAmount` **1325**, and `TaxInclusiveAmount` / `PayableAmount` **1656.25**. Its example tax rate is **25%**. See [official specification](https://docs.peppol.eu/poacc/billing/3.0/bis/). The official syntax [credit note structure](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/tree/) defines the monetary elements.

Reconciliation: 2800 + (-1500) = 1300; 1300 + 25 = 1325; 1325 * .25 = 331.25; 1325 + 331.25 = 1656.25. This is a *published excerpt*, not a downloaded, complete schema-validated invoice. The assumption that a full reversal would have a seller-receivable delta of -1656.25 is **our illustrative accounting perspective**, not a value encoded in the excerpt.

**Price example:** Official Peppol [calculation guidance](https://docs.peppol.eu/poacc/billing/3.0/bis/) shows a price before discount of 450, price discount of 40 and net price of 410. **Gross price here means pre-discount, not VAT-inclusive.** The [price definition](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-InvoiceLine/cac-Price/) requires net price exclusive of VAT.

**Published VAT calculation rules:** [BR-CO-13](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-TaxExclusiveAmount/), [BR-CO-15](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-TaxInclusiveAmount/), and [BR-CO-17](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-TaxTotal/cac-TaxSubtotal/cbc-TaxAmount/) support the selected arithmetic checks. These do not authorize a global tax calculation policy.

## 5. Constructed inclusive source price test (evidence gap remains)

Constructed gross VAT-inclusive price 120 at 20% => net 100, tax 20. If reconciliation begins from gross 120, tax additional contribution is 0; if it begins from net 100, additional contribution is +20. Both lead to 120. **This is not a real source invoice fixture** and the published Peppol credit note does not fill the inclusive-*unit-price* evidence gate.

## 6. Test execution and result

`python tests/test_contract.py` => **16/16 focused assertions pass**. Includes published-excerpt arithmetic, negative credit-note line preservation, source-derived price-before-discount example, constructed inclusive price, rounding, summary discrepancy, currency guard and withholding sign. This is not a full XML parse, XSD/Schematron validation, tax authority test, or legally certified invoice.

## 7. Decision assessment

**T03 should remain Proposed.** The source-based credit-note example strengthens the distinction between document presentation and economic effect; the inclusive price scenario is still synthetic. Recommend T03 contract with `MonetaryBasis` + `MonetaryEffect` as a candidate **logical** model, but defer final field/cardinality decisions until a genuine inclusive-price source payload and at least one jurisdiction-specific withholding example have been mapped with provenance.

## 8. Follow-up evidence gates

- E-T03-01: Obtain licensed, complete, versioned invoice with source VAT-inclusive unit price (not merely tax-inclusive document total), and test its mapping to net/total with preserved source value.
- E-T03-02: Obtain complete Peppol CreditNote fixture or published complete sample and run official XSD + Schematron; verify presentation amounts and relationship to corrected invoice.
- E-T03-03: Obtain an official or verified withholding source sample and show payable effect versus reported tax without double negation.
- E-T03-04: Validate mixed tax currencies, rounding stage and source summary variances with profile-specific rules.

## 9. Session checkpoint

- CTC-003: In Progress.
- Accepted: T01, T02, D2, P1-P7, I-01..I-10 unchanged.
- Proposed: T03 and T03-I01..I10; no new accepted ADR.
- Findings proposed: F-003-07 (credit-note presentation not globally signed); F-003-08 (tax-inclusive document total differs from tax-inclusive unit price); F-003-09 (effect is basis-relative); F-003-10 (missing rule inputs require NOT_EVALUABLE).
- Project records: not modified; GitHub remote not updated.
- Next: Review proposed T03 logical contract and seek complete inclusive-price and credit-note fixtures before approving.
