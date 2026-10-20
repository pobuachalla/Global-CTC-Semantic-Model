# Global CTC Semantic Billing Model

## Architecture, Semantic Model, Jurisdiction Profiles and Extension Framework

**Status:** Draft for architectural and domain review  
**Revision:** 0.3 — incorporates French Extended CTC bidirectional invoice stress test\
**Purpose:** Define a jurisdiction-neutral semantic model and supporting
governance approach for transforming billing documents across ERP,
e-invoicing and Continuous Transaction Control (CTC) ecosystems.

------------------------------------------------------------------------

## 1. Purpose and Scope

Global e-invoicing and CTC solutions must transform documents between
ERP-specific structures, international invoice syntaxes, national
formats and tax-authority interfaces. A direct source-to-target mapping
approach scales poorly because every new source and target increases the
number of mappings and embeds jurisdiction-specific assumptions
throughout the solution.

This proposal introduces a stable semantic layer between source and
target representations.

``` text
Source Format
     |
     v
Source Mapping / Adapter
     |
     v
Semantic Billing Model
     |
     +-- normalisation
     +-- semantic validation
     +-- enrichment
     +-- business rules
     |
     v
Target Mapping / Adapter
     |
     v
Target Format
```

The model is intended to support invoice families such as UBL, UN/CEFACT
CII, FatturaPA, CFDI, ERP-native models and future jurisdictional
formats without allowing any one syntax to become the internal canonical
structure.

### 1.1 What this model is

The model is:

-   a representation of billing **business meaning**;
-   independent of XML, JSON, EDI or database persistence;
-   suitable as an intermediate representation for transformation;
-   designed to support invoices, credit notes, debit notes and related
    billing documents;
-   extensible for fiscal requirements without becoming a union of every
    national schema.

### 1.2 What this model is not

It is not:

-   a relational database schema;
-   a replacement for UBL, CII, EN 16931, Peppol, CFDI, FatturaPA or
    another external standard;
-   a tax-authority submission model;
-   a CTC lifecycle model;
-   a requirement that the canonical object be persisted;
-   a universal superset containing every field from every country.

------------------------------------------------------------------------

## 2. Design Principles

### 2.1 Meaning before syntax

A semantic concept is introduced because it has reusable business
meaning, not because a source format contains a field with that name.

For example:

``` text
UBL AccountingSupplierParty
CII SellerTradeParty
FatturaPA CedentePrestatore
CFDI Emisor
              |
              v
     BillingDocument.seller
```

### 2.2 Jurisdiction-neutral core

The core should remain stable as jurisdictions are added. Adding a
jurisdiction should normally require profiles, rules and mappings rather
than modification of the core model.

### 2.3 Explicit semantics

Avoid overloaded generic fields such as `invoiceId` where multiple
identifiers have different meanings. Commercial document number, fiscal
UUID and CTC submission identifier are separate concepts.

### 2.4 Reuse before extension

Before introducing a local extension, determine whether the requirement:

1.  already maps to an existing concept;
2.  is a jurisdictional constraint on an existing concept;
3.  exposes a reusable concept missing from the model;
4.  is genuinely jurisdiction-specific; or
5.  is actually CTC process metadata rather than document semantics.

### 2.5 Preserve source meaning

The semantic transformation should preserve business meaning and
important source distinctions. It need not preserve the source hierarchy
or syntax.

### 2.6 Persistence independence

Primary keys, foreign keys and database normalisation are implementation
concerns. Relationships in this document express semantic relationships.

------------------------------------------------------------------------

## 3. Conceptual Architecture

The architecture separates five concerns.

``` text
                     +----------------------+
                     | Core Billing Model   |
                     +----------------------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +----------------+          +--------------------+
        | Fiscal Context |          | Jurisdiction      |
        +----------------+          | Profile           |
                                    +--------------------+
                                              |
                                              v
                                    +--------------------+
                                    | Jurisdiction      |
                                    | Extensions        |
                                    +--------------------+

Billing/fiscal artefacts are separately associated with:

                     +----------------------+
                     | Compliance           |
                     | Transaction          |
                     +----------------------+
```

### 3.1 Core Billing Model

Represents reusable commercial billing meaning: parties, lines, items,
quantities, prices, adjustments, taxes, totals, payment, supply and
document relationships.

### 3.2 Fiscal Context

Represents fiscally significant information that belongs to the
legal/fiscal artefact but is not universal commercial billing meaning.
Examples include fiscal document classifications, fiscal regimes,
receiver-use classifications, fiscal identifiers and certification data.

### 3.3 Jurisdiction Profile

Defines how a jurisdiction or regime specializes the shared semantics
through cardinality constraints, code lists, conditional rules,
validation rules and semantic alignments.

### 3.4 Jurisdiction Extension

Represents genuinely distinct local concepts for which no suitable
reusable semantic concept exists.

### 3.5 Compliance Transaction

Represents submission and processing rather than invoice meaning:
channel, submission identifier, authority reference, lifecycle status,
validation results, acknowledgements and rejection responses.

------------------------------------------------------------------------

## 4. Core Semantic Billing Model

### 4.1 BillingDocument

**Purpose:** Root concept representing an amount charged, credited or
otherwise adjusted between trading parties.

  Property           Type             Cardinality Description
  ------------------ -------------- ------------- ----------------------------------------
  documentNumber     String                     1 Business-facing document number
  documentSeries     String                  0..1 Series where semantically distinct
  documentType       Code                       1 Invoice, credit note, debit note, etc.
  issueDate          Date                       1 Document issue date
  issueTime          Time                    0..1 Issue time
  documentCurrency   CurrencyCode               1 Primary billing currency
  taxCurrency        CurrencyCode            0..1 Separate tax reporting currency
  notes              String                  0..n Human-readable document notes

