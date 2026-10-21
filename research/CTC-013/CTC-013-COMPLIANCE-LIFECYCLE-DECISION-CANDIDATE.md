# CTC-013 — Compliance Transaction and Event Model

**Version:** Decision Candidate 0.1 · **Date:** 2026-10-21 · **Status:** Proposed / CTC-013 In Progress

## 1. Baseline and evidence

Source baseline: `Global_CTC_CTC008_Kickoff_Full_Git_2026-10-21.zip`, specifically `BACKLOG.md`, `DECISIONS.md`, `MODEL-BASELINE.md`, `MASTER-PROMPT.md`, and `research/CTC-003/CTC-003-DETAILED-LOGICAL-DICTIONARY-APPROVED-SCOPED.md`. The CTC-008 inventory remains delegated/in progress. Live GitHub HEAD was not verified. Earlier `semantic-billing-model(1) (1).md` and `relational-data-model(1) (1).md` are historical candidates, not approval authority.

Accepted constraints preserved: D2, P1–P7, I-01–I-10; D03-1/2 immutable submission snapshots and evidence attribution; L01–L10 separation of preparation, legal/fiscal recognition and compliance processing; B01–B10 batch and member semantics; qualified C09; G2-C separate `SubmissionAttempt` and `TransportAttempt`; approved scoped CTC-003 detailed logical dictionary. CTC-005 JP-01–JP-10 and CTC-007 V-01–V-10 govern immutable profile/version references. No new detailed fields or physical aggregate decisions are approved here.

## 2. Scope and acceptance

In scope: compliance operation identity, destination and obligation, immutable submitted artifacts, transport and submission attempts, append-only event taxonomy, external correlation, envelope/member outcomes, derived status, legal-state assessment boundary and replay invariants. Out of scope: normalized authority response payload schema (CTC-014), public API/notification payloads (CTC-016), provider-specific retry rules, database/event broker selection, jurisdictional legality, and official fixtures (CTC-008/009/010).

Acceptance: (1) entity/identity and reference map; (2) typed event and state dimensions; (3) deterministic projection and ambiguity rules; (4) bounded synthetic scenario checks; (5) open evidence gates and approval recommendation.

## 3. Candidate logical records and authoritative ownership

| Concept | Responsibility / identity | Logical references and cardinality proposal |
|---|---|---|
| ComplianceTransaction | One document-specific compliance obligation/operation; `transactionId` | Exactly one published revision and one obligation/destination context per transaction; 0..N submission attempts/events. Multiple transactions per revision permitted. |
| SubmissionSnapshot | Immutable exact semantic, interpretation, mapping, outbound representation and destination references | Each submitted `SubmissionAttempt` pins exactly one snapshot. May be shared by retries if payload unchanged. |
| SubmissionAttempt | One document/member-level attempt; `submissionAttemptId` | Exactly one transaction, one snapshot when submitted, 0..N correlated events. |
| SubmissionEnvelope | Transport container and frozen member manifest; `envelopeId` | 1..N member references for submitted envelope; not itself a billing document. |
| EnvelopeMember | Exact member position/identifier and reference to a document-level attempt/snapshot | Exactly one envelope; exact member correlation within envelope. |
| TransportAttempt | One outbound transport operation; `transportAttemptId` | Exactly one immutable envelope/payload snapshot; 0..N transport events; can carry multiple members. |
| ProcessingEvent | Immutable typed observation/decision; `eventId` | Exactly one typed subject; event time, recorded time, source, evidence, correlation confidence. |
| ExternalCorrelation | Provider identifiers with typed namespace and scope | Can be unresolved/ambiguous; never infer unique identity from bare ID alone. |
| LegalStateAssessment | Versioned, evidence-backed jurisdiction-specific legal conclusion | References subject, jurisdiction, profile/rule package, evaluation time and evidence. Not an unconditional transport state. |
| FiscalIdentity / FiscalEvidence | Existing approved D2 identity/evidence concepts | Preserve exact authority attribution and original evidence. |

Cardinalities are **candidates** unless already covered by an accepted D03/B/C09 rule. No new aggregate roots or tables are mandated.

## 4. Four independent status dimensions

| Dimension | Candidate values | Evidence source |
|---|---|---|
| Transport | NOT_SENT, SENT, ACKNOWLEDGED, FAILED, UNKNOWN | TransportAttempt and transport events |
| Validation | NOT_EVALUATED, PASSED, FAILED, PARTIAL, UNKNOWN | Typed validation results |
| Authority processing | NOT_SUBMITTED, PENDING, ACCEPTED, REJECTED, PARTIAL, UNKNOWN | Authority/member-level events with verified correlation |
| Legal/fiscal recognition | NOT_ASSESSED, ISSUED, CLEARED, CANCELLED, NOT_RECOGNIZED, UNKNOWN | Explicit LegalStateAssessment and profile-governed evidence |

These are logical categories, not a universal legal-state machine. In particular `ACCEPTED` in an authority processing dimension does not automatically equal `CLEARED` in the legal dimension.

## 5. Event contract

Minimum candidate event metadata: `eventId`, `subjectType`, `subjectRef`, `eventType`, `occurredAt`, `recordedAt`, `origin`, `correlationRef`, `evidenceRef`, `payloadRepresentationRef`, `profilePackageRef` when applicable, and `supersedesEventRef` only for explicit correction of an erroneous observation. Preserve original observations; never mutate/delete them to change projected status. `eventId` is unique within the event store. `occurredAt` may be unknown; never silently substitute `recordedAt` as authority occurrence time.

