# CTC-003 G4 — Domain Adjudication Draft 2.5

**Status:** Proposed; no additional approvals. **Date:** 2026-10-20.

## Source baseline and limitations

- Historical `SemanticDocument` v1.0 and `BillingDocument` v0.3, represented by the Draft 2.3 extraction inventory.
- Draft 2.4 adjudicated 35 v1.0 identity/tax/monetary rows; this pass reviews additional v1.0 party/control/provenance and v0.3 hierarchy/fiscal/correction candidates.
- Target is the D2 candidate dictionary Draft 2.1–2.2 lineage; precise destination attribute names are **provisional** pending reconciliation with integrated Draft 1.9 and newer field corrections.
- GitHub repository state not independently verified. No regulatory fixture validation performed.

## Coverage

- Additional proposed mapping rows: **83** ({'SemanticDocument v1.0': 38, 'BillingDocument v0.3': 45}).
- Candidate dispositions: {'review': 25, 'renamed': 9, 'retained': 16, 'split': 33}.
- Remaining inventory rows: **195**.
- Previously adjudicated Draft 2.4: **35**. Combined reviewed candidate rows: **118** of original 313, **not** a normative attribute coverage percentage.

## Architectural findings

1. **Party identifiers** are not fiscal certification identities. A generic `scheme` or `value` field cannot be mapped by name alone; preserve its owning entity and issuer namespace.
2. **PartySnapshot and PartyParticipation** represent different semantics: published party facts versus participation role and scope.
3. **FiscalContext** source members need semantic decomposition into source fiscal facts, profile-derived facts and post-submission fiscal identities/evidence. This is a proposed split, not proof of a lossless transformation.
4. **DocumentControl** mixes representation/profile/process/provenance concerns. Map each declared field individually; do not copy the entire object as authoritative billing data.
5. **FormatNativeBag** must not serve as an unvalidated escape hatch. Preserve original artifact and register each unmapped legally significant field with a typed governed extension or explicit loss finding.
6. **v0.3 extracted tokens** include prose and hierarchy labels; they must be verified against their defining sections before counting as source fields.

## High-priority manual checks

- Verify v0.3 `FiscalContext.fiscalIdentifiers` and `partyContexts` member semantics; distinguish pre-existing identifiers from authority-assigned ones.
- Verify `TaxPoint` scope and local tax-point classifications at line/document level.
- Verify `PartyIdentifier.scheme` and `PartyIdentifier.value` against D2 `PartyIdentifier`, never generic `FiscalIdentity`.
- Verify `DocumentControl` signature/QR/clearance fields against original artifact and evidence owners.
- Complete remaining historical fields, particularly line tax, multilingual text, adjustments, conversion and source assertions.
- Execute sample-level round-trip/loss checks before claiming any row lossless.

## Checkpoint

**CTC-003:** Review, not Done. **G4:** In Progress. **Approved decisions:** D2, P1–P7, I-01–I-10, T01–T03, D01–D03, L01–L10, B01–B10, qualified C09 and G2 directions unchanged. No new ADRs accepted.

**Next:** Validate proposed destination paths against the definitive candidate dictionary and adjudicate the remaining 195 extraction entries. Prioritize original field declarations and reverse-map/loss checks; preserve ambiguity explicitly.
