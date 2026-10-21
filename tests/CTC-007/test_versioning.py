import json
from pathlib import Path
result=json.loads((Path(__file__).parent/'results.json').read_text())
assert result['total']==12
assert all(c['pass'] for c in result['cases'])
print(f"{result['passed']}/{result['total']} policy classification assertions passed")
