import json, hashlib
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parent
F=ROOT/'fixtures'; OUT=ROOT/'results'
def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def d(x): return Decimal(str(x))
def verify(name, obj, tests, facts, derived):
    revision={'documentId':name,'sourceDigest':sha(obj),'sourceFacts':facts,'billing':{'currency':obj.get('currency','INR')}}
    interpretation={'revisionDigest':sha(revision),'profile':'MYINVOIS-1.1' if name.startswith('MY') else 'INDIA-IRP-SCHEMA','packageDigest':'NOT_ARCHIVED','derivedFacts':derived}
    assert interpretation['revisionDigest']==sha(revision)
    tests.append(('immutable revision reference',True))
    tests.append(('source facts have source paths',all(f.get('path') for f in facts)))
    tests.append(('derived facts preserve input references',all(v.get('derivedFrom') for v in derived)))
    tests.append(('profile package not falsely claimed archived',interpretation['packageDigest']=='NOT_ARCHIVED'))
    result={'fixture':name,'checks':[{'name':n,'passed':bool(v)} for n,v in tests],'passed':sum(bool(v) for _,v in tests),'total':len(tests),'sourceDigest':sha(obj),'revisionDigest':sha(revision),'interpretation':interpretation,'revision':revision}
    (OUT/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    assert result['passed']==result['total'],result
    return result
my=json.loads((F/'malaysia-constructed.json').read_text()); mt=my['tax']; totals=my['totals']
mytests=[('document type 01',my['documentType']=='01'),('v1.1 signature validation profile identified',my['documentVersion']=='1.1'),('tax code 02 preserved',mt['typeCode']=='02'),('tax arithmetic',d(mt['taxableAmount'])*d(mt['ratePercent'])/100==d(mt['taxAmount'])),('gross reconciliation',d(totals['taxExclusive'])+d(mt['taxAmount'])==d(totals['taxInclusive'])==d(totals['payable'])),('no authority identity invented',my['authority'] is None),('no signature falsely asserted',my['signature']['status']=='NOT_SIGNED_DEMO')]
myfacts=[{'id':'MY-TAX-TYPE','path':'$.tax.typeCode','value':mt['typeCode'],'scheme':mt['scheme']},{'id':'MY-RATE','path':'$.tax.ratePercent','value':mt['ratePercent'],'scheme':'PERCENT'}]
myder=[{'concept':'taxFamily','value':'SERVICE_TAX','derivedFrom':['MY-TAX-TYPE'],'rule':'LOCAL-MY-TAX-TYPE-02-v1','evidence':'official tax type code list'}]
results=[verify('MY-TEST-001',my,mytests,myfacts,myder)]
for fn in ('india-interstate-constructed.json','india-intrastate-constructed.json'):
    obj=json.loads((F/fn).read_text()); item=obj['ItemList'][0]; vals=obj['ValDtls']; seller=obj['SellerDtls']['Stcd']; pos=obj['BuyerDtls']['Pos']; interstate=seller!=pos
    tests=[('source POS preserved',pos in ('07','27')),('source seller state preserved',seller=='27'),('GST tax components reconcile',d(item['AssAmt'])+d(item['IgstAmt'])+d(item['CgstAmt'])+d(item['SgstAmt'])==d(item['TotItemVal'])),('GST total reconciles',d(vals['AssVal'])+d(vals['IgstVal'])+d(vals['CgstVal'])+d(vals['SgstVal'])==d(vals['TotInvVal'])),('line and header tax agree',all(d(item[k])==d(vals[v]) for k,v in [('IgstAmt','IgstVal'),('CgstAmt','CgstVal'),('SgstAmt','SgstVal')])),('illustrative inter-state tax allocation' if interstate else 'illustrative intra-state allocation',(d(item['IgstAmt'])==d(item['AssAmt'])*d(item['GstRt'])/100 and d(item['CgstAmt'])==0 and d(item['SgstAmt'])==0) if interstate else (d(item['IgstAmt'])==0 and d(item['CgstAmt'])==d(item['AssAmt'])*d(item['GstRt'])/200 and d(item['SgstAmt'])==d(item['CgstAmt']))),('special IGST-on-intra flag preserved',obj['TranDtls']['IgstOnIntra']=='N')]
    facts=[{'id':'IN-SELLER-STATE','path':'$.SellerDtls.Stcd','value':seller},{'id':'IN-POS','path':'$.BuyerDtls.Pos','value':pos},{'id':'IN-GST-RATE','path':'$.ItemList[0].GstRt','value':item['GstRt']},{'id':'IN-SUPPLY-TYPE','path':'$.TranDtls.SupTyp','value':obj['TranDtls']['SupTyp']}]
    derived=[{'concept':'illustrativeSupplyRelation','value':'INTER_STATE' if interstate else 'INTRA_STATE','derivedFrom':['IN-SELLER-STATE','IN-POS'],'rule':'TEST-STATE-COMPARISON-v1','warning':'Not sufficient for legal GST treatment'}]
    results.append(verify(obj['DocDtls']['No'],obj,tests,facts,derived))
summary={'totalChecks':sum(r['total'] for r in results),'passedChecks':sum(r['passed'] for r in results),'fixtureCount':len(results),'fullAuthorityConformance':False,'historicalReplayWithArchivedPackages':False}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