Suggested typed event families: `SUBMISSION_PREPARED`, `SUBMISSION_SENT`, `TRANSPORT_ACK`, `TRANSPORT_TIMEOUT`, `TRANSPORT_FAILED`, `VALIDATION_RESULT`, `AUTHORITY_ACK`, `AUTHORITY_ACCEPTED`, `AUTHORITY_REJECTED`, `MEMBER_OUTCOME`, `EVIDENCE_RECEIVED`, `CANCELLATION_REQUESTED`, `CANCELLATION_CONFIRMED`, `CORRELATION_RESOLVED`, `CORRELATION_AMBIGUOUS`, `ASSESSMENT_RECORDED`. These are candidates and do not imply all providers expose each event.

## 6. Proposed projection policy

1. Project by typed subject and independently by dimension. Never infer member outcome from envelope success.
2. Use verified correlation, not arrival order, to attribute responses. Unknown or ambiguous correlation produces `UNKNOWN` or `UNRESOLVED`, not acceptance/rejection.
3. A transport timeout is `UNKNOWN` delivery, not authority rejection. Retry creates a new attempt; preserve the old attempt and original payload/snapshot.
4. Duplicate callbacks with the same provider event identity and content are deduplicated for projection, but retained or referenced for audit. Conflicting callbacks are not silently overwritten; mark unresolved pending authoritative ordering/correction evidence.
5. Later legal-state assessment (e.g., cancellation) does not erase earlier clearance evidence. Store time-scoped assessments and expose latest *supported* assessment, retaining history.
6. Projection output includes `asOf`, input-event references, algorithm/profile version, correlation confidence, and `NOT_EVALUABLE`/`UNKNOWN` reason. Replays over the same pinned inputs and rules must reproduce the same result.
7. Authority responses and source payloads remain immutable representations. Mapping into events is versioned and preserves provenance.

## 7. Proposed CTC-013 decision candidates

| ID | Proposal | Status |
|---|---|---|
| CL-01 | Independent identity for each document/obligation-specific compliance transaction | Proposed |
| CL-02 | Separate per-document SubmissionAttempt and envelope-level TransportAttempt | Already accepted logical separation; detailed contract proposed |
| CL-03 | Append-only typed processing events with immutable subject and evidence references | Proposed (aligned with accepted P5) |
| CL-04 | Independent transport, validation, authority and legal status dimensions | Proposed (aligned with accepted L01–L10) |
| CL-05 | No legal inference from envelope acknowledgement, transport success or unresolved response | Existing accepted constraints; projection detail proposed |
| CL-06 | Deterministic versioned status projection with explicit unknown/ambiguity | Proposed |
| CL-07 | Correlation scoped by provider, operation, envelope/member and attempt; no bare-ID assumption | Proposed |
| CL-08 | Retry, duplicate and out-of-order events preserve full history | Proposed |

No decisions accepted under CTC-013 without user review. Existing accepted logical constraints are not being resubmitted for approval.

## 8. Bounded synthetic scenario matrix

| ID | Case | Expected |
|---|---|---|
| S01 | Single document accepted by authority | Member authority ACCEPTED; legal state remains NOT_ASSESSED without separate assessment |
| S02 | Envelope ACK with two members and no member decisions | Transport ACKNOWLEDGED; both members PENDING/UNKNOWN, never accepted by implication |
| S03 | Partial batch (member A accepted, B rejected) | Independent member outcomes and transaction projections |
| S04 | Timeout then retry | First transport UNKNOWN; second distinct attempt; no inferred rejection |
| S05 | Duplicate callback | No duplicate status transition; audit observation retained |
| S06 | Late/out-of-order callback | Correlate to exact attempt/member, not newest attempt |
| S07 | Ambiguous external ID | UNRESOLVED, no fabricated member outcome |
| S08 | Cancellation after clearance | Preserve earlier CLEARED assessment and later supported CANCELLED assessment |
| S09 | Conflicting outcomes without precedence evidence | UNKNOWN/CONFLICT, not last-write-wins |
| S10 | Replay same immutable event set and policy | Identical projection, including evidence refs |

## 9. Evidence gates and dependencies

- **CTC-014:** actual normalized authority response taxonomy, typed reasons, correlation/evidence payload and provider-specific response precedence.
- **CTC-008/009/010:** licensed version-pinned batch/partial/correction fixtures and official schema validation.
- **CTC-016:** external API status vocabulary, polling and notifications.
- **CTC-011/012:** logical persistence and retention/event storage; physical FiscalContext A/B/C still deferred.
- **CTC-017:** ADR namespace, formal supersession and governance.

## 10. Closure recommendation and checkpoint

**Current status:** CTC-013 In Progress. This is one bounded decision candidate, not an approved contract. Recommend executing S01–S10 and then seeking a single scoped logical lifecycle approval. Country-specific legal state and actual provider event mapping remain deferred. Suggested project-file changes after approval: BACKLOG (CTC-013 status), DECISIONS (CL disposition), FINDINGS (evidence limits), MODEL-BASELINE (logical processing boundary), SESSION-LOG (checkpoint). Do not overwrite authoritative project registers before review.
