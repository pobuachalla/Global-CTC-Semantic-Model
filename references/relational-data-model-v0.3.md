# Global CTC Relational Data Model
## Logical Database Schema for the Semantic Billing Architecture

**Status:** Draft for architectural and data-model review  
**Revision:** 0.3 — incorporates French Extended CTC bidirectional invoice stress test  
**Purpose:** Define a relational/logical persistence model that complements the Global CTC Semantic Billing Model.

---

## 1. Purpose

The semantic model defines business meaning independently of persistence. This document describes one practical relational representation of that model for implementations that need to persist, query, reconcile, audit or operationally process canonical billing documents.

The relational model is deliberately **derived from** the semantic model rather than being allowed to redefine it.

```text
Semantic Model
     |
     | persistence design
     v
Logical Relational Model
     |
     | physical implementation
     v
Database Platform
```

The logical schema should support:

- canonical billing documents;
- reusable party and identifier structures;
- billing lines and tax calculations;
- credit/debit note relationships;
- fiscal context;
- jurisdiction-specific extensions;
- CTC submission/lifecycle processing;
- hierarchical/group/detail billing lines and signed values;
- source/target representation provenance;
- validation results and authority responses;
- optional persistence of jurisdiction profiles and mapping configuration.

---

## 2. Key Design Principles

### 2.1 Semantic model remains authoritative

A table is not automatically required for every semantic concept.

For example:

```text
Semantic:
Money = amount + currency
Quantity = value + unit
```

does not imply:

```text
MONEY table
QUANTITY table
```

For high-frequency value objects, grouped columns are usually simpler and more efficient.

### 2.2 Normalize identity and multiplicity

Concepts with their own multiplicity, identity or reuse characteristics are natural relational entities:

- Party
- BillingLine
- Tax
- DocumentRelationship
- PaymentMeans
- FiscalContext
- ComplianceTransaction

### 2.3 Separate stable schema from variable jurisdiction data

Stable reusable semantics belong in relational columns and tables.

Genuinely jurisdiction-specific structures belong in a governed extension mechanism, initially represented as typed JSON.

### 2.4 Separate billing/fiscal data from CTC processing

The database must preserve the same boundary as the semantic architecture.

```text
BillingDocument
     |
     +--> FiscalContext
     |
     +--> ComplianceTransaction[]
```

A document may exist independently of any CTC transaction and may be processed multiple times.

### 2.5 Avoid a global source-schema superset

The relational schema must not become a physical union of UBL, CII, FatturaPA, CFDI and every future country format.

---

## 3. High-Level Schema

```text
                    BILLING_DOCUMENT
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
 DOCUMENT_PARTY       BILLING_LINE       MONETARY_TOTAL
        |                  |
        v                  +--> TAX
      PARTY                +--> ADJUSTMENT
        |                  +--> LINE_ITEM
        |                  +--> LINE_PRICE
        |                  +--> LINE_CLASSIFICATION
        |                  +--> LINE_PARTY
        |                  +--> LINE_IDENTIFIER
        |                  +--> LINE_TAX_SUMMARY
        |                  +--> PRICE_ADJUSTMENT
        |
        +--> PARTY_IDENTIFIER
        +--> TAX_REGISTRATION
        +--> PARTY_LEGAL_REGISTRATION
        +--> ADDRESS
        +--> CONTACT

BILLING_DOCUMENT
    |
    +--> TAX_SUMMARY
    +--> ADJUSTMENT
    +--> DOCUMENT_RELATIONSHIP
    +--> PAYMENT_MEANS
    +--> PAYMENT_TERMS
    +--> SUPPLY
    +--> ATTACHMENT
    +--> DOCUMENT_REPRESENTATION
    |
    +--> FISCAL_CONTEXT
    |       +--> FISCAL_IDENTIFIER
    |       +--> FISCAL_PARTY_CONTEXT
    |       +--> FISCAL_EXTENSION
    |
    +--> COMPLIANCE_TRANSACTION
            +--> COMPLIANCE_LIFECYCLE_EVENT
            +--> VALIDATION_RESULT
            +--> AUTHORITY_RESPONSE
```

---

## 4. Billing Document

### BILLING_DOCUMENT

Primary relational representation of the semantic `BillingDocument`.

