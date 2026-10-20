# CTC-002 — Italy FatturaPA / SdI Response Evidence Review

Date: 2026-10-19  
Status: Working evidence; no ADR approved.

## Scope
Assess B2B/B2C and B2G SdI notification families, and their implications for semantic aggregate boundaries. This is a documentation-based review, not a verified paired-payload test.

## Sources
- Agenzia delle Entrate guide: https://www1.agenziaentrate.gov.it/web_app_entrate/fatturazione_elettronica.html/guide-gallery.html
- FatturaPA SDIFTP technical specifications v4.2: https://www.fatturapa.gov.it/export/documenti/ftp/v4.x/Specifiche_tecniche_FTP_v4.2.pdf
- Existing Global CTC Semantic Billing Model v0.3 and Relational Model v0.3 (project artifacts).

## Verified distinctions
1. SdI scarto means the invoice is considered not issued; correction and retransmission are required, subject to current authority guidance.
2. Successful SdI processing followed by delivery receipt establishes a delivery timestamp.
3. An invoice processed by SdI but not delivered to the recipient may still be issued for the supplier; buyer receipt/availability is a distinct dimension.
4. Notification families vary by B2G versus B2B/B2C. B2G supports additional recipient-outcome and expiry notifications; do not assume these apply to all invoices.
5. SdI assigns a file identifier; this is not the supplier's commercial invoice number.

## Candidate field ownership
| Data | Candidate owner | Rationale |
|---|---|---|
| Invoice number, parties, lines, taxes | BillingDocument revision | Intrinsic commercial/tax meaning |
| TipoDocumento and RegimeFiscale | FiscalContext / fiscal interpretation | Country fiscal classification |
| Source FatturaPA XML | DocumentRepresentation | Immutable source/target artifact |
| SdI file ID, notification correlation | ComplianceTransaction / SubmissionAttempt | External process identity |
| Scarto code and message | ValidationResult linked to ProcessingEvent | External validation outcome |
| Delivery timestamp and unavailable-delivery status | ProcessingEvent | Distinct from fiscal issuance |
| Recipient outcome (B2G) | ProcessingEvent | Workflow-specific dimension |
| Original notification XML | ResponseArtifact / DocumentRepresentation | Preserve original external evidence |
| Receipt evidence | ComplianceEvidence | Immutable supporting evidence |

## Instance-level branches
### Rejected
Before: DOC-IT-001 / REV-001 / REP-001 / CT-001 / ATT-001 (sent).
After: same frozen revision and representation; append EVT-NS-001 and VAL-001; CT-001 projects REJECTED / NOT_ISSUED. Corrected payload must be a new representation and, if commercial/fiscal meaning changes, a new revision. Exact permitted numbering and timing are jurisdiction-specific.

### Delivered
Before: CT-001 pending. After: append EVT-RC-001 with delivery timestamp and SdI file ID; status projections indicate processed and delivered; document commercial content unchanged.

### Not delivered
Before: CT-001 pending. After: append EVT-MC-001 with recipient-unavailable outcome; supplier issuance and recipient delivery must remain separately represented.

### B2G recipient response
After successful delivery, an additional recipient outcome can be received. Append EVT-EC-001; do not rewrite the original delivery event.

## Architectural implication
Italy provides direct evidence against a single universal document `status` scalar. It supports independently tracked compliance processing and immutable response artifacts, but does not alone prove FiscalContext must be an independently versioned aggregate. Embedded snapshot, independent, and hybrid FiscalContext alternatives remain open.

## Proposed findings (not yet accepted)
- F-002-26: Issuance and recipient delivery must be modeled as distinct lifecycle dimensions.
- F-002-27: Scarto is a process/legal outcome and must not erase the submitted representation.
- F-002-28: SdI file identity is distinct from commercial invoice identity.
- F-002-29: Response/event models must support workflow-specific notification families (B2G vs B2B/B2C).
- F-002-30: SdI response evidence supports separate processing/event ownership, not necessarily independent FiscalContext ownership.

## Remaining evidence gates
- Obtain genuine, licensed, paired FatturaPA and SdI RC/NS/MC notification XML samples, including applicable XSD versions.
- Verify field-level correlation paths and exact cardinalities against schema.
- Compare B2G EC/DT/AT cases and confirm state transitions.
- Validate rejection-correction-resubmission identity and versioning rules using authority examples.

## Checkpoint
CTC-002 remains In Progress. No ADR accepted. Model baseline unchanged. Proposed updates: FINDINGS.md F-002-26..30; SESSION-LOG.md Italy evidence review; DECISIONS.md preserve A/B/C alternatives.