**Relationships**

  -----------------------------------------------------------------------------------------
  Relationship            Target                           Cardinality Description
  ----------------------- ---------------------- --------------------- --------------------
  identifiers             Identifier                              0..n Additional
                                                                       meaningful
                                                                       identifiers

  seller                  Party                                      1 Supplier/seller in
                                                                       the commercial
                                                                       transaction

  buyer                   Party                                      1 Customer/buyer

  additionalParties       PartyRole                               0..n Other participants

  lines                   BillingLine                             1..n Billing lines

  adjustments             Adjustment                              0..n Document-level
                                                                       allowances/charges

  taxSummaries            TaxSummary                              0..n Aggregated tax
                                                                       results

  totals                  MonetaryTotal                              1 Document
                                                                       reconciliation
                                                                       totals

  documentRelationships   DocumentRelationship                    0..n Orders, preceding
                                                                       invoices,
                                                                       corrections, etc.

  paymentMeans            PaymentMeans                            0..n How payment is made

  paymentTerms            PaymentTerms                            0..n When and under what
                                                                       conditions payment
                                                                       is due

  supply                  Supply                                  0..1 Delivery/supply
                                                                       semantics

  accountingPeriod        Period                                  0..1 Billing/accounting
                                                                       period

  attachments             Attachment                              0..n Supporting artefacts
  -----------------------------------------------------------------------------------------

### 4.2 Party

Represents an organisation or person participating in the transaction.
Seller and buyer are relationship roles rather than different entity
types.

  Property      Type       Cardinality
  ------------- -------- -------------
  name          String            0..1
  tradingName   String            0..1
  legalName     String            0..1

Relationships: `identifiers[]`, `taxRegistrations[]`,
`legalRegistration?`, `address?`, `contact?`.

### 4.3 PartyRole

Represents an additional party participating in a defined role.

  Property   Type     Cardinality
  ---------- ------ -------------
  role       Code               1

Relationship: `party -> Party`.

Typical roles include PAYEE, TAX_REPRESENTATIVE, FISCAL_REPRESENTATIVE,
SHIP_TO, SHIP_FROM, FACTOR, INTERMEDIARY and PLATFORM.

### 4.4 Identifier

  --------------------------------------------------------------------------
  Property           Type                       Cardinality Description
  ------------------ ---------------- --------------------- ----------------
  value              String                               1 Identifier value

  type               Code                              0..1 TAX, LEGAL,
                                                            FISCAL, NETWORK,
                                                            etc.

  scheme             Code/String                       0..1 RFC, VAT, GLN,
                                                            DUNS, UUID, etc.

  issuingAuthority   String                            0..1 Authority
                                                            responsible for
                                                            identifier

  country            CountryCode                       0..1 Country context

  jurisdiction       String                            0..1 More specific
                                                            jurisdiction if
                                                            needed
  --------------------------------------------------------------------------

### 4.4a LegalRegistration

Represents legal registration independently from generic or tax identifiers.

`registeredName?`, `registrationIdentifier`, `registrationScheme?`, `legalForm?`, `jurisdiction?`.

This covers constructs such as registered company name, company registration number and legal form without overloading `PartyIdentifier`.

### 4.5 TaxRegistration

Represents registration of a party under a tax scheme.

`identifier`, `scheme`, `countryCode?`, `registrationType?`.

### 4.6 Address

Supports common global address semantics including lines, street,
building number, city, postal code, subdivision and country.
Jurisdiction profiles may strengthen or constrain required components.

### 4.7 Contact

`name?`, `department?`, `telephone?`, `email?`.

### 4.8 BillingLine

A billing line is not assumed to be an independent additive transaction line. Profiles may define standard lines, group/summary lines, detail lines or informational roll-ups.

| Relationship/Property | Type | Notes |
|---|---|---|
| lineNumber | String | Business line identifier |
| lineRole | Code | STANDARD, GROUP, DETAIL or profile-aligned equivalent |
| parentLine | BillingLine? | Parent for hierarchical/grouped lines |
| contributesToDocumentTotals | Boolean/derived | Whether the line participates directly in document reconciliation |
| quantity | Quantity? | Optional for group/summary lines |
| item | Item? | Optional where a line is purely aggregating |
| price | Price? | Price including price-level adjustment semantics |
| lineNetAmount | Money | Signed economic line value |
| parties | PartyRole[] | Optional line-specific participants; document roles act as defaults |
| identifiers | Identifier[] | Line/object identifiers that are not document relationships |
| adjustments | Adjustment[] | Line-level allowances/charges |
| taxes | Tax[] | Tax treatment/calculation at line scope |
| taxSummaries | TaxSummary[] | Aggregated line/group tax results where a profile supplies them |
| period | Period? | Service/billing period |
| taxPoint | TaxPoint? | Line-level tax-point/exigibility semantics |
| documentRelationships | DocumentRelationship[] | References to related business/fiscal documents |

A profile can determine `contributesToDocumentTotals`. For example, where GROUP lines contain the amounts included in document totals and DETAIL lines explain those groups, summing every line would double-count the transaction.

### 4.9 Item

Represents the billed good or service.

Properties/relationships include `name?`, `description[]`, seller/buyer
identifiers, standard identifiers, classifications, country of origin
and extensible attributes.

### 4.10 ItemClassification

Represents classification under a named scheme, for example UNSPSC or a
jurisdictional goods/service catalogue.

`code`, `scheme`, `version?`.

### 4.11 Quantity

`value` + `unit`.

Quantity is a concept rather than two unrelated fields so that
quantity-based calculations and unit semantics remain explicit.

### 4.12 Money

`amount` + `currency`.

Document currency can act as a serialization default, but currency
remains part of the semantic value.

### 4.13 Price

`netAmount: Money`, `baseQuantity?`, `unit?`, `grossAmount?`, `adjustments[]?`.

Price-level adjustments are semantically distinct from line-level allowances/charges. A source may provide a gross price, a price allowance and a resulting net price without that allowance changing the independently stated line allowance total.

### 4.14 Adjustment

Represents an allowance or charge.