| Column | Role |
|---|---|
| `billing_document_id` | Surrogate PK |
| `document_number` | Business-facing document number |
| `document_series` | Optional series |
| `document_type_code` | INVOICE, CREDIT_NOTE, DEBIT_NOTE, etc. |
| `issue_date` | Issue date |
| `issue_time` | Optional issue time |
| `document_currency_code` | Primary currency |
| `tax_currency_code` | Optional alternate tax currency |
| `accounting_period_id` | Optional FK to PERIOD |
| `semantic_model_version` | Model version used to interpret row |
| `created_at`, `updated_at` | Technical audit timestamps |

A surrogate key is used because business document numbers are not reliably unique globally.

Recommended logical uniqueness should normally be defined using business context rather than `document_number` alone.

---

## 5. Parties and Roles

### DOCUMENT_PARTY

Associates parties to documents through semantic roles.

```text
BILLING_DOCUMENT
       |
       +-- SELLER ----------> PARTY
       +-- BUYER -----------> PARTY
       +-- PAYEE -----------> PARTY
       +-- TAX_REP ---------> PARTY
       +-- INTERMEDIARY ----> PARTY
```

Columns:

- `document_party_id` PK
- `billing_document_id` FK
- `party_id` FK
- `role_code`
- `sequence_no`

Suggested constraints:

- one SELLER per billing document;
- one BUYER per billing document;
- multiple rows permitted for roles that allow multiplicity.

### PARTY

Stores reusable party identity.

Core attributes:

- name
- legal_name
- trading_name

Party identifiers, tax registrations, addresses and contacts are normalized into child tables.

### PARTY_IDENTIFIER

Stores identifiers such as:

- VAT
- RFC
- GLN
- DUNS
- company-registration numbers
- network identifiers

Important fields include:

- identifier type
- scheme
- issuing authority
- country/jurisdiction context

### TAX_REGISTRATION

Separates tax registration from generic party identity.

This permits a party to have multiple registrations under different schemes and jurisdictions.

### PARTY_LEGAL_REGISTRATION

Stores legal registration semantics independently from tax or generic identifiers:

- registered name;
- registration identifier and scheme;
- legal form;
- jurisdiction.

This covers source structures where legal form and company-registration identity are first-class information.

### ADDRESS and CONTACT

Both are one-to-many from PARTY to allow multiple addresses/contact points.

---

## 6. Billing Lines

### BILLING_LINE

Represents each semantic billing line, including hierarchical group/detail structures.

Recommended columns:

- `billing_line_id` PK
- `billing_document_id` FK
- `parent_line_id` nullable self-FK
- `line_number`
- `line_role_code` (STANDARD, GROUP, DETAIL, ...)
- `contributes_to_document_totals`
- quantity value/unit
- line-net amount/currency
- optional period/tax-point references
- sequence number

`Money` and `Quantity` remain grouped columns rather than separate tables. Monetary values are **signed**; the database does not infer sign from document type.

`contributes_to_document_totals` may be populated by canonical mapping or derived from profile rules. Reconciliation queries must not blindly sum all physical lines.

### LINE_ITEM

One-to-one extension of a billing line containing product/service descriptive data.

Typical attributes:

- item name/description;
- seller item identifier;
- buyer item identifier;
- standard identifier and scheme;
- country of origin.

The model deliberately avoids introducing a global product master.

### LINE_PRICE

One-to-one extension of the line containing:

- net price amount/currency;
- optional gross price amount/currency;
- base quantity/unit.

### PRICE_ADJUSTMENT

Stores price-level gross-to-net adjustments separately from line-level allowances/charges. This avoids treating a price discount as though it were necessarily a line allowance contributing to invoice allowance totals.

### LINE_CLASSIFICATION

One-to-many classification table supporting global and jurisdictional schemes.

### LINE_PARTY

Associates a party with a billing line through a role. Document-level SELLER/BUYER roles act as defaults unless a profile supplies line-specific participant semantics.

```text
LINE_PARTY
----------
line_party_id PK
billing_line_id FK
party_id FK
role_code
sequence_no
```

### LINE_IDENTIFIER

Stores line/object identifiers that are semantically attached to the line but are not references to another business document.

### LINE_TAX_SUMMARY

Stores group/line-level aggregated tax outcomes where a profile provides a tax total independently from the line tax category/calculation detail.

## 7. Adjustments

