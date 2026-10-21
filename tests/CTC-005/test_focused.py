import json, hashlib, copy
from pathlib import Path
ROOT=Path(__file__).parent
results=[]
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def check(name,condition):
    results.append({'test':name,'passed':bool(condition)})
    if not condition: raise AssertionError(name)

def package_valid(p):
    deps=p['dependencies']
    return p['digest']==digest({'profileId':p['profileId'],'version':p['version'],'dependencies':deps}) and all(k in deps and isinstance(deps[k],dict) and deps[k].get('contentDigest')==digest(deps[k].get('content')) for k in ('mapping','rules','codeLists'))

def make_pkg(version,code):
    deps={k:{'content':v} for k,v in {'mapping':{'A':code},'rules':['R1'],'codeLists':{'TAX':['A','B']}}.items()}
    for d in deps.values():d['contentDigest']=digest(d['content'])
    p={'profileId':'XX-DEMO','version':version,'dependencies':deps}
    p['digest']=digest(p)
    return p
p1=make_pkg('1.0','STANDARD'); p2=make_pkg('2.0','SPECIAL')
check('JP01 immutable package digest verified',package_valid(p1))
check('JP02 all mapping rule and code list digests pinned',all(p1['dependencies'][k]['contentDigest'] for k in ('mapping','rules','codeLists')))
tampered=copy.deepcopy(p1);tampered['dependencies']['rules']['content'].append('R2')
check('JP01/02 reject dependency tampering',not package_valid(tampered))
missing=copy.deepcopy(p1);del missing['dependencies']['codeLists']
check('JP02 reject missing dependency',not package_valid(missing))

REQUIRED={'namespace','owner','semanticConcept','valueType','applicability','provenancePolicy','testEvidence'}
def ext_valid(e):
    return REQUIRED<=e.keys() and all(e.get(k) for k in REQUIRED) and e['namespace'].startswith('jurisdiction.') and e['semanticConcept'] not in {'BillingDocument.documentId','PublishedRevision.issueDate'}
ext={'namespace':'jurisdiction.XX','owner':'team-XX','semanticConcept':'LocalTaxCategory','valueType':'CodedValue','applicability':{'country':'XX'},'provenancePolicy':'source-or-derived','testEvidence':['fixture-001']}
check('JP06 complete extension accepted',ext_valid(ext))
for k in ('namespace','owner','valueType','applicability','provenancePolicy','testEvidence'):
    bad=copy.deepcopy(ext);bad.pop(k)
    check('JP06 missing '+k+' rejected',not ext_valid(bad))

record={'sourceArtifact':'SRC-1','outboundArtifact':'OUT-1','profileValidation':'PASS','authorityResponse':None,'legalAssessment':'UNKNOWN'}
def legal_consistent(r):
    return bool(r.get('sourceArtifact') and r.get('outboundArtifact')) and (r.get('legalAssessment') in ('UNKNOWN','NOT_EVALUABLE') if not r.get('authorityResponse') else True)
check('JP08 validation pass without authority remains unknown',legal_consistent(record))
invalid=copy.deepcopy(record);invalid['legalAssessment']='CLEARED'
check('JP08 reject clearance inferred from validation',not legal_consistent(invalid))
check('JP08 require preserved source and outbound artifacts',not legal_consistent({**record,'outboundArtifact':None}))

release={'activeDigest':p1['digest'],'history':[{'digest':p1['digest'],'event':'PUBLISHED'}], 'interpretations':[{'id':'FI-1','profileDigest':p1['digest'],'result':'STANDARD'}]}
def promote(state,new,regression):
    if not package_valid(new) or not regression.get('passed') or not regression.get('evidenceRef') or not regression.get('rollbackTarget'): return False
    if regression['rollbackTarget']!=state['activeDigest']:return False
    state['history'].append({'digest':new['digest'],'event':'PROMOTED','rollbackTarget':state['activeDigest'],'evidenceRef':regression['evidenceRef']})
    state['activeDigest']=new['digest'];return True
before=copy.deepcopy(release['interpretations'])
check('JP09 reject promotion without regression evidence',not promote(release,p2,{'passed':True,'rollbackTarget':p1['digest']}))
check('JP09 valid promotion accepted',promote(release,p2,{'passed':True,'evidenceRef':'TEST-REG-1','rollbackTarget':p1['digest']}))
check('JP09 old interpretation pinned after promotion',release['interpretations']==before)
check('JP09 rollback target exists',any(h['digest']==release['history'][-1]['rollbackTarget'] for h in release['history']))
release['history'].append({'digest':p1['digest'],'event':'ROLLED_BACK','fromDigest':release['activeDigest']});release['activeDigest']=p1['digest']
check('JP09 rollback restores prior active digest',release['activeDigest']==p1['digest'])
check('JP09 rollback preserves historical interpretation',release['interpretations']==before)

summary={'passed':sum(x['passed'] for x in results),'total':len(results),'tests':results,'limitations':['Synthetic in-memory governance checks','No durable archival, signature verification, or real profile registry','No legal/regulatory conformance validation']}
(ROOT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(f"{summary['passed']}/{summary['total']} passed")
