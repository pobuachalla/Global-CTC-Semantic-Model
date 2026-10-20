# CTC-003 — T03 Decision-Ready Monetary Contribution Review

**Date:** 2026-10-20  
**Status:** Decision recommendation only; T03 remains PROPOSED pending user approval.  
**Task:** CTC-003. T01/T02 Accepted; P1–P7, D2 and I-01..I-10 unchanged.

## Executive recommendation

**Approve T03 as a *logical semantic policy*, with explicit conditional evaluation and provenance; do not approve the draft entity field lists or mandatory physical storage.** `MonetaryBasis` and `MonetaryEffect` remain candidate logical concepts that implement the policy, not yet mandatory aggregate roots. This is stronger than a generic signed tax amount but narrower than approving a complete tax schema.

The policy must distinguish (1) source-asserted presentation values and source signs; (2) nonnegative tax magnitude when the format encodes magnitude; (3) fiscal direction; (4) document economic polarity and perspective; (5) reconciliation basis and already-included tax; (6) currency; (7) rounding rule and stage; (8) signed effect relative to that basis; (9) provenance and rule versions. When any required input is unknown, status is `NOT_EVALUABLE` rather than an invented amount.

## Evidence and actual coverage

| Gate | Source-backed observation | Test executed | Coverage limitation |
|---|---|---|---|
| Inclusive price | HMRC VAT Notice 700 describes extracting VAT from an inclusive price; example £180 at 20% -> £150 net, £30 VAT. HMRC VATREC16051 explicitly permits some invoice line items priced inclusive of VAT. | 4 focused checks for basis-relative contribution | **No complete, machine-readable source invoice with an inclusive *unit price* was validated.** Official worked example is source-backed calculation, not a serialized invoice fixture. |
| Withholding | SAT official CFDI 4.0 description requires nonnegative `Retencion.Importe`. Public CFDI XML example on cfdi.red shows transferred 0.06 and withheld 0.10; example is not independently validated or certified. Italian AGID Peppol rules independently require withholding type, rate, amount and scheme. | 3 checks for magnitude and signed effect on illustrative base 1.00 | Formula `1 + .06 - .10 = .96` is illustrative economic interpretation of the public example; not a PAC certification or independent legal payable validation. |
| Credit note | Official Peppol BIS Billing credit-note example excerpt: signed lines 2800 and -1500, charge 25, 25% VAT, total 1656.25. | 5 arithmetic and polarity checks | Not a complete XSD/Schematron-tested source fixture. Seller-receivable delta is illustrative and not source encoded. |
| Currency | Peppol BIS rules R051/R055 distinguish invoice currency and tax accounting currency, require same operational VAT sign. | 1 synthetic explicit FX check | No official multi-currency document fixture with actual conversion rate/date validated. |
| Rounding | Earlier CTC-003 test established line-vs-aggregate rounding risk. | 3 synthetic tests at 10%: line 0.03 vs aggregate 0.02 | No jurisdiction-specific rounding profile executed. |
| Source subtotal mismatch | T02 requires source assertion separate from calculated subtotal. | 1 synthetic variance test 100.00 vs 99.99 | No real source invoice with mismatch validated. |
| Missing inputs | P7 forbids inferred authoritative results without provenance. | 3 negative tests yield `NOT_EVALUABLE` | Synthetic contract checks. |

**Execution:** `python tests/test_t03.py` → **21/21 focused assertions passed**. No XSD, Schematron, PAC, authority, cryptographic or complete real invoice validation was performed. Do not describe the 21 assertions as regulatory conformance.

## Proposed T03 logical invariants (approval candidate)

1. Preserve original monetary assertions with original sign, currency, scope, representation and provenance.
2. Distinguish fiscal role/direction from the sign and economic effect of a tax.
3. Identify the reconciliation basis, scope, currency and which taxes/adjustments it already includes.
4. Calculate monetary effect relative to the selected basis; never double-count an already-included tax.
5. Preserve legal credit-note presentation independently of perspective-specific economic delta; never automatically negate all credit-note amounts.
6. Keep source tax summary assertions distinct from derived tax summaries; discrepancies are explicit reconciliation findings (T02).
7. Forbid cross-currency arithmetic without an explicit conversion record and provenance.
8. Apply a named rounding policy including stage, precision, method and profile version; preserve source rounded assertions.
9. Retain derivation inputs, source fact references, mapping/profile/code-list versions and calculation rule references (P7).
10. Return `NOT_EVALUABLE` for unknown inclusion, missing conversion, unresolved economic polarity or missing mandatory rounding policy; do not silently invent a payable value.

