"""Verify current lossless WebPs and, optionally, isolate a fresh reproduction."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pixels(path, row, expected_format=None):
    with Image.open(path) as im:
        assert expected_format is None or im.format == expected_format, path
        assert list(im.size) == row['size'], path
        assert hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest() == row['rgba_sha256'], path

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--rebuild', action='store_true')
    cli.add_argument('--blender', default='blender')
    args = cli.parse_args()
    proof = json.loads((ROOT/'display/render-proof.json').read_text())
    rows = proof['rows']
    assert len(rows) == len({row['webp'] for row in rows}) == 7
    for p, expected in proof['native'].items():
        assert digest(ROOT/p) == expected, p
    for base in (ROOT, ROOT/'display'):
        for line in (base/'SHA256SUMS').read_text().splitlines():
            expected, name = line.split('  ', 1)
            assert digest(base/name) == expected, name
    for row in rows:
        current = ROOT/'display'/row['webp']
        assert digest(current) == row['webp_sha256']
        pixels(current, row, 'WEBP')
        thumb = row['thumbnail']
        path = ROOT/'display'/thumb['path']
        assert digest(path) == thumb['sha256']
        with Image.open(path) as im:
            assert im.format == 'WEBP' and list(im.size) == thumb['size'], path
    if args.rebuild:
        with tempfile.TemporaryDirectory(prefix='ncu-general-edu-render-') as temp:
            temp = Path(temp)
            for name in ('model.stl','scene.blend','build_appearance.py'):
                shutil.copy2(ROOT/name, temp/name)
            subprocess.run([args.blender,'-b','-t','1','--python-exit-code','1','-P',str(temp/'build_appearance.py')],cwd=temp,check=True)
            for name in ('appearance.3mf','appearance-materials.json'):
                assert digest(temp/name) == proof['native'][name], name
            for row in rows:
                pixels(temp/row['source'], row, 'PNG')
    print('Seven WebP views, both ledgers and unchanged model files verified.')

if __name__ == '__main__':
    main()