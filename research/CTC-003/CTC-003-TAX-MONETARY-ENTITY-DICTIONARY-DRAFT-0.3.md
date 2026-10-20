# CTC-003 — Tax and Monetary Semantic Entity Dictionary

**Version:** Draft 0.3 | **Date:** 2026-10-20 | **Status:** PROPOSED, not approved  
**Task:** CTC-003 — semantic entity dictionary and cardinalities  
**Companion:** `CTC-003-DOCUMENT-COMMERCIAL-ENTITY-DICTIONARY-DRAFT-0.2.md`

## 1. Authority, scope and evidence

**Accepted constraints:** CTC-002 P1–P7; approved D2 nine-concept logical contract and I-01–I-10. Their exact accepted wording in the current Git repository must take precedence over this draft. This document does **not** accept a new ADR or amend them.

**Primary sources:** `semantic-billing-model(1) (1).md` v0.3 §§4.11–4.17, 6–7, 12.2; `CTC-Semantic-Document-Entity-Model.docx` v1.0 (2026-09-07), especially `TaxRegime`, `TaxApplication`, `RegimeTaxTotal`, `MonetaryTotal`; `relational-data-model(1) (1).md` v0.3 is comparison context only, not the source of semantic truth; commercial Draft 0.2 for line, adjustment, price, tax point and revision ownership.

**Evidence limitations:** Prior Peppol, CFDI, Malaysia and India exercises used constructed/partial fixtures; this is a source-model reconciliation, not new official-schema or fiscal-law validation. Current GitHub HEAD was not read. Jurisdiction-specific formulas, sign requirements and mandatory cardinalities are *not* asserted as universal.

**Scope:** Tax regimes, applications, calculations, withholding, aggregations, totals, monetary values, rounding, tax currencies, signed economic values and their provenance. **Out of scope:** final jurisdictional tax determination, regulatory code lists, persistence tables, clearance evidence, authority statuses and final FiscalContext physical design.

## 2. Proposed design position

Preserve `TaxRegime` as a *typed, scheme-qualified tax context* and `TaxApplication` as a *specific assessed or stated tax on a scoped economic base*. Generalize each application using the v0.3 `Tax` attributes (`direction`, `calculationMethod`, `quantityBase`, `amountPerUnit`, etc.). `TaxSummary` is an aggregation, not a second authoritative tax calculation. `MonetaryTotal` is a published document assertion plus a separately reproducible reconciliation result.

Do **not** equate `TaxRegime` with `FiscalInterpretation`: one invoice can contain several tax regimes while having one fiscal interpretation, and vice versa. Tax classifications explicitly supplied by the source remain authoritative source facts; normalized interpretations are linked through D2 provenance.

## 3. Core value types

| Type | Definition | Candidate constraints |
|---|---|---|
| `Decimal` | Base-10 numeric value, never binary floating point for semantic money/tax | Scale and rounding policy versioned; no global fixed scale |
| `Money` | `{amount: Decimal, currency: CurrencyCode}` | Currency always explicit at semantic value boundary; amounts may be signed |
| `Rate` | `{value: Decimal, unit: PERCENT|FRACTION|OTHER}` | No implicit percent/fraction conversion; preserve original unit in provenance |
| `Quantity` | `{value: Decimal, unit: UnitCode}` | Unit-qualified; may be signed where source semantics permit |
| `CodedValue` | `{code, scheme, version?, authority?}` | No unqualified equality across unrelated code schemes |
| `JurisdictionRef` | Country/region/local jurisdiction identifier | May be more granular than country |
| `FactProvenanceRef` | Reference to source or derivation lineage | Must distinguish source-supplied, calculated, mapped, inferred, enriched |

**Candidate principle:** A `Money` value is not silently converted into document currency; conversions are separately identified calculations with exchange-rate provenance.

## 4. Proposed entity dictionary

### TAX-01 TaxRegime

