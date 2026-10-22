# CTC-012 | Persistence Snapshots and Lineage | Logical Contract v1.0

**Status:** ACCEPTED at logical-policy scope by explicit user approval on 2026-10-21. **Date:** 2026-10-21. **Task:** CTC-012. **Scope:** implementation-neutral snapshot, artifact, lineage and retention decision boundaries. **Source baseline:** 2026-10-21 CTC-011 approved Git package (local); live GitHub HEAD not verified.

## 1. Purpose and governing baseline

This contract defines the logical preservation and traceability requirements for inbound source material, immutable published billing revisions, fiscal interpretations, generated outbound representations, submission attempts, external responses and compliance histories. It derives from the approved D2/P1–P7, D01–D03, L01–L10, B01–B10, qualified C09, JP-01–JP-10, V-01–V-10, CL-01–CL-08, AR-01–AR-10 and CTC-011 scoped logical relationships. It does not alter the approved 51-concept dictionary, create canonical fields, or select physical FiscalContext A/B/C.

## 2. Normative logical behavior proposed for CTC-012

| Rule | Candidate requirement | Boundary |
|---|---|---|
| PS-01 | Preserve original inbound bytes or a governed immutable external artifact reference, with digest, media type, capture time and source correlation. | No universal object-store or database choice. |
| PS-02 | A published revision is immutable; its identity, exact semantic content digest and frozen party/commercial assertions cannot be silently replaced. | Working drafts may evolve before publication. |
| PS-03 | Each generated representation pins exact published revision, interpretation (when used), mapping/profile dependency versions and content digest. | Not every representation requires fiscal interpretation. |
| PS-04 | A fiscal interpretation pins an immutable resolvable input manifest containing revision, source facts, enrichment inputs, rules, mappings and code lists used. | No mutable latest dependency. |
| PS-05 | Provenance differentiates source assertion, copied value, derived fact, enrichment and jurisdictional classification; records the exact source/target references and transformation identity where applicable. | A source artifact alone does not prove field-level semantic coverage. |
| PS-06 | Every submitted attempt pins one immutable submission snapshot and exact transmitted representation or envelope member/payload. Retrying does not rewrite the prior attempt. | Batch transport and document submission remain separate. |
| PS-07 | Responses, processing events and legal-state assessments preserve their own immutable evidence and correlation history; projections are reproducible and not the authoritative record. | No inference of legal clearance from transport success. |
| PS-08 | Digests identify byte-level integrity only when the canonicalization/encoding and digest algorithm are explicit; semantic equivalence must not be inferred from equal or different byte hashes alone. | No universal hash or canonicalization algorithm mandated. |
| PS-09 | Retention, archival, redaction and deletion are governed by applicable jurisdiction, document family, evidence type, legal hold and tenant policy. Policy evaluation must be explicit and versioned. | No universal period or automatic deletion is approved. |
| PS-10 | Historical replay identifies the original input set and package versions and distinguishes deterministic recomputation from reproducing a recorded external authority outcome. Missing inputs yield NOT_REPLAYABLE with reasons. | External responses are observed, not recomputed. |
| PS-11 | Logical references are tenant-scoped where relevant and must not resolve across tenant boundaries; unresolved external references remain typed unresolved values. | Physical FK implementation deferred. |
| PS-12 | Audit chains preserve identity, ordering/correlation and supersession without rewriting prior artifacts; corrections and cancellation evidence remain linked to original revisions. | No global monotonic timestamp assumption. |

All PS-01..PS-12 are **ACCEPTED at logical-policy level** by explicit user approval. They constrain persistence behavior, not a physical schema.

## 3. Logical preservation catalogue

| Record / artifact | Identity and integrity | Pinned context | Mutation policy |
|---|---|---|---|
| IngestionRecord + original DocumentRepresentation | ingestion identity, artifact digest, source locator | source format/version if known | Append-only original; capture correction as new artifact |
| BillingDocument / PublishedRevision | stable document ID; immutable revision ID + semantic digest | published party snapshots, document relationships | Never edit published revision |
| SourceFiscalFact / SourceAssertion | source fact identity and source locator | original representation/revision | Preserve raw assertion; no overwrite by derivation |
| FiscalInterpretation / input manifest | interpretation identity, manifest digest | revision, profile, mapping/rules/code-list digests, enrichment | New interpretation for changed inputs |
| DerivedFiscalFact / FactProvenance | derivation identity and rule reference | interpretation and exact source facts | New derived record for changed interpretation |
| Generated DocumentRepresentation | representation identity + byte digest | revision, interpretation and mapping versions | New representation when bytes change |
| SubmissionSnapshot / SubmissionAttempt | immutable snapshot identity, attempt identity | exact transmitted artifact, destination and manifest | Retries create new attempts |
| SubmissionEnvelope / EnvelopeMember / TransportAttempt | envelope payload digest, member identity, transport attempt | exact member manifest and payload | Freeze submitted manifest; record retries separately |
| Response observation / ProcessingEvent / FiscalEvidence | response digest, correlation subject, event identity | exact operation and external artifact | Append-only observation; no rewriting conflict |
| Status projection / LegalStateAssessment | projection rule/version and input event set | event/evidence references | Rebuildable projection, assessment history preserved |

