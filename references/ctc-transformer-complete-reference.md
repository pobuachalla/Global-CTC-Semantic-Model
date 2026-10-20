# CTC Transformer Framework — Complete Design Reference

> **Purpose of this document**
> This file is the complete design record for the CTC Transformer Service — a production-grade, configuration-driven microservice that transforms invoice documents between the mandate formats required by 25 countries across Europe, LATAM, and APAC. It also handles ERP-native input (SAP, Oracle, NetSuite, Dynamics 365, Workday).
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

Businesses operating across multiple countries must submit invoices to tax authorities in country-specific digital formats. Each country has its own schema, validation rules, signing requirements, and submission protocol. These mandates change frequently and new countries are continuously added. The current state-of-the-art is either:

- **Point-to-point adapters**: one per source-target format pair. N×M adapters. Maintenance nightmare.
- **Hard-coded transformation engines**: monolithic, require rebuild for any mandate change. Cannot keep pace with regulatory change.

Neither approach scales to 25+ countries with diverse ERP entry points.

### Goals

1. **Zero-rebuild mandate updates**: any change to a mandate's field mappings, validation rules, signing parameters, or delivery endpoints must be expressible as a configuration file change — no code deployment required.
2. **Universal entry point**: accept documents from any CTC mandate format (UBL, FatturaPA, CFDI, NF-e, INV-01, MyInvois) or from any ERP system (SAP, Oracle, NetSuite, Dynamics, Workday, custom).
3. **25-country coverage**: all countries listed in §9, covering EU, LATAM, and APAC.
4. **Production-grade from day one**: performance targets, resilience patterns, and observability built in — not retrofitted.
5. **Visualisation-ready**: all internal data structures exposed via a read-only API for an operational mapping UI.

### Countries in scope

**Europe (9):** Belgium, Croatia, France, Germany, Denmark, Italy, Norway, Romania, Slovakia

**LATAM (14):** Mexico, Brazil, Argentina, Chile, Colombia, Costa Rica, Dominican Republic, Ecuador, El Salvador, Guatemala, Panama, Peru, Uruguay, Venezuela *(monitor only)*

**APAC / Other (2):** Malaysia, India

---

## 2. Design principles

### P1 — Configuration-first, zero-rebuild

Every aspect of a mandate that changes between versions — field mappings, code lookup tables, validation rules, signing parameters, delivery endpoints — must be expressible in a configuration file without modifying or redeploying the service binary. The service binary changes only when structural capabilities change (new rule kinds, new format parser base classes). Mandate content is always configuration.

### P2 — Semantic pivot

All transformation passes through the `SemanticDocument` model. No format-to-format direct conversion is permitted. This gives N+M adapters instead of N×M translators.

### P3 — Multi-regime tax by design

The tax model supports concurrent multi-regime taxation (Brazil: ICMS+CBS+IBS+IS per line; India: IGST or CGST+SGST depending on jurisdiction). The flat `taxSubtotals[]` array approach cannot model this. The `TaxRegime` + `TaxApplication` design handles all observed cases.

### P4 — Observable by default

Every transformation emits structured telemetry: parse duration, rule count, validation result, signing result, delivery result, and field-level lineage. Operators can trace any output value back to its source field and the rule that produced it.

### P5 — Resilient by design

Circuit breakers, configurable retry policies, dead-letter queuing, and idempotent delivery are first-class concerns. Authority endpoints are assumed unreliable.

### P6 — Visualisation-ready

All internal data structures are exposed via a read-only Visualisation API. The future operational UI consumes this API. No internal restructuring is needed to add the UI.

### P7 — ERP/CTC stage separation

Stage 1 (ERP connector) and Stage 2 (CTC transformer) are strictly separated with `SemanticDocument` as the only interface. ERP field mapping is a business configuration problem owned by ERP admins. Mandate rules are owned by mandate analysts. These concerns must never bleed into each other.

---

## 3. Architecture overview

### Two-stage pipeline

```
ERP systems ──┐
              ├─→ [Stage 1: ERP Connector] ──→ SemanticDocument ──→ [Stage 2: CTC Transformer] ──→ Authority
CTC formats ──┘                                     ▲
                                                    │
                                         (semantic pivot — all paths normalise here)
```

**Stage 1 (ERP Connector)** — NEW in v2.0
- Accepts raw ERP output (IDoc XML, REST JSON, OData, CSV)
- Applies configurable field map rules (`erp_path`, `erp_lookup`, `erp_custom`, `erp_enrich`)
- Reconstructs tax from GL/tax-code data
- Resolves party identifiers from entity IDs
- Produces a `SemanticDocument`

