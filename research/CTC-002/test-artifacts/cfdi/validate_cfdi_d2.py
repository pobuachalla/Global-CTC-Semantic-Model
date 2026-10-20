from pathlib import Path
from decimal import Decimal
import hashlib, json, xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
raw=(P/'cfdi40-constructed.xml').read_bytes()
root=ET.fromstring(raw)
ns={'cfdi':'http://www.sat.gob.mx/cfd/4'}
assert root.tag=='{http://www.sat.gob.mx/cfd/4}Comprobante'
assert root.get('Version')=='4.0'
emisor=root.find('cfdi:Emisor',ns); receptor=root.find('cfdi:Receptor',ns)
line=root.find('cfdi:Conceptos/cfdi:Concepto',ns)
lt=line.find('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado',ns)
summary=root.find('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado',ns)
assert all(x is not None for x in [emisor,receptor,line,lt,summary])
D=Decimal
assert D(root.get('SubTotal'))==D(line.get('Importe'))
assert D(lt.get('Base'))*D(lt.get('TasaOCuota'))==D(lt.get('Importe'))
assert D(root.get('Total'))==D(root.get('SubTotal'))+D(root.find('cfdi:Impuestos',ns).get('TotalImpuestosTrasladados'))
assert lt.get('Impuesto')==summary.get('Impuesto') and lt.get('Importe')==summary.get('Importe')
assert root.find('{http://www.sat.gob.mx/cfd/4}Complemento') is None
sha=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
source={'id':'REP-MX-001','syntax':'CFDI 4.0','sha256':hashlib.sha256(raw).hexdigest(),'verification':'CONSTRUCTED_UNSIGNED_UNCERTIFIED_DEMO'}
rev={'documentId':'DOC-MX-001','revisionId':'REV-MX-001','commercialIdentity':{'series':root.get('Serie'),'folio':root.get('Folio')},'issueDateTime':root.get('Fecha'),'currency':root.get('Moneda'),'sellerRfc':emisor.get('Rfc'),'buyerRfc':receptor.get('Rfc'),'tax':{'taxCode':lt.get('Impuesto'),'factor':lt.get('TipoFactor'),'rateFraction':lt.get('TasaOCuota'),'base':lt.get('Base'),'amount':lt.get('Importe')},'totals':{'net':root.get('SubTotal'),'gross':root.get('Total')},'sourceRepresentationId':source['id']}
rev['fingerprint']=sha(rev)
paths={'SF-MX-EMISOR-REG':'./cfdi:Emisor/@RegimenFiscal','SF-MX-RECEPTOR-REG':'./cfdi:Receptor/@RegimenFiscalReceptor','SF-MX-USO':'./cfdi:Receptor/@UsoCFDI','SF-MX-OBJETO':'./cfdi:Conceptos/cfdi:Concepto/@ObjetoImp','SF-MX-IMPUESTO':'./cfdi:Conceptos/cfdi:Concepto/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado/@Impuesto'}
values={'SF-MX-EMISOR-REG':emisor.get('RegimenFiscal'),'SF-MX-RECEPTOR-REG':receptor.get('RegimenFiscalReceptor'),'SF-MX-USO':receptor.get('UsoCFDI'),'SF-MX-OBJETO':line.get('ObjetoImp'),'SF-MX-IMPUESTO':lt.get('Impuesto')}
facts=[{'factId':k,'value':values[k],'scheme':'SAT CFDI 4.0 code list (release not archived)','origin':'SOURCE_SUPPLIED','sourceRepresentationId':source['id'],'sourcePath':paths[k]} for k in paths]
profile={'id':'MX-CFDI-4.0-POC','specification':'SAT Anexo 20 CFDI 4.0','mappingId':'CFDI-TO-D2-POC','mappingVersion':'0.1-demo','ruleId':'MX-002-TO-IVA','ruleVersion':'0.1-demo','codeListVersion':'NOT_ARCHIVED','packageDigest':'NOT_ARCHIVED'}
interp={'id':'FI-MX-001','revisionId':rev['revisionId'],'revisionFingerprint':rev['fingerprint'],'sourceFacts':facts,'derivedFacts':[{'factId':'DF-MX-IVA','concept':'normalizedTaxFamily','value':'IVA','origin':'MAPPED','inputFactIds':['SF-MX-IMPUESTO'],'ruleId':profile['ruleId'],'ruleVersion':profile['ruleVersion'],'profileId':profile['id'],'codeListVersion':profile['codeListVersion'],'confidence':'ILLUSTRATIVE_SEMANTIC_ALIGNMENT'}],'profilePackage':profile,'sourceRepresentation':source}
interp['fingerprint']=sha(interp)
assert interp['revisionFingerprint']==rev['fingerprint']
assert all(f['sourceRepresentationId']==source['id'] and f['sourcePath'] for f in facts)
assert interp['derivedFacts'][0]['inputFactIds'][0] in values
assert interp['derivedFacts'][0]['origin']!='SOURCE_SUPPLIED'
assert interp['profilePackage']['packageDigest']=='NOT_ARCHIVED'
for name,obj in [('BILLING-REVISION.json',rev),('FISCAL-INTERPRETATION.json',interp)]: (P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
result={'checks':{'xmlWellFormed':True,'namespaceAndVersion':True,'requiredNodesPresent':True,'lineAndDocumentNetReconcile':True,'lineTaxArithmetic':True,'documentGrossReconcile':True,'taxSummaryMatchesLine':True,'noTimbreBeforeCertification':True,'sourceFiscalCodesPreserved':True,'derivedFactProvenance':True,'immutableRevisionPinned':True,'profileArchiveGapFlagged':True},'sourceSha256':source['sha256'],'notTested':['SAT XSD full validation','SAT catalogs/conditional rules','PAC timbrado','cryptographic signatures','verified certified CFDI pair','historical replay with archived code lists']}
(P/'VALIDATION-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(result['checks']),'focused checks; SHA256',source['sha256'])
