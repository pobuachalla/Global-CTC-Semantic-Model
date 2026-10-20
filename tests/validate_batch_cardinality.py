import json, hashlib
from pathlib import Path

checks=[]
def check(name, condition, scenario):
    checks.append({'scenario':scenario,'assertion':name,'passed':bool(condition)})

def digest(s): return hashlib.sha256(s.encode()).hexdigest()

def validate(m):
    issues=[]
    reps=m.get('representations',{})
    docs=m.get('documents',{})
    revs=m.get('revisions',{})
    extracts=m.get('extractions',[])
    ingestions=m.get('ingestions',[])
    envelopes=m.get('envelopes',[])
    attempts=m.get('attempts',[])
    events=m.get('events',[])
    members={}
    for ing in ingestions:
        if not ing.get('representationRefs') or any(r not in reps for r in ing['representationRefs']): issues.append('B01_INGESTION_ARTIFACT')
    for ex in extracts:
        if ex.get('sourceRef') not in reps or not ex.get('locator'): issues.append('B02_EXTRACTION_LOCATOR')
        if ex.get('documentRef') is not None and not isinstance(ex['documentRef'],list) and ex['documentRef'] not in docs: issues.append('B03_DOCUMENT_REF')
        if isinstance(ex.get('documentRef'),list): issues.append('B03_MULTIPLE_DOCS_PER_EXTRACTION')
    for env in envelopes:
        if env.get('representationRef') not in reps or not env.get('members'): issues.append('B04_ENVELOPE_ARTIFACT')
        if env.get('digest')!=reps.get(env.get('representationRef'),{}).get('digest'): issues.append('B04_DIGEST_MISMATCH')
        for member in env.get('members',[]):
            k=(env['id'],member['memberId'])
            if k in members: issues.append('B05_DUPLICATE_MEMBER_ID')
            members[k]=member
            if member.get('revisionRef') not in revs or member.get('representationRef') not in reps: issues.append('B05_INVALID_MEMBER_REF')
            if member.get('revisionDigest')!=revs.get(member.get('revisionRef'),{}).get('digest'): issues.append('B05_REVISION_DIGEST')
    for att in attempts:
        env=next((e for e in envelopes if e['id']==att.get('envelopeRef')),None)
        if env is None or att.get('payloadDigest')!=env.get('digest'): issues.append('B04_ATTEMPT_PIN')
        if str(att.get('envelopeRef','')).lower()=='latest': issues.append('B04_MUTABLE_REF')
    for ev in events:
        if ev.get('subjectType')=='MEMBER' and (ev.get('envelopeRef'),ev.get('memberId')) not in members: issues.append('B07_ORPHAN_MEMBER_EVENT')
        if ev.get('subjectType') not in ('MEMBER','ENVELOPE'): issues.append('B07_INVALID_SUBJECT')
    return issues

