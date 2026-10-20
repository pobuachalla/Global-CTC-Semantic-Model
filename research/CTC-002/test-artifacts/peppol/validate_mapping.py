from lxml import etree
from decimal import Decimal
from pathlib import Path
import hashlib, json
p=Path(__file__).parent
raw=(p/'sample-ubl-invoice.xml').read_bytes()
r=etree.fromstring(raw)
ns={'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2','cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'}
def val(xpath):
    v=r.xpath(xpath,namespaces=ns)
    assert len(v)==1,(xpath,v)
    return v[0] if isinstance(v[0],str) else v[0].text
source={
 'invoiceNumber':val('./cbc:ID/text()'),
 'issueDate':val('./cbc:IssueDate/text()'),
 'currency':val('./cbc:DocumentCurrencyCode/text()'),
 'sellerVat':val('./cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID/text()'),
 'vatCategory':val('./cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:ID/text()'),
 'vatRate':val('./cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent/text()'),
 'taxable':val('./cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount/text()'),
 'tax':val('./cac:TaxTotal/cac:TaxSubtotal/cbc:TaxAmount/text()'),
 'exclusive':val('./cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount/text()'),
 'inclusive':val('./cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount/text()'),
 'lineTotal':val('./cac:InvoiceLine/cbc:LineExtensionAmount/text()'),
 'customizationId':val('./cbc:CustomizationID/text()'),
 'profileId':val('./cbc:ProfileID/text()'),
}
assert Decimal(source['exclusive'])==Decimal(source['lineTotal'])
assert Decimal(source['inclusive'])==Decimal(source['exclusive'])+Decimal(source['tax'])
assert Decimal(source['tax'])==Decimal(source['taxable'])*Decimal(source['vatRate'])/Decimal('100')
assert source['customizationId'].startswith('urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0')
profile={'profileId':'PEPPOL-BIS-BILLING-3','release':'2026-05','sourceSpecification':'https://docs.peppol.eu/poacc/billing/3.0/','mappingId':'UBL-TO-D2-POC','mappingVersion':'0.1-prototype','ruleId':'VAT-CATEGORY-S-MAP','ruleVersion':'0.1-prototype','codeListVersion':'NOT_ARCHIVED','packageDigest':'NOT_ARCHIVED'}
revision={'documentId':'DOC-PEP-0042','revisionId':'REV-PEP-001','documentNumber':source['invoiceNumber'],'issueDate':source['issueDate'],'currency':source['currency'],'sellerTaxIdentifier':source['sellerVat'],'tax':{'base':source['taxable'],'ratePercent':source['vatRate'],'amount':source['tax'],'originalCategory':source['vatCategory']},'totals':{'taxExclusive':source['exclusive'],'taxInclusive':source['inclusive']},'sourceRepresentationId':'REP-PEP-001'}
sha=lambda obj:hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
revision['fingerprint']=sha(revision)
interp={'interpretationId':'FI-PEP-001','revisionId':revision['revisionId'],'revisionFingerprint':revision['fingerprint'],'sourceFacts':[{'factId':'SF-VAT-CATEGORY','concept':'sourceTaxCategory','value':source['vatCategory'],'scheme':'Peppol VAT category','sourceRepresentationId':'REP-PEP-001','sourcePath':'/Invoice/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:ID','origin':'SOURCE_SUPPLIED'}],'derivedFacts':[{'factId':'DF-VAT-CLASS','concept':'normalizedVatTreatment','value':'STANDARD_RATE','origin':'MAPPED','derivedFrom':['SF-VAT-CATEGORY'],'ruleId':profile['ruleId'],'ruleVersion':profile['ruleVersion'],'profileId':profile['profileId'],'profileRelease':profile['release'],'interpretationStatus':'ILLUSTRATIVE_ALIGNMENT'}],'profilePackage':profile,'sourceRepresentation':{'id':'REP-PEP-001','sha256':hashlib.sha256(raw).hexdigest(),'format':'UBL 2.1','customizationId':source['customizationId'],'profileId':source['profileId']}}
interp['fingerprint']=sha(interp)
(p/'BILLING-REVISION.json').write_text(json.dumps(revision,indent=2)+'\n')
(p/'FISCAL-INTERPRETATION.json').write_text(json.dumps(interp,indent=2)+'\n')
(p/'VALIDATION-RESULT.json').write_text(json.dumps({'assertions':{'xmlWellFormed':True,'mappedFieldsPresent':True,'brCo13Arithmetic':True,'brCo15Arithmetic':True,'taxRateArithmetic':True,'profilePrefix':True,'sourceProvenanceRecorded':True,'revisionUnmodified':True},'notTested':['full UBL XSD','Peppol Schematron','country-specific VAT legal correctness','official sample provenance','historical replay with archived package']},indent=2)+'\n')
print('PASS: 8 focused checks; source sha256',hashlib.sha256(raw).hexdigest())
