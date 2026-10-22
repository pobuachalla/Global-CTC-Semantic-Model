import json
from pathlib import Path


def project(events):
    outcomes={}; observations=[]
    for e in events:
        observations.append(e['id'])
        if e.get('correlation')!='RESOLVED' or e.get('subject_type')!='MEMBER':
            continue
        k=e['subject']; code=e.get('outcome')
        if code not in ('ACCEPTED','REJECTED'):
            continue
        outcomes.setdefault(k,set()).add(code)
    return {'members':{k: ('CONFLICT' if len(v)>1 else next(iter(v))) for k,v in sorted(outcomes.items())},'observations':sorted(observations)}


def ev(id,subject=None,outcome=None,correlation='RESOLVED',subject_type='MEMBER'):
    return dict(id=id,subject=subject,outcome=outcome,correlation=correlation,subject_type=subject_type)

results={}
results['R01']=project([ev('ack','batch', 'ACCEPTED',subject_type='ENVELOPE')])['members']=={}
results['R02']=project([ev('a','A','ACCEPTED'),ev('b','B','REJECTED')])['members']=={'A':'ACCEPTED','B':'REJECTED'}
results['R03']=project([ev('amb','A','ACCEPTED',correlation='AMBIGUOUS')])['members']=={}
results['R04']=len(project([ev('x','A','ACCEPTED'),ev('x2','A','ACCEPTED')])['observations'])==2 and project([ev('x','A','ACCEPTED'),ev('x2','A','ACCEPTED')])['members']['A']=='ACCEPTED'
results['R05']=project([dict(ev('late','A','ACCEPTED'),attempt='first'),dict(ev('retry','A'),attempt='second')])['members']['A']=='ACCEPTED'
results['R06']=project([ev('x','A','ACCEPTED'),ev('y','A','REJECTED')])['members']['A']=='CONFLICT'
identity={'referenceType':'FISCAL_IDENTITY','value':'F-123','issuer':'AUTH','scheme':'AUTH_DOC'}; corr={'referenceType':'SUBMISSION_CORRELATION','value':'F-123','issuer':'AUTH','scheme':'SUB'}
results['R07']=identity['referenceType']!=corr['referenceType']
finding={'sourceCode':'X-42','sourceMessage':'Original failure','language':'en','severity':'ERROR'}
results['R08']=finding['sourceCode']=='X-42' and finding['sourceMessage']=='Original failure'
assessments=[{'state':'CLEARED','evidence':'receipt-1'},{'state':'CANCELLED','evidence':'receipt-2'}]
results['R09']=len(assessments)==2 and assessments[0]['evidence']=='receipt-1'
events=[ev('a','A','ACCEPTED'),ev('b','B','REJECTED')]
results['R10']=project(events)==project(list(reversed(events)))
output={'scope':'synthetic logical policy checks, not regulatory conformance','results':results,'passed':sum(results.values()),'total':len(results)}
Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
assert all(results.values())