`type`, `reason?`, `reasonCode?`, `percentage?`, `baseAmount?`,
`amount`, `taxes[]?`.

Scope is expressed by the relationship: an adjustment under
`BillingLine` is line-level; one under `BillingDocument` is
document-level.

### 4.15 Tax

Tax must support more than European VAT.

  Property            Description
  ------------------- --------------------------------------------------
  taxType             VAT, GST, sales tax, excise, withholding, etc.
  direction           CHARGE or WITHHOLD
  category            Tax treatment/category
  code                Scheme-specific code
  jurisdiction        Relevant jurisdiction
  calculationMethod   PERCENTAGE, PER_UNIT, FIXED_AMOUNT, EXEMPT, etc.
  rate                Percentage/rate where applicable
  taxableBase         Money where applicable
  quantityBase        Quantity where applicable
  amountPerUnit       Money where applicable
  amount              Calculated tax amount
  exemption           Exemption code/reason where applicable

Withholding is modelled explicitly through tax direction rather than as
an arbitrary negative allowance.

### 4.16 TaxSummary

Represents aggregated tax results, usually grouped by tax
type/category/rate.

Relationships/properties: `tax`, `taxableAmount`, `taxAmount`.

### 4.17 MonetaryTotal

Recommended semantic totals:

-   lineNetAmount
-   allowanceTotalAmount?
-   chargeTotalAmount?
-   taxExclusiveAmount
-   taxChargeAmount?
-   withholdingAmount?
-   taxInclusiveAmount
-   prepaidAmount?
-   roundingAmount?
-   payableAmount

The model should support reconciliation rules while recognising that
exact statutory total formulas vary by regime.

### 4.18 PaymentMeans

Represents **how** payment is made.

`type`, `paymentReference?`, `amount?`, `dueDate?`, `account?`,
`mandate?`.

### 4.19 PaymentTerms

Represents **when and under what conditions** payment occurs.

`dueDate?`, `baseDate?`, `days?`, `description?`, `percentage?`,
`amount?`, `settlementPeriod?`.

### 4.20 FinancialAccount

Supports account identifiers such as IBAN and local bank-account schemes
plus financial institution identifiers such as BIC where applicable.

### 4.21 DocumentRelationship

Represents a meaningful relationship to another business/fiscal
document.

  -----------------------------------------------------------------------
  Property                            Examples
  ----------------------------------- -----------------------------------
  relationshipType                    ORDER, CONTRACT, DELIVERY,
                                      REFERENCES, CREDITS, DEBITS,
                                      CORRECTS, REPLACES, CANCELS

  relatedDocument                     DocumentReference
  -----------------------------------------------------------------------

### 4.22 DocumentReference

`documentNumber?`, `documentType?`, `issueDate?`, `identifiers[]`,
`description?`.

### 4.23 Supply

Represents supply/delivery semantics:

`supplyDate?`, `supplyPeriod?`, `placeOfSupply?`, `deliveryLocation?`, `dispatchLocation?`, `deliveryParty?`, `dispatchParty?`, `incoterm?`, `transportReference?`.

Party and location are intentionally separate because delivery may identify both a named receiving party and a physical address.

### 4.24 Period

`startDate?`, `startTime?`, `endDate?`, `endTime?`, `description?`.

### 4.24a TaxPoint

Represents tax-point/exigibility meaning rather than source syntax placement.

`date?`, `basisCode?`, `period?`, `description?`.

The concept can occur at document or line scope. A national profile may encode the basis code inside an otherwise familiar period structure; the mapper resolves that into this semantic concept.

### 4.24b Note

Represents typed or untyped document notes.

`code?`, `subject?`, `text`, `language?`.

Profiles can parse structured prefixes or qualifiers while preserving the original text.

### 4.24c DocumentRepresentation

Represents a source or target serialization of a semantic document.

`direction`, `formatFamily`, `formatVersion?`, `customizationId?`, `profileId?`, `mappingVersion?`, `contentHash?`, `artifactReference?`, `createdAt?`.

This is intentionally distinct from both `FiscalContext` and `ComplianceTransaction`.

### 4.25 Attachment

`identifier?`, `filename?`, `mimeType?`, `description?`, `content?`,
`externalUri?`.

The semantic model does not dictate attachment persistence.

------------------------------------------------------------------------

## 5. Complete Core Hierarchy

```text
BillingDocument
|
+-- identifiers[] -----------------> Identifier
+-- notes[] -----------------------> Note
+-- seller ------------------------> Party
|    +-- identifiers[] -----------> Identifier
|    +-- taxRegistrations[] ------> TaxRegistration
|    +-- legalRegistrations[] ----> LegalRegistration
|    +-- addresses[] -------------> Address
|    +-- contacts[] --------------> Contact
|
+-- buyer -------------------------> Party
+-- additionalParties[] -----------> PartyRole --> Party
|
+-- lines[] -----------------------> BillingLine
|    +-- parentLine --------------> BillingLine
|    +-- quantity ----------------> Quantity
|    +-- item --------------------> Item
|    |    +-- classifications[] --> ItemClassification
|    +-- price -------------------> Price
|    |    +-- adjustments[] ------> Adjustment
|    +-- lineNetAmount -----------> Money
|    +-- parties[] ---------------> PartyRole --> Party
|    +-- identifiers[] -----------> Identifier
|    +-- adjustments[] -----------> Adjustment
|    +-- taxes[] -----------------> Tax
|    +-- taxSummaries[] ----------> TaxSummary
|    +-- period ------------------> Period
|    +-- taxPoint ----------------> TaxPoint
|    +-- documentRelationships[] -> DocumentRelationship
|
+-- adjustments[] -----------------> Adjustment
+-- taxSummaries[] ----------------> TaxSummary
+-- totals ------------------------> MonetaryTotal
+-- documentRelationships[] -------> DocumentRelationship
+-- paymentMeans[] ----------------> PaymentMeans
+-- paymentTerms[] ----------------> PaymentTerms
+-- supply ------------------------> Supply
+-- accountingPeriod -------------> Period
+-- taxPoint ----------------------> TaxPoint
+-- attachments[] -----------------> Attachment
+-- representations[] ------------> DocumentRepresentation
```