A reusable *within-document* classification for a tax scheme/authority, not an invoice processing status.

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `regimeId` | OpaqueIdentifier | 1 | Stable within published revision |
| `taxType` | CodedValue | 1 | VAT, GST, excise, sales/consumption tax, withholding, etc.; taxonomy open |
| `taxScheme` | CodedValue | 1 | Source/local scheme qualified by issuing authority |
| `jurisdiction` | JurisdictionRef | 0..1 | Optional when source lacks it; profile may require |
| `legalBasis` | CodedValue / DocumentReference | 0..N | Only when source or validated derivation supplies it |
| `sourceFactRefs` | SourceFiscalFactRef | 0..N | Source codes are not overwritten by normalized scheme |

**Invariant candidate:** Multiple regimes can coexist; `regimeId` is unique within revision. `TaxRegime` does not itself imply a tax liability or amount.

### TAX-02 TaxApplication

A tax calculation or stated tax amount on a particular economic base, attached to a line, document adjustment or document scope.

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `applicationId` | OpaqueIdentifier | 1 | Unique within revision |
| `regimeRef` | TaxRegimeRef | 1 | References TAX-01 within same revision |
| `scopeRef` | Revision/Line/AdjustmentRef | 1 | Exactly one authoritative economic scope |
| `direction` | `CHARGE|WITHHOLD` | 1 | Withholding not disguised as negative allowance |
| `category` | CodedValue | 0..1 | Normalized classification, with source preserved separately |
| `localTaxCode` | CodedValue | 0..N | Scheme-qualified original/local codes |
| `calculationMethod` | `PERCENTAGE|PER_UNIT|FIXED_AMOUNT|EXEMPT|OTHER` | 1 | `OTHER` requires explicit calculation descriptor |
| `rate` | Rate | 0..1 | Required conditionally for percentage method |
| `taxableBase` | Money | 0..1 | Conditional for ad valorem taxes |
| `quantityBase` | Quantity | 0..1 | Conditional for per-unit taxes |
| `amountPerUnit` | Money | 0..1 | Conditional for per-unit taxes |
| `taxAmount` | Money | 1 | Asserted/source or derived value with provenance |
| `exemptionReason` | Text/CodedValue | 0..1 | Distinguish exempt from zero-rated treatment |
| `provenanceRefs` | FactProvenanceRef | 1..N* | At least one lineage mechanism for published facts under P7 |

`*` Logical traceability requirement; exact embedded-versus-referenced representation deferred. If source states tax amount but not its base/rate, do not fabricate a base/rate. Conditional validation rules depend on source format and profile.

**Critical sign proposal:** `direction` represents tax economic effect, while `taxAmount.amount` represents signed or magnitude value according to one consistent convention to be approved. Draft recommendation: preserve signed source economics and use `direction` for semantic classification; **do not automatically negate `taxAmount` again**. A canonical effect function must be specified before approval (see §8).

### TAX-03 TaxSummary

An aggregate by declared grouping dimensions. It is a *derived or source-stated summary*, not the owner of individual applications.

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `summaryId` | OpaqueIdentifier | 1 | Unique within revision |
| `scopeRef` | Revision/Line/GroupRef | 1 | May summarize a contributing GROUP line |
| `regimeRef` | TaxRegimeRef | 1 | Regime of summarized applications |
| `category` | CodedValue | 0..1 | Additional grouping dimension |
| `rate` | Rate | 0..1 | Only when meaningful |
| `direction` | CHARGE/WITHHOLD | 1 | Prevent mixing charge and withholding totals |
| `taxableAmount` | Money | 0..1 | Source-stated or computed; provenance needed |
| `taxAmount` | Money | 1 | Sum or asserted total, provenance and reconciliation result |
| `applicationRefs` | TaxApplicationRef | 0..N | 0 if source supplies only an aggregate |
| `summaryOrigin` | SOURCE_STATED/DERIVED | 1 | Distinguish authority of asserted versus calculated summary |

**Open:** A summary can be source-stated without any line-level tax application. Never invent detailed applications solely to populate a collection.

### TAX-04 TaxPoint