**Stage 2 (CTC Transformer)** — core, unchanged by ERP addition
- Accepts `SemanticDocument` (from Stage 1 or direct CTC format submission)
- Resolves active `MandateScope` and loads rule files
- Runs pipeline: enrich → validate → sign → emit
- Delivers to authority endpoint

### Six logical layers

| Layer | Name | Responsibility |
|---|---|---|
| L1 | Ingestion | Accept documents via HTTP, queue, or file drop. Route to correct parser. |
| L2 | Parse | Format-specific parsers produce `ParseResult`. One parser per `FormatFamily`. Stateless. |
| L3 | Assemble | `DocumentAssembler` converts `ParseResult` → `SemanticDocument`. One per `FormatFamily`. |
| L4 | Transform | Rule engine executes ordered pipeline against active `MandateScope`. |
| L5 | Deliver | Format-specific emitter serialises `SemanticDocument` → target format. Delivery adapter submits to authority. |
| L6 | Observe | Audit log, lineage store, metrics, health endpoints, Visualisation API. |

### Deployment topology (production)

- 2–4 stateless service replicas behind a load balancer
- Redis cluster: config cache, idempotency keys, party lookup cache
- Message broker (RabbitMQ or Kafka): async ingestion and dead-letter queuing
- PostgreSQL: lineage store, transformation history (10-year retention required)
- S3-compatible object store: raw document archive, emitted output archive
- Mounted config volume: rule files, lookup tables, extension packs (shared across all replicas)

### Technology choices (PoC recommendation)

```
Runtime:       Node.js 20+ (TypeScript)
HTTP:          Fastify or Hono
Queue:         BullMQ (Redis-backed) for PoC; Kafka for production
Cache:         ioredis
Database:      PostgreSQL via Drizzle ORM
Config watch:  chokidar (file-system events)
XML parsing:   fast-xml-parser
Validation:    Zod (runtime) + JSON Schema (config files)
Testing:       Vitest
```

---

## 4. Semantic document model

### 4.1 Overview

The `SemanticDocument` is the canonical pivot type. Every inbound document — regardless of source format or ERP origin — is normalised into a `SemanticDocument` before any transformation, validation, signing, or delivery step runs.

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
| `FormatFamily` | Enum | `ubl \| sdi \| sat \| sefaz \| gstn \| lhdn \| custom` | Identifies parser/assembler family |
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
  targetScope?: MandateScope;       // Set before Stage 2 begins. Absent during Stage 1 only.
  clearanceModel: ClearanceModel;
  signature?: SignatureData;        // Present after clearance
  qrCode?: string;                  // MX: SAT URL. SA B2C: TLV base64. MY: LHDN URL.
  invoiceCounter?: number;          // ZATCA ICV — mandatory SA Phase 2
  cancellationDeadline?: ISODateTime; // India IRP: 24h from issue
  transmissionProfile?: string;     // Peppol profile URN
  lineage?: LineageRecord[];
}
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
| assemble | 1 | tax_regime, field_map, code_map, concat, jurisdiction, semantic_text, fn | Assembler |
| enrich | 2 | field_map, code_map, fn, conditional | Extension pack |
| validate | 3 | validate, fn | Extension pack |
| sign | 4 | fn (signing only) | Signing plugin |
| emit | 5 | field_map, code_map, fn | Emitter |

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
// Must be pure and stateless. Signing functions are the sole exception.
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
| `latam_dte` | Chile, Argentina, Ecuador, Guatemala, El Salvador, Panama, Uruguay, Dominican Rep., Costa Rica | LATAMClearanceBase abstract class; per-country `LatamParserConfig` YAML |

### 6.4 LATAMClearanceBase

The highest-ROI architectural decision for LATAM. All 9 new-family LATAM countries share the same clearance pattern: proprietary XML or JSON, national web service, digital signature (XAdES or equivalent), authorization code returned in response, printable document generated post-authorization.

The `LATAMClearanceBase` abstract class implements the shared pattern. Each country provides a `LatamParserConfig` YAML declaring schema-specific paths and key formulas — no new TypeScript class per country.

