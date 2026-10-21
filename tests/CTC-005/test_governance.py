import json, hashlib
from pathlib import Path

BASE=Path(__file__).resolve().parent

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def evaluate_profiles(profiles, facts):
    matches=[]
    for p in profiles:
        basis=p['dateBasis']
        if basis not in facts: return 'NOT_EVALUABLE'
        if p['from']<=facts[basis] and (p.get('to') is None or facts[basis]<p['to']): matches.append(p)
    if not matches:return 'NOT_APPLICABLE'
    if len(matches)>1:
        ordered=[p for p in matches if p.get('precedence') is not None]
        if len(ordered)!=len(matches) or len(set(p['precedence'] for p in ordered))!=len(ordered):return 'AMBIGUOUS'
        return max(ordered,key=lambda p:p['precedence'])['id']
    return matches[0]['id']

def interpret(code, package):return {'sourceCode':code,'sourceScheme':'XX','derived':package['mapping'].get(code),'profileDigest':digest(package)}

def extension_decision(concept,core):return 'REJECT_REDUNDANT_EXTENSION' if concept in core else 'REQUIRE_TYPED_EXTENSION_REVIEW'

def ownership_decision(target):return 'REJECT_WRONG_OWNER' if target=='BillingDocument.authorityResponseId' else 'ALLOW_CANDIDATE'

def core_promotion(evidence):return 'ADR_AND_MIGRATION_REQUIRED' if evidence['crossJurisdiction'] else 'INSUFFICIENT_REUSE_EVIDENCE'

cases=[]
def test(name,actual,expected):
    cases.append({'name':name,'expected':expected,'actual':actual,'passed':actual==expected})

profiles=[{'id':'p1','dateBasis':'issueDate','from':'2026-01-01','to':'2027-01-01'},{'id':'p2','dateBasis':'issueDate','from':'2026-06-01','to':'2027-06-01'}]
test('Overlapping published profiles without precedence',evaluate_profiles(profiles,{'issueDate':'2026-10-01'}),'AMBIGUOUS')
test('Missing applicability date basis',evaluate_profiles(profiles,{'supplyDate':'2026-10-01'}),'NOT_EVALUABLE')
p1={'version':'1.0','mapping':{'LOCAL-A':'STANDARD'}}; p2={'version':'2.0','mapping':{'LOCAL-A':'SPECIAL'}}
historical=interpret('LOCAL-A',p1); new=interpret('LOCAL-A',p2)
test('Historical v1 mapping unchanged after v2 release',historical==interpret('LOCAL-A',p1) and historical['derived']=='STANDARD' and new['derived']=='SPECIAL' and historical['profileDigest']!=new['profileDigest'],True)
test('Redundant local extension rejected',extension_decision('BillingDocument.issueDate',{'BillingDocument.issueDate'}),'REJECT_REDUNDANT_EXTENSION')
unknown=interpret('UNRECOGNIZED',p1)
test('Unknown local source code preserved',unknown['sourceCode']=='UNRECOGNIZED' and unknown['derived'] is None,True)
test('Authority response ID cannot become billing field',ownership_decision('BillingDocument.authorityResponseId'),'REJECT_WRONG_OWNER')
test('Reusable core concept requires ADR and migration',core_promotion({'crossJurisdiction':True}),'ADR_AND_MIGRATION_REQUIRED')
results={'source':'CTC-005 jurisdiction profile governance decision candidate 2026-10-21','scope':'synthetic logical governance contract','cases':cases,'passed':sum(c['passed'] for c in cases),'total':len(cases)}
(BASE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
for c in cases:print(('PASS' if c['passed'] else 'FAIL'),c['name'])
print(f"TOTAL {results['passed']}/{results['total']}")
assert results['passed']==results['total']
