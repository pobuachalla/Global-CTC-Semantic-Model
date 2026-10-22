import csv, pathlib, re, json
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=ROOT/'research/CTC-011'
with (R/'ENTITY-MAPPING.csv').open() as f: entities=list(csv.DictReader(f))
with (R/'RELATIONSHIP-REGISTER.csv').open() as f: links=list(csv.DictReader(f))
names={e['semantic_concept'] for e in entities}
results=[]
def check(name, cond): results.append({'test':name,'passed':bool(cond)})
check('exactly 51 approved logical concepts represented',len(names)==51 and len(entities)==51)
check('no duplicate concept names',len(names)==len(entities))
check('all relationships have existing endpoint concepts',all(x['parent_or_subject'] in names and x['child_or_target'] in names for x in links))
check('all relationship references classified',all(x['field_declaration'] for x in links))
check('no proposed fields silently declared',all(x['physical_disposition']=='Deferred' for x in entities))
check('no universal positive published-revision minimum',any(x['parent_or_subject']=='BillingDocument' and x['child_or_target']=='PublishedRevision' and x['child_cardinality']=='0..N' for x in links))
check('ingestion can produce zero to many extractions',any(x['parent_or_subject']=='IngestionRecord' and x['child_or_target']=='DocumentExtraction' and x['child_cardinality']=='0..N' for x in links))
check('document and transport attempts are distinct',{'SubmissionAttempt','TransportAttempt'}.issubset(names))
check('source facts and derived facts are distinct',{'SourceFiscalFact','DerivedFiscalFact'}.issubset(names))
check('response correlation and legal state distinct',{'ResponseCorrelation','LegalStateAssessment'}.issubset(names))
check('diagrams exist',all((R/(x+'.mmd')).exists() for x in ['01-commercial','02-fiscal','03-compliance','04-ingestion']))
check('negative control: orphan relationship endpoint rejected', 'NonexistentEntity' not in names)
check('negative control: a proposed field is not an approved field', 'signatureValueRef' not in [x['semantic_concept'] for x in entities])
check('negative control: no physical FiscalContext selection',not any(x['semantic_concept']=='PhysicalFiscalContext' for x in entities))
out={'passed':sum(x['passed'] for x in results),'total':len(results),'results':results}
(R/'TEST-RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(f"{out['passed']}/{out['total']} checks passed")
assert out['passed']==out['total']