Reuse `COM-03 TaxPoint` from commercial Draft 0.2. Tax point date/period supplied by the source is a billing/tax fact; legal exigibility classifications derived by a profile are D2 `DerivedFiscalFact`s. Avoid two independently editable `TaxPoint` objects.

### MON-01 MonetaryTotal

An immutable published monetary assertion on a revision, with reconciliation outcomes linked separately.

| Attribute | Type | Cardinality | Notes |
|---|---|---|---|
| `lineNetAmount` | Money | 0..1 | Contributing lines only; document profile may require |
| `allowanceTotalAmount` | Money | 0..1 | Document-level allowances; no double-counting price/line adjustments |
| `chargeTotalAmount` | Money | 0..1 | Document-level charges |
| `taxExclusiveAmount` | Money | 0..1 | Semantics must be explicitly documented by profile |
| `taxChargeAmount` | Money | 0..1 | Charge taxes only, not withholdings |
| `withholdingAmount` | Money | 0..1 | Separately stated withheld taxes |
| `taxInclusiveAmount` | Money | 0..1 | Tax-inclusive amount under applicable formula |
| `prepaidAmount` | Money | 0..1 | Previously paid/credited amounts as represented |
| `roundingAmount` | Money | 0..1 | Signed adjustment; source vs calculated retained |
| `payableAmount` | Money | 0..1 | Amount due as stated |
| `currency` | CurrencyCode | 1 | Document monetary currency; tax/reporting currencies separately handled |
| `reconciliationRefs` | ReconciliationResultRef | 0..N | Derived checks do not overwrite source-stated totals |

**Candidate publication constraint:** A published ordinary invoice should provide sufficient monetary assertions to evaluate its applicable total formula; exact mandatory fields remain profile-specific. No universal single formula is approved.

### MON-02 MonetaryConversion

A proposed derived monetary fact for tax/reporting currencies.

`sourceMoney: Money (1)`, `convertedMoney: Money (1)`, `exchangeRate: Decimal (1)`, `rateBasis: CodedValue (0..1)`, `rateDate: Date (0..1)`, `sourceFactRefs: FactProvenanceRef[] (1..N)`, `ruleOrProviderVersion: VersionRef (1)`.

This is a **candidate** to accommodate dual-currency tax totals without embedding country-named fields such as `AEDTotals` in the global core. Source-stated reporting-currency amounts may be preserved without implying a conversion was performed.

### MON-03 ReconciliationResult

`checkId: Identifier (1)`, `scopeRef: Revision/Line/GroupRef (1)`, `formulaVersion: VersionRef (1)`, `inputRefs: FactRef[] (1..N)`, `computedValue: Money (0..1)`, `assertedValue: Money (0..1)`, `difference: Money (0..1)`, `tolerance: Money (0..1)`, `outcome: PASS|FAIL|NOT_EVALUABLE (1)`, `reason: Text (0..1)`.

This is a validation/evaluation result, not an authoritative rewrite of `MonetaryTotal`.

## 5. Proposed relationships and cardinalities

| From | To | Cardinality | Condition |
|---|---|---|---|
| PublishedRevision | TaxRegime | 0..N | Tax-exempt/non-taxable documents may still declare regime, profile determines |
| PublishedRevision | TaxApplication | 0..N | Tax may exist at line/adjustment/document scope |
| TaxApplication | TaxRegime | 1 | Same revision |
| TaxApplication | Economic scope | 1 | One owning scope; avoid duplicate line and document charges |
| PublishedRevision | TaxSummary | 0..N | May be source-stated or derived |
| TaxSummary | TaxApplication | 0..N | Zero when only source aggregate exists |
| PublishedRevision | MonetaryTotal | 0..1 draft / 1 published ordinary invoice | Publication condition; other document families TBD |
| PublishedRevision | MonetaryConversion | 0..N | Reporting currencies where applicable |
| PublishedRevision | ReconciliationResult | 0..N | Versioned validation results |
| BillingLine | TaxApplication | 0..N | Line-scoped |
| Adjustment | TaxApplication | 0..N | Adjustment-scoped; price adjustment distinction maintained |
| BillingLine | TaxSummary | 0..N | Group-level tax summaries possible |

