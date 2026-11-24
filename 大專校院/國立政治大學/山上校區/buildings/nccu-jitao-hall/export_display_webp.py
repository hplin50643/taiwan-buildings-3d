"""Export only the five signed display WebPs; raw PNG and Blend rebuild are isolated."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image, features

VIEW_NAMES=('front','rear','elevation','top','left_oblique')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def signatures(package):
    return {p:h for line in (package/'SHA256SUMS').read_text().splitlines() for h,p in (line.split('  ',1),)}

def original_records(package):
    return {r['path']:r for r in json.loads((package/'qa/render-manifest.json').read_text())['files']}

def encode(source, target):
    with Image.open(source) as image:
        rgba=image.convert('RGBA')
        if rgba.size!=(1200,1200):
            raise ValueError('Unexpected preview dimensions')
        rgba.save(target,'WEBP',lossless=True,quality=75,method=4,exact=True)
    with Image.open(target) as image:
        if image.size!=rgba.size or image.convert('RGBA').tobytes()!=rgba.tobytes():
            raise ValueError('Lossless pixels did not round trip')

def validate(package, stage, display):
    if Image.__version__!='13.0.0' or features.version('webp')!='1.6.0':
        raise RuntimeError('Use Pillow 13.0.0 and libwebp 1.6.0 for exact reproduction')
    signed=signatures(package)
    archived=original_records(package)
    if set(archived)!={f'previews/{n}.png' for n in VIEW_NAMES}:
        raise ValueError('Unexpected archived render records')
    for label in VIEW_NAMES:
        p=stage/'previews'/f'{label}.png'
        historical=archived[f'previews/{label}.png']
        if p.stat().st_size!=historical['bytes'] or sha(p)!=historical['sha256']:
            raise ValueError(f'Raw rerender differs from original QA: {label}')
        result=display/f'{label}.webp';encode(p,result)
        if sha(result)!=signed[f'previews/{label}.webp']:
            raise ValueError(f'WebP rerender differs from signed asset: {label}')

def export(package, blender, threads):
    signed=signatures(package)
    with tempfile.TemporaryDirectory(prefix='nccu-webp-') as tmp:
        stage=Path(tmp)
        (stage/'previews').mkdir();(stage/'qa').mkdir()
        for n in ('model.stl','model.3mf','palette.json','render_model.py'):
            if sha(package/n)!=signed[n]:
                raise ValueError(f'Source differs from signed asset: {n}')
            shutil.copyfile(package/n,stage/n)
        subprocess.run([blender,'-b','-t',threads,'--python-exit-code','19',
                        '-P',str(stage/'render_model.py')],cwd=stage,check=True)
        output=stage/'display';output.mkdir()
        validate(package,stage,output)
        for label in VIEW_NAMES:
            name=f'{label}.webp'
            shutil.copyfile(output/name,package/'previews'/name)

if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--blender',default='blender')
    cli.add_argument('--threads',default='4')
    args=cli.parse_args()
    export(Path(__file__).resolve().parent,args.blender,args.threads)
