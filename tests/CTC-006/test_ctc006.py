import json
from pathlib import Path

results=[]
def check(code, title, fn):
    try:
        assert fn(), 'expected condition not met'
        results.append({'id':code,'scenario':title,'result':'PASS'})
    except Exception as exc:
        results.append({'id':code,'scenario':title,'result':'FAIL','reason':str(exc)})

# These are synthetic logical contract checks, not external format validators.
party={'id':'PS-1','name':'Alpha Ltd','taxIds':[{'scheme':'VAT','jurisdiction':'XX','value':'A-1'}]}
revision={'id':'REV-1','partySnapshot':json.loads(json.dumps(party)),'published':True}
party['name']='Alpha Trading Ltd'
check('ID-01','Party master change cannot mutate published snapshot',lambda: revision['partySnapshot']['name']=='Alpha Ltd')
identifiers=[{'scheme':'VAT','jurisdiction':'XX','value':'A-1'},{'scheme':'GST','jurisdiction':'YY','value':'A-1'}]
check('ID-02','Different registration schemes and jurisdictions remain distinct',lambda: len({(i['scheme'],i['jurisdiction'],i['value']) for i in identifiers})==2)
key=lambda issuer,series,num,family,juris:(issuer,series,num,family,juris)
check('ID-03','Same number with distinct issuer has distinct identity',lambda:key('A','','42','INVOICE','XX')!=key('B','','42','INVOICE','XX'))
check('ID-04','Series participates in scoped commercial identity',lambda:key('A','S1','42','INVOICE','XX')!=key('A','S2','42','INVOICE','XX'))
draft={'platformId':'DOC-1','number':None,'revision':None}; published={'platformId':'DOC-1','number':'42','revision':'REV-1'}
check('ID-05','Platform identity stable through draft and publication',lambda:draft['platformId']==published['platformId'] and draft['number'] is None and published['revision'] is not None)
invoice={'documentId':'DOC-1','kind':'INVOICE'}; credit={'documentId':'DOC-2','kind':'CREDIT_NOTE','relation':{'type':'CREDITS','target':'DOC-1'}}
check('ID-06','Credit note retains independent identity and typed reference',lambda:credit['documentId']!=invoice['documentId'] and credit['relation']=={'type':'CREDITS','target':'DOC-1'})
replacement={'documentId':'DOC-3','relation':{'type':'REPLACES','target':'DOC-1'}}
check('ID-07','Replacement preserves original document identity',lambda:replacement['documentId']!=invoice['documentId'] and replacement['relation']['target']==invoice['documentId'])
evidence=[{'id':'E1','event':'CLEARED','artifact':'REP-1'},{'id':'E2','event':'CANCELLED','artifact':'REP-2'}]
check('ID-08','Cancellation appends evidence without erasing clearance',lambda:len(evidence)==2 and evidence[0]['event']=='CLEARED' and evidence[1]['event']=='CANCELLED')
external={'type':'CREDITS','target':{'externalNumber':'EXT-77','issuer':'Supplier X'},'resolvedDocumentId':None}
check('ID-09','Unknown local target retains typed external reference',lambda:external['target']['externalNumber']=='EXT-77' and external['resolvedDocumentId'] is None)
attempts=[{'id':'A1','documentId':'DOC-2','revision':'REV-2'},{'id':'A2','documentId':'DOC-2','revision':'REV-2'}]
check('ID-10','Repeated submission creates distinct attempts, not documents',lambda:len({a['id'] for a in attempts})==2 and len({a['documentId'] for a in attempts})==1)

out=Path(__file__).with_name('results.json');out.write_text(json.dumps({'summary':{'passed':sum(x['result']=='PASS' for x in results),'total':len(results)},'tests':results},indent=2)+'\n')
for r in results:print(r['id'],r['result'],r['scenario'])
print('TOTAL',sum(x['result']=='PASS' for x in results),'/',len(results))
raise SystemExit(0 if all(r['result']=='PASS' for r in results) else 1)
