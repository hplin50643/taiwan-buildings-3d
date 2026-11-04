"""Recheck the four curved units with exact rational arithmetic in a NEW directory.
Copies the unchanged independent algorithms; only SOURCE's local input path is rebound.
No network or source images required. Python standard library only.
"""
from pathlib import Path
import sys,shutil,subprocess,json,hashlib
ROOT=Path(__file__).resolve().parent;src=ROOT/'qa/curved-domain';out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=False)
shutil.copytree(src/'inputs',out/'inputs')
changes=[]
for p in src.glob('*.py'):
 s=p.read_text()
 if p.name=='exact_domain_audit.py':
  old="SOURCE=HERE.parents[2]/'curved-build/output-v7'";assert s.count(old)==1;s=s.replace(old,"SOURCE=HERE/'inputs'");changes.append({'file':p.name,'change':'SOURCE input directory only, algorithm unchanged','original_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (out/p.name).write_text(s)
for name in ['selftest_exact_geometry.py','exact_embedding_audit.py','exact_domain_audit.py','exact_input_front_audit.py','exact_minkowski_envelope_final.py']:
 with (out/(name+'.log')).open('w')as f:subprocess.run([sys.executable,str(out/name)],check=True,stdout=f,stderr=subprocess.STDOUT)
(out/'RECHECK-CONFIGURATION.json').write_text(json.dumps({'path_rebinding_only':changes,'source_inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in (out/'inputs').iterdir()}},indent=2)+'\n')
