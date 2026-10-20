"""CTC-003 Draft 1.2 synthetic logical cardinality checks. No jurisdiction conformance."""
import json
from pathlib import Path

class Invalid(Exception): pass

def check(x):
    docs={d['id']:d for d in x.get('documents',[])}
    revs={r['id']:r for r in x.get('revisions',[])}
    parties={p['id']:p for p in x.get('partySnapshots',[])}
    interps={i['id']:i for i in x.get('interpretations',[])}
    events={e['id']:e for e in x.get('events',[])}
    assessments=x.get('legalAssessments',[])
    for r in revs.values():
        if r['documentId'] not in docs: raise Invalid('orphan revision')
        if r.get('published') and not r.get('digest'): raise Invalid('published revision missing digest')
        for participation in r.get('participations',[]):
            if participation['snapshotId'] not in parties:raise Invalid('unresolved party snapshot')
            if r.get('published') and not parties[participation['snapshotId']].get('immutable'):raise Invalid('published party mutable')
    for i in interps.values():
        if i['revisionId'] not in revs:raise Invalid('orphan interpretation')
        if not i.get('manifestDigest') or not i.get('profileDigest'):raise Invalid('unreproducible interpretation')
    for a in assessments:
        if a['revisionId'] not in revs:raise Invalid('orphan legal assessment')
        if a.get('outcome') in ('ISSUED','CANCELLED','REJECTED') and not a.get('evidenceIds'):raise Invalid('unsupported legal determination')
    for e in events.values():
        if not e.get('subjectType') or not e.get('subjectId'):raise Invalid('untyped event')
    for p in x.get('profileChecks',[]):
        if p['revisionId'] not in revs:raise Invalid('orphan profile check')
        if p['requiredSeller'] and not any(y.get('role')=='SELLER' for y in revs[p['revisionId']].get('participations',[])):raise Invalid('profile seller missing')
        if p['requiredLine'] and not revs[p['revisionId']].get('lines'):raise Invalid('profile line missing')
    return True

base={
 'documents':[{'id':'DOC-1'},{'id':'DOC-2'}],
 'revisions':[{'id':'REV-1','documentId':'DOC-1','published':True,'digest':'hash-1','participations':[{'role':'SELLER','snapshotId':'P-1'},{'role':'BUYER','snapshotId':'P-2'}],'lines':['L1']},{'id':'REV-2','documentId':'DOC-2','published':True,'digest':'hash-2','participations':[],'lines':[]}],
 'partySnapshots':[{'id':'P-1','immutable':True},{'id':'P-2','immutable':True}],
 'interpretations':[{'id':'FI-1','revisionId':'REV-1','manifestDigest':'m1','profileDigest':'p1'},{'id':'FI-2','revisionId':'REV-1','manifestDigest':'m1','profileDigest':'p2'}],
 'legalAssessments':[{'revisionId':'REV-1','outcome':'UNDETERMINED','evidenceIds':[]}],
 'events':[{'id':'E-1','subjectType':'COMPLIANCE_TRANSACTION','subjectId':'CT-1'}],
 'profileChecks':[{'revisionId':'REV-1','requiredSeller':True,'requiredLine':True}]
}
from copy import deepcopy
cases=[]
def add(name,change,valid):
 x=deepcopy(base);change(x)
 try:check(x);result=True
 except Invalid:result=False
 cases.append({'name':name,'expected':valid,'observed':result,'pass':valid==result})
add('baseline published invoice',lambda x:None,True)
add('draft document without revision',lambda x:x['documents'].append({'id':'DOC-3'}),True)
add('published invoice missing digest',lambda x:x['revisions'][0].pop('digest'),False)
add('orphan revision',lambda x:x['revisions'][0].update(documentId='DOC-X'),False)
add('published mutable party snapshot',lambda x:x['partySnapshots'][0].update(immutable=False),False)
add('orphan party snapshot',lambda x:x['revisions'][0]['participations'][0].update(snapshotId='P-X'),False)
add('multiple interpretations of one revision',lambda x:x['interpretations'].append({'id':'FI-3','revisionId':'REV-1','manifestDigest':'m1','profileDigest':'p3'}),True)
add('interpretation missing manifest',lambda x:x['interpretations'][0].pop('manifestDigest'),False)
add('interpretation missing profile',lambda x:x['interpretations'][0].pop('profileDigest'),False)
add('orphan interpretation',lambda x:x['interpretations'][0].update(revisionId='REV-X'),False)
add('undetermined legal state without evidence',lambda x:None,True)
add('issued state without evidence',lambda x:x['legalAssessments'][0].update(outcome='ISSUED'),False)
add('issued state with evidence',lambda x:x['legalAssessments'][0].update(outcome='ISSUED',evidenceIds=['EV-1']),True)
add('multiple legal assessments',lambda x:x['legalAssessments'].append({'revisionId':'REV-1','outcome':'ISSUED','evidenceIds':['EV-1']}),True)
add('event missing typed subject',lambda x:x['events'][0].pop('subjectType'),False)
add('multiple events',lambda x:x['events'].append({'id':'E-2','subjectType':'SUBMISSION_ATTEMPT','subjectId':'ATT-1'}),True)
add('published credit-note no line globally',lambda x:None,True)
add('profile requires missing line',lambda x:x['profileChecks'].append({'revisionId':'REV-2','requiredSeller':False,'requiredLine':True}),False)
add('profile requires missing seller',lambda x:x['profileChecks'].append({'revisionId':'REV-2','requiredSeller':True,'requiredLine':False}),False)
add('profile allows sparse document',lambda x:x['profileChecks'].append({'revisionId':'REV-2','requiredSeller':False,'requiredLine':False}),True)
add('cancelled state without evidence',lambda x:x['legalAssessments'][0].update(outcome='CANCELLED'),False)
add('rejected state with evidence',lambda x:x['legalAssessments'][0].update(outcome='REJECTED',evidenceIds=['EV-2']),True)
assert all(c['pass'] for c in cases)
result={'suite':'CTC-003 Draft 1.2 synthetic cardinality','total':len(cases),'passed':sum(c['pass'] for c in cases),'cases':cases,'limits':'Only local structural invariants; no official payloads, legal profiles, or external response validation.'}
Path(__file__).with_name('ctc003_draft12_results.json').write_text(json.dumps(result,indent=2))
print(f"{result['passed']}/{result['total']} synthetic assertions passed")