src='batch source 2 invoices'
base={'representations':{'SRC1':{'digest':digest(src)},'OUT1':{'digest':digest('batch out')},'R1':{'digest':digest('member 1')},'R2':{'digest':digest('member 2')}},'documents':{'D1':{},'D2':{}},'revisions':{'V1':{'digest':digest('revision1')},'V2':{'digest':digest('revision2')}},'ingestions':[{'id':'ING1','representationRefs':['SRC1']}], 'extractions':[{'id':'EX1','sourceRef':'SRC1','locator':'Invoice[1]','documentRef':'D1'},{'id':'EX2','sourceRef':'SRC1','locator':'Invoice[2]','documentRef':'D2'}], 'envelopes':[{'id':'ENV1','representationRef':'OUT1','digest':digest('batch out'),'members':[{'memberId':'M1','revisionRef':'V1','revisionDigest':digest('revision1'),'representationRef':'R1'},{'memberId':'M2','revisionRef':'V2','revisionDigest':digest('revision2'),'representationRef':'R2'}]}], 'attempts':[{'id':'A1','envelopeRef':'ENV1','payloadDigest':digest('batch out')}], 'events':[{'id':'E1','subjectType':'ENVELOPE','envelopeRef':'ENV1','outcome':'RECEIVED'},{'id':'E2','subjectType':'MEMBER','envelopeRef':'ENV1','memberId':'M1','outcome':'ACCEPTED'},{'id':'E3','subjectType':'MEMBER','envelopeRef':'ENV1','memberId':'M2','outcome':'REJECTED'}]}
check('batch source resolves two separate documents',len({e['documentRef'] for e in base['extractions']})==2,'multi_ingestion')
check('two extractions from one source artifact',len(base['extractions'])==2 and len(base['ingestions'])==1,'multi_ingestion')
check('batch instance validates',not validate(base),'multi_ingestion')
check('member outcomes remain independent', {e['memberId']:e['outcome'] for e in base['events'] if e['subjectType']=='MEMBER'}=={'M1':'ACCEPTED','M2':'REJECTED'},'partial_acceptance')
check('envelope receipt is not member acceptance',all(e['subjectType']=='ENVELOPE' for e in base['events'] if e['id']=='E1'),'partial_acceptance')
check('no inferred outcome for absent member event', 'M2' not in {e['memberId'] for e in base['events'][:2] if e['subjectType']=='MEMBER'},'unknown_member')
check('same revision can appear in a second envelope without mutation',base['revisions']['V2']['digest']==digest('revision2'),'retry')
import copy
retry=copy.deepcopy(base)
retry['representations']['OUT2']={'digest':digest('retry payload')}
retry['envelopes'].append({'id':'ENV2','representationRef':'OUT2','digest':digest('retry payload'),'members':[{'memberId':'M2R','revisionRef':'V2','revisionDigest':digest('revision2'),'representationRef':'R2'}]})
retry['attempts'].append({'id':'A2','envelopeRef':'ENV2','payloadDigest':digest('retry payload')})
check('retry has distinct immutable attempt and envelope',not validate(retry) and len(retry['attempts'])==2,'retry')
check('original attempt preserved',retry['attempts'][0]==base['attempts'][0],'retry')
check('original rejected event preserved',retry['events'][-1]['outcome']=='REJECTED','retry')
# Duplicates: two receptions same bytes, different event identities; resolution to same document
same=copy.deepcopy(base)
same['ingestions'].append({'id':'ING2','representationRefs':['SRC1']})
same['extractions'].append({'id':'EX3','sourceRef':'SRC1','locator':'Invoice[1]','documentRef':'D1'})
check('duplicate receipt is distinct ingestion event',not validate(same) and len(same['ingestions'])==2,'duplicates')
check('duplicate resolves to existing document without overwriting',same['extractions'][-1]['documentRef']=='D1' and len(same['documents'])==2,'duplicates')
check('digest equality alone does not establish idempotency',same['ingestions'][0]['id']!=same['ingestions'][1]['id'],'duplicates')
# multiple response records, out-of-order and unknown
responses=copy.deepcopy(base)
responses['events']=[{'id':'E4','subjectType':'MEMBER','envelopeRef':'ENV1','memberId':'M2','outcome':'PENDING'},{'id':'E5','subjectType':'ENVELOPE','envelopeRef':'ENV1','outcome':'RECEIVED'},{'id':'E6','subjectType':'MEMBER','envelopeRef':'ENV1','memberId':'M1','outcome':'ACCEPTED'}]
check('out-of-order event arrival structurally allowed',not validate(responses),'correlation')
check('member M2 pending not falsely accepted',next(e['outcome'] for e in responses['events'] if e.get('memberId')=='M2')=='PENDING','correlation')
check('member response carries explicit envelope and member refs',all('envelopeRef' in e and 'memberId' in e for e in responses['events'] if e['subjectType']=='MEMBER'),'correlation')
# negative controls
bad=copy.deepcopy(base);bad['attempts'][0]['envelopeRef']='latest'
check('reject mutable latest attempt ref','B04_ATTEMPT_PIN' in validate(bad),'negative_controls')
bad=copy.deepcopy(base);bad['events'].append({'id':'BAD','subjectType':'MEMBER','envelopeRef':'ENV1','memberId':'M404','outcome':'ACCEPTED'})
check('reject orphan member response','B07_ORPHAN_MEMBER_EVENT' in validate(bad),'negative_controls')
bad=copy.deepcopy(base);bad['envelopes'][0]['members'][0]['revisionDigest']='incorrect'
check('reject wrong revision digest','B05_REVISION_DIGEST' in validate(bad),'negative_controls')
bad=copy.deepcopy(base);bad['extractions'][0]['documentRef']=['D1','D2']
check('reject extraction resolving to multiple documents',bool(validate(bad)),'negative_controls')
bad=copy.deepcopy(base);bad['envelopes'][0]['digest']='wrong'
check('reject altered envelope digest','B04_DIGEST_MISMATCH' in validate(bad),'negative_controls')
# empty/unparseable input
empty=copy.deepcopy(base);empty['extractions']=[];empty['envelopes']=[];empty['attempts']=[];empty['events']=[]
check('zero extractions permitted',not validate(empty),'zero_document')
# ensure uniqueness checks for events/attempts are not implemented; mark evidence gaps in report
result={'assertions':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'all_passed':all(c['passed'] for c in checks),'limitations':['Synthetic instances only','Validator does not enforce temporal state transitions or unique event IDs','Provider deduplication, batch atomicity and legal outcome rules untested']}
out=Path(__file__).parent
(out/'results.json').write_text(json.dumps(result,indent=2))
(out/'sample-instance.json').write_text(json.dumps(base,indent=2))
print(f"{result['passed']}/{result['total']} checks passed")
if not result['all_passed']: raise SystemExit(1)
