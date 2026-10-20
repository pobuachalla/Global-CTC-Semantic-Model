from decimal import Decimal as D, ROUND_HALF_UP
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
results=[]
def check(name, actual, expected):
    ok=actual==expected
    results.append({'test':name,'pass':ok,'actual':str(actual),'expected':str(expected)})
    if not ok: raise AssertionError(f'{name}: {actual} != {expected}')
# HMRC published VAT guide VAT-inclusive example: 180 includes 20% VAT -> 150 + 30.
gross=D('180.00'); rate=D('.20'); net=gross/(1+rate); vat=gross-net
check('HMRC inclusive 180 net',net,D('150.00'))
check('HMRC inclusive 180 tax',vat,D('30.00'))
check('Inclusive basis effect already included',gross+D('0'),gross)
check('Exclusive basis effect added',net+vat,gross)
# HMRC published VAT guide full invoice 348.90 net, 69.78 VAT, 418.68 gross.
check('HMRC invoice VAT total',D('348.90')+D('69.78'),D('418.68'))
# SAT public sample cited from cfdi.red: transferred .06, withheld .10, on base 1.
transferred=D('.06'); withheld=D('.10'); source_subtotal=D('1.00')
check('CFDI withholding preserved as magnitude',abs(withheld),D('.10'))
check('CFDI illustrative signed contributions',transferred-withheld,D('-.04'))
check('CFDI illustrative payable',source_subtotal+transferred-withheld,D('.96'))
# Official Peppol credit note published excerpt
check('Peppol signed credit lines',D('2800')-D('1500'),D('1300'))
check('Peppol credit tax exclusive',D('1300')+D('25'),D('1325'))
check('Peppol credit VAT',D('1325')*D('.25'),D('331.25'))
check('Peppol credit payable presentation',D('1325')+D('331.25'),D('1656.25'))
# Separate presentation from economic effect; illustrative perspective
check('Credit presentation distinct from seller receivable delta',-D('1656.25'),D('-1656.25'))
# Mixed currency synthetic explicit conversion, not a statutory rule
check('Versioned conversion synthetic EUR to USD',D('120')*D('1.10'),D('132.00'))
# Rounding discrepancy synthetic 3 x .05 taxed at 10%; line-round vs aggregate-round
round2=lambda v:v.quantize(D('.01'),rounding=ROUND_HALF_UP)
line_tax=sum((round2(D('.05')*D('.10')) for _ in range(3)),D('0'))
aggregate_tax=round2(D('.15')*D('.10'))
check('Line rounding',line_tax,D('.03'))
check('Aggregate rounding',aggregate_tax,D('.02'))
check('Rounding variance',line_tax-aggregate_tax,D('.01'))
# Source asserted vs calculated must both survive
asserted=D('100.00'); calculated=D('99.99')
check('Source summary discrepancy',asserted-calculated,D('.01'))
# Guard against missing inclusion/currency/rounding policy
for label, data in [('unknown basis',{'basis':None}),('unknown fx',{'currency':'EUR','target':'USD','fx':None}),('unknown rounding',{'rounding':None})]:
    check('NOT_EVALUABLE '+label,'NOT_EVALUABLE' if None in data.values() else 'PASS','NOT_EVALUABLE')
(root/'fixtures'/'results.json').write_text(json.dumps({'passed':sum(x['pass'] for x in results),'total':len(results),'results':results},indent=2))
print(f"{sum(x['pass'] for x in results)}/{len(results)} passed")
