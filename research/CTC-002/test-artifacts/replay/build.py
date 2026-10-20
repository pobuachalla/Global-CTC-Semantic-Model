import json,hashlib,zipfile,pathlib,copy
p=pathlib.Path('/mnt/data/CTC-002-D2-Prototype')
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canon(x)).hexdigest()
def write(name,x):(p/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
source={'representationId':'REP-SRC-001','formatFamily':'SYNTHETIC-JSON','sourcePath':'invoice.tax.localCategory','payload':{'documentNumber':'INV-2026-0042','issueDate':'2026-10-20','currency':'XCU','seller':'Alpha Trading Ltd','buyer':'Beta Services Ltd','netAmount':'1000.00','taxRate':'10.00','taxAmount':'100.00','payableAmount':'1100.00','localTaxCategory':'LOCAL-TAX-A','localTaxScheme':'XX-TAX-SCHEME'}}
source['contentSha256']=digest(source['payload'])
revision={'documentId':'DOC-001','revisionId':'REV-001','publicationState':'PUBLISHED','sourceRepresentationRef':'REP-SRC-001','commercial':{k:source['payload'][k] for k in ('documentNumber','issueDate','currency','seller','buyer','netAmount','taxRate','taxAmount','payableAmount')},'sourceFiscalFacts':[{'factId':'SF-01','concept':'localTaxClassification','value':'LOCAL-TAX-A','scheme':'XX-TAX-SCHEME','origin':'SOURCE_SUPPLIED','representationRef':'REP-SRC-001','sourcePath':'invoice.tax.localCategory'}]}
revision['revisionSha256']=digest({k:v for k,v in revision.items() if k!='revisionSha256'})
profiles=[{'profileId':'XX-CTC','profileVersion':'1.0.0','mappingId':'MAP-XX','mappingVersion':'1.0.0','codeListId':'XX-TAX','codeListVersion':'1.0.0','ruleId':'TAX-CLASSIFY-001','lookup':{'LOCAL-TAX-A':'STANDARD'}},{'profileId':'XX-CTC','profileVersion':'2.0.0','mappingId':'MAP-XX','mappingVersion':'2.0.0','codeListId':'XX-TAX','codeListVersion':'2.0.0','ruleId':'TAX-CLASSIFY-001','lookup':{'LOCAL-TAX-A':'SPECIAL'}}]
for prof in profiles:prof['packageSha256']=digest({k:v for k,v in prof.items() if k!='packageSha256'})
def interpret(prof,ref):
 f=revision['sourceFiscalFacts'][0];v=prof['lookup'][f['value']]
 result={'interpretationId':ref,'sourceRevisionRef':revision['revisionId'],'sourceRevisionSha256':revision['revisionSha256'],'profile':{k:prof[k] for k in ('profileId','profileVersion','mappingId','mappingVersion','codeListId','codeListVersion','ruleId','packageSha256')},'derivedFacts':[{'factId':'IF-'+ref[-3:],'concept':'normalizedTaxTreatment','value':v,'origin':'DERIVED','derivedFrom':[f['factId']],'derivation':{'operation':'CODE_LOOKUP','ruleId':prof['ruleId'],'inputValue':f['value'],'sourcePath':f['sourcePath'],'sourceRepresentationRef':f['representationRef'],'sourceRepresentationSha256':source['contentSha256']}}]}
 result['interpretationSha256']=digest({k:v for k,v in result.items() if k!='interpretationSha256'})
 return result
fi1=interpret(profiles[0],'FI-001');fi2=interpret(profiles[1],'FI-002')
assert revision['revisionSha256']==digest({k:v for k,v in revision.items() if k!='revisionSha256'})
assert fi1['derivedFacts'][0]['value']=='STANDARD' and fi2['derivedFacts'][0]['value']=='SPECIAL'
assert fi1['sourceRevisionSha256']==fi2['sourceRevisionSha256']
assert fi1==interpret(profiles[0],'FI-001') and fi2==interpret(profiles[1],'FI-002')
assert fi1['interpretationSha256']!=fi2['interpretationSha256']
assert all(f['derivedFacts'][0]['derivedFrom']==['SF-01'] for f in [fi1,fi2])
for name,obj in [('SOURCE-REPRESENTATION.json',source),('BILLING-REVISION.json',revision),('PROFILE-V1.json',profiles[0]),('PROFILE-V2.json',profiles[1]),('INTERPRETATION-V1.json',fi1),('INTERPRETATION-V2.json',fi2)]:write(name,obj)
report=f'''# CTC-002 — D2 Minimal Fiscal Interpretation Contract and Reproducibility Test

**Date:** 2026-10-20  
**Status:** Prototype completed; no ADR approved  
**Scope:** Synthetic fixture only. No official country validation or external XML processing.  
**Source baseline:** Semantic Billing Model v0.3; CTC-002 semantic contract consistency test; approved P1–P7 (as confirmed by user). GitHub remote HEAD was not read.

## 1. Minimal implementation-neutral contract

This is a **logical contract**, not a JSON Schema, table design, API definition or mandatory serialization. Reference strings and hashes are sample realizations of abstract identifiers.

| Component | Required logical properties | Invariant |
|---|---|---|
| Published billing revision | document identity, revision identity, source fiscal facts, revision content fingerprint | Publication freezes intrinsic content (P2) |
| Source fiscal fact | fact identity, concept, value, scheme, origin=SOURCE_SUPPLIED, source artifact and path | One authoritative owner; preserve original value (P6/P7) |
| Fiscal interpretation | interpretation identity, exact revision reference/fingerprint, profile package identity/fingerprint, derived facts | Never changes the referenced revision |
| Derived fiscal fact | fact identity, concept, value, origin=DERIVED, source fact refs, rule and package provenance | Cannot masquerade as a source fact (P7) |
| Profile package | profile/mapping/code-list IDs and versions, immutable package fingerprint, deterministic rule inputs | Reproducibility requires preserved executable rule semantics, not version labels alone |
| Representation | immutable artifact identity and content fingerprint | Original bytes must be retained separately (P3) |
| Compliance transaction (out of scope for execution) | exact revision, interpretation and submitted representation references | Processing history remains independent (P1/P4/P5) |

**Uniform logical resolver** (illustrative): `billing.revision(REV-001)`, `fiscal.sourceFact(SF-01)`, `fiscal.interpretation(FI-001).derivedFact(IF-001)`, `fiscal.interpretation(FI-002).derivedFact(IF-002)`. These paths identify meaning, not physical nesting. Resolution must specify interpretation ID explicitly; an implicit 'latest' lookup is unsafe for historical submissions.

## 2. Controlled input

- Document: `DOC-001`, published revision `REV-001`, invoice `INV-2026-0042`.
- Net `XCU 1000.00`, illustrative 10% tax `XCU 100.00`, payable `XCU 1100.00`.
- Source fact `SF-01`: local tax code `LOCAL-TAX-A` under `XX-TAX-SCHEME`.
- Original representation `REP-SRC-001`; source path `invoice.tax.localCategory`.
- Source content SHA-256: `{source['contentSha256']}`.
- Published revision SHA-256: `{revision['revisionSha256']}`.

`XX`, `XCU`, the code, profiles and rules are fictional; the mapping difference is intentionally manufactured to test interpretation history.

## 3. Two immutable profile packages

| Attribute | Version 1 | Version 2 |
|---|---|---|
| Profile | XX-CTC 1.0.0 | XX-CTC 2.0.0 |
| Mapping | MAP-XX 1.0.0 | MAP-XX 2.0.0 |
| Code list | XX-TAX 1.0.0 | XX-TAX 2.0.0 |
| Rule ID | TAX-CLASSIFY-001 | TAX-CLASSIFY-001 |
| Lookup LOCAL-TAX-A | STANDARD | SPECIAL |
| Package SHA-256 | `{profiles[0]['packageSha256']}` | `{profiles[1]['packageSha256']}` |

This test deliberately changes the lookup, so the same source fact yields a different derived interpretation. It is not evidence of any real jurisdictional code-list change.

## 4. Execution outputs

| Assertion | V1 result | V2 result | Outcome |
|---|---|---|---|
| Source revision | REV-001 | REV-001 | PASS — same identity |
| Revision fingerprint | identical | identical | PASS — unchanged source revision |
| Source fact | SF-01 / LOCAL-TAX-A | SF-01 / LOCAL-TAX-A | PASS — unchanged authority |
| Derived treatment | STANDARD | SPECIAL | PASS — distinct derived facts |
| Interpretation ID | FI-001 | FI-002 | PASS — distinct historical identities |
| Exact profile version | 1.0.0 | 2.0.0 | PASS — explicit version binding |
| Exact rule / code list | 1.0.0 / 1.0.0 | 2.0.0 / 2.0.0 | PASS — provenance captured |
| Deterministic replay | byte-equivalent canonical JSON | byte-equivalent canonical JSON | PASS — within this Python test |

Interpretation V1 SHA-256: `{fi1['interpretationSha256']}`  
Interpretation V2 SHA-256: `{fi2['interpretationSha256']}`.

## 5. Historical reproducibility procedure

1. Load the frozen source representation and revision; verify their stored fingerprints.
2. Load the exact historical profile/mapping/code-list package by immutable fingerprint, **not** by a mutable 'current' version pointer.
3. Evaluate the preserved rule against the preserved source fact and record derivation references.
4. Canonically serialize the resulting interpretation and compare its fingerprint with the stored historical result.
5. Repeat for V2; verify V1 remains unchanged and the commercial revision fingerprint remains identical.

The accompanying `build.py` performed this controlled replay deterministically and checked both interpretations. The SHA-256 values are real computed hashes of canonical JSON *within this synthetic prototype*. This does not establish durable archive integrity, real XML signature validity, or long-term runtime reproducibility across different rule engines.

## 6. Findings

- **D2-F1 (proposed):** Uniform interpretation shape supports version-specific outputs without mutating the published revision (P2).
- **D2-F2 (proposed):** P6 is preserved because `SF-01` has one source authority; both interpretations reference rather than overwrite it.
- **D2-F3 (proposed):** P7 requires immutable rule package contents or fingerprints as well as human-readable version strings.
- **D2-F4 (proposed):** A logical resolver must require an explicit interpretation identity for historical reproduction; 'latest' introduces drift.
- **D2-F5 (proposed):** The two-profile test demonstrates D2 consistency, **not** a real-world need for multiple interpretations of the same invoice.

## 7. Architectural assessment

D2 passes the limited synthetic reproducibility test. This is consistent with C, but does not prove that D2 requires a separate independently persisted aggregate or that an embedded snapshot cannot achieve the same outcomes. It does support defining a stable interpretation contract with explicit provenance and identity. **FiscalContext A/B/C/D2 remain unapproved.**

## 8. Open questions / evidence gates

1. What exactly freezes a published billing revision: ERP issuance, acceptance into platform, or a jurisdiction-specific legal milestone?
2. Can a fiscal source fact have legal ownership outside the billing revision while remaining frozen and source-traceable?
3. Is there a real verified invoice requiring two materially different interpretations under two jurisdiction profiles?
4. Which code-list, lookup, enrichment and external data inputs must be archived for replay?
5. How should version migration and correction of a faulty historic mapping be recorded without rewriting past interpretations?
6. What precision, locale, timezone, canonicalization and engine-version rules are necessary for cross-runtime determinism?
7. How should fiscal identity and authority evidence link to a specific generated representation and interpretation?

## 9. Decision and checkpoint

**CTC-002 remains Review / evidence-gated.** P1–P7 remain accepted at principle level. No new ADR or aggregate cardinality approved; CTC-003 remains not started. Add this report under `research/CTC-002/`. Review proposed findings before updating authoritative `FINDINGS.md`; preserve existing `DECISIONS.md` and `MODEL-BASELINE.md` until approval. GitHub was not written.
'''
(p/'CTC-002-D2-CONTRACT-AND-REPLAY.md').write_text(report)
(p/'README.md').write_text('# CTC-002 D2 prototype\n\nPlace the research report under `research/CTC-002/`. The JSON files and `build.py` are synthetic reproducibility fixtures. Run `python build.py` to regenerate the exact JSON outputs. No authoritative project register is replaced by this package.\n')
with zipfile.ZipFile('/mnt/data/CTC-002-D2-Contract-Reproducibility.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(p.iterdir()):z.write(f,arcname='research/CTC-002/D2-prototype/'+f.name)
print('PASS',revision['revisionSha256'],fi1['interpretationSha256'],fi2['interpretationSha256'])
