"""Rebuild in a clean directory, never altering delivered files or historical QA."""
from pathlib import Path
import argparse, subprocess, shutil, sys
from verify_webp import verify
A=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--output',type=Path,required=True)
p.add_argument('--blender',default='blender')
p.add_argument('--threads',default='4')
a=p.parse_args()
R=a.output.resolve()
assert R!=A and A not in R.parents and not R.exists(),'Use a new external scratch output directory'
R.mkdir(parents=True)
for d in ['previews','qa']:(R/d).mkdir()
for f in ['build_model.py','render_model.py']:shutil.copy2(A/f,R/f)
subprocess.run([sys.executable,str(R/'build_model.py')],check=True)
subprocess.run([a.blender,'--disable-autoexec','-b','--factory-startup','-t',a.threads,'--python-exit-code','1','--python',str(R/'render_model.py')],check=True)
for f in ['model.stl','model.3mf','mesh.json','palette.json']:
    assert (R/f).read_bytes()==(A/f).read_bytes(),f
assert verify(A,R)==5
print('Four exact core artifacts and five rebuilt PNG/active WebP pixel bindings pass; delivered files unchanged.')