## 6. Billing Document Types and Directionality

A shared `BillingDocument` model should support at least:

-   INVOICE
-   CREDIT_NOTE
-   DEBIT_NOTE
-   SELF_BILLED_INVOICE
-   SELF_BILLED_CREDIT_NOTE

Further types should be introduced through controlled taxonomy rather
than separate duplicated models.

### 6.1 Canonical sign convention

The canonical model preserves **signed economic values**.

> `documentType` expresses the nature of the document; it does not determine the sign of every amount or quantity.

An invoice can contain negative deduction lines, and a credit note can contain mixed positive/negative adjustments. Source and target mappings should preserve or deliberately transform sign conventions rather than normalize all amounts to positive magnitude.

Semantic reconciliation must also respect line contribution semantics. For hierarchical invoices, document line totals are calculated from lines that contribute to document totals, not necessarily from every physical/canonical line.

### 6.2 Corrections

Correction semantics should be explicit:

``` yaml
documentType: CREDIT_NOTE
documentRelationships:
  - relationshipType: CREDITS
    relatedDocument:
      documentNumber: INV-1001
```

------------------------------------------------------------------------

## 7. Tax Model

Tax is intentionally broader than an EN 16931 VAT category.

The model must be capable of representing:

-   VAT and GST;
-   sales/consumption taxes;
-   withholding/retention;
-   excise;
-   percentage taxes;
-   per-unit taxes;
-   fixed amounts;
-   exemptions and zero rating;
-   multiple tax jurisdictions where required.

Example:

``` yaml
taxType: EXCISE
direction: CHARGE
calculationMethod: PER_UNIT
quantityBase:
  value: 100
  unit: LTR
amountPerUnit:
  amount: 0.50
  currency: EUR
amount:
  amount: 50.00
  currency: EUR
```

versus:

``` yaml
taxType: VAT
direction: CHARGE
category: STANDARD
calculationMethod: PERCENTAGE
rate: 23
taxableBase:
  amount: 1000
  currency: EUR
amount:
  amount: 230
  currency: EUR
```

------------------------------------------------------------------------

## 8. Fiscal Context

`FiscalContext` holds legal/fiscal artefact semantics that should not
distort the reusable billing model.

``` text
FiscalContext
|
+-- jurisdiction
+-- fiscalDocumentType?
+-- fiscalIdentifiers[]
+-- partyContexts[]
+-- taxPoint?
+-- placeOfTaxation?
+-- exportClassification?
+-- fiscalAttributes[]
+-- certification?
+-- signature?
+-- extensions[]
```

### 8.1 FiscalPartyContext

A party can have fiscal attributes that are meaningful only in a
particular regime.

``` text
FiscalPartyContext
+-- partyRole
+-- fiscalRegimeCode?
+-- fiscalResidence?
+-- documentUseCode?
+-- jurisdictionalAttributes[]
```

This avoids adding fields such as `regimenFiscal` or `usoCFDI` directly
to the universal `Party`.

### 8.2 Examples

``` text
Commercial invoice number   -> BillingDocument.documentNumber
Italian TD01 classification -> FiscalContext.fiscalDocumentType
Mexican CFDI UUID            -> FiscalContext.fiscalIdentifiers[]
```

------------------------------------------------------------------------

## 9. Jurisdiction Profiles

A jurisdiction profile specializes the semantic model without forking
it.

A profile may define:

-   stronger cardinality;
-   prohibited optional concepts;
-   allowed code lists;
-   conditional requirements;
-   cross-field rules;
-   fiscal requirements;
-   semantic alignment of local concepts;
-   target validation requirements.

Example:

``` yaml
jurisdiction: MX
regime: CFDI
version: "4.0"

constraints:
  - path: billingDocument.seller.identifiers
    require:
      type: TAX
      scheme: RFC

  - path: billingDocument.buyer.identifiers
    require:
      type: TAX
      scheme: RFC

fiscalRequirements:
  - path: fiscalContext.partyContexts[SELLER].fiscalRegimeCode
  - path: fiscalContext.partyContexts[BUYER].fiscalRegimeCode
  - path: fiscalContext.partyContexts[BUYER].documentUseCode
  - path: fiscalContext.exportClassification
```

A profile is conceptually similar to the role played by
constrained/specialized semantic models such as EN 16931 CIUS or PINT
specializations, but the internal architecture is not dependent on those
standards.

------------------------------------------------------------------------

## 10. Jurisdiction-Specific Extensions

Extensions are a controlled escape mechanism, not the default home for
unfamiliar fields.

A true extension should:

-   have a namespace;
-   have a defined semantic meaning;
-   be versioned;
-   have validation rules;
-   identify its owning jurisdiction/regime;
-   be reviewable for later promotion into shared semantics.

Example:

``` yaml
fiscalContext:
  jurisdiction: XX
  extensions:
    - namespace: urn:example:ctc:xx:fiscal
      type: MUNICIPAL_TRADE_ZONE
      version: "1.0"
      data:
        zoneCode: A17
```

### 10.1 Field-modeller decision tree

``` text
New source/jurisdiction field
            |
            v
Does the semantic concept already exist?
       |                 |
      YES                NO
       |                  |
       v                  v
Map to existing      Is it a constraint,
semantic path        code-list restriction
and apply profile    or local expression of
rules if needed      an existing concept?
                         |          |
                        YES         NO
                         |           |
                         v           v
                    Profile /   Does equivalent
                    alignment   business/fiscal
                                meaning occur in
                                other regimes?
                                   |       |
                                  YES      NO
                                   |        |
                                   v        v
                              Generalise   Is it
                              shared       submission /
                              semantic     processing
                              concept      metadata?
                                             |      |
                                            YES     NO
                                             |       |
                                             v       v
                                       Compliance   Create
                                       Transaction  namespaced
                                                    extension
```

