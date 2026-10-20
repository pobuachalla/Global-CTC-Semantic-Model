# CTC-003 — T01/T02 approvals and T03 sign test

**Date:** 2026-10-20 | **Status:** T01/T02 accepted; T03 proposed/provisional | **Scope:** Synthetic arithmetic only

## Decision disposition

- **T01 Accepted:** Separate TaxRegime and TaxApplication. Every application references exactly one tax regime and explicitly identified economic scope; no duplicate application from document-level summary.
- **T02 Accepted:** TaxSummary is a derived grouped/reconciled view, with independently preserved source-supplied summary assertions. Source assertions do not become additive applications.
- **T03 Proposed:** Nonnegative tax magnitude plus explicit signed payable contribution and separate fiscal direction. It is *not* an approved global sign policy.

## Five scenarios

| Scenario | Signed line total | Tax applications (direction; magnitude; payable contribution) | Tax contribution sum | Illustrative payable | Result |
|---|---:|---|---:|---:|---|
| Positive invoice | 1000.00 | CHARGE; 100; +100 | +100 | 1100.00 | PASS |
| Negative line | 800.00 (1000-200) | CHARGE; 80; +80 | +80 | 880.00 | PASS |
| Withholding | 1000.00 | CHARGE; 100; +100 / WITHHOLD; 50; -50 | +50 | 1050.00 | PASS |
| Credit note | -1000.00 | CHARGE; 100; -100 | -100 | -1100.00 | PASS |
| Informational tax | 1000.00 | INFORMATIONAL; 75; 0 / CHARGE; 100; +100 | +100 | 1100.00 | PASS |

The calculations represent a **synthetic seller-receivable adjustment model** and are not universal invoice/credit-note tax or payable formulas. The credit-note negative total is an economic delta, not necessarily the displayed legal document amount. The informational-tax case does not claim a particular country's tax treatment.

## Preliminary semantic rule under test

`payableDelta = sum(contributing signed lines) + sum(explicit tax payable contributions)`, *only* in a fixture with no document-level charges/allowances, advances, rounding, price-inclusive taxes or currency conversions. Each application carries a positive magnitude and a separately signed payable contribution. Fiscal direction is descriptive and must not trigger a second sign inversion.

### Reconciliation and ownership implications

- Tax application is authoritative for its asserted or derived scoped tax value, with provenance.
- Tax summary groups applications; source-stated tax subtotal remains separately preserved and is compared against calculated summary.
- A tax may be reportable but have zero payable contribution.
- `direction=CHARGE` does not always imply positive contribution (credit/reversal).
- `payableContribution` might be derived from effect/polarity and inclusion rules rather than an independent source assertion: **unresolved P6 issue**.
- No profile-based rounding tolerances, currency reconciliation or mixed inclusive/exclusive tax tested.

## Open questions before T03 approval

1. Is contribution a stored immutable derived fact, or an on-demand deterministic projection?
2. How do reversal polarity, credit-note presentation and tax direction interact?
3. How are tax-inclusive prices and taxes already included in line totals represented?
4. Can a reportable tax affect payable in some profiles but not others?
5. Which currency, rounding precision, tolerance and rate versions govern each sum?
6. How should source-stated summary amounts and totals be reconciled without overwriting them?

## Test reproducibility

Run `python tests/test_tax_signs.py`. The script uses Python Decimal and writes `tests/test-results.json`. It passed 5/5 on 2026-10-20. This does not validate XML, tax-law applicability, official jurisdictional rules or source fixtures.

## Governance

P1–P7 and D2/I-01..I-10 remain accepted. FiscalContext A/B/C physical choices deferred. CTC-003 remains In Progress; detailed dictionary not accepted.