### ADJUSTMENT

A shared relational representation for line-level and document-level allowances and charges.

Important columns:

- `adjustment_type_code`
- reason code/text
- percentage
- base amount/currency
- amount/currency

Scope is defined through ownership:

```text
document adjustment:
billing_document_id populated
billing_line_id null

line adjustment:
billing_line_id populated
billing_document_id optional/derived
```

A database CHECK constraint should prevent ambiguous ownership.

---

## 8. Tax

Tax is intentionally normalized separately from monetary totals.

### TAX

Represents a tax calculation or treatment at line or document scope.

Important fields:

- tax type
- direction: CHARGE / WITHHOLD
- category/code
- jurisdiction
- calculation method
- rate
- taxable base
- quantity base
- amount per unit
- tax amount
- exemption code/reason

The model supports VAT/GST but is not restricted to them.

### TAX_SUMMARY

Stores aggregated document-level tax outcomes, typically grouped by:

```text
tax type
+ direction
+ category
+ rate
```

Typical values:

- taxable amount
- tax amount
- currency

This keeps individual tax semantics separate from aggregated reporting totals.

---

## 9. Monetary Totals

### MONETARY_TOTAL

One row per billing document.

Suggested columns:

- line net amount
- allowance total
- charge total
- tax exclusive amount
- charged tax total
- withholding total
- tax inclusive amount
- prepaid amount
- rounding amount
- payable amount
- currency code

A single currency is used for the row because most document totals share the document currency.

If future regimes require multiple independently materialized total currencies, this can be normalized later.

---

## 10. Document Relationships

### DOCUMENT_RELATIONSHIP

Represents relationships such as:

- ORDER
- CONTRACT
- DELIVERY
- REFERENCES
- CREDITS
- DEBITS
- CORRECTS
- REPLACES
- CANCELS

A relationship may be document-level or line-level.

Typical relational fields:

- relationship type
- related document number
- related document type
- related issue date

External identifiers such as fiscal UUIDs can be added through an identifier child table if required.

This is preferable to creating dedicated nullable columns for every possible related-document type.

---

## 11. Payment

### PAYMENT_MEANS

Represents **how** payment is made.

Examples:

- bank transfer
- card
- direct debit
- cash
- jurisdiction-specific payment codes

Supports:

- payment reference
- amount
- currency
- due date
- account relationship

### FINANCIAL_ACCOUNT

Stores payment account information independently from the document.

Possible identifiers include:

- IBAN
- domestic account number
- BIC
- bank/institution identifiers

### PAYMENT_TERMS

Represents **when and under what conditions** payment is due.

Supports:

- due date
- base date
- number of days
- description
- percentage
- amount

---

## 12. Supply and Period

### SUPPLY

One-to-one optional relationship from BILLING_DOCUMENT.

Captures:

- supply date
- place of supply
- delivery party
- delivery address
- dispatch party
- dispatch address
- Incoterm
- transport reference

### PERIOD

Reusable period structure used by:

- billing documents
- lines
- payment terms
- future delivery structures

Contains start/end dates/times and description.

---

## 13. Attachments

### ATTACHMENT

Attachments should normally store metadata and a storage reference rather than large binary payloads directly in core relational rows.

Recommended attributes:

- identifier
- filename
- MIME type
- description
- external URI
- object-storage/content reference

---

## 13A. Document Representation

### DOCUMENT_REPRESENTATION

Captures provenance for each source or target serialization of a billing document.

Suggested columns:

- `document_representation_id` PK
- `billing_document_id` FK
- `direction_code` (SOURCE/TARGET)
- `format_family`
- `format_version`
- `customization_id`
- `profile_id`
- `mapping_version`
- `content_hash`
- `artifact_reference`
- `created_at`

Examples include UBL 2.1 + French Extended CTC CustomizationID/ProfileID, a generated CII representation, or an ERP JSON source. These values do not belong on `BILLING_DOCUMENT` itself.

## 14. Fiscal Context

### FISCAL_CONTEXT

One-to-one optional extension of BILLING_DOCUMENT.

Suggested columns:

- jurisdiction
- regime
- fiscal document type
- tax-point date
- place of taxation
- export classification
- fiscal model version

This table is the root for fiscal semantics that should not pollute the commercial billing tables.

### FISCAL_IDENTIFIER