### 10.2 Modelling rule

A jurisdiction requirement alone is not sufficient justification for
modifying the core model.

------------------------------------------------------------------------

## 11. Compliance Transaction Model

Billing/fiscal semantics must remain separate from CTC processing state.

``` text
ComplianceTransaction
|
+-- jurisdiction
+-- regime
+-- channel
+-- transmissionId?
+-- submissionId?
+-- submittedAt?
+-- receivedAt?
+-- authorityReference?
+-- status
+-- lifecycleEvents[]
+-- validationResults[]
+-- authorityResponses[]
```

Example:

``` text
INV-123              -> BillingDocument.documentNumber
TD01                 -> FiscalContext.fiscalDocumentType
SdI processing ID    -> ComplianceTransaction.authorityReference
SdI rejection        -> ComplianceTransaction.lifecycleEvents/status
```

This boundary prevents country-specific transmission protocols from
contaminating invoice semantics.

------------------------------------------------------------------------

## 12. Cross-Format Validation

The proposed model has been conceptually tested against four
deliberately different families.

  -----------------------------------------------------------------------------------------------------------------------
  Semantic       UBL                       UN/CEFACT CII               FatturaPA                CFDI 4.0
  concept                                                                                       
  -------------- ------------------------- --------------------------- ------------------------ -------------------------
  Document       ID                        ExchangedDocument ID        Numero                   Folio
  number                                                                                        

  Seller         AccountingSupplierParty   SellerTradeParty            CedentePrestatore        Emisor

  Buyer          AccountingCustomerParty   BuyerTradeParty             CessionarioCommittente   Receptor

  Lines          InvoiceLine               SupplyChainTradeLineItem    DettaglioLinee           Concepto

  Quantity       InvoicedQuantity          BilledQuantity              Quantita                 Cantidad

  Price          PriceAmount               NetPriceProductTradePrice   PrezzoUnitario           ValorUnitario

  Line amount    LineExtensionAmount       LineTotalAmount             PrezzoTotale             Importe

  Tax rate       Percent                   RateApplicablePercent       AliquotaIVA              TasaOCuota

  Tax base       TaxableAmount             BasisAmount                 ImponibileImporto        Base

  Tax amount     TaxAmount                 CalculatedAmount            Imposta                  Importe

  Payment means  PaymentMeansCode          TypeCode                    ModalitaPagamento        FormaPago

  Related        Billing/Order refs        ReferencedDocument          Dati\* references        CfdiRelacionados
  document                                                                                      

  Local fiscal   Profile/external          Profile/external            Local semantics          RegimenFiscal
  regime                                                                                        

  Fiscal UUID    Not core                  Not core                    Process/fiscal IDs       UUID

  Transmission   Not billing semantics     Not billing semantics       SdI lifecycle            Certification/authority
  status                                                                                        lifecycle
  -----------------------------------------------------------------------------------------------------------------------

### 12.1 Key conclusion

If formats use different structures and terminology for the same
business meaning, that is evidence for a canonical semantic concept. If
a field has no reusable commercial/fiscal meaning outside one regime, it
should be treated as profile-specific or an extension rather than added
directly to the core.

------------------------------------------------------------------------

### 12.2 French Extended CTC bidirectional stress test

A French UBL Extended CTC example exposed semantics that are not adequately represented by a flat EN 16931-style invoice model:

- GROUP and DETAIL line roles;
- parent/child line hierarchy;
- group lines that contribute to document totals while detail lines explain the group and must not be double-counted;
- negative prices and negative lines inside an otherwise positive invoice;
- line-level seller/participant identity that can differ from the document-level seller;
- line/group tax totals in addition to detailed tax categories;
- tax-point/exigibility codes encoded in period structures;
- structured note prefixes;
- legal-form/registration information;
- source representation metadata such as UBL version, CustomizationID and ProfileID.

These findings strengthen rather than replace the existing cross-format abstraction. They result in additional reusable semantics (`lineRole`, line hierarchy/contribution, `TaxPoint`, line parties, `DocumentRepresentation`) rather than French-named core fields.

The test also invalidates a previous positive-magnitude-only canonical sign convention. Signed economic values are now retained in the semantic model.

## 13. Mapping Model

Mappings connect source syntax to semantic paths and semantic paths to
target syntax.

``` text
Source path
    |
    | transformation
    v
Semantic path
    |
    | transformation
    v
Target path
```

Supported mapping operations should remain deliberately small and
composable:

-   direct;
-   rename;
-   code translation;
-   default;
-   conditional;
-   concatenate;
-   split;
-   format;
-   lookup;
-   calculation;
-   aggregate;
-   collection mapping.

Example:

``` yaml
mappings:
  - source: Invoice.ID
    target: billingDocument.documentNumber
    transform: direct

  - source: Invoice.AccountingSupplierParty.Party.PartyName.Name
    target: billingDocument.seller.name
    transform: direct

  - source: Invoice.InvoiceTypeCode
    target: billingDocument.documentType
    transform:
      function: lookup
      table: ubl-document-types

  - source:
      - Invoice.TaxTotal.TaxSubtotal[*].TaxableAmount
    target: billingDocument.taxSummaries
    transform:
      function: collectionMap
      mapping: ubl-tax-subtotal
```

Mapping configuration should describe transformations; it should not
become a general-purpose programming language.

------------------------------------------------------------------------

## 14. Validation Model

Validation occurs at distinct layers.

### 14.1 Structural validation

Is the object structurally a valid `BillingDocument`?

Examples: required types, valid cardinality, valid primitive
representation.

### 14.2 Semantic validation

Does the document make business sense?

Examples:

-   line totals reconcile;
-   tax totals reconcile;
-   payable amount reconciles;
-   credit-note relationship rules are consistent.