The catalogue describes logical records and artifacts; it does **not** require one database table per row.

## 4. Snapshot boundaries and lifecycle

1. **Receive:** record source bytes, metadata, digest and extraction membership. Multiple extracted documents may reference one inbound batch.
2. **Normalize:** preserve source facts and provenance; working documents may be revised.
3. **Publish:** freeze semantic revision, commercial identity assertions, party snapshots and digest. Legal issuance remains a separate determination.
4. **Interpret:** create a new version-pinned interpretation manifest. Do not mutate source facts or a prior interpretation.
5. **Generate:** persist the exact output representation and mapping dependency set.
6. **Submit:** freeze the submitted artifact, member manifest and submission snapshot before or atomically with dispatch; attempts are individually identifiable.
7. **Observe:** append transport/authority responses, correlation decisions and evidence without overwriting conflicting observations.
8. **Assess/project:** compute current status from pinned event inputs and rules; preserve the evidence behind legal-state assessments.
9. **Correct/cancel:** link new documents or operations to prior immutable identities; never rewrite clearance history.

## 5. Referential and consistency constraints

- Every published revision resolves to exactly one platform document; references to revisions include the correct tenant and immutable revision identity.
- Every interpretation manifest resolves all required pinned inputs or is explicitly `NOT_REPLAYABLE` / `NOT_EVALUABLE` for the attempted operation. A hash without retrievable or lawfully archived dependencies is not sufficient to claim replay.
- A submitted envelope member resolves to the exact submitted document revision and representation; mismatches fail integrity validation.
- A response may remain `AMBIGUOUS` or `UNRESOLVED` when external identifiers are insufficient. No guessed correlation is allowed.
- Duplicate receptions and duplicate callback deliveries may be linked without erasing distinct observed occurrences.
- Byte digests and semantic digests are different notions; each must declare algorithm and canonicalization/encoding context.

## 6. Retention decision boundary

Retention requirements are **profile/policy decisions**, not global constants. A policy decision should identify jurisdiction and obligation, artifact class, effective policy version, trigger event, retention duration when verified, permitted disposal action, legal holds and audit evidence. If legal retention is unknown or a hold exists, the design must not assume disposal is permitted. Personal-data minimization and regulatory evidence obligations require a separately approved policy. Encryption, storage tiers, key rotation, cryptographic signature verification and backup strategy are physical/security workstreams, not approved here.

## 7. Replay guarantees and limitations

**Reproducible semantic interpretation:** possible when original revision, all source/enrichment facts and immutable versioned profile dependencies are available, the execution semantics are pinned, and the relevant computation is deterministic. **Historical observed outcome:** reproduce from preserved response/event evidence; never regenerate authority decisions. **Missing dependency:** return `NOT_REPLAYABLE` with missing references. **Changed mapping:** a new interpretation is created; earlier interpretation remains unchanged.

## 8. Deferrals and follow-ups

- `CTC-002-FU01`: physical FiscalContext A/B/C remains Deferred; no implied embedded/hybrid selection.
- `CTC-002-FU03` / `CTC-012`: long-term archival availability and package preservation implementation remain open.
- `CTC-008/009/010`: real format fixtures, field-level semantic-loss and jurisdictional validation remain open.
- `CTC-016`: API retrieval, status notifications and error payload contracts remain open.
- 18 proposed CTC-003 field additions remain Proposed, including any overlap with logical preservation metadata here.
- No universal legal retention periods, deletion triggers or crypto standards are asserted.

## 9. Acceptance evidence and scoped closure recommendation

The accompanying test suite checks 12 synthetic logical scenarios (positive and negative controls). This is evidence of logical consistency, not production persistence, regulatory retention compliance or real historical replay. **Recommend CTC-012 Done — scoped only after explicit approval of PS-01..PS-12** and acknowledgement of deferrals. No authoritative status is changed to Done in this candidate.
