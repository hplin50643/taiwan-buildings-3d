"""Check the released package or regenerate previews in an isolated directory."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
from PIL import Image, features
A=Path(__file__).resolve().parent
VIEWS=('front','rear','elevation','top','left_oblique')
CORE=('model.stl','model.3mf','mesh.json','palette.json')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):
    with Image.open(p) as im:
        return im.size,hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()
def encode(p,q):
    if Image.__version__!='13.0.0' or features.version('webp')!='1.6.0':
        raise RuntimeError('Exact reproduction requires Pillow 13.0.0 and libwebp 1.6.0')
    with Image.open(p) as im:
        im.convert('RGBA').save(q,'WEBP',lossless=True,quality=75,method=4,exact=True)
    if rgba(p)!=rgba(q): raise ValueError(f'RGBA round trip failed: {p.name}')
def records(a):
    return json.loads((a/'qa/preview-webp.json').read_text())['views']
def validate(stage,out):
    for name,r in records(A).items():
        p=stage/'previews'/(name+'.png');q=out/(name+'.webp')
        size,px=rgba(p)
        if list(size)!=r['dimensions'] or px!=r['rgba_sha256']:
            raise ValueError(f'Render differs from signed pixels: {p.name}')
        encode(p,q)
        if sha(q)!=r['webp_sha256']:raise ValueError(f'Signed WebP differs: {q.name}')
def reproduce(dest,blender,threads,rebuild=True):
    dest=dest.resolve()
    if dest.exists() or A in dest.parents: raise ValueError('Use a new directory outside this package')
    with tempfile.TemporaryDirectory(prefix='building-preview-') as t:
        t=Path(t);(t/'previews').mkdir();(t/'qa').mkdir(); display=t/'display';display.mkdir()
        for name in ('render_model.py','build_model.py'):shutil.copyfile(A/name,t/name)
        if rebuild:subprocess.run([sys.executable,str(t/'build_model.py')],cwd=t,check=True)
        else:
            for name in CORE:shutil.copyfile(A/name,t/name)
        for name in CORE:
            if sha(t/name)!=sha(A/name):raise ValueError(f'Native file differs: {name}')
        subprocess.run([blender,'-b','-t',threads,'--python-exit-code','19','-P',str(t/'render_model.py')],cwd=t,check=True)
        validate(t,display)
        dest.mkdir()
        shutil.copytree(display,dest/'previews')
        if rebuild:
            for name in (*CORE,'scene.blend'):shutil.copyfile(t/name,dest/name)
def cli(rebuild=False):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--blender',default='blender')
    p.add_argument('--threads',default='4')
    a=p.parse_args();reproduce(a.output,a.blender,a.threads,rebuild=rebuild)
if __name__=='__main__':cli()