```yaml
# latam-country/cl-paths.yaml (Chile DTE)
document_id:    "DTE/Documento/Encabezado/IdDoc/Folio"
issue_date:     "DTE/Documento/Encabezado/IdDoc/FchEmis"
type_code:      "DTE/Documento/Encabezado/IdDoc/TipoDTE"
supplier_rut:   "DTE/Documento/Encabezado/Emisor/RUTEmisor"
supplier_name:  "DTE/Documento/Encabezado/Emisor/RznSoc"
access_key_formula: "{TipoDTE}-{Folio}-{RUTEmisor}"
identifier_scheme: "CL:RUT"
authority_endpoint: "https://palena.sii.cl/cgi_dte/UPL/DTEUpload"
signing_type: xades-bes
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

### 8.1 Directory layout

```
/config
  /erp                            # ERP integration configuration (hot-reload)
    /connectors                   # One file per (erpType, version)
      sap-idoc-s4hana2023.yaml
      netsuite-2026.1.yaml
      oracle-fusion-24b.yaml
      dynamics-365-fo-2024.yaml
      custom-{customerId}.yaml
    /fieldmaps                    # ERP → SemanticDocument mapping rules
      sap-idoc-s4hana2023-invoice.yaml
      sap-idoc-s4hana2023-creditmemo.yaml
    /valuemaps                    # Tax, UOM, payment term code translations
      sap-s4hana2023.yaml
    /customfields                 # Per-customer custom field registries
      acme-corp-sap.yaml
    /partylookup                  # Party resolution strategies
      sap-idoc-partylookup.yaml

  /mandates                       # One directory per MandateScope (hot-reload)
    /IT-FATTURAPA-1.3.2
      manifest.yaml
      rules-assemble.yaml
      rules-enrich.yaml
      rules-validate.yaml
      signing-profile.yaml
      delivery-profile.yaml
    /MX-CFDI-4.0
    /BR-NFE-4.0
    /IN-GSTINV01-1.1
    /BE-PEPPOL-3.0
    /... (25 mandate directories total)

  /lookups                        # Shared canonical lookup tables (hot-reload)
    uncl1001.yaml                 # Invoice type codes
    uncl4461.yaml                 # Payment means codes
    iso-units.yaml                # UN/CEFACT unit codes
    mx-clave-unidad.yaml          # SAT unit codes (800+ entries)
    it-natura.yaml                # FatturaPA Natura → EN16931 category
    latam-country/                # Per-country LATAM path configurations

  /schemas                        # JSON Schema for config validation (no hot-reload)
  /certs                          # Signing certificates (no hot-reload)
```

### 8.2 Manifest file

```yaml
mandateId: IT-FATTURAPA-1.3.2
scope:
  country: IT
  mandateId: FATTURAPA
  version: "1.3.2"
  effectiveFrom: "2024-01-01"
family: sdi
clearanceModel: clearance
rules:
  assemble: rules-assemble.yaml
  enrich:   rules-enrich.yaml
  validate: rules-validate.yaml
signing:  signing-profile.yaml
delivery: delivery-profile.yaml
metadata:
  authorityName: "Agenzia delle Entrate / SDI"
  documentationUrl: "https://www.fatturapa.gov.it"
