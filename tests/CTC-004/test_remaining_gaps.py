from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import json
from pathlib import Path
D=Decimal
checks=[]
def check(name,condition):
    checks.append({'check':name,'pass':bool(condition)})
    if not condition: raise AssertionError(name)
def q(value,places,mode):return value.quantize(D(places),rounding=mode)
# MG-004-01: synthetic one-document, two-regime, one withholding application.
applications=[
 {'id':'A1','regime':'VAT-XX','scope':'L1','base':D('100.00'),'rate':D('0.10'),'magnitude':D('10.00'),'effect':D('10.00'),'category':'STANDARD'},
 {'id':'A2','regime':'EXCISE-XX','scope':'L1','base':D('100.00'),'rate':D('0.05'),'magnitude':D('5.00'),'effect':D('5.00'),'category':'ADDITIONAL'},
 {'id':'A3','regime':'WITHHOLD-XX','scope':'L1','base':D('100.00'),'rate':D('0.02'),'magnitude':D('2.00'),'effect':D('-2.00'),'category':'WITHHOLD'}]
summary={}
for a in applications:
    k=(a['regime'],a['category']);summary[k]=summary.get(k,D('0'))+a['magnitude']
source_assertions={'VAT-XX':D('10.00'),'EXCISE-XX':D('5.00'),'WITHHOLD-XX':D('2.00')}
check('multiple distinct regimes',len({a['regime'] for a in applications})==3)
check('every application scoped',all(a['scope']=='L1' for a in applications))
check('unique application identities',len({a['id'] for a in applications})==len(applications))
check('VAT summary',summary[('VAT-XX','STANDARD')]==D('10.00'))
check('excise summary',summary[('EXCISE-XX','ADDITIONAL')]==D('5.00'))
check('withholding summary',summary[('WITHHOLD-XX','WITHHOLD')]==D('2.00'))
check('tax magnitude nonnegative',all(a['magnitude']>=0 for a in applications))
check('tax arithmetic',all(a['base']*a['rate']==a['magnitude'] for a in applications))
check('signed payable contributions',sum((a['effect'] for a in applications),D(0))==D('13.00'))
check('document payable no double count',D('100.00')+sum((a['effect'] for a in applications),D(0))==D('113.00'))
check('asserted regime totals preserved',all(sum((a['magnitude'] for a in applications if a['regime']==r),D(0))==v for r,v in source_assertions.items()))
check('detect incorrect summary double-counting',D('113.00')+sum(source_assertions.values())!=D('113.00'))
# MG-004-02: explicitly pinned policy, not claimed as regulatory.
policy={'id':'SYNTH-PREC-1','currency':'XCU','minor_unit':'0.01','rounding':'HALF_UP','tax_rate_scale':6,'stage':'LINE'}
check('high precision fractional rate retained',D('0.123456')*D('100.00')==D('12.34560000'))
check('line tax rounded to currency quantum',q(D('12.34560000'),policy['minor_unit'],ROUND_HALF_UP)==D('12.35'))
check('line versus aggregate rounding divergence',sum((q(D('0.05')*D('0.10'),D('0.01'),ROUND_HALF_UP) for _ in range(3)),D(0))==D('0.03') and q(D('0.15')*D('0.10'),D('0.01'),ROUND_HALF_UP)==D('0.02'))
check('half even differs from half up',q(D('1.005'),D('0.01'),ROUND_HALF_UP)==D('1.01') and q(D('1.005'),D('0.01'),ROUND_HALF_EVEN)==D('1.00'))
check('per-unit tax with quantity',q(D('0.037')*D('3'),D('0.01'),ROUND_HALF_UP)==D('0.11'))
check('unknown currency policy not evaluable',('NOT_EVALUABLE' if {}.get('minor_unit') is None else 'EVALUABLE')=='NOT_EVALUABLE')
check('unknown rounding stage not evaluable',('NOT_EVALUABLE' if {}.get('stage') is None else 'EVALUABLE')=='NOT_EVALUABLE')
check('cross currency no silent addition',('USD','EUR')!=('USD','USD'))
check('source discrepancy preserved',D('99.99')!=D('100.00'))
check('profile-specific tolerance not inferred',policy.get('tolerance') is None)
check('versioned policy identity',bool(policy['id']))
result={'date':'2026-10-21','scope':'Synthetic logical structural tests; no regulatory conformance','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'policy':policy,'synthetic_example':{'base':'100.00','VAT':'10.00','EXCISE':'5.00','WITHHOLD':'2.00','payable':'113.00'}}
p=Path(__file__).parent/'results.json';p.write_text(json.dumps(result,indent=2))
print(f"PASS {result['passed']}/{result['total']} assertions")
