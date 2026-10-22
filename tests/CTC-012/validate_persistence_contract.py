import hashlib, json
from copy import deepcopy

def digest(b): return hashlib.sha256(b).hexdigest()

def validate(s):
    errors=[]
    artifacts=s.get('artifacts',{})
    for k,a in artifacts.items():
        if a.get('digest')!=digest(a.get('bytes','').encode()): errors.append('DIGEST_MISMATCH:'+k)
        if not a.get('algorithm') or not a.get('encoding'): errors.append('DIGEST_CONTEXT_MISSING:'+k)
    revs=s.get('revisions',{}); snaps=s.get('snapshots',{}); manifests=s.get('manifests',{}); attempts=s.get('attempts',{}); events=s.get('events',[])
    for k,r in revs.items():
        if r.get('frozen') is not True: errors.append('REVISION_MUTABLE:'+k)
        if r.get('tenant')!=s.get('tenant'): errors.append('CROSS_TENANT_REVISION:'+k)
    for k,m in manifests.items():
        for x in m.get('dependencies',[]):
            if x not in artifacts and x not in revs: errors.append('MISSING_INPUT:'+k+':'+x)
        if not m.get('profile_digest'): errors.append('UNPINNED_PROFILE:'+k)
    for k,t in snaps.items():
        if t.get('revision') not in revs: errors.append('MISSING_REVISION:'+k)
        if t.get('representation') not in artifacts: errors.append('MISSING_REPRESENTATION:'+k)
        if t.get('manifest') and t['manifest'] not in manifests: errors.append('MISSING_MANIFEST:'+k)
        if not t.get('frozen'): errors.append('SNAPSHOT_MUTABLE:'+k)
    for k,a in attempts.items():
        if a.get('snapshot') not in snaps: errors.append('MISSING_SNAPSHOT:'+k)
    for e in events:
        if e.get('kind')=='ENVELOPE_ACK' and e.get('legal_state')=='CLEARED': errors.append('ILLEGAL_CLEARANCE_INFERENCE')
        if e.get('correlation')=='AMBIGUOUS' and e.get('resolved'): errors.append('AMBIGUOUS_RESOLVED')
    if s.get('retention',{}).get('delete') and (s['retention'].get('legal_hold') or not s['retention'].get('policy_version')): errors.append('UNSAFE_RETENTION')
    if s.get('replay') and s['replay'].get('status')=='REPLAYABLE' and not s['replay'].get('all_dependencies_available'): errors.append('FALSE_REPLAYABILITY')
    if s.get('submitted_manifest') and s['submitted_manifest'].get('members')!=s['submitted_manifest'].get('pinned_members'): errors.append('ENVELOPE_MEMBER_MISMATCH')
    if s.get('source_fact_overwritten'): errors.append('SOURCE_FACT_OVERWRITE')
    if s.get('revision_overwritten'): errors.append('PUBLISHED_REVISION_OVERWRITE')
    return errors

base={'tenant':'tenantA','artifacts':{'source':{'bytes':'<Invoice/>','digest':digest(b'<Invoice/>'),'algorithm':'SHA-256','encoding':'UTF-8'},'out':{'bytes':'<Output/>','digest':digest(b'<Output/>'),'algorithm':'SHA-256','encoding':'UTF-8'}},'revisions':{'r1':{'tenant':'tenantA','frozen':True}},'manifests':{'m1':{'dependencies':['source','r1'],'profile_digest':'profile-sha'}},'snapshots':{'s1':{'revision':'r1','representation':'out','manifest':'m1','frozen':True}},'attempts':{'a1':{'snapshot':'s1'}},'events':[],'retention':{'delete':False},'replay':{'status':'REPLAYABLE','all_dependencies_available':True},'submitted_manifest':{'members':['s1'],'pinned_members':['s1']}}
cases=[]
def case(name, mutate, expected):
    obj=deepcopy(base);mutate(obj);errors=validate(obj); passed= expected in errors if expected else errors==[]
    cases.append({'scenario':name,'expected_error':expected,'observed_errors':errors,'passed':passed})
case('S01 immutable valid published snapshot',lambda x:None,None)
case('S02 altered original artifact digest',lambda x:x['artifacts']['source'].update(bytes='<Altered/>'),'DIGEST_MISMATCH:source')
case('S03 mutable published revision',lambda x:x['revisions']['r1'].update(frozen=False),'REVISION_MUTABLE:r1')
case('S04 missing interpretation dependency',lambda x:x['manifests']['m1']['dependencies'].append('absent'),'MISSING_INPUT:m1:absent')
case('S05 unpinned profile',lambda x:x['manifests']['m1'].update(profile_digest=''),'UNPINNED_PROFILE:m1')
case('S06 mutable submission snapshot',lambda x:x['snapshots']['s1'].update(frozen=False),'SNAPSHOT_MUTABLE:s1')
case('S07 envelope success cannot clear document',lambda x:x['events'].append({'kind':'ENVELOPE_ACK','legal_state':'CLEARED'}),'ILLEGAL_CLEARANCE_INFERENCE')
case('S08 ambiguous correlation not resolved',lambda x:x['events'].append({'kind':'AUTHORITY_RESPONSE','correlation':'AMBIGUOUS','resolved':True}),'AMBIGUOUS_RESOLVED')
case('S09 legal hold blocks deletion',lambda x:x['retention'].update(delete=True,legal_hold=True,policy_version='v1'),'UNSAFE_RETENTION')
case('S10 missing replay dependency',lambda x:x['replay'].update(all_dependencies_available=False),'FALSE_REPLAYABILITY')
case('S11 envelope manifest inconsistent',lambda x:x['submitted_manifest'].update(members=['s2']),'ENVELOPE_MEMBER_MISMATCH')
case('S12 source fact overwrite forbidden',lambda x:x.update(source_fact_overwritten=True),'SOURCE_FACT_OVERWRITE')
print(json.dumps({'total':len(cases),'passed':sum(c['passed'] for c in cases),'cases':cases},indent=2))
if not all(c['passed'] for c in cases): raise SystemExit(1)