Stores fiscal identifiers such as tax-authority UUIDs or other legally significant document identifiers.

### FISCAL_PARTY_CONTEXT

Associates jurisdictional fiscal data with a specific party and role.

Examples include:

- fiscal regime
- fiscal residence
- receiver document-use classification

### FISCAL_EXTENSION

Controlled escape mechanism for genuinely country-specific structures.

```text
namespace
extension_type
extension_version
payload_json
```

JSON is used here deliberately because the data is variable by jurisdiction.

This should not become a generic location for fields that simply have not yet been modeled correctly.

---

## 15. Compliance Transactions

### COMPLIANCE_TRANSACTION

One billing document may have zero or many compliance transactions.

Examples:

- initial clearance submission
- retry
- correction/cancellation workflow
- post-clearance reporting event
- lifecycle status interaction

Suggested columns:

- jurisdiction
- regime
- channel
- transmission ID
- submission ID
- authority reference
- submitted/received timestamps
- current status

### COMPLIANCE_LIFECYCLE_EVENT

Stores status history and processing events.

Examples:

- submitted
- accepted
- cleared
- rejected
- delivered
- cancelled
- reported

### VALIDATION_RESULT

Stores validation findings by layer:

```text
STRUCTURAL
SEMANTIC
PROFILE
TARGET
AUTHORITY
```

Important attributes:

- rule ID
- severity
- semantic path
- message

### AUTHORITY_RESPONSE

Stores structured metadata about responses from tax authorities/platforms.

Large/raw authority payloads should typically be referenced or retained separately.

---

## 16. Configuration Schema

Runtime document persistence and transformer configuration should be logically separated.

### JURISDICTION_PROFILE

Stores profile metadata:

- jurisdiction
- regime
- version
- effective dates
- status

### PROFILE_CONSTRAINT

Defines restrictions against semantic paths:

- required cardinality
- conditional requirement
- prohibition
- other constraint types

### PROFILE_CODE_LIST

Associates semantic paths with controlled code lists.

### PROFILE_RULE

Stores machine-evaluable profile/validation rules.

### MAPPING_DEFINITION

Defines one versioned source-to-semantic, semantic-to-target or direct transformation mapping.

Typical metadata:

- mapping ID
- direction
- source family/version
- target family/version
- semantic-model version
- mapping version
- status

### MAPPING_RULE

Stores individual mapping rules:

- source path
- semantic path
- target path
- transformation type
- transformation configuration
- sequence

Complex transform configuration can be stored as JSON because it is configuration rather than canonical business data.

---

## 17. Cardinality Summary

| Parent | Child | Cardinality |
|---|---|---|
| BillingDocument | BillingLine | 1:N |
| BillingDocument | DocumentParty | 1:N |
| Party | DocumentParty | 1:N |
| Party | PartyIdentifier | 1:N |
| Party | TaxRegistration | 1:N |
| Party | Address | 1:N |
| Party | Contact | 1:N |
| BillingLine | LineItem | 1:0..1 |
| BillingLine | LinePrice | 1:0..1 |
| BillingLine | LineClassification | 1:N |
| BillingLine | LineParty | 1:N |
| BillingLine | LineIdentifier | 1:N |
| BillingLine | LineTaxSummary | 1:N |
| LinePrice | PriceAdjustment | 1:N |
| BillingDocument / BillingLine | Adjustment | 1:N |
| BillingDocument / BillingLine | Tax | 1:N |
| BillingDocument | TaxSummary | 1:N |
| BillingDocument | MonetaryTotal | 1:1 |
| BillingDocument | PaymentMeans | 1:N |
| BillingDocument | PaymentTerms | 1:N |
| BillingDocument | DocumentRepresentation | 1:N |
| BillingDocument | FiscalContext | 1:0..1 |
| BillingDocument | ComplianceTransaction | 1:N |
| ComplianceTransaction | LifecycleEvent | 1:N |
| ComplianceTransaction | ValidationResult | 1:N |
| ComplianceTransaction | AuthorityResponse | 1:N |

---

## 18. Normalization Decisions

### Kept normalized

The following are normalized because of reuse or multiplicity:

- Party
- identifiers
- tax registrations
- addresses
- contacts
- billing lines and parent/child hierarchy
- line parties and identifiers
- classifications
- taxes
- adjustments
- document relationships
- payments
- fiscal context
- document representations/provenance
- compliance transactions