**Interpretation:** These ten statements are a *refined T03 approval proposal*, not automatic approval of previously drafted T03-I01..I10 or final entity cardinalities.

## Formal candidate types

- `TaxApplication`: tax classification, economic scope, source asserted tax amount, normalized nonnegative magnitude when meaningful, fiscal direction, tax basis and provenance. It does **not** own a universal payable contribution.
- `MonetaryBasis` (candidate): scope, currency, base amount, inclusive/exclusive semantics, included taxes and adjustments, source/derivation provenance.
- `MonetaryEffect` (candidate): tax/adjustment reference, named basis reference, signed effect, effect kind, currency, calculation rule, provenance. Not a competing source tax assertion.
- `DocumentEconomicEffect` (candidate): original legal presentation amount, effect perspective, normalized delta and polarity derivation.
- `MonetaryReconciliation` (candidate): source asserted and calculated totals, differences, tolerance/rounding rules, result including `NOT_EVALUABLE`.

## Decision options

**Recommended:** Accept the ten *logical policy statements* as T03 and retain field/cardinality details as CTC-003 Draft 0.5 pending evidence. The policy can be accepted without claiming full regulatory coverage.

**Conservative:** Keep T03 Proposed until a complete inclusive-unit-price XML/JSON invoice and certified withholding fixture are executed. This is appropriate if the project requires regulatory fixture evidence before any logical policy is accepted.

**Not recommended:** Accept a universal sign-only formula, or require every `TaxApplication` to store one fixed `payableContribution` independent of basis.

## Open evidence gates (do not close automatically)

- **E-T03-01:** Full, licensed machine-readable source invoice showing tax-inclusive *unit* price, with a documented calculation/profile.
- **E-T03-02:** Full Peppol CreditNote fixture with official XSD and Schematron validation.
- **E-T03-03:** Complete verified withholding invoice (e.g. CFDI or FatturaPA) with applicable rule and payable reconciliation.
- **E-T03-04:** Versioned mixed-currency example with source FX rate/date, tax accounting currency and rounding policy.
- **E-T03-05:** Source-asserted tax subtotal variance and jurisdiction-specific tolerance behavior.

## Sources

- HMRC VAT Notice 700: https://www.gov.uk/guidance/vat-guide-notice-700
- HMRC VATREC16051: https://www.gov.uk/hmrc-internal-manuals/vat-trader-records/vatrec16051
- SAT official CFDI 4.0 field specification (Retenciones): https://wwwmat.sat.gob.mx/cs/Satellite?blobcol=urldata&blobkey=id&blobtable=MungoBlobs&blobwhere=1461175119714&ssbinary=true
- Public third-party CFDI XML withholding example (unverified): https://factura.cfdi.red/blog-facturacion-electronica/ejemplo-de-una-factura-xml-cfdi-con-c-objetoimp-07/
- Italian AGID withholding rules: https://peppol-docs.agid.gov.it/xml/ITA/sch/peppolbis-en16931-ubl-3.0-invoice/Schematron/ITA/AGID/AGID-EN16931-EXT-UBL.html
- Peppol BIS Billing 3.0: https://docs.peppol.eu/poacc/billing/3.0/bis/
- Peppol BIS currency rules R051/R055: https://docs.peppol.eu/poacc/billing/3.0/bis/
- Previous internal report: CTC-003-T03-FORMAL-CONTRIBUTION-CONTRACT-DRAFT-0.4.md

## Session checkpoint

CTC-003 remains In Progress. T01/T02 Accepted. T03 remains Proposed pending explicit approval. No changes to P1–P7, D2, I-01..I-10. No remote GitHub changes. This package contains a standalone report, source register, and executable focused tests; it does not replace authoritative project files before decision review.
