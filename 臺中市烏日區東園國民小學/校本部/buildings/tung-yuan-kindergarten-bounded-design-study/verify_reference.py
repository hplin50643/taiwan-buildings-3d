from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent/'reference-nominal'
a=json.load(open(P/'expected-stl.json'))
for x in a:assert hashlib.sha256((P/x['file']).read_bytes()).hexdigest()==x['sha256'],x['file']
print('49 generated nominal reference STL hashes verified')
