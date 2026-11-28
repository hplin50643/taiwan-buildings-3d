"""Validate current guides and rerun legacy STL QA in a disposable package copy."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
r=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(r/'check_readme_views.py')],check=True)
assert hashlib.sha256((r/'check_thin_features.py').read_bytes()).hexdigest()=='059f7378c74a1400dcf010365ebf35df3027fd853f1c960462a233dc68ce8915'
with tempfile.TemporaryDirectory(prefix='dila-stl-qa-') as d:
    t=Path(d)/r.name
    shutil.copytree(r,t,ignore=shutil.ignore_patterns('__pycache__'))
    for f in ['validate_model.py','check_thin_features.py','check_all_layers.py','check_layer_components.py','check_recess_roots.py','summarize_component_losses.py','check_preview_rebuild.py']:
        subprocess.run([sys.executable,str(t/f)],cwd=t,check=True)
    for n in ['validation.json','layer-component-check.json','recess-root-check.json','component-loss-summary.json','preview-rebuild-check.json']:
        j=json.loads((t/n).read_text());assert j['passed'] and all(j['checks'].values()),n
print('Current views and historical STL QA passed. Release artifacts were not overwritten.')