```

### 8.3 Hot-reload protocol

1. File-system watch (inotify on Linux) detects config file change
2. Distributed lock acquired (Redis `SETNX` with 30s TTL) — ensures only one replica initiates reload
3. Changed file validated against its JSON Schema
4. If valid: in-memory config tree updated atomically (read-write lock)
5. Other replicas receive cache-invalidation signal and re-fetch from config cache
6. In-flight requests complete against previous config; new requests use updated config
7. Reload event emitted to audit log with diff of changed rule counts

**Partial hot-reload caveat**: signing certificate files require rolling restart. Endpoint URLs, auth tokens, and rule files can hot-reload freely.

### 8.4 Adding a new country (no rebuild)

1. Create `/config/mandates/{COUNTRY}-{MANDATEID}-{VERSION}/`
2. Write `manifest.yaml`, rule files, `delivery-profile.yaml`, `signing-profile.yaml`
3. If country uses existing `FormatFamily` (UBL, LATAM-DTE): no code change
4. If new `FormatFamily`: add `LatamParserConfig` YAML (for LATAM countries)
5. Commit to config repository; CI/CD validates against JSON Schema and pushes to mounted volume
6. Service hot-reloads within 5 seconds
7. Optional: `POST /admin/config/reload` to force immediate reload

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
| Croatia | `ubl` | reporting + real-time | EN 16931 | Needed | CIUS-HR + FINA AP + real-time reporting adapter |
| France | `ubl` | Y-model (PPF) | UBL or CII | Needed + new delivery adapter | PPF relay is architecturally distinct from direct clearance |
| Germany | `ubl` | post-audit | XRechnung / ZUGFeRD | Needed | Receive obligation live; send Jan 2027 for large cos |
| Denmark | `ubl` | post-audit | OIOUBL / Peppol BIS | Needed | B2G live; B2B expanding |
| Italy | `sdi` | clearance | FatturaPA 1.3.2 | **Exists — update** | Audit p7m pre-parser, B2C scope, FY2024 schema updates |
| Norway | `ubl` | post-audit | EHF3 / Peppol BIS | Needed | EHF3 is BIS 3.0-compliant — minimal delta |
| Romania | `ubl` | clearance (ANAF) | e-Factura UBL | Needed | CIUS-RO + ANAF portal submission adapter |
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
| Peru | `ubl` | clearance (SUNAT) | UBL-based (SUNAT) | Needed | SIRE reporting adapter; OSE intermediary |
| Uruguay | `latam_dte` | clearance (DGI UY) | XML | Needed (new family) | Universal from 2025; CAE auth flow; RUT identifier |
| Venezuela | `latam_dte` | clearance (SENIAT) | XML / fiscal machines | **Monitor only** | SENIAT ruling unstable; do not build yet |

---

## 10. Country disruption analysis

### UAE (PINT-AE) — already designed, reference implementation

**Disruption level**: Low (UBL-based)

CIM changes:
- `lines[].vatAmountAED?: Decimal` + `lines[].netAmountAED?: Decimal` (mandatory, populated by UAE enrich())
- `meta.exchangeRate?: Decimal` + `meta.exchangeRateDate?: ISODate`
- `AEDTotals` entity on `MonetaryTotal`
- `"dctce"` added to `ClearanceModel` enum

New artefacts:
- `UAEPINTAEAdapter` (extends `UBLPEPPOLAdapter`)
- `AE:TRN` and `AE:TIN` identifier schemes
- UAE extension pack: `validate()` (TRN regex `/^1\d{14}$/`, TIN derivation) + `enrich()` (AED conversion)
- `ASPConnector` interface (new delivery architecture — ASP signs, not the framework)

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
- `LATAMClearanceBase` + per-city `LatamParserConfig` YAML

CNPJ alphanumeric transition (from 2026):
- New regex: `/^[A-Z0-9]{12}\d{2}$/` alongside legacy `/^\d{14}$/`
- NF-e 44-digit access key construction affected

### India INV-01 — most invasive format addition

**Disruption level**: High (no UBL ancestry, tripartite tax)

Unique challenges:
- INV-01 is flat JSON with Indian field names — no UBL delegation possible
- Tripartite CGST/SGST/IGST split driven by jurisdiction (state codes in GSTIN)
- 24-hour IRP cancellation window — state management concern
- eWayBill coupling (`EwbDtls`) — separate regulatory document, carried in native bag
- IRN is 64-char SHA-256 hash derived from `GSTIN + FY + docType + docNo`

### Saudi Arabia ZATCA — most demanding signing requirement

**Disruption level**: Medium (UBL-based, but device certificate lifecycle)

Unique requirements:
- ZATCA issues device certificate (CSID) per taxpayer device via onboarding API
- Invoices must be signed with CSID before submission — device credential management
- PIH chain: each invoice must hash its predecessor (`native.ubl.zatca.pih`)
- `invoiceCounter` (ICV) must be sequential — chain state management
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

**Decision**: Every mandate field mapping, code translation, validation rule, signing parameter, and delivery endpoint is expressed as a YAML configuration file. The service binary only changes when structural capabilities change.

**Rejected alternatives**:
- Code-based mandate packs: too slow for operational compliance cadence; every authority update requires engineering

---

### ADR-03: LATAMClearanceBase shared adapter for LATAM countries

**Status**: Accepted

**Context**: 9 LATAM countries need new `FormatFamily` registrations. All share the same clearance pattern: proprietary XML/JSON + national web service + XAdES/local signing + authorization code + printable document.

**Decision**: `LATAMClearanceBase` abstract class + per-country `LatamParserConfig` YAML. Reduces each new country from 10–14 weeks to 3–5 weeks.

**Rejected**: Separate adapter per country — prohibitive build time; maintenance compounds.

---

### ADR-04: FormatNativeBag typed by FormatFamily, not by country

**Status**: Accepted

**Decision**: UBL-family mandates (PINT-AE, ZATCA, EN 16931, PEPPOL) share `UBLFamilyNative`. New UBL countries extend the same namespace rather than adding a new country type.

**Rejected**: Per-country extension namespace — grows linearly; ZATCA and PINT-AE would duplicate UBL extension patterns.

---

### ADR-05: Redis for config/idempotency cache; PostgreSQL for lineage

**Status**: Accepted

**Decision**: Hot-reload and idempotency require sub-millisecond distributed state (Redis). Lineage requires durability, querying, and 10-year retention (PostgreSQL). Different requirements → different stores.

**Rejected**: PostgreSQL for everything — too slow for hot-reload cache. In-memory only — not shared across replicas.

---

### ADR-06: Visualisation API as first-class read-only surface

**Status**: Accepted

**Decision**: All internal data structures exposed via `/v1/viz/*` endpoints. The future operational UI consumes this API. No internal restructuring needed to add the UI.

**Rejected**: UI reads internal structures directly — couples UI to internal code; no stability guarantee.

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

## 12. Known gaps and open questions

### G1 — Brazil NFS-e municipality pack management

**Gap**: 5,500 municipalities with distinct sub-mandates. `ScopeRegistry` with `municipality` dimension handles routing correctly, but generating and maintaining 1,280+ packs (each with its own XSD version, webservice endpoint, and validation rules) requires a semi-automated pipeline.

**Open question**: Should there be a pack generator that takes a municipality's XSD and produces a `LatamParserConfig` YAML? Or a dynamic resolver that fetches the municipality schema at runtime?

### G2 — France PPF Y-model delivery architecture

**Gap**: France's PPF (Portail Public de Facturation) Y-model is fundamentally different from direct clearance. Invoices route via PPF as relay and data concentrator. This requires a new delivery adapter class — not just a new delivery profile.

**Open question**: Is PPF an authority-as-intermediary pattern that could be abstracted as a `RelayDeliveryAdapter` base class (useful for future mandates that adopt similar Y-models)? Or is it France-specific enough that a dedicated `PPFAdapter` is cleaner?

### G3 — ZATCA device certificate lifecycle

**Gap**: ZATCA Phase 2 requires each taxpayer device to be registered and receive a CSID. The framework needs a device registration and certificate renewal flow. CSIDs expire and must be renewed before expiry.

**Open question**: Is certificate lifecycle management in scope for this service, or is it a separate operational concern delegated to the taxpayer's IT team with the framework only consuming the certificate?

### G4 — PIH chain state management for ZATCA

**Gap**: The `previousDocumentHash` (PIH) field creates a cryptographic chain. The service must persist the hash of each cleared ZATCA invoice to populate the next invoice's PIH. This is a stateful concern in an otherwise stateless service.

**Open question**: Where does PIH state live? PostgreSQL (document history table)? Redis (last-PIH-per-device key)? What happens if the service restarts between two invoices?

### G5 — India eWayBill coupling

**Gap**: For goods movement above ₹50,000 inter-state, the IRP generates an eWayBill alongside the IRN. The framework carries `ewayBill` data in `GSTNFamilyNative` but the eWayBill must be submitted separately to the EWB portal.

**Open question**: Should the framework include an eWayBill delivery adapter, or is this explicitly out of scope? If out of scope, what is the handoff mechanism?

### G6 — Signing for LATAM XAdES-BES countries

**Gap**: Ecuador, Guatemala, El Salvador, Panama, Uruguay all require XAdES-BES signing with customer-held P12 keystores. The signing plugin interface is defined but not implemented for XAdES-BES.

**Open question**: Is there a shared XAdES-BES implementation that all LATAM countries can use with different certificate configurations? Or do individual countries have enough signing variation to require separate plugins?

### G7 — Venezuela mandate stability

**Gap**: SENIAT ruling published March 2025 but political and economic instability means the technical framework may change. Currently monitor-only.

**Open question**: What is the trigger condition that moves Venezuela from "monitor" to "build"? Sustained technical specification for 6+ months? A specific SENIAT API going live?

### G8 — Performance under party lookup cache miss

**Gap**: Party lookup cache misses (ERP entity ID → master data API call) can take 200–800ms, threatening the 500ms p99 SLA for synchronous transforms.

**Open question**: Should cache-miss requests automatically route to async? Or should there be a configurable timeout after which the sync request returns a 202 Accepted and completes async?

### G9 — Schema version transitions mid-year

**Gap**: Mandate schemas change during the year (e.g. Brazil NF-e NT updates, SAT catalog changes). The `effectiveFrom` / `effectiveTo` date range on `MandateScope` handles this, but documents submitted on the day of a transition need to know which version applies.

**Open question**: For a document with `issueDate = 2026-08-01` and a mandate where v1 has `effectiveTo = 2026-07-31` and v2 has `effectiveFrom = 2026-08-01`, the rule resolver must pick v2. Is `issueDate` always the correct date to use for version resolution, or should there be a `submissionDate` field that takes precedence?

---

## 13. PoC implementation guide

### 13.1 Recommended PoC scope

For a local deployable PoC that validates the core architecture, implement:

1. **SemanticDocument model** — TypeScript interfaces exactly as defined in §4
2. **Rule engine** — supports `field_map`, `code_map`, `conditional`, `fn`, `tax_regime`, `tax_application`, `validate` rule kinds
3. **Two inbound adapters**: UBL (covers Belgium, Croatia, Romania, Germany, Denmark, Norway, Slovakia, Colombia, Peru) + CFDI (covers Mexico)
4. **One outbound emitter**: UBL (bidirectional for the EU countries)
5. **Two mandate extension packs**: IT-FATTURAPA-1.3.2 (SDI clearance) + BE-PEPPOL-3.0 (Peppol reporting)
6. **Config hot-reload**: file-system watch + atomic rule set swap
7. **REST API**: `POST /v1/transform` (sync) + `GET /v1/viz/scopes` + `GET /v1/viz/scopes/{id}/mapping`
8. **Basic lineage**: populate `LineageRecord[]` and return in API response

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
        delivery-profile.yaml
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
        const partial = await fn(current, context);
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
| Submit same document twice with same idempotency key | Returns cached result; no duplicate authority submission |
| Parse UBL → SemanticDocument; inspect lineage | Every field traceable to source path and rule ID |

---

## 14. Critique prompts for AI models

Use these prompts when sharing this document with other AI models to get structured critique and expansion:

### For architecture critique

> Review the CTC Transformer architecture in this document. Identify: (1) any design decisions that will not scale to 25 countries in production; (2) the three riskiest assumptions; (3) any missing concerns in the resilience model; (4) whether the two-stage ERP/CTC separation introduces any edge cases where data fidelity is lost.

### For the semantic model

> Review the SemanticDocument entity model in §4. For each entity, identify: (1) fields that should be required but are marked optional; (2) fields that are missing and would be needed by at least two of the countries in §9; (3) whether the `TaxRegime` + `TaxApplication` design correctly handles the Brazil IBS/CBS transition period where legacy and new regimes coexist on the same invoice.

### For the rule DSL

> Review the Rule DSL v2 in §5. Evaluate: (1) whether the six rule kinds cover all transformation patterns in §6.5 without requiring `fn` rules; (2) identify any transformation that cannot be expressed in the DSL at all and would require a structural DSL extension; (3) is the `jurisdiction` rule kind expressive enough for India's GSTIN-based supply type derivation and Brazil's ICMS state routing simultaneously?

### For PoC implementation

> Using the entity model in §4, the rule DSL in §5, and the adapter guidance in §6, design a TypeScript implementation plan for the PoC described in §13. Identify: (1) the minimum viable set of abstractions to implement; (2) any TypeScript-specific concerns with the `SemanticDocument` type definition as written; (3) how to structure the tests to validate the multi-regime tax model without requiring a full end-to-end integration test.

### For country expansion

> I want to add [COUNTRY] to the CTC Transformer. Using the disruption analysis pattern in §10, analyse: (1) which entities in the SemanticDocument model need new fields; (2) which `FormatFamily` applies and whether a new one is needed; (3) what configuration artefacts are needed and in what order; (4) what the authority signing and delivery model is and how it maps to the existing delivery adapter types.

### For performance and resilience review

> Review the performance and resilience design implied by the architecture in §3. Identify: (1) any single points of failure; (2) whether the party lookup cache miss scenario in G8 is correctly handled; (3) the correct approach for ZATCA PIH chain state management described in G4; (4) how the system should behave when the authority endpoint for one country is down while all other countries continue to function.

---

*End of document. Version 1.0. Generated from design session covering: semantic model design, format adapter analysis, rule DSL specification, ERP integration layer, 25-country rollout plan, country disruption analysis, entity model specification.*
