import json
from pathlib import Path
p=Path(__file__).with_name("CTC-003-SYNTHETIC-REFERENCE-FIXTURES.json")
d=json.loads(p.read_text())
checks={
"ingestion prepublication link":d["ingestion"]["sourceRepresentationId"].startswith("REP-SRC"),
"revision pinned parties":len(d["revision"]["partySnapshotIds"])==2,
"interpretations same revision":all(i["revisionId"]==d["revision"]["id"] for i in d["interpretations"]),
"source facts pinned":all(i["sourceFactIds"]==d["revision"]["sourceFactIds"] for i in d["interpretations"]),
"profiles differ":len({i["profilePackageId"] for i in d["interpretations"]})==2,
"manifests distinct":len({i["manifestId"] for i in d["interpretations"]})==2,
"attempt exact revision":d["submission"]["revisionId"]==d["revision"]["id"],
"attempt exact representation":d["submission"]["representationId"]!="latest" and d["submission"]["representationDigest"].startswith("sha256:"),
"correction separate document":d["correction"]["documentId"]!=d["correction"]["targetDocumentId"],
"fiscal identity retained":d["evidence"][0]["identityId"]==d["evidence"][1]["identityId"],
"evidence distinct":d["evidence"][0]["id"]!=d["evidence"][1]["id"],
"reject mutable latest reference": "latest" not in [d["submission"]["representationId"],d["submission"]["revisionId"]],
}
for k,v in checks.items(): print(("PASS" if v else "FAIL")+" | "+k)
assert all(checks.values())
print(f"RESULT: {sum(checks.values())}/{len(checks)} synthetic structural checks passed")
