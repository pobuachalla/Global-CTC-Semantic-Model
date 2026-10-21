import json, hashlib
from pathlib import Path
OUT=Path(__file__).parent

def project(events, subject, asof=100, policy='CL-candidate-0.1'):
    relevant=[e for e in events if e['subject']==subject and e['recorded']<=asof]
    seen=set(); effective=[]; duplicates=[]
    for e in sorted(relevant,key=lambda x:(x['recorded'],x['id'])):
        key=(e.get('provider_event_id'),e['kind'],e.get('value'),e.get('attempt'))
        if e.get('provider_event_id') and key in seen:
            duplicates.append(e['id']);continue
        seen.add(key);effective.append(e)
    valid=[e for e in effective if e.get('correlation')=='VERIFIED']
    auth=[e for e in valid if e['kind']=='AUTHORITY_OUTCOME']
    values={e['value'] for e in auth}
    authority=next(iter(values)) if len(values)==1 else ('CONFLICT' if len(values)>1 else 'UNKNOWN')
    assessments=[e for e in valid if e['kind']=='LEGAL_ASSESSMENT']
    legal=assessments[-1]['value'] if assessments else 'NOT_ASSESSED'
    return {'subject':subject,'authority':authority,'legal':legal,'evidence':[e['id'] for e in effective], 'duplicates':duplicates,'policy':policy,'asOf':asof}

def ev(id,subject,kind,value=None,attempt=None,recorded=1,correlation='VERIFIED',provider_event_id=None):
    return dict(id=id,subject=subject,kind=kind,value=value,attempt=attempt,recorded=recorded,correlation=correlation,provider_event_id=provider_event_id)

results=[]
def check(case, condition, observation):
    results.append({'scenario':case,'passed':bool(condition),'observation':observation})

s01=project([ev('a1','m1','AUTHORITY_OUTCOME','ACCEPTED')],'m1');check('S01',s01['authority']=='ACCEPTED' and s01['legal']=='NOT_ASSESSED',s01)
s02=project([ev('ack','envelope','TRANSPORT_ACK','ACKNOWLEDGED')],'m1');s02b=project([ev('ack','envelope','TRANSPORT_ACK','ACKNOWLEDGED')],'m2');check('S02',s02['authority']=='UNKNOWN' and s02b['authority']=='UNKNOWN',{'m1':s02,'m2':s02b})
s03a=project([ev('m1a','m1','AUTHORITY_OUTCOME','ACCEPTED')],'m1');s03b=project([ev('m2r','m2','AUTHORITY_OUTCOME','REJECTED')],'m2');check('S03',s03a['authority']=='ACCEPTED' and s03b['authority']=='REJECTED',{'m1':s03a,'m2':s03b})
first=ev('t1','transport1','TRANSPORT_TIMEOUT','UNKNOWN',attempt='t1');second=ev('t2','transport2','TRANSPORT_ACK','ACKNOWLEDGED',attempt='t2');check('S04',first['attempt']!=second['attempt'] and project([first,second],'m1')['authority']=='UNKNOWN',{'attempts':[first,second]})
dup=[ev('cb1','m1','AUTHORITY_OUTCOME','ACCEPTED',provider_event_id='P-1'),ev('cb2','m1','AUTHORITY_OUTCOME','ACCEPTED',recorded=2,provider_event_id='P-1')];p=project(dup,'m1');check('S05',p['authority']=='ACCEPTED' and p['duplicates']==['cb2'],p)
late=[ev('new','m2','AUTHORITY_OUTCOME','REJECTED',attempt='attempt2',recorded=1),ev('late','m1','AUTHORITY_OUTCOME','ACCEPTED',attempt='attempt1',recorded=3)];check('S06',project(late,'m1')['authority']=='ACCEPTED' and project(late,'m2')['authority']=='REJECTED',{'late':late})
amb=project([ev('amb','m1','AUTHORITY_OUTCOME','ACCEPTED',correlation='AMBIGUOUS')],'m1');check('S07',amb['authority']=='UNKNOWN',amb)
legal=[ev('clear','m1','LEGAL_ASSESSMENT','CLEARED',recorded=1),ev('cancel','m1','LEGAL_ASSESSMENT','CANCELLED',recorded=2)];p=project(legal,'m1');check('S08',p['legal']=='CANCELLED' and 'clear' in p['evidence'] and 'cancel' in p['evidence'],p)
conflict=project([ev('accept','m1','AUTHORITY_OUTCOME','ACCEPTED'),ev('reject','m1','AUTHORITY_OUTCOME','REJECTED',recorded=2)],'m1');check('S09',conflict['authority']=='CONFLICT',conflict)
fixture=[ev('e1','m1','AUTHORITY_OUTCOME','ACCEPTED'),ev('e2','m1','LEGAL_ASSESSMENT','CLEARED',recorded=2)];a=project(fixture,'m1');b=project(list(reversed(fixture)),'m1');check('S10',a==b,{'first':a,'replay':b})
output={'source':'CTC-013 decision candidate 0.1','test_type':'synthetic focused contract checks','results':results,'passed':sum(x['passed'] for x in results),'total':len(results)}
(OUT/'results.json').write_text(json.dumps(output,indent=2))
for r in results: print(r['scenario'], 'PASS' if r['passed'] else 'FAIL')
print('TOTAL',output['passed'],'/',output['total'])
assert output['passed']==output['total']