### Intentionally denormalized/value-object columns

The following semantic value objects are stored inline:

```text
Money
Quantity
```

Example:

```text
quantity_value
quantity_unit_code

tax_amount
tax_currency_code
```

This keeps SQL queries practical without losing semantic meaning.

### JSON usage

JSON should be restricted to areas with inherently variable structure:

- fiscal extensions
- raw lifecycle-event payloads
- authority responses
- transformation configuration

It should not be used as a substitute for modelling stable business semantics.

---

## 19. Recommended Constraints

Examples of logical/database constraints:

### Document roles

```text
UNIQUE(billing_document_id, role_code)
```

for singular roles such as SELLER and BUYER.

For roles allowing multiples, a more targeted constraint or role metadata table is required.

### Line hierarchy and contribution

`parent_line_id` must reference a line on the same `billing_document_id`.

Profiles can additionally validate allowed parent/child `line_role_code` combinations. Reconciliation uses `contributes_to_document_totals`, not an unconditional sum of all lines.

### Adjustment ownership

Exactly one supported owner should be populated:

```text
billing_document_id XOR billing_line_id
```

### Tax ownership

Same principle:

```text
billing_document_id XOR billing_line_id
```

if document and line taxes share one table.

### Monetary total

```text
billing_document_id UNIQUE NOT NULL
```

### Fiscal context

```text
billing_document_id UNIQUE NOT NULL
```

### Document numbering

Do not globally enforce uniqueness on `document_number`.

A meaningful uniqueness key may require:

```text
seller
+ document number
+ series
+ document type
+ jurisdiction/context
```

and may vary by source domain.

---

## 20. Indexing Considerations

Likely high-value indexes:

```text
BILLING_DOCUMENT(document_number)
BILLING_DOCUMENT(issue_date)
BILLING_DOCUMENT(document_type_code)
DOCUMENT_PARTY(billing_document_id, role_code)
PARTY_IDENTIFIER(identifier_value, scheme_code)
TAX_REGISTRATION(identifier_value, scheme_code)
BILLING_LINE(billing_document_id, sequence_no)
BILLING_LINE(billing_document_id, parent_line_id)
LINE_PARTY(billing_line_id, role_code)
DOCUMENT_REPRESENTATION(billing_document_id, direction_code)
TAX(billing_document_id)
TAX(billing_line_id)
COMPLIANCE_TRANSACTION(billing_document_id)
COMPLIANCE_TRANSACTION(authority_reference)
COMPLIANCE_TRANSACTION(status_code)
FISCAL_IDENTIFIER(identifier_value, scheme_code)
```

Indexing should ultimately be driven by runtime usage rather than the logical model alone.

---

## 21. Semantic-to-Relational Mapping

| Semantic concept | Relational representation |
|---|---|
| BillingDocument | BILLING_DOCUMENT |
| Party | PARTY |
| seller / buyer / role | DOCUMENT_PARTY |
| Identifier | PARTY_IDENTIFIER / FISCAL_IDENTIFIER |
| TaxRegistration | TAX_REGISTRATION |
| BillingLine | BILLING_LINE |
| BillingLine.parentLine / lineRole / contributesToDocumentTotals | BILLING_LINE self-FK + columns |
| BillingLine.parties | LINE_PARTY |
| BillingLine.identifiers | LINE_IDENTIFIER |
| Quantity | BILLING_LINE grouped columns |
| Money | grouped amount/currency columns |
| Item | LINE_ITEM |
| Price | LINE_PRICE |
| Price.adjustments | PRICE_ADJUSTMENT |
| ItemClassification | LINE_CLASSIFICATION |
| Adjustment | ADJUSTMENT |
| Tax | TAX |
| TaxSummary | TAX_SUMMARY |
| MonetaryTotal | MONETARY_TOTAL |
| DocumentRelationship | DOCUMENT_RELATIONSHIP |
| PaymentMeans | PAYMENT_MEANS |
| PaymentTerms | PAYMENT_TERMS |
| Supply | SUPPLY |
| Period | PERIOD |
| Attachment | ATTACHMENT |
| DocumentRepresentation | DOCUMENT_REPRESENTATION |
| FiscalContext | FISCAL_CONTEXT |
| FiscalPartyContext | FISCAL_PARTY_CONTEXT |
| JurisdictionExtension | FISCAL_EXTENSION |
| ComplianceTransaction | COMPLIANCE_TRANSACTION |