**No global requirement:** exactly one regime, at least one line tax, VAT-style percentage, positive quantity or one tax currency.

## 6. Source-model reconciliation

| Earlier v1.0 | Billing v0.3 | Draft 0.3 decision | Why |
|---|---|---|---|
| `TaxRegime` | Tax `taxType`, `jurisdiction` | **Retain refined `TaxRegime`** | Explicit multi-regime identity without equating it to FiscalContext |
| `TaxApplication` | `Tax` | **Merge calculation capabilities into `TaxApplication`** | Preserve per-scope applications plus per-unit/fixed/withhold methods |
| `RegimeTaxTotal` | `TaxSummary` | **Generalize as `TaxSummary`** | Aggregation can group by regime, category, rate, direction |
| `MonetaryTotal` | `MonetaryTotal` | **Use v0.3 breadth; defer universal arithmetic** | Withholding, prepayment, rounding and signed lines need explicit treatment |
| `AEDTotals` | Generic currency-aware Money | **Candidate `MonetaryConversion`** | Keep reporting-currency values generic; local mandates constrain use |
| Positive-only line quantity / amounts | Signed economic values | **Preserve signed source semantics** | Avoid losing credit/correction/negative-line meaning |
| `JurisdictionContext` transient | `FiscalContext` + `Supply` + profiles | **Keep distinct** | Place of supply as fact vs derived tax jurisdiction under P7 |

No source model is accepted wholesale; all row decisions remain proposed.

## 7. Cross-format semantic stress cases (illustrative, not legal conformance)

| Format / scenario | Required expressive capability | Draft treatment | Evidence limit |
|---|---|---|---|
| Peppol UBL | VAT categories, percentage rates, monetary totals | TaxRegime + percentage TaxApplication + summaries | Constructed fixture in earlier CTC-002 tests |
| Mexico CFDI 4.0 | IVA tax code, `TipoFactor`, fractional `TasaOCuota`, withholding | Scheme-qualified codes; rate unit; direction | Constructed fixture, no SAT conformance |
| Malaysia MyInvois | Tax type codes, possible tax currencies | Local codes and source fact provenance | Earlier simplified JSON fixture |
| India GST | IGST vs CGST/SGST, place-of-supply interpretation | Multiple TaxRegimes and TaxApplications; source/derived separation | Earlier partial IRP-shaped cases; legal classification not inferred solely from state equality |
| Brazil NF-e | Concurrent ICMS/PIS/COFINS and other evolving regimes | Multiple regimes with independently scoped applications | No executable Brazil fixture in this draft |
| France Extended CTC | Signed GROUP/DETAIL and noncontributing detail lines | Contribution-aware line totals; group summaries | Internal example only, not raw XSD validation |
| Excise per unit | Quantity base and per-unit rate | `PER_UNIT`, `Quantity`, `Money` | Synthetic illustration from v0.3 |

## 8. Arithmetic and sign invariants for decision

**T-INV-01 — No double counting.** An amount represented at line and GROUP/detail scope must be counted according to the contributing-line rules; do not sum explanatory DETAIL amounts again.

**T-INV-02 — Distinguish tax direction.** `CHARGE` and `WITHHOLD` remain distinct. A withheld tax must not be silently represented as an allowance or assumed to have the same payable effect in every profile.

**T-INV-03 — No fabricated tax inputs.** Missing bases, rates, exemption grounds or local codes are unknown unless legitimately derived with versioned provenance. Do not invent defaults for legal fiscal facts.

**T-INV-04 — Explicit rate unit.** `0.16` fraction and `16` percent are semantically equivalent only after an explicit conversion with source provenance.

**T-INV-05 — Scoped application.** Each application has one economic scope; summaries can reference many applications, but do not own a second editable tax amount.

**T-INV-06 — Currency consistency.** All operands of a monetary reconciliation use a common currency or explicitly documented conversion.

