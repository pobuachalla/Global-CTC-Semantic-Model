# CTC-003 — Ownership and Relationship Review (Draft 0.6)

**Status:** Proposed; no new detailed-model decisions accepted. **Basis:** Unified D2 Entity Dictionary Draft 0.5 and approved D2, P1–P7, I-01–I-10, T01–T03 logical principles.

## Scope
Review document/party ownership (D01), fiscal interpretation provenance (D02), and compliance/representation/evidence correlation (D03). No database schema or physical FiscalContext aggregation decision.

## D01 — Document and party identity
- `BillingDocument.documentId` is the stable internal logical identity. `PublishedRevision` is authoritative for commercial number, type, issue date and currency at publication; any current-document projection is non-authoritative.
- Proposed invariant D01-1: A published revision pins immutable party snapshots for all participants and scopes. Reuse of a snapshot is allowed only by immutable reference and must not pull later party-master values.
- Proposed invariant D01-2: Post-issuance change to legal identifying facts is routed through a governed correction/replacement decision, not silent revision replacement.
- Open: legal issuance boundary, cross-revision party snapshot reuse, issuer+series+number uniqueness scope, document-type-specific party cardinality.

## D02 — Fiscal interpretation and source facts
- `SourceFiscalFact` preserves local source-supplied fiscal facts; source commercial fields remain authoritative in their shared billing entities with provenance, avoiding duplicated fact ownership.
- Proposed `InterpretationInputManifest`: revision ID and digest; source fact IDs; source representation IDs and digests; immutable profile/rule/mapping/code-list package digests; enrichment snapshot IDs; canonicalization version; relevant evaluation parameters.
- Proposed invariant D02-1: An interpretation is reproducible from a pinned revision, immutable package and complete input manifest, or explicitly reports NOT_EVALUABLE with the missing dependency.
- Proposed invariant D02-2: Derived facts never overwrite source facts. Conflicts retain both values and produce a validation finding.
- Open: manifest granularity, completeness verification, interpretation uniqueness/idempotency, whether an interpretation is materialized, and how missing external inputs are represented.

## D03 — Compliance, representation and evidence
- `DocumentRepresentation` has immutable artifact identity and hash. Source draft artifacts can exist without a published revision but require stable ingestion/document correlation.
- Proposed `SubmissionSnapshot` (logical candidate, not mandatory entity): revision ID/digest, interpretation ID/result digest when used, profile and mapping package references, outbound representation ID/hash, obligation/destination context.
- Proposed invariant D03-1: Every submitted attempt pins an immutable submission snapshot and never resolves mutable 'latest' references.
- Proposed invariant D03-2: Fiscal identity and evidence reference the exact artifact/operation they attest, without duplicating the authoritative identifier.
- Open: pre-publication source-to-revision correlation; attempt retries using the same versus newly generated representation; response-only artifact correlation; multiple identities per certified artifact; legal evidence revocation.

## Candidate logical relationship constraints
| From | To | Candidate cardinality | Condition |
|---|---|---|---|
| BillingDocument | PublishedRevision | 0..N | Publication may not yet have occurred |
| PublishedRevision | PartyParticipation | 0..N | Profile-dependent seller/buyer requirements |
| PartyParticipation | PartySnapshot | 1 | Immutable reference |
| PublishedRevision | SourceFiscalFact | 0..N | No duplicate authoritative commercial fact |
| PublishedRevision | FiscalInterpretation | 0..N | Physical aggregation deferred |
| FiscalInterpretation | InterpretationInputManifest | 1 | Proposed for reproducibility |
| PublishedRevision | DocumentRepresentation | 0..N | Source drafts may predate publication |
| PublishedRevision | ComplianceTransaction | 0..N | Each transaction pins exact revision |
| ComplianceTransaction | SubmissionAttempt | 0..N | Attempt pins snapshot once submitted |
| SubmissionAttempt | SubmissionSnapshot | 1 once submitted | Candidate logical reference |
| ComplianceTransaction | ProcessingEvent | 0..N | Append-only |
| FiscalIdentity | FiscalEvidence | 0..N | Evidence references authoritative typed identity |

## Test cases required before approval
1. Draft ingestion -> published invoice with party master changes between ingestion and publication.
2. Published invoice -> corrected legal document, preserving original party and commercial identifiers.
3. Same immutable revision -> two profile versions, one enrichment-dependent interpretation; verify replay and missing-input behavior.
4. Submit -> timeout -> reconcile -> retry; ensure pinned payloads and no duplicate legal inference.
5. Certification -> fiscal ID and certified artifact -> cancellation/revocation evidence, preserving history.

## Decision checkpoint
D01, D02, D03 and invariants D01-1/2, D02-1/2, D03-1/2 are **Proposed**. `InterpretationInputManifest` and `SubmissionSnapshot` are candidate logical concepts only. Approved D2, P1–P7, I-01–I-10 and T01–T03 remain unchanged. CTC-003 stays In Progress.

## Evidence limitations
Draft 0.5 is a design source, not an official regulatory specification. Real fixture coverage, physical aggregate design, publication semantics, and full CTC-013/014 operational models remain outstanding.
