# PICK UP NEXT SESSION — Global CTC Semantic Model

**Checkpoint date:** 2026-10-19  
**Active task:** CTC-002 — Agree semantic aggregate boundaries  
**Current status:** REVIEW / EVIDENCE-GATED; not Done  
**Approved new ADRs:** NONE  
**Current model:** UNAPPROVED candidate models; no final semantic contract.

## Read first (in order)

1. `PROJECT-FILES/PROJECT-INSTRUCTIONS.md` and `PROJECT-FILES/MASTER-PROMPT.md`.
2. `PROJECT-FILES/BACKLOG.md`, `PROJECT-FILES/DECISIONS.md`, `PROJECT-FILES/MODEL-BASELINE.md`, `PROJECT-FILES/FINDINGS.md`, `PROJECT-FILES/SESSION-LOG.md`.
3. `RESEARCH/CTC-002-AGGREGATE-BOUNDARIES-DRAFT.md`, `RESEARCH/CTC-002-FISCAL-FIELD-OWNERSHIP-MATRIX.md`, and `RESEARCH/CTC-002-FRANCE-EXTENDED-CTC-STRESS-TEST.md`.
4. If needed, the Mexico CFDI and Italy SdI evidence reviews, then CTC-001 reconciliation.

## State to preserve

- User selected composed semantic contract as **leading hypothesis for investigation**, not an accepted decision.
- FiscalContext alternatives **A embedded immutable**, **B independently versioned**, **C hybrid** are all OPEN.
- Billing meaning, serialized representations and compliance events have conceptually distinct ownership; aggregate cardinality and fiscal interpretation independence remain unapproved.
- French v0.3 example: GROUP 10 +21,425.59; DETAIL 11 +21,425.59 noncontributing; GROUP 20 -204.78. Contributing sum **EUR 21,220.81**.
- French test is **internal worked-example validation only**, not executed raw XML/XSD or verified current French mandate requirements.
- F-002-11..35 are in FINDINGS.md as **Pending review**. No project-wide ADR was accepted.

## Recommended next steps

1. **CTC-002 review:** inspect proposed field-ownership and invariant matrix. Decide whether to accept any *principles* (not necessarily fiscal context cardinality). Explicitly record user approval.
2. **Evidence gate:** obtain licensed, versioned French Extended CTC UBL fixture and profile/XSD; genuine CFDI pre/post certification pair; FatturaPA + SdI response pair. Run field-level preservation and profile tests.
3. **Discriminator:** seek real case requiring two independent fiscal interpretations for the *same immutable billing revision*. If none, avoid overengineering B/C purely for hypothetical cases.
4. Only after CTC-002 approval, begin **CTC-003** entity dictionary/cardinalities, keeping relational schema design deferred.

## Copy/paste starter prompt

> Resume Global CTC Semantic Model from the 2026-10-19 evening checkpoint. Read PROJECT-INSTRUCTIONS.md, MASTER-PROMPT.md, BACKLOG.md, DECISIONS.md, FINDINGS.md, MODEL-BASELINE.md and SESSION-LOG.md, then the CTC-002 France stress test and field ownership matrix. Work on CTC-002 only. Review evidence and present a decision-ready aggregate boundary/invariant matrix. Preserve A/B/C as unapproved until I explicitly approve. Clearly distinguish the internal French example from independently verified regulatory fixtures. Produce a session checkpoint and proposed file changes; do not silently mark CTC-002 Done.

## How to apply this bundle

- This ZIP contains **updated working copies**, not synchronized ChatGPT Project files. Review and replace the six matching Markdown files in your Project with `PROJECT-FILES/*` (the README, instructions and master prompt are included for completeness).
- Add the files in `RESEARCH/` as project reference artifacts. Keep original source specifications attached separately.
- Use the **latest bundled copies** rather than older same-named files from prior conversations. Do not combine conflicting copies blindly.
- The bundle does not contain original source specifications, uploaded Excel, or code ZIP. Those remain external references in the Project.