---

## 22. Open Design Questions

The following should be reviewed before physical implementation.

### Party reuse

Should PARTY represent:

1. reusable cross-document master-like identities; or
2. immutable party snapshots captured per document?

For audit/regulatory systems, snapshots are often safer because supplier/customer names and addresses can change over time.

### Hierarchical lines

Should `contributes_to_document_totals` be persisted as canonical state, or derived entirely from the active jurisdiction/profile rule set? Persisting it simplifies reconciliation and audit but duplicates a derivable rule.

### Line-level party snapshots

Should line parties point to the same PARTY snapshot rows used by document roles, or should a separate immutable line-party snapshot be permitted when the source supplies partial/different identity?

### Shared TAX table

A single TAX table for both line/document scope is compact but introduces nullable owner FKs. Separate LINE_TAX and DOCUMENT_TAX tables may provide stronger integrity.

### Shared ADJUSTMENT table

The same trade-off applies to adjustments.

### Currency normalization

Should currency remain embedded in each monetary column pair, or should document-currency inheritance be used to reduce storage?

### Fiscal extension storage

Should extension payloads remain JSON only, or should frequently used jurisdiction-specific extensions receive dedicated relational projections?

### Historical profile linkage

Should every persisted document retain the exact:

```text
semantic model version
jurisdiction profile version
mapping version
code-list version
```

used when it was transformed?

For auditability, the likely answer is yes.

### Provenance

`DOCUMENT_REPRESENTATION` captures document-level source/target provenance. Should the database also persist source-to-semantic lineage at field level, or should that remain in mapping/trace logs?

A dedicated field-lineage model may be valuable for explainability and regulatory assurance.

---

## 22A. French Extended CTC Stress-Test Findings

A bidirectional French Extended CTC UBL example materially strengthened the logical model:

1. **Hierarchical lines:** GROUP and DETAIL lines require self-referencing `BILLING_LINE.parent_line_id` and explicit line-role semantics.
2. **Reconciliation scope:** detail lines can repeat/explain a group amount and must not necessarily contribute independently to document totals.
3. **Signed values:** invoices can contain negative prices and deduction lines, so sign cannot be inferred from document type.
4. **Line parties:** participant identity can be supplied at line level and can differ from the document seller/buyer context.
5. **Line tax summary:** group lines may carry a tax total independently from detail-line tax category data.
6. **Price adjustments:** price-level allowance data should not automatically become line-level adjustment data.
7. **Tax point:** tax exigibility codes can be encoded in period structures and require profile-aware semantic mapping.
8. **Representation provenance:** UBLVersionID, CustomizationID and ProfileID identify the external representation/profile and should be retained outside the billing core.

These changes do not introduce France-specific columns into the shared relational core; they introduce reusable structures needed to persist the richer semantics exposed by the French profile.

## 23. Relationship to the Semantic Model

The relational schema is an implementation view of the semantic architecture.

It must be possible to change physical database design without changing business meaning.

For example:

```text
Semantic:
BillingDocument.seller -> Party
```

may be implemented relationally as:

```text
BILLING_DOCUMENT
      |
      v
DOCUMENT_PARTY(role='SELLER')
      |
      v
PARTY
```

Likewise:

```text
Semantic:
BillingLine.quantity -> Quantity
```

is implemented as:

```text
BILLING_LINE.quantity_value
BILLING_LINE.quantity_unit_code
```

The semantic model should therefore remain the contract used by mapping and business-rule layers, while the relational schema remains an implementation concern beneath it.

---

## 24. Review Outcome Sought

The relational-model review should determine:

1. whether the proposed normalization is appropriate for a transformation/compliance platform;
2. whether semantic boundaries are preserved in persistence;
3. whether fiscal and compliance processing data are sufficiently separated;
4. whether the schema can support multiple global invoice families without structural churn;
5. whether audit, provenance and versioning requirements require additional first-class entities;
6. whether shared TAX/ADJUSTMENT tables or scope-specific tables provide the better physical design.

The next step after review should be a physical schema for the selected database technology, including exact SQL types, indexes, constraints, migration/versioning strategy and representative queries.
