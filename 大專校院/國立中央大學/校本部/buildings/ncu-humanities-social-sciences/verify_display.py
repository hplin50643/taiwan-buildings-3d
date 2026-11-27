"""Check current display references, and optionally replay the seven cameras in isolation."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image
R=Path(__file__).resolve().parent

def sha(file):
    return sha256(file.read_bytes()).hexdigest()

def assert_pixels(path,row):
    with Image.open(path) as im:
        assert list(im.size)==row['size'],path
        assert sha256(im.convert('RGBA').tobytes()).hexdigest()==row['rgba_sha256'],path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rebuild',action='store_true')
    p.add_argument('--blender',default='blender')
    args=p.parse_args()
    proof=json.loads((R/'display/render-proof.json').read_text())
    assert len(proof['rows'])==7
    assert len({row['webp'] for row in proof['rows']})==7
    for name,digest in proof['native'].items():
        assert sha(R/name)==digest,name
    for base,ledger in [(R,R/'SHA256SUMS'),(R/'display',R/'display/SHA256SUMS')]:
        for line in ledger.read_text().splitlines():
            expected,name=line.split('  ',1)
            assert sha(base/name)==expected,name
    for row in proof['rows']:
        current=R/'display'/row['webp']
        assert sha(current)==row['webp_sha256'],current
        assert_pixels(current,row)
        thumb=row['thumbnail']; path=R/'display'/thumb['path']
        assert sha(path)==thumb['sha256'],path
        with Image.open(path) as im:
            assert im.format=='WEBP' and list(im.size)==thumb['size'],path
    if args.rebuild:
        with tempfile.TemporaryDirectory(prefix='ncu-humanities-render-') as tmp:
            tmp=Path(tmp)
            for name in ('model.stl','scene.blend','build_appearance.py'):
                shutil.copy2(R/name,tmp/name)
            subprocess.run([args.blender,'-b','-t','1','--python-exit-code','1','-P',str(tmp/'build_appearance.py')],cwd=tmp,check=True)
            for name in ('appearance.3mf','appearance-materials.json'):
                assert sha(tmp/name)==proof['native'][name],name
            for row in proof['rows']:
                assert_pixels(tmp/row['source'],row)
    print('7 current WebP views, both checksum ledgers and native locks verified.')

if __name__=='__main__':
    main()
