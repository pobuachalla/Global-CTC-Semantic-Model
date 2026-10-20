# CTC-003 — T03 Extended Monetary Stress Test

**Date:** 2026-10-20  
**Status:** Research / proposed changes only. T01 and T02 Accepted; T03 Proposed (provisional).  
**Evidence:** 24/24 executable exact-decimal assertions against synthetic examples, not authority or regulatory validation.

## 1. Purpose and baseline

The earlier `CTC-003-T01-T03-DECISION-AND-SIGN-TEST.md` established a proposed nonnegative tax magnitude plus signed payable contribution and tested five basic scenarios, explicitly excluding inclusive prices, credit presentation, rounding and currency conversion. This report extends those boundaries.

Approved T01: TaxRegime and TaxApplication are distinct; each application references a regime and economic scope. Approved T02: TaxSummary is a derived grouping; source-asserted summaries are preserved independently and reconciled. T03 remains unapproved.

## 2. Results

| Scenario | Synthetic input | Result | Semantic consequence |
|---|---|---|---|
| Tax-inclusive pricing | Gross 120.00 at 20% | Base 100.00, tax 20.00, payable 120.00 | Tax already embedded in gross cannot also increase payable. |
| Mixed inclusive/exclusive lines | Gross 120.00 inclusive; 50.00 exclusive with 10% tax | Payable 175.00 | Contributions require a price-basis/inclusion context. |
| Credit and reversal polarity | Credit note displays 100.00 + 10.00 tax | Display 110.00, signed economic adjustment -110.00 | Distinguish legal document display convention from economic delta. |
| Mixed currencies | EUR net 100.00, VAT 20.00; fictional USD/EUR rate 1.10 | EUR 120.00, USD reporting 132.00 | Currency-qualified amounts and conversion provenance required. Do not sum EUR and USD. |
| Rounding | Two bases 0.05 at 10% | Per-line HALF_UP 0.02; aggregate HALF_UP 0.01 | Rounding stage, precision and mode are part of rule context. |
| Source asserted summary | Source 100.00; derived 99.99 | Variance 0.01 | Preserve both and create reconciliation finding; no silent overwrite. |
| Negative controls | EUR + USD and withholding double negation | Both detected | Explicit currency and sign semantics prevent invalid arithmetic. |

The examples are constructed and do not claim the shown rates, conventions or tolerances apply to any real jurisdiction.

## 3. Proposed T03 refinement

Separate at least five dimensions:

1. `taxAmountMagnitude` — nonnegative magnitude of tax asserted or computed in a specified currency; **candidate**.
2. `taxDirection` — fiscal role (charged, withheld, informational, recovered, etc.); **candidate**, not an arithmetic operator.
3. `documentPolarity` or equivalent economic-effect context — distinguishes invoice versus reversal effects without assuming the sign convention of legal display amounts; **candidate**.
4. `priceTaxInclusion` — whether tax is already contained in the economic amount used as the payable base; should be evaluated at the relevant line/price/tax application scope, not assumed globally; **candidate**.
5. `payableContribution` — signed amount in the payable currency *relative to a precisely defined reconciliation base*. It may be an immutable derived fact/projection with provenance rather than a separately source-authoritative amount; **unresolved**.

**Critical nuance:** A contribution of zero for inclusive tax is only correct if the reconciliation base already includes that tax. A model that first extracts the net base must add the tax back. The calculation base must therefore be explicit, not inferred from the `INCLUSIVE` flag alone.

## 4. Reconciliation design implications

- `Money` must carry currency; conversion must record original amount/currency, converted amount/currency, rate, direction, effective date, rounding policy and source/version.
- Do not mix original invoice currency and reporting currency within the same additive total.
- Preserve source-stated subtotals, tax summaries and payable assertions; derived summaries and computed totals must be separate, traceable and reconciled.
- Profile-driven rounding policies specify precision, mode, application stage (line, category, document) and tolerances. The 0.01 discrepancy in this test is not necessarily an error.
- Credit-note displayed monetary values and signed economic deltas require an explicit distinction, potentially a typed presentation/economic-effect model.
- Reconciliation formula must be conditional on the chosen base: net/exclusive versus gross/inclusive, plus allowances, charges, prepayments, withholding and rounding as applicable.
- TaxApplication scope, T01, and source/derived summary separation, T02, are unaffected.

## 5. Proposed new findings (not yet registered)

- **F-003-01:** Inclusive-tax magnitude is not necessarily an additional payable contribution; the reconciliation base controls whether it is additive.
- **F-003-02:** Credit/reversal economic polarity and legally displayed credit amounts may differ.
- **F-003-03:** Currency and conversion provenance are required to avoid adding unlike monetary units.
- **F-003-04:** Line-versus-aggregate rounding may produce different valid results; policy version is material.
- **F-003-05:** Source-asserted and calculated tax summaries can disagree without either being silently overwritten.
- **F-003-06:** Tax direction alone cannot determine payable effect; T03 needs price-inclusion and base semantics.

## 6. Open decisions

1. Whether payableContribution is a stored source assertion, immutable derived fact, or on-demand deterministic projection (P6).
2. Exact semantics and cardinalities for tax-inclusive price basis at line, adjustment and tax-application level.
3. Legal display polarity versus normalized economic delta for different credit and correction documents.
4. Conversion and rounding ownership; per-jurisdiction and per-profile requirements.
5. Tax summary aggregation grouping dimensions and reconciliation tolerances.
6. Whether a source-supplied total with missing line tax detail should be a distinct scoped assertion rather than an inferred TaxApplication.

## 7. Recommendation

**Keep T03 Proposed.** Refine it to require explicit amount magnitude, fiscal direction, economic polarity, price inclusion/reconciliation base, currency and versioned calculation provenance. Do not approve a universal payable formula. Test source-supplied inclusive-tax payloads and legally valid credit-note examples before formal approval.

CTC-003 remains In Progress. P1-P7, D2/I-01..I-10, T01 and T02 remain Accepted. FiscalContext physical aggregation remains deferred.

## 8. Reproduction

Run `python tests/test_monetary.py` from the package root. Results are written to `tests/results.json`. Expected result: **PASS 24/24**. The script requires only Python standard library. No official schema, external exchange rate, legal tax calculation, or production payload validation is performed.