### 14.3 Jurisdiction-profile validation

Does the semantic document satisfy the requirements of the intended
jurisdiction/regime?

Examples: required fiscal identifiers, permitted tax codes, conditional
buyer information.

### 14.4 Target-format validation

Can the semantic object be represented as a valid target artefact?

A semantically valid document may still be unrepresentable in a
particular target profile.

### 14.5 Authority validation

Does the resulting artefact satisfy tax-authority or platform rules at
submission time?

Authority validation results belong to the compliance process, not the
core billing model.

------------------------------------------------------------------------

## 15. Jurisdiction Onboarding Process

A repeatable onboarding process is essential to protect the model from
uncontrolled growth.

``` text
1. Analyse specification and representative documents
                         |
                         v
2. Identify business, fiscal and processing concepts
                         |
                         v
3. Map business concepts to existing core semantics
                         |
                         v
4. Map fiscal concepts to FiscalContext
                         |
                         v
5. Apply field-modeller decision tree to gaps
                         |
                         v
6. Define Jurisdiction Profile
                         |
                         v
7. Define code lists and validation rules
                         |
                         v
8. Define source/target mappings
                         |
                         v
9. Build representative test corpus
                         |
                         v
10. Test semantic preservation and reconciliation
                         |
                         v
11. Review proposed extensions/core changes
                         |
                         v
12. Publish and version profile/mappings
```

### 15.1 Recommended outputs

Each jurisdiction onboarding should produce:

-   source/target specification inventory;
-   semantic coverage matrix;
-   profile definition;
-   code-list definitions;
-   mapping configurations;
-   extension proposals, if any;
-   representative positive and negative samples;
-   validation rules;
-   known-loss/unsupported-feature register;
-   version and effective-date metadata.

### 15.2 Exit criteria

A jurisdiction should not be considered onboarded until:

-   mandatory source concepts are accounted for;
-   target mandatory concepts can be produced or explicitly identified
    as enrichment dependencies;
-   semantic reconciliation tests pass;
-   extension proposals are reviewed;
-   profile and mappings are versioned;
-   representative documents pass target validation.

------------------------------------------------------------------------

## 16. Model Governance and Evolution

The model needs governance because uncontrolled flexibility will
eventually produce an unmaintainable global superset.

### 16.1 Change categories

Changes should be classified as:

1.  mapping-only change;
2.  jurisdiction-profile change;
3.  jurisdiction-extension change;
4.  reusable fiscal-model change;
5.  core semantic-model change.

The review threshold should increase down this list.

### 16.2 Core-change criteria

A core concept should normally be added only when:

-   the concept has clear semantic meaning;
-   it is not merely a source syntax artefact;
-   it is reusable across multiple formats/regimes or represents a
    demonstrably universal billing concept;
-   existing concepts cannot represent it without semantic distortion;
-   its relationship to existing concepts is understood;
-   mapping and backward-compatibility impacts are assessed.

### 16.3 Independent versioning

The following should evolve independently:

``` text
Core semantic model:      1.2.0
Fiscal semantic model:    1.1.0
Jurisdiction profile:     FR-2.0
Source mapping:           UBL-2.1-to-core-3.4
Target mapping:           core-to-FR-profile-2.2
Code-list package:        FR-2027.01
```

The exact versioning scheme is an implementation decision, but the
artefacts should not be coupled to one release number.

### 16.4 Compatibility

Breaking semantic changes require explicit migration guidance. Renaming
a field is not necessarily harmless if mappings, profiles and stored
canonical documents depend on its path.

------------------------------------------------------------------------

## 17. Extension Promotion Process

Extensions should not automatically become permanent.

If similar concepts appear in multiple jurisdictions:

``` text
Jurisdiction Extension
          |
          v
Observed in other regimes
          |
          v
Candidate Shared Concept
          |
          v
Semantic Review
       /      \
      /        \
     v          v
Promote to     Remain
shared model   extension
```

Promotion should consider whether the apparent similarity reflects
genuinely shared meaning rather than coincidentally similar fields.

When promoted, existing extensions should have a defined
migration/deprecation path.

------------------------------------------------------------------------

## 18. Worked Examples

### 18.1 UBL to semantic model

``` text
Invoice/ID
   -> billingDocument.documentNumber

Invoice/AccountingSupplierParty/Party
   -> billingDocument.seller

Invoice/AccountingCustomerParty/Party
   -> billingDocument.buyer

Invoice/InvoiceLine[]
   -> billingDocument.lines[]

Invoice/TaxTotal/TaxSubtotal[]
   -> billingDocument.taxSummaries[]

Invoice/LegalMonetaryTotal
   -> billingDocument.totals
```

The UBL hierarchy is discarded; its business meaning is retained.

### 18.2 Credit note

``` yaml
billingDocument:
  documentNumber: CN-1002
  documentType: CREDIT_NOTE
  issueDate: 2026-09-10
  documentCurrency: EUR

  documentRelationships:
    - relationshipType: CREDITS
      relatedDocument:
        documentNumber: INV-1001

  lines:
    - lineNumber: "1"
      quantity:
        value: 2
        unit: EA
      item:
        name: Widget
      price:
        amount:
          amount: 100
          currency: EUR
      lineNetAmount:
        amount: 200
        currency: EUR
```

The target adapter determines whether the target syntax expects positive
or negative credit amounts.

### 18.3 CFDI decomposition

``` text
CFDI Comprobante
       |
       +-- commercial meaning --------> BillingDocument
       |
       +-- fiscal classification -----> FiscalContext
       |
       +-- fiscal certification ------> FiscalContext / certification
       |
       +-- submission/lifecycle ------> ComplianceTransaction
```

Example:

``` text
Folio                   -> BillingDocument.documentNumber
Emisor/Rfc              -> BillingDocument.seller tax identifier
RegimenFiscal           -> FiscalPartyContext.fiscalRegimeCode
UsoCFDI                 -> FiscalPartyContext.documentUseCode
UUID                    -> FiscalContext.fiscalIdentifiers
authority processing    -> ComplianceTransaction
```

