"""Rebuild canonical color exports in a scratch directory using immutable, hash-verified inputs."""
import argparse, hashlib,json,os,subprocess,tempfile, urllib.parse, urllib.request
from pathlib import Path
package=Path(__file__).resolve().parents[1]
src=package/'source'
spec=json.loads((src/'pinned-inputs.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def restore(p,dest,gitdir=None):
    item=spec['files'][p]
    repo_path=spec['package']+'/'+p
    if gitdir:
        b=subprocess.check_output(['git','--git-dir',str(gitdir),'show',item['commit']+':'+repo_path],
                                  env=os.environ|{'GIT_NO_LAZY_FETCH':'1'})
    else:
        u='https://raw.githubusercontent.com/hplin50643/taiwan-buildings-3d/'+item['commit']+'/'+urllib.parse.quote(repo_path)
        with urllib.request.urlopen(u,timeout=30) as r:b=r.read()
    assert sha(b)==item['sha256'],p
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(b)
def main():
    import sys
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--git-dir',type=Path,help='Optional local Git object store, same hashes required')
    ap.add_argument('--blender',default='blender')
    ap.add_argument('--historical-layout',action='store_true',help='Also rerun original geometry-difference QA with its dependencies installed')
    a=ap.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        for rel in spec['files']:
            restore(rel,root/rel,a.git_dir)
        v2=root/'facade-layout-v2'
        out=root/'stair-door-color-20261120'
        stl=(package/'model-v2.stl').read_bytes()
        assert sha(stl)==spec['current_stl_sha256']
        (v2/'model-v2.stl').write_bytes(stl)
        subprocess.run([a.blender,'-b',str(v2/'scene.blend'),'-t','2','--python-exit-code','1','-P',str(out/'apply_stair_door.py')],check=True)
        subprocess.run([sys.executable,str(out/'rebuild_exchange.py')],check=True)
        if a.historical_layout:
            (v2/'qa').mkdir()
            subprocess.run([sys.executable,str(v2/'source/verify_layout.py')],check=True)
            (a.output/'historical-layout-rerun.json').write_bytes((v2/'qa/layout-validation.json').read_bytes())
        for name,data in [('model-v2.stl',stl),('model.3mf',(out/'model-colored.3mf').read_bytes()),('scene.blend',(out/'scene.blend').read_bytes())]:
            (a.output/name).write_bytes(data)
if __name__=='__main__':main()