**T-INV-07 — Signed amounts.** Preserve source economic signs; separate direction classification from numeric sign; no implicit double negation.

**T-INV-08 — Asserted vs computed totals.** Source-stated totals are retained even when a reconciliation fails; errors are represented in `ReconciliationResult`.

**T-INV-09 — Versioned formula.** A reconciliation references exact formula/rule/profile versions, rounding policy and tolerance.

**T-INV-10 — No universal formula.** A candidate common total identity may be useful, but payable reconciliation is selected by document family, jurisdiction/profile and tax treatment, not hard-coded globally.

### Worked numerical probes

**Probe A — Simple charged tax:** net 1000, charge tax 100, no other adjustments or payments => total 1100 under a specified illustrative formula.

**Probe B — Withholding:** net 1000, charged tax 100, withholding 50. An illustrative payable result is 1050 **only if** the selected profile/formula deducts that withholding from payable. Do not impose that outcome globally.

**Probe C — Group/detail:** GROUP +21425.59 contributes; DETAIL +21425.59 noncontributing; GROUP -204.78 contributes => contributing net 21220.81, not 42646.40.

**Probe D — Per unit:** 100 LTR × 0.50 EUR/LTR = 50 EUR excise (synthetic).

**Probe E — Fractional rate:** source `TasaOCuota=0.160000` as fraction => normalized 16 percent; retain original source value, unit and conversion provenance.

## 9. Open questions / review gates

1. **Tax sign convention:** Is `taxAmount` always a signed economic effect, or a magnitude with `direction`? This must be resolved before a stable schema; a dual convention is unacceptable.
2. **Adjustment sign convention:** Align `Adjustment.type` with signed economic amounts and prevent double negation.
3. **Tax scope:** Are document-level applications authoritative calculations or only summaries for certain formats? Permit both without duplication.
4. **Regime identity:** Can several local tax codes map to one normalized regime, and what constitutes identity across profile versions?
5. **Tax currencies:** Are separate tax-currency assertions a specialized `MonetaryTotal` view or a generic conversion fact?
6. **Rounding:** Which rounding points (line, tax subtotal, invoice) and tolerances are selected by profiles?
7. **Line contribution:** How do tax summaries on noncontributing detail lines avoid double counting group-level tax?
8. **Exemption:** Separate exemption, out-of-scope, zero rate, reverse charge and non-taxable classifications without collapsing legal meaning.
9. **Source summary only:** How do we represent valid documents that provide aggregate tax totals without detailed tax bases?
10. **Version/provenance:** Which immutable packages and external lookup inputs are needed to reproduce derived tax facts?

## 10. Decision proposals (none accepted)

- **CTC-003-T01:** Retain `TaxRegime` and `TaxApplication` as distinct semantic concepts, incorporating v0.3 generalized calculation attributes.
- **CTC-003-T02:** Use `TaxSummary` as an explicitly sourced or derived aggregate, never an independently editable duplicate of application amounts.
- **CTC-003-T03:** Model withholding through `direction` and a consistent approved numeric sign policy.
- **CTC-003-T04:** Represent `Money`, `Rate`, `Quantity` and `CodedValue` as explicit semantic value types with provenance.
- **CTC-003-T05:** Reconciliation is versioned and non-destructive to source assertions.
- **CTC-003-T06:** Support generic tax/reporting currency conversions, without country-specific core fields.

## 11. CTC-003 checkpoint

**Status:** In Progress. Commercial dictionary Draft 0.2 and tax/monetary Draft 0.3 are proposals. No new ADR accepted. D2 logical contract, P1–P7 and I-01–I-10 remain accepted. FiscalContext physical A/B/C deferred.

**Suggested Git changes after review:** Add this file under `research/CTC-003/`; update `SESSION-LOG.md` and `FINDINGS.md` only after review, using complete replacement files. No remote repository write was performed.

**Next review:** Decide tax/application/summary ownership (T01/T02), then resolve tax and adjustment sign policy (T03). Following that, validate formulas and cardinalities using representative fixtures before accepting CTC-003.