### 18.4 FatturaPA decomposition

``` text
Numero                  -> BillingDocument.documentNumber
CedentePrestatore       -> BillingDocument.seller
CessionarioCommittente  -> BillingDocument.buyer
TipoDocumento           -> normalized documentType + fiscal classification
DatiBeniServizi         -> BillingDocument.lines/taxes
DatiPagamento           -> paymentMeans/paymentTerms
transmission data       -> ComplianceTransaction
```

------------------------------------------------------------------------

### 18.5 French grouped/detail and bidirectional example

```yaml
billingDocument:
  documentNumber: AUTOF202600035
  documentType: INVOICE
  documentCurrency: EUR

  lines:
    - lineNumber: "10"
      lineRole: GROUP
      contributesToDocumentTotals: true
      lineNetAmount: { amount: 21425.59, currency: EUR }

    - lineNumber: "11"
      lineRole: DETAIL
      parentLine: "10"
      contributesToDocumentTotals: false
      quantity: { value: 43.8100, unit: LTR }
      price:
        netAmount: { amount: 489.0570, currency: EUR }
      lineNetAmount: { amount: 21425.59, currency: EUR }

    - lineNumber: "20"
      lineRole: GROUP
      contributesToDocumentTotals: true
      lineNetAmount: { amount: -204.78, currency: EUR }
```

The canonical representation retains the negative economic value while preventing the DETAIL line from being counted again in the document line total.

## 19. Review Questions and Open Areas

Reviewers are specifically asked to challenge the following.

### Semantic boundaries

-   Is `BillingDocument` the correct scope, or are important reusable
    billing concepts absent?
-   Is the boundary between `BillingDocument` and `FiscalContext`
    sufficiently clear?
-   Are any proposed fiscal concepts actually core business concepts?

### Tax

-   Does the proposed abstraction cover non-VAT tax families adequately?
-   Is `direction = CHARGE | WITHHOLD` sufficient?
-   Are compound/cascading taxes and taxes calculated over other taxes
    adequately representable?
-   Do we need explicit tax-point semantics in the core or fiscal layer?

### Credit/debit documents

-   Are signed economic values sufficient across ERP, UBL, CII and national formats?
-   Which profiles require explicit line contribution/roll-up rules?
-   How should mixed-sign lines and corrections be validated without assuming sign from document type?

### Parties

-   Should seller and buyer remain first-class relationships while other roles use `PartyRole`?
-   How should line-level party roles inherit or override document-level parties?
-   Are issuer, supplier and seller always safely alignable?

### Money and currency

-   Should every semantic `Money` carry currency, even when
    serialization omits repeated values?
-   How should exchange-rate provenance and multiple reporting
    currencies be represented?

### Supply

-   Does `Supply` sufficiently cover services, goods, place-of-supply
    and cross-border scenarios?

### Extensions

-   Is the extension decision tree strict enough?
-   What evidence should be required before promoting an extension to
    shared semantics?

### Transformation fidelity

-   What does "lossless" mean for source-to-semantic mapping?
-   Should unmapped source data be retained as provenance/raw fragments?
-   Is `DocumentRepresentation` sufficient for document-level provenance, or is field-level lineage also required?
-   How should mappings expose semantic information that cannot be
    represented in a target?

------------------------------------------------------------------------

## 20. Recommended Supporting Processes

The model should be supported by processes rather than treated as a
static schema.

### 20.1 Semantic change review

Proposed model changes should include:

-   business definition;
-   source examples;
-   formats/jurisdictions demonstrating need;
-   existing semantic paths considered;
-   proposed cardinality and datatype;
-   mapping impact;
-   profile impact;
-   compatibility impact.

### 20.2 Mapping review

Mappings should be testable independently from the transformation engine
and include traceability from source field to semantic path to target
field.

### 20.3 Regulatory change management

A regulatory change should first be classified as affecting:

-   mapping;
-   profile constraint;
-   code list;
-   validation rule;
-   fiscal semantics;
-   jurisdiction extension;
-   core semantics;
-   CTC lifecycle/process.

This classification determines which artefact must change and prevents
unnecessary core releases.

### 20.4 Test corpus management

Maintain representative documents covering:

-   standard invoice;
-   credit note;
-   debit note;
-   allowances/charges;
-   multiple tax rates;
-   exemption;
-   withholding;
-   foreign currency;
-   payment variations;
-   document corrections;
-   local extensions;
-   invalid/negative cases.

### 20.5 Provenance and traceability

The transformer should be able to explain how a target value was
derived:

``` text
Source field(s)
     |
     v
Transformation / lookup / aggregation
     |
     v
Semantic path
     |
     v
Target transformation
     |
     v
Target field
```

This supports debugging, regulatory assurance and the planned visual
mapping PoC.

------------------------------------------------------------------------

