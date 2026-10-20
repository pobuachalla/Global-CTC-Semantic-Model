# CTC Transformation Framework — Complete Design Reference

> **Architecture revision: v1.1 — module boundary clarified**

> **Purpose of this document**
> This file is the complete design record for the CTC Transformation Framework — a configuration-driven service or embeddable library that sits inside a wider CTC compliance solution. Its responsibility is to transform invoice and related fiscal documents between ERP/native inbound representations, a common semantic model, and mandate-specific target formats across multiple countries.
>
> The framework is intentionally **not** the end-to-end CTC compliance platform. Authentication, tenant security, credential custody, authority transport, retries/reconciliation, regulatory lifecycle management, legal archiving, and operational case management are responsibilities of the host solution. The framework exposes clean contracts so those platform capabilities can invoke transformation consistently.
>
> It is structured for consumption by AI models assisting with implementation, critique, expansion, or PoC development. Every design decision is recorded with its rationale and the alternatives that were considered and rejected.
>
> **How to use this document**
> - For PoC implementation: start with §4 (Semantic model), §5 (Rule DSL), §6 (Adapters), §7 (ERP layer)
> - For critique and expansion: start with §11 (Decision log) and §12 (Known gaps)
> - For country-specific work: see §9 (Country rollout) and §10 (Disruption analysis)
> - For entity modelling: see §4 (complete entity definitions with all fields, types, cardinality, constraints)

---

## Table of contents

