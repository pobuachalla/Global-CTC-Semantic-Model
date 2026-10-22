# CTC-014 — Normalized Authority Response Contract

**Version:** Candidate 0.1 | **Date:** 2026-10-21 | **Status:** Proposed / In Progress

## Baseline and authority

Reviewed local 2026-10-21 CTC-013 approved snapshot: MASTER-PROMPT, BACKLOG, DECISIONS, MODEL-BASELINE, and CTC-013 decision candidate. CTC-001–007 and CTC-013 are Done—scoped; CTC-008 is delegated. Live GitHub HEAD and real provider response fixtures were not verified. CL-01–CL-08 and existing D2/P1–P7/JP/V principles are accepted; the following response-field definitions are candidates only. The 18 CTC-003 field proposals and FiscalContext A/B/C remain deferred.

## Bounded scope

Normalize responses from PAs, providers and tax authorities to immutable observations with typed subject, correlation, status dimension, findings, external identifiers, evidence and provenance. Support client-consumable *logical* projections, but defer HTTP/webhooks/ERP payload contracts to CTC-016. No universal country-specific legal rules are asserted.

## Candidate logical contract

| Concept | Required candidate attributes | Optional candidate attributes | Rule |
|---|---|---|---|
| AuthorityResponseObservation | observationId, sourceSystem, receivedAt, originalRepresentationRef, originalDigest, responseKind, subjectType, correlationStatus | occurredAt, providerMessageId, responseProfileRef | One immutable received observation, even if duplicate |
| ResponseSubject | subjectType, subjectRef when resolved | envelopeId, memberId, submissionAttemptId, transportAttemptId, complianceTransactionId | Unresolved/ambiguous response must not fabricate subjectRef |
| ResponseCorrelation | sourceSystem, identifierScheme, identifierValue, scope, resolutionState | candidateSubjects, resolutionEvidenceRefs | Provider-scoped; ambiguity is explicit |
| NormalizedOutcome | dimension, outcomeCode, observedOrAsserted, effectiveAt when known | reasonRefs, evidenceRefs, policyRef | Observed outcome is not automatically legal assessment |
| ResponseFinding | category, severity, sourceCode, sourceSystem | canonicalCategory, sourceMessage, language, sourcePath, semanticPath, ruleRef | Preserve original code and message; avoid invented translations |
| ExternalReference | referenceType, scheme, issuer, value, subjectType | jurisdiction, subjectRef, evidenceRef | Fiscal identity != submission correlation != certification event |
| ResponseEvidence | evidenceType, representationRef, digest | signatureRef, verificationState, verificationMethodRef | A signature presence does not imply cryptographic verification |
| ClientStatusProjection | subjectRef, asOf, policyVersion, dimensionStatuses, evidenceRefs | unresolvedReason, correlationConfidence | Derived versioned projection, not source response or API schema |

Candidate `responseKind`: TRANSPORT_ACK, VALIDATION_RESULT, AUTHORITY_ACK, AUTHORITY_DECISION, FISCAL_IDENTITY_ASSIGNED, CANCELLATION_RESPONSE, INFORMATIONAL, UNKNOWN. These are internal taxonomy proposals, not mandated provider codes.

Candidate `correlationStatus`: RESOLVED, AMBIGUOUS, UNRESOLVED. Unknown provider codes remain source-native and are mapped to UNKNOWN when unsupported.

## Proposed logical rules for review

| ID | Rule |
|---|---|
| AR-01 | Preserve each original response representation, digest, arrival time and provenance immutably. |
| AR-02 | Normalize observations without replacing original source codes, messages or unknown fields. |
| AR-03 | Correlate by scoped typed identifiers; unresolved/ambiguous references cannot establish document-specific outcomes. |
| AR-04 | Distinguish envelope, member, submission, transport and compliance-transaction subjects. |
| AR-05 | Keep transport, validation, authority-processing and legal-state dimensions separate. |
| AR-06 | Do not infer legal clearance or issuance from transport ACK or authority acceptance alone. |
| AR-07 | Distinguish authority-issued fiscal identity, correlation IDs and certification-event references. |
| AR-08 | Preserve duplicate, late, conflicting and superseding responses in append-only history; projections use explicit precedence evidence. |
| AR-09 | Preserve response findings with original code, text, language, severity and applicable location when supplied. |
| AR-10 | Produce deterministic, versioned, evidence-linked client status projections; unknown/ambiguous outcomes remain explicit. |

## Representative examples

1. Envelope ACK for two members: envelope transport ACKNOWLEDGED; neither member is ACCEPTED by inference.
2. Member A accepted, member B rejected: two correlated authority outcomes and separate findings.
3. Timeout, retry, late first response: attribute by original attempt, preserve both histories.
4. Authority-assigned ID: typed FiscalIdentity with issuer/scheme/subject, never copied to commercial document number.
5. Cancellation after clearance: retain both evidence sets and distinct legal assessments.

## Validation matrix and evidence gates

| ID | Synthetic scenario | Expected |
|---|---|---|
| R01 | Transport ACK only | No member acceptance or legal clearance |
| R02 | Partial batch | Outcomes isolated by member |
| R03 | Ambiguous external ID | No resolved subject |
| R04 | Duplicate callback | Original observations retained; no duplicate projection transition |
| R05 | Late callback | Original attempt correlation retained |
| R06 | Conflicting decisions | Explicit conflict without precedence evidence |
| R07 | Fiscal identity | Typed identity distinct from correlation |
| R08 | Validation failure | Original codes and messages preserved |
| R09 | Cancellation | Earlier clearance evidence retained |
| R10 | Deterministic projection replay | Identical output for pinned inputs |

**Missing evidence:** real version-pinned authority response fixtures (CTC-008/009/010), provider precedence/correlation semantics, cryptographic signature validation, legal status rules and API transport contracts (CTC-016). These are not CTC-014 logical approval prerequisites if scoped closure is accepted.

## Closure recommendation

Run the ten bounded scenarios; if they pass and no ownership contradiction emerges, seek one scoped approval of AR-01–AR-10. Do not mark CTC-014 Done or modify accepted ADRs without user approval. Keep all detailed entity/cardinality choices candidate and all provider-specific rules deferred.