# Appendix A. Representative Field Mapping Matrix

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Semantic path           UBL                        CII                          FatturaPA                                  CFDI 4.0                  Layer
  ----------------------- -------------------------- ---------------------------- ------------------------------------------ ------------------------- -------------
  documentNumber          Invoice/ID                 ExchangedDocument/ID         DatiGeneraliDocumento/Numero               Comprobante/Folio         CORE

  documentType            InvoiceTypeCode / document TypeCode                     TipoDocumento                              TipoDeComprobante         CORE/FISCAL
                          type                                                                                                                         mapping

  issueDate               IssueDate                  IssueDateTime                Data                                       Fecha                     CORE

  documentCurrency        DocumentCurrencyCode       InvoiceCurrencyCode          Divisa                                     Moneda                    CORE

  seller.name             PartyName/Name             SellerTradeParty/Name        CedentePrestatore/.../Denominazione        Emisor/Nombre             CORE

  seller.taxId            PartyTaxScheme/CompanyID   Seller tax registration      IdFiscaleIVA                               Emisor/Rfc                CORE

  buyer.name              PartyName/Name             BuyerTradeParty/Name         CessionarioCommittente/.../Denominazione   Receptor/Nombre           CORE

  buyer.taxId             PartyTaxScheme/CompanyID   Buyer tax registration       IdFiscaleIVA                               Receptor/Rfc              CORE

  line.quantity           InvoicedQuantity           BilledQuantity               Quantita                                   Concepto/Cantidad         CORE

  line.unit               @unitCode                  unitCode                     UnitaMisura                                ClaveUnidad               CORE

  item.name/description   Item                       SpecifiedTradeProduct        Descrizione                                Descripcion               CORE

  item.classification     CommodityClassification    Classification               CodiceArticolo where applicable            ClaveProdServ             CORE

  price                   PriceAmount                NetPriceProductTradePrice    PrezzoUnitario                             ValorUnitario             CORE

  lineNetAmount           LineExtensionAmount        LineTotalAmount              PrezzoTotale                               Importe                   CORE

  adjustment              AllowanceCharge            TradeAllowanceCharge         ScontoMaggiorazione                        Descuento / local         CORE
                                                                                                                             semantics                 

  tax.type                TaxScheme                  TradeTax/TypeCode            VAT/withholding structures                 Impuesto                  CORE

  tax.rate                Percent                    RateApplicablePercent        AliquotaIVA                                TasaOCuota                CORE

  tax.base                TaxableAmount              BasisAmount                  ImponibileImporto                          Base                      CORE

  tax.amount              TaxAmount                  CalculatedAmount             Imposta                                    Importe                   CORE

  withholding             representable              representable                DatiRitenuta                               Retenciones               CORE

  payableAmount           PayableAmount              DuePayableAmount             totals/payment semantics                   Total                     CORE

  payment means           PaymentMeansCode           PaymentMeans/TypeCode        ModalitaPagamento                          FormaPago                 CORE

  payment due date        PaymentTerms               SpecifiedTradePaymentTerms   DataScadenzaPagamento                      regime-dependent          CORE

  preceding document      BillingReference           ReferencedDocument           related document structures                CfdiRelacionados          CORE

  fiscal regime           profile/external           profile/external             jurisdictional                             RegimenFiscal             FISCAL

  receiver fiscal use     none                       none                         none                                       UsoCFDI                   FISCAL

  export classification   contextual                 contextual                   contextual                                 Exportacion               FISCAL

  fiscal UUID             none core                  none core                    fiscal/process IDs                         TFD UUID                  FISCAL

  transmission ID/status  external                   external                     SdI transmission/lifecycle                 authority/certification   CTC
                                                                                                                             lifecycle                 
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Appendix B. Example Jurisdiction Profile Skeleton

``` yaml
profile:
  id: MX-CFDI-4.0
  jurisdiction: MX
  regime: CFDI
  version: "4.0"

  constraints:
    - path: billingDocument.documentCurrency
      cardinality: "1"

    - path: billingDocument.seller.identifiers
      condition: "contains(type=TAX, scheme=RFC)"

  fiscalRequirements:
    - path: fiscalContext.partyContexts[SELLER].fiscalRegimeCode
    - path: fiscalContext.partyContexts[BUYER].fiscalRegimeCode
    - path: fiscalContext.partyContexts[BUYER].documentUseCode

  codeLists:
    - path: fiscalContext.partyContexts[SELLER].fiscalRegimeCode
      list: MX_FISCAL_REGIME

  rules:
    - id: MX-001
      description: Example conditional fiscal rule
      when: "..."
      assert: "..."
```

------------------------------------------------------------------------

# Appendix C. Example Mapping Skeleton

``` yaml
mapping:
  id: UBL-2.1-TO-SEMANTIC
  sourceFamily: UBL
  sourceVersion: "2.1"
  semanticModelVersion: "1.0"

  rules:
    - id: MAP-001
      source: /Invoice/cbc:ID
      target: billingDocument.documentNumber
      transform: direct

    - id: MAP-002
      source: /Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyName/cbc:Name
      target: billingDocument.seller.name
      transform: direct

    - id: MAP-003
      source: /Invoice/cbc:InvoiceTypeCode
      target: billingDocument.documentType
      transform:
        function: lookup
        table: UBL_DOCUMENT_TYPE_TO_SEMANTIC
```

------------------------------------------------------------------------

# Appendix D. Glossary

**Canonical model** --- Stable intermediate representation used to
reduce source-to-target coupling. In this proposal, canonical behaviour
is achieved through semantic meaning rather than copying one external
syntax.

**Semantic model** --- Model of business/fiscal concepts and their
relationships, independent of storage or message syntax.

**Jurisdiction profile** --- Rules specializing shared semantics for a
jurisdiction or regime.

**Jurisdiction extension** --- A namespaced, governed concept that is
genuinely distinct and cannot be represented by existing shared
semantics.

**Fiscal context** --- Fiscally significant information associated with
the legal invoice artefact but not universal commercial billing
semantics.

**Compliance transaction** --- Submission, clearance and lifecycle
processing of a document through a CTC regime.

**Alignment** --- Mapping a local term or structure to an existing
semantic concept.

**Promotion** --- Moving a previously local extension into shared
semantics after evidence demonstrates broader reusable meaning.

------------------------------------------------------------------------

## Review Outcome Sought

The immediate review is intended to answer four questions:

1.  **Are the semantic boundaries correct?**
2.  **Can the core represent materially different billing families
    without becoming format-specific?**
3.  **Are jurisdiction profiles and extensions sufficient to accommodate
    local requirements safely?**
4.  **Is the governance/onboarding approach strong enough to keep the
    model maintainable as country coverage grows?**

The next phase should use representative real documents and
specifications from additional non-European regimes to challenge these
assumptions and convert validated concepts into a formal
machine-readable schema and mapping catalogue.
