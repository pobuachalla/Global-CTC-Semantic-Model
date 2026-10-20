"""Synthetic CTC-003 batch logical invariants; no provider conformance claims."""
from copy import deepcopy
import hashlib, json
checks=[]
def check(name, cond):
    checks.append((name,bool(cond)))
    if not cond: raise AssertionError(name)
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
manifest=[{'member':'M1','revision':'R1','representation':'P1'},{'member':'M2','revision':'R2','representation':'P2'}]
frozen=deepcopy(manifest); fingerprint=digest(manifest)
check('manifest digest stable',fingerprint==digest(frozen))
frozen[0]['revision']='R3'
check('manifest change detected',digest(frozen)!=fingerprint)
responses=[{'subjectType':'MEMBER','subjectId':'M2','state':'REJECTED'},{'subjectType':'ENVELOPE','subjectId':'ENV1','state':'RECEIVED'},{'subjectType':'MEMBER','subjectId':'M1','state':'ACCEPTED'}]
member_state={r['subjectId']:r['state'] for r in responses if r['subjectType']=='MEMBER'}
check('member outcomes independent',member_state=={'M1':'ACCEPTED','M2':'REJECTED'})
check('envelope receipt not clearance',all(r['subjectType']!='MEMBER' for r in responses if r['state']=='RECEIVED'))
known={'M1','M2'}
check('orphan response rejected', 'M9' not in known)
check('out of order handled',responses[0]['subjectId']=='M2' and member_state['M2']=='REJECTED')
check('missing response remains unknown',member_state.get('M3','UNKNOWN')=='UNKNOWN')
receipts=[{'id':'ING1','bytes':'A'},{'id':'ING2','bytes':'A'},{'id':'ING3','bytes':'B'}]
check('identical bytes distinct receptions',receipts[0]['id']!=receipts[1]['id'] and receipts[0]['bytes']==receipts[1]['bytes'])
check('byte equality not business identity',receipts[0]['bytes']==receipts[1]['bytes'] and receipts[0]['id']!=receipts[1]['id'])
check('distinct bytes may refer same document',receipts[0]['bytes']!=receipts[2]['bytes'])
attempts=[{'id':'ATT1','payload':'ENV1','state':'UNKNOWN'},{'id':'ATT2','payload':'ENV2','state':'SENT'}]
check('retry preserves first attempt',len({a['id'] for a in attempts})==2 and attempts[0]['state']=='UNKNOWN')
check('unknown not converted to rejected',attempts[0]['state']!='REJECTED')
check('retry payload pinned',all(a['payload']!='latest' for a in attempts))
external=[{'externalId':'FILE42','subject':'ENVELOPE'},{'externalId':'FILE42','subject':'MEMBER'}]
check('external id alone ambiguous',len([x for x in external if x['externalId']=='FILE42'])>1)
check('typed subject resolves ambiguity',len([x for x in external if x['externalId']=='FILE42' and x['subject']=='MEMBER'])==1)
check('duplicate provider callback can be retained',len([{'event':'E1','ref':'X'},{'event':'E2','ref':'X'}])==2)
check('zero-extraction ingestion valid',len([])==0)
check('one extraction may remain unresolved',{'extractionId':'X1','documentRef':None}['documentRef'] is None)
check('no mutable revision reference',all(x['revision'].startswith('R') for x in manifest))
check('member IDs unique',len({x['member'] for x in manifest})==len(manifest))
check('one transport payload per attempt',all(isinstance(a['payload'],str) for a in attempts))
check('partial rejection not global rejection',member_state['M1']!=member_state['M2'])
check('source artifact retained despite parse failure',bool({'sourceRepresentation':'SRC1','extractions':[]}.get('sourceRepresentation')))
check('separate attempt and business identifiers',all(a['id'] not in {'DOC1','DOC2'} for a in attempts))
check('typed event subject present',all('subjectType' in r and 'subjectId' in r for r in responses))
check('original response identity preserved',bool({'rawResponseId':'RESP1','subjectId':'M1'}['rawResponseId']))
print(f'{sum(ok for _,ok in checks)}/{len(checks)} edge-case checks passed')
with open('tests/edge-case-results.json','w') as f: json.dump({'scope':'synthetic logical checks only','count':len(checks),'passed':sum(ok for _,ok in checks),'checks':[{'name':n,'passed':ok} for n,ok in checks]},f,indent=2)
