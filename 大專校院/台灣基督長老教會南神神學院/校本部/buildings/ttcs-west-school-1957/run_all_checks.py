"""Run West School checks in a private temporary copy to preserve historical reports."""
from pathlib import Path
import argparse, os, shutil, subprocess, sys, tempfile
A=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--lib3mf-python',required=True)
p.add_argument('--blender',default='blender')
a=p.parse_args()
with tempfile.TemporaryDirectory(prefix='ttcs-west-all-checks-') as td:
    root=Path(td)
    for row in (A/'SHA256SUMS').read_text().splitlines():
        _,rel=row.split('  ',1)
        src=(A/rel).resolve()
        assert A in src.parents and src.is_file(),rel
        dest=root/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dest)
    for name in ['qa_model.py','check_features.py']:
        subprocess.run([sys.executable,str(root/name)],check=True)
    e=dict(os.environ,BUILD_PYTHON=sys.executable)
    subprocess.run([a.lib3mf_python,str(root/'verify_exchange.py')],env=e,check=True)
    subprocess.run([sys.executable,str(root/'verify_webp.py')],check=True)
    for name in ['verify_scene.py','verify_render.py']:
        command=[a.blender,'--disable-autoexec','-b','-t','4','--python-exit-code','1','--python',str(root/name)]
        if name=='verify_render.py':command+=['--','--image-python',sys.executable]
        subprocess.run(command,check=True)
print('TTCS West School geometry, exchange, scene and WebP checks pass; historical reports unchanged; no physical print claim.')