1. [Project context and goals](#1-project-context-and-goals)
2. [Design principles](#2-design-principles)
3. [Architecture overview](#3-architecture-overview)
4. [Semantic document model](#4-semantic-document-model)
5. [Rule DSL v2](#5-rule-dsl-v2)
6. [Format adapters](#6-format-adapters)
7. [ERP integration layer](#7-erp-integration-layer)
8. [Configuration system](#8-configuration-system)
9. [Country rollout plan](#9-country-rollout-plan)
10. [Country disruption analysis](#10-country-disruption-analysis)
11. [Architecture decision log](#11-architecture-decision-log)
12. [Known gaps and open questions](#12-known-gaps-and-open-questions)
13. [PoC implementation guide](#13-poc-implementation-guide)
14. [Critique prompts for AI models](#14-critique-prompts-for-ai-models)

---

## 1. Project context and goals

### Problem statement

A global CTC compliance solution must accept invoice data from many ERP systems and inbound mechanisms, then produce the country- and mandate-specific document representations required by tax authorities, access points, intermediaries, and downstream compliance components.

Without a common transformation layer, integrations tend to become either:

- **Point-to-point translators**: one implementation per source-target pair, creating N×M growth and duplicated mandate logic.
- **Hard-coded country engines**: transformation behaviour embedded in application code, making regulatory changes slow and difficult to govern.

The purpose of this module is to provide a reusable transformation capability that decouples inbound source diversity from outbound mandate diversity.

### Module responsibility

The framework owns:

- parsing supported inbound representations;
- mapping ERP/native source data into a common semantic document;
- semantic enrichment required for transformation;
- mandate-specific structural and business validation needed to create a valid target payload;
- transformation between the semantic model and supported target formats;
- preservation of source/native fields where needed for fidelity;
- deterministic rule execution and field-level lineage;
- reusable configuration packs for mandate mappings, code lists, and target rendering rules.

The host CTC compliance solution owns:

- external authentication and authorisation;
- tenant and legal-entity isolation;
- secret, key, and certificate custody;
- authority/API connectivity and transport;
- submission retries, reconciliation, acknowledgements, and regulatory status lifecycle;
- statutory archiving and evidence retention;
- workflow, exception handling, case management, and user-facing operations.

The framework may expose extension points used by host signing or delivery components, but it does not own those concerns.

### Goals

1. **Common transformation entry point**: accept supported ERP-native, structured fiscal, or already-normalised semantic input through one stable contract.
2. **Semantic pivot**: transform through a common `SemanticDocument` so source and target adapters scale approximately N+M rather than N×M.
3. **Configuration-driven mandate evolution**: express mapping, validation, lookup, and rendering changes as versioned configuration wherever the underlying structural capability already exists.
4. **Global format coverage**: support the country and format families listed in §9 while allowing new mandate packs to be added incrementally.
5. **Embeddable deployment**: run as a stateless service or library inside a wider compliance platform.
6. **Deterministic and explainable output**: every generated value should be traceable to source data, configuration, or an explicitly registered transform function.
7. **Fidelity-aware transformation**: preserve source-native information where semantic normalisation alone would make faithful re-emission impossible.

### Non-goals

This module is not responsible for deciding whether an invoice is legally in scope for a mandate, managing the end-to-end clearance lifecycle, transporting documents to authorities, holding taxpayer credentials, or providing the platform's security boundary. These concerns are expected to exist in the wider CTC solution and invoke this framework through well-defined contracts.

### Countries in scope

**Europe (9):** Belgium, Croatia, France, Germany, Denmark, Italy, Norway, Romania, Slovakia

**LATAM (14):** Mexico, Brazil, Argentina, Chile, Colombia, Costa Rica, Dominican Republic, Ecuador, El Salvador, Guatemala, Panama, Peru, Uruguay, Venezuela *(monitor only)*

**APAC / Other (2):** Malaysia, India

**Reference/stress-test mandates outside committed 25-country scope:** UAE PINT-AE and Saudi Arabia ZATCA are used to validate architectural extensibility for ASP-mediated flows, multilingual content, signatures, and stateful regulatory metadata. They are not part of the initial 25-country delivery commitment.

---

## 2. Design principles

### P1 — Transformation boundary first

The framework is a bounded transformation component inside a wider CTC platform. It transforms, validates for target-format correctness, renders, and explains. It does not own authority submission lifecycle, tenant security, credential custody, or legal archiving.

### P2 — Configuration-first, not configuration-only

Mandate changes that can be represented using existing structural capabilities — field mappings, code lists, validation rules, target rendering parameters, and semantic enrichment — should be configuration changes rather than service rebuilds. New parsers, new cryptographic mechanisms, new document structures, or genuinely new transformation primitives may still require code.

### P3 — Semantic pivot

All cross-format transformation passes through the `SemanticDocument` model. This gives N+M adapter scaling while providing a stable contract between inbound connectors and mandate-specific output packs.

### P4 — Fidelity is explicit

The semantic model captures reusable business and regulatory concepts. Source-specific representation details that cannot be safely normalised are retained in a native/source envelope rather than silently discarded. The framework distinguishes semantic equivalence from byte-for-byte round-trip fidelity.

### P5 — Multi-regime tax by design

The tax model supports concurrent multi-regime taxation (Brazil: legacy and reform taxes coexisting; India: IGST or CGST+SGST depending on jurisdiction). `TaxRegime` + `TaxApplication` is the core extensibility mechanism and must be validated against representative transition-period documents.

### P6 — Deterministic and observable by default

Every transformation records the resolved pack version, executed rules, warnings/errors, and field-level lineage. The same input plus the same immutable transformation pack must produce the same semantic and rendered output.

### P7 — ERP and mandate concerns remain separate but interoperable

ERP mapping is source-system configuration; mandate transformation is target-compliance configuration. `SemanticDocument` is the interface between them. The framework may expose a semantic requirements report so the host solution can identify when an ERP mapping cannot supply fields required by a selected target mandate.

### P8 — Host-platform integration through contracts

The framework exposes stable contracts for invocation, transformation results, validation errors, lineage, and rendered payloads. Security context, tenant context, authority route, signing credentials, delivery status, and lifecycle state are supplied or managed by the host platform rather than embedded in the transformation core.

---

## 3. Architecture overview

### Position within the wider CTC solution

```text
ERP / files / APIs / inbound CTC formats
                 │
                 ▼
      ┌─────────────────────────┐
      │ CTC Transformation      │
      │ Framework (this module) │
      │                         │
      │ Parse → Assemble        │
      │ → Enrich → Validate     │
      │ → Render                │
      └───────────┬─────────────┘
                  │ TransformationResult
                  ▼
      ┌─────────────────────────┐
      │ Wider CTC Platform      │
      │ scope / tenant / auth   │
      │ signing / routing       │
      │ submission / retry      │
      │ status / reconciliation │
      │ archive / operations    │
      └───────────┬─────────────┘
                  ▼
      Authority / ASP / AP / PAC / intermediary
```

The wider platform determines the business context and target obligation, resolves the relevant mandate scope, and invokes this framework. The framework returns a deterministic transformation result; it does not itself own the subsequent regulatory transaction lifecycle.

### Two transformation entry paths

```text
ERP-native input ──→ [Source Adapter / ERP Mapping] ──┐
                                                     ├─→ SemanticDocument → [Target Mandate Pack] → Rendered Payload
CTC/native format ─→ [Format Parser + Assembler] ────┘
```

**Stage 1 — Source normalisation**
- accepts raw ERP output, file/API payloads, or supported CTC formats;
- detects or is told the source profile;
- applies configurable source mappings and lookups;
- reconstructs semantic tax/party structures where source systems represent them differently;
- produces a `SemanticDocument` plus transformation lineage and preserved native/source data.

**Stage 2 — Target transformation**
- accepts `SemanticDocument`;
- uses a host-supplied or explicitly resolved `MandateScope`;
- loads one immutable transformation-pack version;
- runs enrich → validate → render;
- returns rendered content, validation results, lineage, pack identity, and optional metadata required by the host platform.

### Logical layers

| Layer | Name | Responsibility |
|---|---|---|
| L1 | Invocation | Stable library/service API; receives source profile, target scope, host context, and payload. |
| L2 | Parse | Format-specific parsers produce `ParseResult`. Stateless and side-effect free. |
| L3 | Assemble | Source/ERP assemblers convert parsed input into `SemanticDocument`. |
| L4 | Transform | Rule engine applies ordered enrichment and validation against an immutable transformation pack. |
| L5 | Render | Target emitter serialises `SemanticDocument` into the required target representation. No authority submission. |
| L6 | Explain | Returns lineage, validation issues, source/native preservation metadata, pack version/hash, and transformation metrics. |

### Core request/response contract

```typescript
interface TransformationRequest {
  source: SourceDescriptor;
  targetScope: MandateScope;
  payload: unknown;
  packVersion?: string;          // Optional explicit pin; host may resolve before invocation
  context?: TransformContext;    // Non-secret contextual values needed by rules
}

interface TransformationResult {
  semanticDocument: SemanticDocument;
  renderedPayload?: string | Uint8Array;
  targetFormat: string;
  packId: string;
  packVersion: string;
  packHash: string;
  validation: ValidationResult[];
  lineage: LineageRecord[];
  warnings: TransformationWarning[];
  hostActions?: HostActionRequirement[]; // e.g. external signing required
}
```

`HostActionRequirement` describes work the wider platform must perform after transformation, for example `SIGN_EXTERNALLY`, `SUBMIT_TO_AUTHORITY`, or `EMBED_AUTHORITY_RESPONSE`. It is descriptive only; the transformer does not perform those actions.

### Deployment modes

**Library mode** — embedded in a host process; configuration packs loaded from an injected repository/provider.

**Service mode** — stateless HTTP/gRPC service scaled horizontally. The host platform supplies tenant/security context and owns external persistence and workflow.

The transformation core should not require Redis, Kafka, PostgreSQL, or object storage to execute a deterministic transform. Those may be used by a service wrapper for caching/config distribution, but they are not architectural dependencies of the core library.

### Technology choices (PoC recommendation)

```text
Runtime:       Node.js 20+ (TypeScript)
HTTP wrapper:  Fastify or Hono (service mode only)
Validation:    Zod (runtime) + JSON Schema (configuration)
XML parsing:   fast-xml-parser with hardened parser settings
Config watch:  chokidar for local/service PoC; production provider is pluggable
Testing:       Vitest
```

---

## 4. Semantic document model

### 4.1 Overview

The `SemanticDocument` is the canonical pivot type. Every inbound document — regardless of source format or ERP origin — is normalised into a `SemanticDocument` before any target enrichment, validation, or rendering step runs.

**Why this is not a flat field container**: earlier versions used a flat `CanonicalInvoiceModel` with one field per concept. This broke on:
- Brazil: 4 concurrent tax regimes per line (ICMS + CBS + IBS + IS)
- India: one GST rate that splits into 1 or 2 tax applications depending on jurisdiction
- Malaysia: 3 party identifiers simultaneously (TIN + BRN + MSIC)
- Saudi Arabia: mandatory Arabic on all human-readable fields

The `SemanticDocument` uses typed sub-models for tax (`TaxRegime` + `TaxApplication`), multilingual text (`SemanticText`), and party identity (`PartyIdentifier[]`) that absorb all these cases without structural surgery.

### 4.2 Primitive types

All primitive types used in the model:

| Type alias | Base type | Format / constraint | Rationale |
|---|---|---|---|
| `ISODate` | string | `YYYY-MM-DD` (ISO 8601) | Avoids timezone ambiguity |
| `ISODateTime` | string | `YYYY-MM-DDThh:mm:ss±hh:mm` | Full timestamp with offset |
| `Decimal` | string | Numeric string, max 6dp | Avoids floating-point drift in monetary values |
| `CurrencyCode` | string | ISO 4217 alpha-3 | e.g. EUR, MXN, MYR |
| `CountryCode` | string | ISO 3166-1 alpha-2 | e.g. IT, MX, MY |
| `RegionCode` | string | ISO 3166-2 | e.g. BR-SP, IN-MH |
| `LanguageTag` | string | BCP-47 | e.g. en, ar, pt-BR |
| `FormatFamily` | Enum | `ubl \| sdi \| sat \| sefaz \| gstn \| lhdn \| latam_dte \| custom` | Identifies parser/assembler family |
| `ClearanceModel` | Enum | `clearance \| dctce \| post_audit \| reporting` | Authority submission model |

### 4.3 SemanticText

Multilingual string carrier. Used for all human-readable text fields.

```typescript
interface SemanticText {
  default: string;                    // Primary / always present
  [lang: LanguageTag]: string;        // BCP-47 keyed variants: "ar", "ptBR", "frFR"
}

// Examples:
// { default: "Acme Corp" }
// { default: "Acme Corp", ar: "شركة أكمي" }   // Saudi Arabia: ar mandatory
// { default: "Indústria Ltda", ptBR: "..." }
```

**Mandate enforcement**: Saudi Arabia ZATCA pack enforces `.ar` on `supplier.legalName`, `buyer.legalName`, `lines[].description`, all address fields. UAE PINT-AE warns if `.ar` absent (recommended, not mandatory).

### 4.4 PartyIdentifier

A single typed identifier. Parties carry an array (`identifiers[]`) to support multi-identifier schemes.

```typescript
interface PartyIdentifier {
  scheme: string;   // e.g. "EU:VAT", "IT:PIVA", "IT:CF", "MX:RFC", "IN:GSTIN",
                    //      "BR:CNPJ", "BR:CPF", "SA:VAT", "AE:TRN", "AE:TIN",
                    //      "MY:TIN", "MY:BRN", "MY:MSIC", "PEPPOL:GLN"
  value: string;    // Raw identifier value as issued
}
```

**Why an array**: Malaysia carries TIN + BRN + MSIC simultaneously. UAE carries TRN + TIN (TIN = first 10 digits of TRN). Brazil carries CNPJ + CPF for natural persons. The v1 single `taxId + taxIdScheme` pair cannot model this.

### 4.5 SemanticAddress

```typescript
interface SemanticAddress {
  streetLine1?: SemanticText;   // FatturaPA: Indirizzo+NumeroCivico concatenated
  streetLine2?: SemanticText;
  city: SemanticText;           // Required. GSTIN: Loc field. NF-e: xMun.
  state?: string;               // ISO 3166-2 preferred. NF-e UF; GSTIN Stcd.
  postalCode?: string;          // Format varies by country
  countryCode: CountryCode;     // Hardcoded by adapters where absent (NF-e→BR, GSTIN→IN)
}
```

### 4.6 Contact

```typescript
interface Contact {
  name?: string;
  phone?: string;
  email?: string;
}
```

### 4.7 SemanticParty

```typescript
interface SemanticParty {
  legalName: SemanticText;          // Mandatory Arabic (.ar) for SA ZATCA. Recommended for AE.
  tradingName?: SemanticText;
  identifiers: PartyIdentifier[];   // Min 1. First entry = primary tax ID.
  address: SemanticAddress;
  contact?: Contact;
}
```

### 4.8 TaxRegime

Registers a named tax authority and jurisdictional scope. All `TaxApplication` records reference a `TaxRegime` by `regimeId`.

```typescript
interface TaxRegime {
  regimeId: string;         // Unique within document. FK for TaxApplication.regimeRef.
  name: string;             // Display name: "VAT", "IVA", "IGST", "ICMS", "CBS"
  authority: string;        // "Agenzia delle Entrate", "SAT", "GSTN", "SEFAZ"
  country: CountryCode;
  region?: RegionCode;      // Present for state-level regimes (e.g. BR-SP for ICMS SEFAZ-SP)
  level: 'federal' | 'state' | 'municipal';
}
```

**Standard regimes by format:**

| Format | Regimes registered | Notes |
|---|---|---|
| UBL / EN 16931 | `VAT_EU` (or `VAT_DE`, `VAT_NL`, etc.) | Single regime |
| FatturaPA | `VAT_IT` | Single regime. Natura code maps to categoryCode. |
| CFDI 4.0 | `IVA_MX`, `IEPS_MX`, `ISR_MX`, `RETENCION_MX` | One per Impuesto present |
| NF-e 4.0 | `ICMS_BR`, `PIS_BR`, `COFINS_BR` (+ `CBS_BR`, `IBS_BR`, `IS_BR` from Aug 2026) | Multi-regime mandatory |
| INV-01 | `GST_IN_IGST` (inter-state) OR `GST_IN_CGST` + `GST_IN_SGST` (intra-state) | Jurisdiction-dependent |
| MyInvois | `SST_MY_SALES` or `SST_MY_SERVICE` | Two sub-regimes |

### 4.9 JurisdictionContext

Transient routing context. Not persisted in `SemanticDocument` after assembly — used by conditional tax rules.

```typescript
interface JurisdictionContext {
  supplyType?: 'inter_state' | 'intra_state' | 'union_territory' | 'export' | 'sez';
  sellerStateCode?: string;   // 2-digit state from GSTIN prefix (IN) or UF (BR)
  placeOfSupply?: string;     // India BuyerDtls.Pos; Brazil cMun for services
  exportCategory?: string;    // EXPWP / EXPWOP / SEZWP / SEZWOP (India)
}
```

### 4.10 TaxApplication

One tax regime applied to one taxable base. Core multi-regime construct.

```typescript
interface TaxApplication {
  regimeRef: string;                // FK → TaxRegime.regimeId (must exist in document.taxRegimes)
  categoryCode: 'S'|'Z'|'E'|'AE'|'K'|'G'|'O';  // EN 16931: S=standard, Z=zero, E=exempt,
                                                   // AE=reverse charge, K=OSS/IOSS, G=export, O=other
  rate: Decimal | null;             // Percentage string e.g. "19.00". null for E/AE/K.
  taxableAmount: Decimal;
  taxAmount: Decimal;
  withholdingAmount?: Decimal;      // MX retenciones; IN TDS; SA withholding
  exemptionReasonCode?: string;     // FatturaPA Natura (N1–N7); UBL TaxExemptionReasonCode
  exemptionReasonText?: string;
  jurisdiction?: JurisdictionContext;
}
```

**Cardinality by format:**

| Format | TaxApplication count | Explanation |
|---|---|---|
| UBL single rate | 1 | One S-category application |
| UBL mixed rates | 2–3 | One per distinct rate |
| FatturaPA with Natura | 2 | One S + one E/AE/Z per Natura code |
| CFDI IVA only | 1 | One IVA_MX application |
| CFDI IVA + ISR | 2 | IVA_MX + ISR_MX (withholding) |
| NF-e (3 regimes) | 3 | ICMS_BR + PIS_BR + COFINS_BR |
| NF-e (Aug 2026+) | 4–6 | + CBS_BR + IBS_BR + IS_BR |
| INV-01 inter-state | 1 | GST_IN_IGST only |
| INV-01 intra-state + cess | 3 | GST_IN_CGST + GST_IN_SGST + GST_IN_CESS |
| MyInvois SST | 1 | SST_MY_SALES or SST_MY_SERVICE |

### 4.11 ItemClassification

```typescript
interface ItemClassification {
  scheme: string;   // CPV (EU), HSN (India), SAT:ClaveProdServ (Mexico), NCM (Brazil)
  code: string;
  name?: string;    // Present in some formats (SAP IDoc)
}
```

### 4.12 LineCharge

```typescript
interface LineCharge {
  isCharge: boolean;            // true = surcharge, false = allowance/discount
  scope: 'line';
  amount: Decimal;
  percentage?: Decimal;
  reasonCode?: string;
  reasonText?: SemanticText;
}
```

### 4.13 SemanticLine

```typescript
interface SemanticLine {
  id: string;
  description: SemanticText;            // Mandatory Arabic for SA ZATCA
  sellerItemId?: string;
  buyerItemId?: string;
  classifications?: ItemClassification[];
  unitCode: string;                     // UN/CEFACT. Default "C62" when absent in source.
  quantity: Decimal;
  unitPrice: Decimal;
  grossUnitPrice?: Decimal;
  netAmount: Decimal;
  taxApplications: TaxApplication[];    // Line-level. Brazil: 3–6 per line. India: 1 or 2.
  placeOfSupply?: string;               // Mandatory India; present Brazil service lines
  charges?: LineCharge[];
  deliveryPeriodStart?: ISODate;
  deliveryPeriodEnd?: ISODate;
  note?: SemanticText;
}
```

### 4.14 RegimeTaxTotal

```typescript
interface RegimeTaxTotal {
  regimeRef: string;              // FK → TaxRegime.regimeId
  taxableAmount: Decimal;
  taxAmount: Decimal;
  withholdingAmount?: Decimal;
}
```

### 4.15 AEDTotals

UAE PINT-AE mandatory. Present only when `targetScope.country = "AE"` and `currencyCode ≠ "AED"`.

```typescript
interface AEDTotals {
  taxableAmount: Decimal;
  taxAmount: Decimal;
  totalAmount: Decimal;
  exchangeRate: Decimal;          // FTA daily rate or contractual rate
  exchangeRateDate: ISODate;      // Must be recorded for audit
}
```

### 4.16 MonetaryTotal

```typescript
interface MonetaryTotal {
  lineExtensionAmount: Decimal;     // Sum of all lines[].netAmount
  taxExclusiveAmount: Decimal;      // Pre-tax total after doc-level charges
  taxAmountByRegime: RegimeTaxTotal[]; // One per registered TaxRegime (NOT a scalar)
  totalTaxAmount: Decimal;          // Derived: sum of taxAmountByRegime[].taxAmount
  taxInclusiveAmount: Decimal;      // taxExclusiveAmount + totalTaxAmount
  allowanceTotalAmount?: Decimal;
  chargeTotalAmount?: Decimal;
  roundingAmount?: Decimal;         // null ≠ 0.00 (different semantics)
  prepaidAmount?: Decimal;
  duePayableAmount: Decimal;        // taxInclusiveAmount − prepaidAmount ± rounding
  aedTotals?: AEDTotals;            // UAE PINT-AE only
}
```

**Critical design note**: `taxAmountByRegime[]` replaces a single `taxAmount` scalar. This is mandatory for Brazil (4 regimes) and India (IGST or CGST+SGST). Emitters must sum all entries when the target format expects a single total.

### 4.17 DocumentCharge

```typescript
interface DocumentCharge {
  isCharge: boolean;
  scope: 'document';
  amount: Decimal;
  baseAmount?: Decimal;
  percentage?: Decimal;
  reasonCode?: string;
  reasonText?: SemanticText;
  regimeRef?: string;             // FK → TaxRegime when charge itself is taxable
  taxRate?: Decimal;
}
```

### 4.18 PaymentMeans

```typescript
interface PaymentMeans {
  meansCode: string;              // UNCL4461. Adapters map: MP05→30, FormaPago 03→30
  paymentDueDate?: ISODate;
  paymentTermsNote?: SemanticText;
  accountId?: string;             // IBAN or account number
  financialInstitutionId?: string; // BIC/SWIFT
  paymentReference?: string;
}
```

### 4.19 SemanticDelivery

```typescript
interface SemanticDelivery {
  date?: ISODate;
  periodStart?: ISODate;
  periodEnd?: ISODate;
  address?: SemanticAddress;
  partyName?: SemanticText;
}
```

### 4.20 SemanticReferences

```typescript
interface SemanticReferences {
  orderRef?: string;
  contractRef?: string;
  projectRef?: string;
  precedingDocumentRef?: string;    // Used for credit notes and debit notes
  precedingDocumentDate?: ISODate;
  despatchRef?: string;
  receivingAdviceRef?: string;
}
```

### 4.21 SemanticAttachment

```typescript
interface SemanticAttachment {
  id: string;
  description?: SemanticText;
  mimeType?: string;
  embeddedContent?: string;         // Base64-encoded. Mutually exclusive with externalUri.
  externalUri?: string;
}
```

### 4.22 MandateScope

The resolution unit for the extension pack registry and rule resolver. Replaces the simpler `country + version` pair to support sub-national mandates.

```typescript
interface MandateScope {
  country: CountryCode;
  region?: RegionCode;          // Brazil NFS-e: "BR-SP" for São Paulo
  municipality?: string;        // Brazil NFS-e: "SAO_PAULO", "RIO_DE_JANEIRO"
  mandateId: string;            // "FATTURAPA", "CFDI", "NFE", "GSTINV01", "ZATCA_PHASE2"
  version: string;              // "1.3.2", "4.0", "2024"
  effectiveFrom: ISODate;
  effectiveTo?: ISODate;        // Absent = open-ended
}
```

**Resolution priority** (most specific wins):
1. `country + region + municipality + mandateId + version`
2. `country + region + mandateId + version`
3. `country + mandateId + version`
4. `country + mandateId` + highest version ≤ `effectiveDate`

### 4.23 SignatureData

```typescript
interface SignatureData {
  value: string;                      // Base64 signature/seal. MX: sello. IT: CAdES-BES.
  algorithm?: string;                 // XAdES-BES, CAdES-BES, RSA-SHA256, ECDSA-P256
  certificateSerial?: string;         // MX: NoCertificado. SA: CSID.
  signingDateTime?: ISODateTime;
  authorityRef?: string;              // MX UUID (36-char); IN IRN (64-char SHA-256);
                                      // MY LHDN UUID; SA UUID
  previousDocumentHash?: string;      // ZATCA PIH — SHA-256 of preceding invoice XML
}
```

### 4.24 LineageRecord

```typescript
interface LineageRecord {
  targetConcept: string;    // SemanticDocument path written: "taxApplications[0].rate"
  sourceField: string;      // Source path read: "Traslado/@TasaOCuota"
  ruleId: string;           // Rule ID from rule file: "map-tax-rate-cfdi"
  ruleKind: string;         // field_map | code_map | fn | tax_application | erp_path | etc.
  inputValue?: string;      // Raw value before transform
  outputValue?: string;     // Value after transform
  transform?: string;       // Transform description: "percent_from_decimal ×100"
  rationale?: string;       // Why this mapping was applied
  durationMs?: number;
}
```

### 4.25 DocumentControl

```typescript
interface DocumentControl {
  sourceFamily: FormatFamily;
  sourceFormat: string;             // "CFDI:4.0", "FATTURAPA:1.3.2", "GSTINV01:1.1"
  targetScope?: MandateScope;       // Supplied/resolved before target transformation.
  clearanceModel?: ClearanceModel;  // Descriptive metadata for the host platform; not workflow state.
  transmissionProfile?: string;     // e.g. Peppol profile URN
  lineage?: LineageRecord[];
  sourceDocumentHash?: string;      // Optional fidelity/audit correlation supplied or calculated by wrapper.
}

// Regulatory lifecycle values such as authority signatures, clearance UUIDs,
// invoice counters, cancellation deadlines, acknowledgement status, retries,
// and authority responses belong to the wider CTC platform. Where a target
// payload structurally requires one of those values, the transformer exposes
// it as a required host input or HostActionRequirement rather than owning state.
```

### 4.26 FormatNativeBag

Carries mandate-specific fields with no semantic equivalent. Typed by `FormatFamily`, not country.

```typescript
interface FormatNativeBag {
  ubl?: UBLFamilyNative;
  sdi?: SDIFamilyNative;
  sat?: SATFamilyNative;
  sefaz?: SEFAZFamilyNative;
  gstn?: GSTNFamilyNative;
  lhdn?: LHDNFamilyNative;
  [family: string]: unknown;    // Third-party families registered at runtime
}

interface UBLFamilyNative {
  customizationId?: string;
  profileId?: string;
  zatca?: {
    uuid: string;
    icv: number;                    // Invoice counter (mandatory Phase 2)
    pih: string;                    // Previous invoice hash (mandatory Phase 2)
    stamp?: string;                 // ZATCA cryptographic stamp after clearance
    deviceCertificateSerial?: string;
    invoiceTypeCode: string;        // "0100000" standard, "0200000" simplified
  };
  pintAE?: {
    supplierTIN: string;            // First 10 digits of TRN
    buyerTIN?: string;
    transactionType: 'standard' | 'free_zone' | 'import_service' | 'reverse_charge';
    aspId?: string;
    ftaSubmissionId?: string;
  };
}

interface SDIFamilyNative {
  tipoDocumento: string;            // TD01, TD04, TD05…
  regimeFiscale: string;            // RF01, RF19…
  codiceDestinatario?: string;      // 7-char SDI routing code
  pecDestinatario?: string;
  cig?: string;                     // Public procurement CIG code
  cup?: string;                     // Public works CUP code
  art73?: 'SI';
  lineNatura?: Record<string, { natura?: string; esigibilitaIVA?: string }>;
}

interface SATFamilyNative {
  uuid?: string;
  serie?: string;
  folio?: string;
  sello?: string;
  noCertificado?: string;
  noCertificadoSAT?: string;
  selloSAT?: string;
  exportacion?: string;
  complementoType?: string;
  supplierRFC: string;
  buyerRFC: string;
  usoCFDI?: string;
  rawTasaOCuota?: string;           // "0.160000" — preserved for CFDI re-emit
  lineClaveProdServ?: Record<string, string>;
}

interface SEFAZFamilyNative {
  accessKey: string;                // 44-digit NF-e access key (chNFe)
  authorizationCode?: string;
  serie?: string;
  numero?: string;
  tipoEmissao?: string;
  cnpjEmissor: string;              // From 2026: may be alphanumeric
  cUFDestino?: string;
  modelo?: string;                  // "55" NF-e, "65" NFC-e
  cMunPrestador?: string;
  cMunTomador?: string;
  ibsCbsClassification?: Record<string, {
    cClassTrib: string;
    isDeferral?: boolean;
    isPresumedCredit?: boolean;
    cbsRate?: Decimal;
    ibsFederalRate?: Decimal;
    ibsMunicipalRate?: Decimal;
  }>;
}

interface GSTNFamilyNative {
  irn?: string;                     // 64-char SHA-256 from IRP
  transactionCategory: string;      // "B2B", "EXPWP", "EXPWOP", "SEZWP", "SEZWOP"
  regRev: string;                   // "RG" regular / "RV" reverse charge
  docType?: string;
  supplierGstin: string;
  buyerGstin: string;
  placeOfSupply: string;            // 2-digit state code
  isReverseCharge?: boolean;
  exportDetails?: {
    exportCategory: string;
    shippingBillNo?: string;
    shippingBillDate?: ISODate;
    port?: string;
    foreignCurrency?: string;
    countryCode?: string;
  };
  ewayBill?: {                      // Submitted separately to EWB portal, not via invoice
    eWayBillNo?: string;
    transMode?: string;
    transDistance?: string;
    transporterGstin?: string;
    vehicleNo?: string;
    vehicleType?: string;
  };
  cessAmount?: Decimal;
  stateCessAmount?: Decimal;
}

interface LHDNFamilyNative {
  uuid?: string;                    // LHDN-assigned after validation
  submittedDateTime?: ISODateTime;
  validatedDateTime?: ISODateTime;
  eInvoiceVersion?: string;
  invoiceTypeCode: string;          // "01" invoice, "02" credit note…
  supplierTIN: string;
  buyerTIN?: string;
  supplierSST?: string;
  supplierMSIC?: string;
}
```

### 4.27 Root: SemanticDocument

```typescript
interface SemanticDocument {
  identity: DocumentIdentity;
  supplier: SemanticParty;
  buyer: SemanticParty;
  payee?: Pick<SemanticParty, 'legalName' | 'identifiers'>;
  taxRepresentative?: Pick<SemanticParty, 'legalName' | 'identifiers'>;
  taxRegimes: TaxRegime[];              // All regimes active on this document. Min 1.
  taxApplications: TaxApplication[];   // Document-level. Min 1.
  lines: SemanticLine[];               // Min 1.
  totals: MonetaryTotal;
  charges?: DocumentCharge[];
  paymentMeans?: PaymentMeans[];
  delivery?: SemanticDelivery;
  references?: SemanticReferences;
  attachments?: SemanticAttachment[];
  control: DocumentControl;
  native: FormatNativeBag;
}
```

### 4.28 Entity relationships

```
SemanticDocument 1..1 ──── DocumentIdentity
SemanticDocument 1..N ──── SemanticParty (supplier, buyer; optional: payee, taxRepresentative)
SemanticDocument 1..N ──── TaxRegime
SemanticDocument 1..N ──── TaxApplication   (document-level)
SemanticDocument 1..N ──── SemanticLine
SemanticDocument 1..1 ──── MonetaryTotal
SemanticDocument 0..N ──── DocumentCharge
SemanticDocument 0..N ──── PaymentMeans
SemanticDocument 0..1 ──── SemanticDelivery
SemanticDocument 0..1 ──── SemanticReferences
SemanticDocument 0..N ──── SemanticAttachment
SemanticDocument 1..1 ──── DocumentControl
SemanticDocument 1..1 ──── FormatNativeBag

SemanticParty   1..N ──── PartyIdentifier
SemanticParty   1..1 ──── SemanticAddress
SemanticParty   0..1 ──── Contact

SemanticLine    1..N ──── TaxApplication   (line-level, same type as document-level)
SemanticLine    0..N ──── ItemClassification
SemanticLine    0..N ──── LineCharge

TaxApplication  }o──|| ── TaxRegime        (regimeRef FK → regimeId)
TaxApplication  0..1 ──── JurisdictionContext

MonetaryTotal   1..N ──── RegimeTaxTotal   (one per TaxRegime)
MonetaryTotal   0..1 ──── AEDTotals        (UAE PINT-AE only)

DocumentControl 0..1 ──── MandateScope     (target scope)
DocumentControl 0..1 ──── SignatureData
DocumentControl 0..N ──── LineageRecord

FormatNativeBag 0..1 ──── UBLFamilyNative
FormatNativeBag 0..1 ──── SDIFamilyNative
FormatNativeBag 0..1 ──── SATFamilyNative
FormatNativeBag 0..1 ──── SEFAZFamilyNative
FormatNativeBag 0..1 ──── GSTNFamilyNative
FormatNativeBag 0..1 ──── LHDNFamilyNative
```

### 4.29 Cross-entity validation constraints

These constraints are enforced by the validate stage after all field mappings and enrichments run.

| ID | Constraint | Severity | Scope |
|---|---|---|---|
| CV-01 | `TaxApplication.regimeRef` must match a `TaxRegime.regimeId` in the same document | error | All |
| CV-02 | Sum of line-level `taxApplications[r].taxAmount` (by regimeRef) must equal document-level within ±0.02 | error | All |
| CV-03 | `MonetaryTotal.totalTaxAmount` must equal sum of all `RegimeTaxTotal.taxAmount` within ±0.01 | error | All |
| CV-04 | `taxInclusiveAmount = taxExclusiveAmount + totalTaxAmount ± roundingAmount` within ±0.02 | error | All |
| CV-05 | `lineExtensionAmount` must equal sum of all `SemanticLine.netAmount` within ±0.02 | error | All |
| CV-06 | If `categoryCode ∈ {E, AE, K}`: `rate` must be null | error | All |
| CV-07 | If `categoryCode = S` and `rate` is null: emit warning | warning | All |
| CV-08 | India: exactly one of `{GST_IN_IGST}` or `{GST_IN_CGST, GST_IN_SGST}` must appear — not both | error | IN |
| CV-09 | Brazil NF-e: ICMS_BR, PIS_BR, COFINS_BR must all be present | error | BR:NFE |
| CV-10 | `DocumentControl.targetScope` must be set before validate stage | error | All |
| CV-11 | If `aedTotals` present: `targetScope.country` must equal "AE" | error | AE |
| CV-12 | SA ZATCA Phase 2: `invoiceCounter` must be present and sequential | error | SA |
| CV-13 | SA ZATCA Phase 2: `previousDocumentHash` must match SHA-256 of preceding invoice | error | SA |
| CV-14 | `taxRegimes[]` must contain at least one entry | error | All |
| CV-15 | India: if `placeOfSupply` absent on any line: emit warning | warning | IN |

### 4.30 Null and default conventions

| Field | Convention when absent in source |
|---|---|
| `SemanticLine.unitCode` | Default to `"C62"` (UN/CEFACT each/unit) |
| `SemanticParty.identifiers[0].scheme` | Infer from source country where unambiguous |
| `SemanticAddress.city` | Set to empty string `""` |
| `TaxApplication.rate` | Set to `null` — emitters handle per target format |
| `MonetaryTotal.roundingAmount` | Omit (null). Do NOT default to 0.00. |
| `DocumentControl.transmissionProfile` | Omit. Required only for Peppol-family mandates. |
| `SemanticText` variants beyond `default` | Omit. Empty string ≠ absent — different semantics. |

---

## 5. Rule DSL v2

### 5.1 Overview

The Rule DSL is a YAML-based declarative language for expressing field mappings, code translations, tax regime registrations, and validation rules. It is the primary authoring interface for mandate analysts. Complex transforms use `fn` rules implemented by engineers.

**Authorship model**: declarative rules (`field_map`, `code_map`, `tax_regime`, `tax_application`, `jurisdiction`, `semantic_text`, `validate`) are analyst-owned. `fn` rules are engineer-owned.

### 5.2 File structure

```yaml
id: cfdi-4.0-to-cim-base
description: >
  Inbound assembly rules for CFDI 4.0 (Mexico SAT) to SemanticDocument.
scope:
  country: MX
  mandate_id: CFDI
  version: "4.0"
  # Optional sub-national:
  # region: BR-SP
  # municipality: SAO_PAULO
stage: assemble   # assemble | enrich | validate | sign
rules:
  - id: map-invoice-id
    kind: field_map
    ...
```

### 5.3 Rule kinds

#### field_map
Direct field copy with optional transform.

```yaml
- id: map-issue-date
  kind: field_map
  source: "@Fecha"                    # XPath / JSONPath / attribute
  target: "identity.issueDate"
  transform: date_from_datetime       # strip time component
  priority: 10
  on_error: warn                      # skip | warn | fail

- id: map-currency-literal
  kind: field_map
  source: ~                           # null source = use literal
  literal: "INR"
  target: "identity.currencyCode"
```

#### code_map
Lookup table translation of source codes to canonical codes.

```yaml
- id: map-invoice-type
  kind: code_map
  source: "@TipoDeComprobante"
  target: "identity.typeCode"
  lookup:
    I: "380"
    E: "381"
    T: "380"
    P: "386"
  default: "380"
  on_error: fail

- id: map-unit-code
  kind: code_map
  source: "Conceptos/Concepto[].@ClaveUnidad"
  target: "lines[].unitCode"
  lookup_file: lookups/mx-unit-codes.yaml    # External lookup file
  default: "C62"
```

#### concat
Concatenate multiple source fields.

```yaml
- id: map-street-address
  kind: concat
  sources:
    - "Sede/Indirizzo"
    - "Sede/NumeroCivico"
  separator: ", "
  prefix: "n. "                       # Applied to second source
  skip_empty: true
  target: "supplier.address.streetLine1.default"
```

#### conditional
Apply a sub-rule only when a condition is met.

```yaml
- id: map-tax-rate-exento
  kind: conditional
  condition:
    field: "Traslado/@TipoFactor"
    op: eq                            # eq | neq | exists | not_exists | in | regex | gt | lt
    value: "Exento"
  then:
    kind: field_map
    source: ~
    literal: null
    target: "lines[].taxRate"
```

#### tax_regime
Register a `TaxRegime` in the document.

```yaml
- id: regime-icms
  kind: tax_regime
  regime_id: ICMS_BR
  name: "ICMS"
  authority: "SEFAZ"
  country: BR
  level: state
  priority: 5
```

#### tax_application
Create a `TaxApplication` referencing a registered regime.

```yaml
- id: tax-igst-inter-state
  kind: conditional
  condition:
    field: "_context.supplyType"
    op: eq
    value: "inter_state"
  then:
    kind: tax_application
    regime_ref: GST_IN_IGST
    source_rate:   "ItemList[].GstRt"
    source_base:   "ItemList[].AssAmt"
    source_amount: "ItemList[].IgstAmt"
    target_lines:  "lines[].taxApplications"
    category_code: S
    jurisdiction:
      supply_type: inter_state
      state_code_field: "native.gstn.placeOfSupply"
```

#### jurisdiction
Derive supply type from party identifiers.

```yaml
- id: derive-supply-type
  kind: jurisdiction
  inputs:
    supplier_state: "native.gstn.supplierGstin"    # extract chars 0-1
    buyer_state:    "native.gstn.buyerGstin"
    place_of_supply: "BuyerDtls.Pos"
  outputs:
    - target: "native.gstn.placeOfSupply"
    - target: "_context.supplyType"
```

#### semantic_text
Populate `SemanticText` with language variants.

```yaml
- id: map-supplier-name-bilingual
  kind: semantic_text
  source_default: "SellerDtls/cbc:PartyLegalEntity/cbc:RegistrationName[@xml:lang='en']"
  source_ar:      "SellerDtls/cbc:PartyLegalEntity/cbc:RegistrationName[@xml:lang='ar']"
  target: "supplier.legalName"
  on_missing_ar: error               # SA ZATCA: error. AE PINT-AE: warn
```

#### fn
Engineer-owned escape hatch for complex transforms.

```yaml
- id: fn-derive-invoice-number
  kind: fn
  fn: mx.deriveInvoiceNumber
  outputs:
    - target: "identity.id"
  priority: 10
```

#### validate
Business rule assertion. Runs in validate stage.

```yaml
- id: val-rfc-format
  kind: validate
  stage: validate
  condition:
    field: "supplier.identifiers[scheme=MX:RFC].value"
    op: regex
    value: "^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$"
  message: "Supplier RFC '{{value}}' does not match SAT format"
  severity: error
  mandate_ref: "SAT CFDI 4.0 §3.1.1"
```

### 5.4 Pipeline stages

| Stage | Order | Rule kinds allowed | Owner |
|---|---|---|---|
| assemble | 1 | tax_regime, field_map, code_map, concat, jurisdiction, semantic_text, fn | Source adapter / assembler |
| enrich | 2 | field_map, code_map, fn, conditional | Target transformation pack |
| validate | 3 | validate, fn | Target transformation pack |
| render | 4 | field_map, code_map, fn | Target emitter |

Signing is not a core pipeline stage. If a mandate requires a signature before the final wire payload can be produced, the renderer returns a `HostActionRequirement` plus the canonical/signable content. The host platform performs signing and may call a completion/finalisation function with the signature result.

### 5.5 Built-in transforms

```
date_from_datetime        "2024-03-15T14:30:00" → "2024-03-15"
date_ddmmyyyy_to_iso      "15/11/2024" → "2024-11-15"
decimal_string            any numeric → normalised "1234.56" string (6dp max)
percent_from_decimal      0.160000 → "16.00" (×100)
uppercase                 string → UPPERCASE
trim                      strip leading/trailing whitespace
strip_prefix(n)           remove first n characters
default(val)              if source is null/absent, use val
halve                     divide rate by 2 (India CGST/SGST split)
```

### 5.6 Function registry contract

```typescript
interface TransformFunction {
  (
    source: unknown,                     // raw parsed source document
    doc: SemanticDocument,               // document in current state
    context: TransformContext            // mandate version, effective date, etc.
  ): Partial<SemanticDocument>           // deep-merged into working document
}
// Location: src/functions/{country}/{name}.ts
// Must be pure and stateless. External signing, delivery, and lifecycle state are not TransformFunction responsibilities.
```

---

## 6. Format adapters

### 6.1 FormatParser contract

```typescript
interface FormatParser<TRaw = unknown> {
  readonly family: FormatFamily;
  readonly supportedFormats: string[];
  validate(raw: TRaw): void;           // Structural validation only. Throw AdapterError on failure.
  parse(raw: TRaw): ParseResult;
}

interface ParseResult {
  raw: unknown;
  family: FormatFamily;
  scope: Omit<MandateScope, 'effectiveFrom' | 'effectiveTo'>;
  sourceVersion: string;
}
```

### 6.2 DocumentAssembler contract

```typescript
interface DocumentAssembler {
  readonly family: FormatFamily;
  assemble(result: ParseResult, scope: MandateScope): SemanticDocument;
}
```

### 6.3 Format families and parsers

| FormatFamily | Countries | Key parsing challenges |
|---|---|---|
| `ubl` | Belgium, Croatia, France, Germany, Denmark, Norway, Romania, Slovakia, Colombia, Peru | Namespace stripping; UBL vs CII detection; `CustomizationID` routing |
| `sdi` | Italy | p7m container pre-parse; multi-body FatturaPA; CodiceDestinatario routing |
| `sat` | Mexico | CFDI version negotiation (3.3/4.0); Serie+Folio ID derivation; TimbreFiscalDigital |
| `sefaz` | Brazil | nfeProc vs NFe root; 44-digit access key decomposition; multi-regime ICMS/CBS/IBS/IS |
| `gstn` | India | Flat JSON; DD/MM/YYYY conversion; GSTIN state code extraction; eWayBill decoupling |
| `lhdn` | Malaysia | Nested JSON; invoiceTypeCode routing; LHDN UUID injection post-clearance |
| `latam_dte` | Chile, Argentina, Ecuador, Guatemala, El Salvador, Panama, Uruguay, Dominican Rep., Costa Rica | `LATAMFormatBase` parsing/rendering base; per-country `LatamParserConfig` YAML |

### 6.4 LATAMFormatBase

The highest-ROI shared abstraction for LATAM is at the **document transformation** level, not at the authority-transport level. The countries in this family use proprietary XML or JSON documents with recurring concepts such as national identifiers, access keys, signature placeholders, authorization references, and printable-document metadata.

`LATAMFormatBase` provides reusable parsing, assembly, validation, and rendering hooks. Each country supplies a `LatamParserConfig`/render configuration declaring schema-specific paths and formulas. SOAP/REST transport, authority authentication, certificate custody, sequence allocation, and acknowledgement handling remain outside this module.

```yaml
# latam-country/cl-paths.yaml (Chile DTE)
document_id:    "DTE/Documento/Encabezado/IdDoc/Folio"
issue_date:     "DTE/Documento/Encabezado/IdDoc/FchEmis"
type_code:      "DTE/Documento/Encabezado/IdDoc/TipoDTE"
supplier_rut:   "DTE/Documento/Encabezado/Emisor/RUTEmisor"
supplier_name:  "DTE/Documento/Encabezado/Emisor/RznSoc"
access_key_formula: "{TipoDTE}-{Folio}-{RUTEmisor}"
identifier_scheme: "CL:RUT"
host_action: external_xades_signing
# Authority endpoint and credentials are configured by the host platform.
```

### 6.5 Key mapping decisions

#### Many-to-one (collapse)

| Mapping | Source fields → semantic | Transform |
|---|---|---|
| CFDI invoice number | `@Serie` + `@Folio` → `identity.id` | `fn: mx.deriveInvoiceNumber`. Outbound CFDI must split on "-" to recover. |
| FatturaPA street | `Indirizzo` + `NumeroCivico` → `streetLine1.default` | `concat(", n. ")`. Outbound FatturaPA splits on last `, n. `. |
| India supply type | `Stcd` + `BuyerDtls.Pos` + `SupTyp` → `_context.supplyType` | `fn: in.deriveSupplyType`. Routes IGST vs CGST/SGST. |
| FatturaPA references | `DatiOrdineAcquisto` + `DatiContratto` + `DatiFattureCollegate` → `references.*` | 3 field_map rules → one References object |

#### One-to-many (explode)

| Mapping | Source field → semantic fields | Transform |
|---|---|---|
| CFDI `@Rfc` | → `identifiers[0]` + `native.sat.supplierRFC` | Wrap in typed identifier + native copy |
| FatturaPA `Natura` | → `categoryCode` + `exemptionReasonCode` + `rate=null` + `native.sdi.natura` | Code map + conditional null + native copy |
| India `GstRt` | → 1× `GST_IN_IGST` OR 2× `GST_IN_CGST` + `GST_IN_SGST` | Conditional explode via jurisdiction rule |
| UBL `InvoicedQuantity` node | → `quantity` + `unitCode` | Split node text from `@_unitCode` attribute |

#### Value split

| Mapping | Source field components |
|---|---|
| NF-e 44-digit access key | `identity.id` (nNF portion) + `native.sefaz.accessKey` (full) + `supplier.address.state` (cUF) |
| CFDI `TasaOCuota` | `taxApplications[].rate` (×100 as %) + `native.sat.rawTasaOCuota` (original fraction for re-emit) |
| GSTIN 15-char | `identifiers[0].value` (full) + `native.gstn.supplierStateCode` (chars 0-1) + `_context.supplierState` (routing) |

#### Aggregate

| Mapping | Source → semantic |
|---|---|
| NF-e multi-regime | 3 tax groups × N `det/imposto` elements → 3 `TaxApplication` records (ICMS_BR, PIS_BR, COFINS_BR) |
| CFDI line taxes | N `Concepto/Traslado` elements → 1 document-level `TaxApplication` per (Impuesto, TipoFactor, TasaOCuota) group |

### 6.6 AdapterRegistry detection

```typescript
class AdapterRegistry {
  static detect(raw: Record<string, any>): FormatParser {
    // Detection order matters — more specific before less specific
    if ('rsm:CrossIndustryInvoice' in raw) return EN16931CIIParser;
    if ('FatturaElettronica' in raw) return FatturaPAParser;
    if (raw?.['Comprobante']?.['@_Version']) return CFDIParser;
    if ('TranDtls' in raw && raw.TranDtls?.TaxSch === 'GST') return GSTNParser;
    if ('invoiceTypeCode' in raw && /^\d{2}$/.test(raw.invoiceTypeCode)) return LHDNParser;
    // UBL: check CustomizationID before generic UBL fallback
    const custId = raw?.Invoice?.['cbc:CustomizationID'] ?? '';
    if (custId.includes('pint-ae') || custId.includes('urn:peppol:pint')) return PINTAEParser;
    if (custId.includes('zatca')) return ZATCAParser;
    if ('Invoice' in raw || 'CreditNote' in raw) return UBLParser;
    throw new AdapterError('Registry', 'No adapter matched');
  }
}
```

---

## 7. ERP integration layer

### 7.1 The ERP problem

ERP data models are designed to run a business, not to carry tax authority data. Key differences from CTC formats:

| Dimension | CTC mandate format | ERP output |
|---|---|---|
| Field names | Standardised by authority | ERP-vendor-specific (`E1EDK01-BELNR`, `entity.id`, `custbody_*`) |
| Schema stability | Authority-controlled, announced changes | Customer-controlled; custom fields added without notice |
| Tax representation | Explicit subtotals, categories, rates | GL account codes, tax codes, posting keys |
| Party data | Structured party objects | Internal entity IDs requiring master data lookup |
| Custom extensions | Fixed extension points | Unlimited custom fields |

### 7.2 Stage 1 components

#### Connector Registry

Resolves connector profile for incoming document by `(erpType, erpVersion, outputFormat, entityType)`.

**Connector profile fields:**
```yaml
erpType: SAP_IDOC                    # SAP_IDOC | ORACLE_FUSION | NETSUITE | DYNAMICS_365 | WORKDAY | CUSTOM
erpVersion: S4HANA_2023
outputFormat: IDOC_XML               # IDOC_XML | IDOC_FLAT | REST_JSON | BI_XML | CSV | ODATA_JSON
entityType: INVOICE                  # INVOICE | CREDIT_MEMO | DEBIT_NOTE
fieldMapFile: fieldmaps/sap-idoc-s4hana2023-invoice.yaml
valueMapsFile: valuemaps/sap-s4hana2023.yaml
customFieldsFile: customfields/acme-corp-sap.yaml   # optional
gapPolicy: warn                      # error | warn | skip
```

#### ERP-specific rule kinds

```yaml
# erp_path: extract value using format-specific path
- id: map-supplier-rfc
  kind: erp_path
  source: "E1EDK01/BELNR"            # XPath (IDoc/XML), JSONPath (REST), CSV column index
  target: "identity.id"

# erp_lookup: translate ERP code to canonical via lookup table
- id: map-tax-category
  kind: erp_lookup
  source: "E1EDK01/MWSKZ"
  lookupTable: tax_codes              # References named table in valueMapsFile
  target: "taxApplications[0].categoryCode"

# erp_custom: extract from custom field by alias
- id: map-po-reference
  kind: erp_custom
  customFieldAlias: po_reference      # Declared in customFieldsFile
  target: "references.orderRef"
  condition:
    targetCountry: BE               # Only emit when targeting Belgium

# erp_enrich: complex derivation via fn rule
- id: fn-reconstruct-tax
  kind: erp_enrich
  fn: "sap.aggregateTaxFromMwskz"
  outputs:
    - target: "taxApplications"
```

#### Value maps YAML format

```yaml
# valuemaps/sap-s4hana2023.yaml
tax_codes:
  A1: { categoryCode: "S", rate: "19.00" }   # DE standard VAT
  A2: { categoryCode: "S", rate: "7.00" }    # DE reduced VAT
  B1: { categoryCode: "E", rate: null }       # exempt
  V5: { categoryCode: "AE", rate: "0.00" }   # reverse charge

payment_terms:
  ZB01: { meansCode: "30", daysNet: 30 }
  Z000: { meansCode: "10" }

unit_of_measure:
  ST: "C62"    # SAP "piece" → UN/CEFACT each
  KG: "KGM"
```

#### Custom field registry

```yaml
# customfields/acme-corp-sap.yaml
custom_fields:
  - alias: po_reference
    erp_path: "ZACME_HDR/ZREF_PO"
    target: "references.orderRef"

  - alias: it_cig_code
    erp_path: "ZACME_HDR/ZCIG_CODE"
    target: "native.sdi.cig"
    condition:
      targetCountry: IT              # Only relevant for Italian invoices
```

### 7.3 Tax reconstruction

ERP tax data requires reconstruction:

```typescript
// fn: sap.aggregateTaxFromMwskz
// MWSKZ on each line → look up in value map → build TaxApplication
function aggregateTaxFromMwskz(source, doc, context) {
  const valueMap = context.loadValueMap('tax_codes');
  const apps: Record<string, TaxApplication> = {};

  for (const line of source.E1EDP01) {
    const mwskz = line.MWSKZ;
    const mapping = valueMap[mwskz];
    if (!mapping) continue;
    const key = `${mwskz}`;
    if (!apps[key]) {
      apps[key] = {
        regimeRef: resolveRegime(mapping, doc),
        categoryCode: mapping.categoryCode,
        rate: mapping.rate,
        taxableAmount: '0.000000',
        taxAmount: '0.000000',
      };
    }
    apps[key].taxableAmount = add(apps[key].taxableAmount, line.NETWR);
    // Tax amount from E1EDK04 totals segment, not line level
  }
  return { taxApplications: Object.values(apps) };
}
```

**NetSuite caveat**: REST API does not expose `taxDetails`. Tax must be retrieved via SuiteQL query or BI Publisher XML. Documented in NetSuite connector profile; handled by `erp_enrich` fn rule `netsuite.reconstructTaxFromSuiteTax`.

### 7.4 Party resolution strategies

| Strategy | When to use | Performance |
|---|---|---|
| `inline` | Party data embedded in ERP output (IDoc E1EDKA1 segments) | < 2ms — no I/O |
| `lookup_api` | Party data in ERP master data API | 200–800ms on cache miss; < 1ms on hit |
| `lookup_file` | Pre-exported YAML/CSV of customer/vendor master | < 2ms — file in memory |

Cache: Redis, 1-hour TTL by default. Pre-warm recommended at startup.

### 7.5 ERP system characteristics

| ERP | Format | Custom field mechanism | Tax data location |
|---|---|---|---|
| SAP S/4HANA | IDoc XML (INVOIC02) | Z-segments (`ZXXX`) | MWSKZ on E1EDP01; amounts in E1EDK04 |
| Oracle Fusion | REST JSON / BI Publisher XML | Descriptive Flexfields (DFF) | SuiteTax; taxLines array |
| NetSuite | REST JSON | `custbody_*`, `custcol_*` | `taxDetails` (not in REST; use SuiteQL) |
| Dynamics 365 | OData JSON | Custom entities via solutions | `TaxGroup`, `TaxItemGroup` |
| Workday | REST JSON / XML | Extended Business Objects (EBO) | Worktags |

---

## 8. Configuration system

### 8.1 Transformation pack structure

Configuration is packaged as immutable, versioned transformation packs. Packs contain transformation behaviour only; secrets, authority credentials, tenant settings, and operational workflow configuration are supplied by the host platform.

```text
/config
  /erp
    /connectors
    /fieldmaps
    /valuemaps
    /customfields

  /mandates
    /IT-FATTURAPA-1.3.2
      manifest.yaml
      rules-assemble.yaml
      rules-enrich.yaml
      rules-validate.yaml
      render-profile.yaml
    /MX-CFDI-4.0
    /BR-NFE-4.0
    /IN-GSTINV01-1.1
    /BE-PEPPOL-3.0

  /lookups
    uncl1001.yaml
    uncl4461.yaml
    iso-units.yaml
    mx-clave-unidad.yaml
    it-natura.yaml
    latam-country/

  /schemas
```

There is deliberately no `/certs`, delivery credential, API token, or tenant-secret directory in the transformation pack.

### 8.2 Manifest file

```yaml
packId: IT-FATTURAPA-1.3.2
scope:
  country: IT
  mandateId: FATTURAPA
  version: "1.3.2"
  effectiveFrom: "2024-01-01"
family: sdi
clearanceModel: clearance       # descriptive only
rules:
  assemble: rules-assemble.yaml
  enrich:   rules-enrich.yaml
  validate: rules-validate.yaml
render: render-profile.yaml
hostRequirements:
  - authority_submission
metadata:
  authorityName: "Agenzia delle Entrate / SDI"
  documentationUrl: "https://www.fatturapa.gov.it"
```

### 8.3 Pack identity and deterministic execution

Every loaded pack is assigned an immutable identity:

`packId + version + content hash`

A transformation resolves exactly one pack snapshot before execution. All stages in that invocation use that same snapshot. The resulting `TransformationResult` records `packId`, `packVersion`, and `packHash` so the wider platform can persist them with its regulatory transaction record.

A production host should promote packs through its normal configuration governance and CI/CD process. The core framework requires only that the provider expose immutable snapshots; it does not prescribe Git, Redis, mounted volumes, or a particular approval workflow.

### 8.4 Configuration provider contract

```typescript
interface TransformationPackProvider {
  resolve(scope: MandateScope, requestedVersion?: string): Promise<TransformationPackSnapshot>;
}

interface TransformationPackSnapshot {
  packId: string;
  version: string;
  hash: string;
  manifest: TransformationPackManifest;
  rules: CompiledRuleSet;
  renderProfile: RenderProfile;
}
```

Service mode may add hot reload or distributed cache invalidation around this contract. Library mode may use an in-process repository. In either case, in-flight transformations never switch pack versions mid-execution.

### 8.5 Adding a new country or mandate version

1. Create `/config/mandates/{COUNTRY}-{MANDATEID}-{VERSION}/`.
2. Add `manifest.yaml`, transformation rules, validation rules, lookup tables, and `render-profile.yaml`.
3. Reuse an existing `FormatFamily` where structurally compatible.
4. Add code only when a genuinely new parser/emitter family or transformation primitive is required.
5. Validate pack schema and regression fixtures in CI.
6. Publish an immutable pack version for the host platform to resolve.
7. Configure authority routing, credentials, security, and lifecycle behaviour separately in the wider CTC solution.

---

## 9. Country rollout plan

### Priority classification

| Class | Criteria | Countries |
|---|---|---|
| **Remediate now** | Live mandate, potentially non-compliant today | Italy, Romania, Malaysia, India, Mexico, Brazil, Colombia |
| **Urgent** | Mandate live Jan–Sep 2026 | Belgium, Croatia, France |
| **Build Q3 2026** | Mandate expanding or transitioning | Denmark, Ecuador (real-time Jan 2026), Dominican Rep. (May 2026) |
| **Build Q4 2026** | Slovakia, Norway mandatory Jan 2027 | Slovakia (DCTCE), Norway (EHF3) |
| **Build Q1–Q2 2027** | Germany mandatory Jan 2027 (large cos); LATAM wave 1 | Germany, Chile, Argentina, Peru, Uruguay |
| **Build Q3–Q4 2027** | LATAM wave 2 | Guatemala, El Salvador, Panama, Costa Rica |
| **Monitor** | Unstable mandate | Venezuela |

### Country-by-country specification

| Country | Format family | Clearance model | Schema version | Pack status | Key notes |
|---|---|---|---|---|---|
| Belgium | `ubl` | reporting (Peppol) | BIS 3.0 | Needed | CIUS-BE + Peppol AP registration |
| Croatia | `ubl` | reporting + real-time | EN 16931 | Needed | CIUS-HR transformation; FINA AP/real-time transport is host-platform responsibility |
| France | `ubl` | Y-model (PPF) | UBL or CII | Needed | Host platform requires PPF relay/routing adapter; transformer supports UBL/CII target representations |
| Germany | `ubl` | post-audit | XRechnung / ZUGFeRD | Needed | Receive obligation live; send Jan 2027 for large cos |
| Denmark | `ubl` | post-audit | OIOUBL / Peppol BIS | Needed | B2G live; B2B expanding |
| Italy | `sdi` | clearance | FatturaPA 1.3.2 | **Exists — update** | Audit p7m pre-parser, B2C scope, FY2024 schema updates |
| Norway | `ubl` | post-audit | EHF3 / Peppol BIS | Needed | EHF3 is BIS 3.0-compliant — minimal delta |
| Romania | `ubl` | clearance (ANAF) | e-Factura UBL | Needed | CIUS-RO transformation; ANAF submission adapter belongs to host platform |
| Slovakia | `ubl` | DCTCE | Peppol BIS / EN 16931 | Needed | Mandatory Jan 2027; from Jan 2027 buyers lose input VAT on non-compliant invoices |
| Malaysia | `lhdn` | clearance | MyInvois 1.1 | **Exists — update** | Phase 3 (all businesses) from Apr 2025 |
| India | `gstn` | clearance (IRP) | INV-01 v1.1 | **Exists — update** | 24h cancellation window state management |
| Mexico | `sat` | clearance (PAC) | CFDI 4.0 | **Exists — update** | 2025 SAT catalog updates; PAC list verification |
| Brazil | `sefaz` | clearance (SEFAZ) | NF-e 4.0 | **Exists — extend** | IBS/CBS multi-regime extension urgent from Aug 2026 |
| Argentina | `latam_dte` | clearance (ARCA) | ARCA web service | Needed (new family) | CUIT identifier; ARCA renamed from AFIP Apr 2025 |
| Chile | `latam_dte` | clearance (SII) | DTE XML | Needed (new family) | SII SOAP; CAF authorization flow; RUT identifier |
| Colombia | `ubl` | clearance (DIAN) | UBL-based (DIAN) | Needed | DIAN technical annex v1.9 |
| Costa Rica | `latam_dte` | clearance | XML v4.4 (Hacienda CR) | Needed (new family) | Mandatory buyer acceptance message |
| Dominican Rep. | `latam_dte` | clearance (DGII) | e-CF XML | Needed (new family) | NCF sequence management; final phase May 2026 |
| Ecuador | `latam_dte` | clearance (SRI) | XML + XAdES-BES | Needed (new family) | 49-digit access key; XAdES signing; real-time Jan 2026 |
| El Salvador | `latam_dte` | clearance (MH) | JSON DTE | Needed (new JSON family) | First genuinely JSON-native LATAM format |
| Guatemala | `latam_dte` | clearance (SAT-GT) | FEL XML | Needed (new family) | Live since 2022 |
| Panama | `latam_dte` | clearance (DGI/PAC) | XML (SFEP) | Needed (new family) | PAC-mediated like Mexico |
| Peru | `ubl` | clearance (SUNAT) | UBL-based (SUNAT) | Needed | SIRE/OSE routing and submission handled by host platform |
| Uruguay | `latam_dte` | clearance (DGI UY) | XML | Needed (new family) | Universal from 2025; CAE auth flow; RUT identifier |
| Venezuela | `latam_dte` | clearance (SENIAT) | XML / fiscal machines | **Monitor only** | SENIAT ruling unstable; do not build yet |

---

## 10. Country disruption analysis

### UAE (PINT-AE) — already designed, reference implementation

**Disruption level**: Low (UBL-based)

Transformation-model changes:
- `AEDTotals` on `MonetaryTotal` carries AED-converted taxable/tax/total values plus exchange rate/date when document currency is not AED.
- `"dctce"` remains descriptive `ClearanceModel` metadata for the host platform.

New transformation artefacts:
- `UAEPINTAEAdapter` (extends UBL/Peppol parsing and rendering capability)
- `AE:TRN` and `AE:TIN` identifier schemes
- UAE pack validation and enrichment rules for TRN/TIN and AED conversion
- `HostActionRequirement: SIGN_EXTERNALLY/SUBMIT_VIA_ASP` where required; ASP connectivity itself belongs to the host solution.

### Brazil NF-e — highest ongoing complexity

**Disruption level**: High (multi-regime reform)

IBS/CBS tax reform (Aug 2026 – 2032):
- 4–6 concurrent tax regimes per line during transition
- New `ibsCbsClassification` in `SEFAZFamilyNative`
- `CBS_BR`, `IBS_BR`, `IS_BR` regime registrations
- `cClassTrib`, deferral indicators, presumed credits per line
- No CIM structural change — `TaxRegime` + `TaxApplication` design absorbs this

NFS-e municipality problem:
- 5,500 municipalities with distinct sub-mandates
- Requires `ScopeRegistry` with `municipality` dimension
- `LATAMFormatBase` + per-city `LatamParserConfig` YAML

CNPJ alphanumeric transition (from 2026):
- New regex: `/^[A-Z0-9]{12}\d{2}$/` alongside legacy `/^\d{14}$/`
- NF-e 44-digit access key construction affected

### India INV-01 — most invasive format addition

**Disruption level**: High (no UBL ancestry, tripartite tax)

Unique challenges:
- INV-01 is flat JSON with Indian field names — no UBL delegation possible
- Tripartite CGST/SGST/IGST split driven by jurisdiction (state codes in GSTIN)
- 24-hour IRP cancellation window — exposed as host lifecycle metadata; state management belongs to the wider platform
- eWayBill coupling (`EwbDtls`) — transformer preserves/maps required data; separate EWB submission belongs to the host platform
- IRN is 64-char SHA-256 hash derived from `GSTIN + FY + docType + docNo`

### Saudi Arabia ZATCA — most demanding signing requirement

**Disruption level**: Medium (UBL-based, but device certificate lifecycle)

Unique requirements:
- ZATCA requires a device certificate (CSID); certificate onboarding/custody is supplied by the host platform
- Transformer must prepare canonical/signable content and support signature injection; signing execution is external
- PIH value is a required host-supplied input for rendering; chain state is managed outside the transformer
- ICV is a required host-supplied input; sequence allocation is managed outside the transformer
- Two invoice types with different flows: Standard (clearance B2B), Simplified (24h reporting B2C)
- PDF/A-3 with embedded XML for B2C; QR code is TLV-encoded (not a URL)
- Mandatory Arabic on all human-readable fields
- XAdES-B-LT signing by ZATCA device (not delegated to ASP like UAE)

---

## 11. Architecture decision log

### ADR-01: SemanticDocument as semantic pivot, not field container

**Status**: Accepted

**Context**: Initial design used a flat `CanonicalInvoiceModel` with one field per concept. This broke on Brazil (4 concurrent tax regimes), India (jurisdiction-dependent tax split), Malaysia (3 party identifiers), Saudi Arabia (mandatory Arabic).

**Decision**: `SemanticDocument` uses typed sub-models (`TaxRegime[]`, `TaxApplication[]`, `PartyIdentifier[]`, `SemanticText`) that absorb all observed cases without structural surgery.

**Rejected alternatives**:
- Single CIM field superset: cannot model concurrent tax regimes without ad-hoc fields
- Per-country CIM extension types: grows linearly, bleeds country concerns into core model

---

### ADR-02: Configuration-first, zero-rebuild mandate content

**Status**: Accepted

**Decision**: Mandate field mappings, code translations, validation rules, semantic enrichment, and rendering behaviour are expressed as versioned configuration wherever existing structural capabilities are sufficient. External signing, credential management, authority endpoints, and delivery lifecycle remain host-platform concerns.

**Rejected alternatives**:
- Code-based mandate packs: too slow for operational compliance cadence; every authority update requires engineering

---

### ADR-03: LATAMFormatBase shared transformation adapter for LATAM countries

**Status**: Accepted

**Context**: 9 LATAM countries need a new document family. Their transport and authority workflows differ, but their document parsing/rendering patterns share enough structure to reuse a transformation base.

**Decision**: `LATAMFormatBase` + per-country parser/render configuration. Authority transport and signing execution are explicitly excluded.

**Rejected**: A shared clearance/delivery base in this module, because that would pull authority workflow responsibilities into the transformer.

---

### ADR-04: FormatNativeBag typed by FormatFamily, not by country

**Status**: Accepted

**Decision**: UBL-family mandates (PINT-AE, ZATCA, EN 16931, PEPPOL) share `UBLFamilyNative`. New UBL countries extend the same namespace rather than adding a new country type.

**Rejected**: Per-country extension namespace — grows linearly; ZATCA and PINT-AE would duplicate UBL extension patterns.

---

### ADR-05: Transformation core has no mandatory external state store

**Status**: Accepted

**Decision**: The core transformation engine is deterministic and stateless. Pack loading/caching is abstracted behind `TransformationPackProvider`; persistence of lineage, idempotency, regulatory transaction history, and archives belongs to the host platform. A service wrapper may use Redis or another cache, but it is not required by library mode.

**Rejected**: Embedding platform persistence concerns directly into the transformation library.

---

### ADR-06: Explainability contract is first-class; visualisation API is optional wrapper

**Status**: Accepted

**Decision**: The core exposes stable explainability data structures for mappings, lineage, pack metadata, and validation. Service mode may expose these via `/v1/viz/*`; library mode returns them directly.

**Rejected**: Making an HTTP visualisation API a mandatory dependency of the transformation core.

---

### ADR-07: `"dctce"` added to ClearanceModel enum

**Status**: Accepted

**Decision**: UAE PINT-AE and Slovakia use ASP-mediated near-real-time reporting with no prior authority stamp. Semantically distinct from `"clearance"` and `"reporting"`. Approximating as `"reporting"` causes silent misbehaviour in delivery adapter routing.

**Rejected**: Approximate as `"reporting"` — delivery adapter cannot determine whether to call ASP or authority directly.

---

### ADR-08: Venezuela — monitor only, no build

**Status**: Accepted

**Decision**: SENIAT framework published March 2025 but regime instability means the technical spec could change. Engineering cost not justified until framework confirmed stable.

---

### ADR-09: Stage 1 (ERP) and Stage 2 (CTC) strictly separated

**Status**: Accepted

**Decision**: `SemanticDocument` is the only interface between Stage 1 and Stage 2. ERP admins configure Stage 1; mandate analysts configure Stage 2. Neither concern can bleed into the other.

**Rejected**: Single-stage adapter per (ERP type, target mandate) — N×M adapters; ERP admin must understand mandate schema.

---

### ADR-10: Custom fields in per-customer file, not merged into base connector profile

**Status**: Accepted

**Decision**: Two customers running same SAP version have different custom fields. Separate `customFieldsFile` maintains clean base profile while allowing unlimited customer-specific extension.

**Rejected**: Per-customer connector profile — duplicates entire base field map; maintenance burden when base SAP schema changes.

---

### ADR-11: `MandateScope` replaces `country + version` as resolution unit

**Status**: Accepted

**Decision**: Brazil has 5,500 sub-national NFS-e schemas. India's tax routing depends on sub-national state codes. `MandateScope` adds `region?` and `municipality?` dimensions.

**Rejected**: Country + version only — cannot route to São Paulo-specific pack vs national NFS-e pack.

---

### ADR-12: Tax reconstruction from ERP GL data uses `erp_enrich` fn rules

**Status**: Accepted

**Decision**: ERP tax codes (MWSKZ, TaxGroup, SuiteTax) require ERP-specific resolution logic that cannot be expressed declaratively. `erp_enrich` fn rules are engineer-owned; value map lookup tables (tax code → categoryCode + rate) are analyst-owned.

---

### ADR-13: Transformation framework is a bounded module inside the wider CTC platform

**Status**: Accepted

**Decision**: The framework owns source normalisation, semantic transformation, target validation, rendering, and lineage. The host platform owns security boundary, mandate applicability, tenant/legal-entity context, credential custody, signing execution, authority routing/submission, retries/reconciliation, regulatory lifecycle, and statutory archive.

**Rationale**: Keeping transport and lifecycle concerns outside the transformer allows the same engine to run as a library or service and prevents country-specific authority workflows from contaminating the common transformation model.

---

### ADR-14: Immutable transformation-pack snapshot per invocation

**Status**: Accepted

**Decision**: Every transformation pins one `TransformationPackSnapshot` identified by pack ID, version, and content hash. In-flight requests never resolve "latest" rules between stages.

**Rationale**: Deterministic execution and reproducibility are required even when the host platform hot-reloads or promotes new mandate content.

---

## 12. Known gaps and open questions

The following gaps are limited to the transformation framework boundary. Authority workflow, credential lifecycle, regulatory sequencing, security controls, and submission reconciliation remain host-platform concerns unless a transformation-specific interface is required.

### G1 — Semantic fidelity and native-data boundaries

**Gap**: `FormatNativeBag` currently mixes format-family and mandate-specific fields. UBL-based mandates such as ZATCA and PINT-AE already require different native extensions.

**Open question**: Should native preservation be split into `formatNative` and `mandateNative`, or replaced by a generic `SourceEnvelope` plus typed mandate extensions?

### G2 — Deterministic rule dependencies

**Gap**: Rule ordering currently relies mainly on numeric priority. That does not explicitly model read/write dependencies, conflicting writes, or cycles.

**Open question**: Add `reads`, `writes`, and `dependsOn` metadata and compile each stage into a validated DAG before execution?

### G3 — Configuration purity versus `fn` escape hatch

**Gap**: Complex transforms use engineer-owned `fn` rules. Without governance, country packs can gradually become code-driven again.

**Open question**: Should recurring `fn` patterns be promoted into new DSL primitives and should packs report a configuration-purity metric?

### G4 — Source-to-target losslessness

**Gap**: A semantic pivot guarantees semantic normalisation, not exact round-trip reproduction. Some formats require preservation of lexical values, extension fields, or source-native metadata.

**Open question**: Define explicit transformation modes such as `semantic` and `round_trip`, with stronger source-envelope preservation in the latter?

### G5 — ERP semantic capability gaps

**Gap**: The strict ERP/mandate separation means an ERP connector may produce a valid `SemanticDocument` that still lacks concepts required by a selected target mandate.

**Open question**: Add a `SemanticRequirementSet` per target pack and an API that reports which required concepts an ERP/source profile cannot populate before runtime?

### G6 — Tax-model stress testing

**Gap**: `TaxRegime` + `TaxApplication` supports concurrent regimes, but the claim that Brazil's transition requires no structural change is not yet proven against a broad fixture set covering deferrals, presumed credits, withholding, compounding, and jurisdictional dimensions.

**Open question**: What minimum representative tax fixture matrix must a pack pass before the semantic model is considered sufficient?

### G7 — Defaulting and missing-value semantics

**Gap**: Current defaults such as `unitCode = C62` and `city = ""` can turn missing source data into apparently valid semantic values.

**Open question**: Introduce provenance/status for mapped values (`source`, `derived`, `defaulted`, `enriched`) and distinguish absent, unknown, not-applicable, and empty?

### G8 — Version resolution responsibility

**Gap**: `MandateScope.effectiveFrom/effectiveTo` supports multiple versions, but the transformer should not independently decide legal applicability when the wider compliance platform already owns mandate scoping.

**Decision direction**: Prefer the host platform to supply an explicit target scope/pack version. Date-based resolution remains an optional convenience of the pack provider, not the legal source of truth.

### G9 — Signing boundary for formats whose signature changes the rendered payload

**Gap**: Some target formats require signing before the final document can be serialised completely.

**Open question**: Standardise a two-step contract: `prepareForSigning()` returns signable bytes/digest plus metadata; `finaliseWithSignature()` injects the host-provided signature into the final payload.

### G10 — Output contract for authority-specific metadata

**Gap**: Some downstream authority adapters require metadata derived during transformation but not embedded directly in the invoice payload.

**Open question**: Define a typed `transportHints`/`hostActions` object in `TransformationResult` without allowing authority transport behaviour to leak into the core engine.

---

## 13. PoC implementation guide

### 13.1 Recommended PoC scope

For a local deployable PoC that validates the core architecture, implement:

1. **SemanticDocument model** — TypeScript interfaces exactly as defined in §4
2. **Rule engine** — supports `field_map`, `code_map`, `concat`, `conditional`, `jurisdiction`, `semantic_text`, `fn`, `tax_regime`, `tax_application`, `validate` rule kinds
3. **Two inbound adapters**: UBL (covers Belgium, Croatia, Romania, Germany, Denmark, Norway, Slovakia, Colombia, Peru) + CFDI (covers Mexico)
4. **One outbound emitter**: UBL (bidirectional for the EU countries)
5. **Two mandate extension packs**: IT-FATTURAPA-1.3.2 (SDI clearance) + BE-PEPPOL-3.0 (Peppol reporting)
6. **Config hot-reload**: file-system watch + atomic rule set swap
7. **Invocation wrapper**: `POST /v1/transform` in service mode, plus equivalent direct library API; optional explainability endpoints
8. **Basic lineage**: populate `LineageRecord[]`, pack identity/hash, and return in `TransformationResult`

### 13.2 PoC project structure

```
ctc-transformer-poc/
  src/
    types/
      semantic-document.ts      # §4 interfaces — copy directly
      mandate-scope.ts
      rule-dsl.ts
    engine/
      rule-resolver.ts          # Load rule files by MandateScope
      rule-engine.ts            # Execute pipeline stages
      config-watcher.ts         # chokidar file watch + hot-reload
    adapters/
      ubl/
        ubl-parser.ts           # UBL 2.1 / PEPPOL BIS parser
        ubl-assembler.ts        # ParseResult → SemanticDocument
        ubl-emitter.ts          # SemanticDocument → UBL XML
      cfdi/
        cfdi-parser.ts
        cfdi-assembler.ts
    packs/
      IT-FATTURAPA-1.3.2/       # MandateExtensionPack implementation
        pack.ts
      BE-PEPPOL-3.0/
        pack.ts
    api/
      transform.ts              # POST /v1/transform
      viz.ts                    # GET /v1/viz/*
      health.ts
    functions/                  # fn rule implementations
      mx/
        derive-invoice-number.ts
        aggregate-tax-subtotals.ts
      in/
        derive-supply-type.ts
  config/
    mandates/
      IT-FATTURAPA-1.3.2/
        manifest.yaml
        rules-assemble.yaml
        rules-validate.yaml
        render-profile.yaml
      BE-PEPPOL-3.0/
        manifest.yaml
        rules-assemble.yaml
    lookups/
      uncl1001.yaml
      uncl4461.yaml
      it-natura.yaml
  tests/
    fixtures/                   # Sample documents (see §6 for samples)
      cfdi-sample.xml
      fattura-sample.xml
      ubl-sample.xml
    unit/
    integration/
```

### 13.3 Rule engine implementation sketch

```typescript
class RuleEngine {
  async execute(
    doc: SemanticDocument,
    ruleFiles: RuleFile[],
    stage: PipelineStage,
    context: TransformContext
  ): Promise<{ doc: SemanticDocument; lineage: LineageRecord[] }> {
    const lineage: LineageRecord[] = [];
    let current = structuredClone(doc);

    const rules = ruleFiles
      .flatMap(f => f.rules.filter(r => (r.stage ?? stage) === stage))
      .sort((a, b) => (a.priority ?? 100) - (b.priority ?? 100));

    for (const rule of rules) {
      if (rule.kind === 'field_map') {
        const result = this.applyFieldMap(rule, current, context);
        current = result.doc;
        lineage.push(result.record);
      } else if (rule.kind === 'code_map') {
        const result = this.applyCodeMap(rule, current, context);
        current = result.doc;
        lineage.push(result.record);
      } else if (rule.kind === 'fn') {
        const fn = this.fnRegistry.get(rule.fn);
        const partial = await fn(context.source, current, context);
        current = deepMerge(current, partial);
        lineage.push({ ruleId: rule.id, ruleKind: 'fn', targetConcept: rule.outputs?.[0]?.target ?? '' });
      } else if (rule.kind === 'validate') {
        const passed = this.evaluateCondition(rule.condition, current, context);
        if (!passed) {
          const error = interpolate(rule.message, current);
          if (rule.severity === 'error') throw new ValidationError(error, rule.id);
          // warning: add to lineage, continue
        }
      }
      // ... other rule kinds
    }

    current.control.lineage = [...(current.control.lineage ?? []), ...lineage];
    return { doc: current, lineage };
  }
}
```

### 13.4 Config hot-reload sketch

```typescript
class ConfigWatcher {
  private cache = new Map<string, RuleFile[]>();
  private lock = new AsyncLock();

  start(configDir: string) {
    chokidar.watch(configDir, { ignoreInitial: true })
      .on('change', (path) => this.reload(path))
      .on('add', (path) => this.reload(path));
  }

  private async reload(changedPath: string) {
    await this.lock.acquire('reload', async () => {
      const content = fs.readFileSync(changedPath, 'utf-8');
      const parsed = yaml.parse(content);
      const valid = this.schema.validate(parsed);
      if (!valid) { logger.error('Config validation failed', { path: changedPath }); return; }
      const scopeKey = this.pathToScopeKey(changedPath);
      this.cache.set(scopeKey, this.compileRules(parsed));
      logger.info('Config reloaded', { scope: scopeKey, ruleCount: parsed.rules.length });
    });
  }

  getRules(scope: MandateScope): RuleFile[] {
    return this.resolve(scope).map(key => this.cache.get(key) ?? []).flat();
  }
}
```

### 13.5 Sample test documents

Six representative test documents are defined in the conversation history. For the PoC, use:

1. **UBL**: German → Dutch B2B invoice, 19% VAT, PEPPOL BIS 3.0, `INV-2024-00142`
2. **FatturaPA**: Italian domestic, 22% IVA, SDI, `2024/0089`
3. **CFDI 4.0**: Mexican ERP software, 16% IVA, `A-00234`
4. **MyInvois**: Malaysian cloud services, 8% SST, `MY-INV-2024-11001`
5. **NF-e**: Brazilian industrial goods, ICMS 12% + PIS 0.65% + COFINS 3%, inter-state SP→RJ
6. **INV-01**: Indian automation equipment, 18% GST (IGST inter-state MH→DL)

### 13.6 Key PoC validation scenarios

These scenarios validate the core architectural claims:

| Scenario | What it proves |
|---|---|
| Parse CFDI → SemanticDocument → emit UBL | Semantic pivot works; CFDI TasaOCuota ×100 transform correct |
| Parse NF-e → SemanticDocument; verify 3 TaxApplications | Multi-regime tax model correctly aggregates ICMS+PIS+COFINS |
| Parse INV-01 inter-state → SemanticDocument; verify IGST (not CGST+SGST) | Jurisdiction rule correctly routes by GSTIN state code |
| Update `rules-validate.yaml` → verify new rule active without restart | Hot-reload works |
| Run same input twice with same pinned pack | Produces identical semantic output, rendered payload, and lineage |
| Parse UBL → SemanticDocument; inspect lineage | Every field traceable to source path and rule ID |

---

## 14. Critique prompts for AI models

Use these prompts when sharing this document with other AI models to get structured critique and expansion:

### For architecture critique

> Review the CTC Transformation Framework as a bounded module inside a wider compliance platform. Identify: (1) transformation decisions that will not scale to 25 countries; (2) the three riskiest assumptions in the semantic pivot or rule/config model; (3) places where host-platform concerns still leak into the transformation core; (4) edge cases where source-to-target fidelity is lost.

### For the semantic model

> Review the SemanticDocument entity model in §4. For each entity, identify: (1) fields that should be required but are marked optional; (2) fields that are missing and would be needed by at least two of the countries in §9; (3) whether the `TaxRegime` + `TaxApplication` design correctly handles the Brazil IBS/CBS transition period where legacy and new regimes coexist on the same invoice.

### For the rule DSL

> Review the Rule DSL v2 in §5. Evaluate: (1) whether the six rule kinds cover all transformation patterns in §6.5 without requiring `fn` rules; (2) identify any transformation that cannot be expressed in the DSL at all and would require a structural DSL extension; (3) is the `jurisdiction` rule kind expressive enough for India's GSTIN-based supply type derivation and Brazil's ICMS state routing simultaneously?

### For PoC implementation

> Using the entity model in §4, the rule DSL in §5, and the adapter guidance in §6, design a TypeScript implementation plan for the PoC described in §13. Identify: (1) the minimum viable set of abstractions to implement; (2) any TypeScript-specific concerns with the `SemanticDocument` type definition as written; (3) how to structure the tests to validate the multi-regime tax model without requiring a full end-to-end integration test.

### For country expansion

> I want to add [COUNTRY] to the CTC Transformation Framework. Using the disruption analysis pattern in §10, analyse: (1) which semantic entities need new fields; (2) which `FormatFamily` applies and whether a new parser/emitter family is needed; (3) what transformation-pack artefacts are required; (4) what signing, sequencing, or submission requirements must be surfaced as host inputs/actions rather than implemented in the transformer.

### For performance and resilience review

> Review the transformation engine for deterministic performance and isolation. Identify: (1) expensive parsing/mapping patterns; (2) how ERP enrichment I/O should be abstracted or avoided in the core path; (3) whether pack resolution can ever change during an invocation; (4) whether one malformed/expensive country pack can affect transformations for other formats.

---

*End of document. Version 1.1 — transformation-module boundary clarified. Generated from design session covering: semantic model design, format adapter analysis, rule DSL specification, ERP integration layer, 25-country rollout plan, country disruption analysis, entity model specification.*
