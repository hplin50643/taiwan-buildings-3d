"""Check report hashes against actual delivery files; no artifact repair."""
from pathlib import Path
import json,hashlib,zipfile
A=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256((A/p).read_bytes()).hexdigest()
import sys
sys.dont_write_bytecode=True
from export_display_webp import rgba, VIEWS
evidence=json.loads((A/'qa/preview-webp.json').read_text())
current=evidence['views']
assert tuple(current)==VIEWS
arch={row['archive_png']:row['archive_png_sha256'] for row in current.values()}
def historic_digest(name):
 return arch[name] if name in arch else sha(name)
sums={name:digest for digest,name in (line.split('  ',1) for line in (A/'SHA256SUMS').read_text().splitlines())}
actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
assert set(sums)|{'SHA256SUMS'}==actual
assert all(sha(name)==digest for name,digest in sums.items())
stl=sha('model.stl')
for f,k in [('release.json','stl_sha256'),('qa-topology.json','sha256'),('qa-layers.json','stl_sha256'),('qa/local-features.json','stl_sha256'),('qa/exchange-validation.json','source_STL_SHA256')]:assert json.loads((A/f).read_text())[k]==stl,f
assert json.loads((A/'qa/scene-validation.json').read_text())['scene_sha256']==sha('scene.blend')
for r in json.loads((A/'qa/render-manifest.json').read_text())['files']:assert historic_digest(r['path'])==r['sha256']
assert json.loads((A/'qa/render-reopen-validation.json').read_text())['front_sha256']==historic_digest('previews/front.png')
assert zipfile.ZipFile(A/'model.3mf').testzip() is None
for name,h in json.loads((A/'qa/isolated-rebuild.json').read_text())['files_identical'].items():assert historic_digest(name)==h
review=json.loads((A/'qa/source-visual-review.json').read_text());assert review['status'].startswith('PASS'),review['status']
for name,h in review['artifacts'].items():assert historic_digest(name)==h['sha256']
assert not list(A.rglob('*.pyc'))
assert not list((A/'previews').glob('*.png'))
assert {p.stem for p in (A/'previews').glob('*.webp')}==set(VIEWS)|{n+'-640' for n in VIEWS}
for thumb in json.loads((A/'previews/thumbnail-proof.json').read_text())['views']:
 assert sha(thumb['thumbnail'])==thumb['thumbnail_sha256'] and rgba(A/thumb['thumbnail'])==(tuple(thumb['size']),thumb['thumbnail_rgba_sha256'])
for label,r in current.items():
 p=A/'previews'/(label+'.webp'); size,h=rgba(p)
 assert list(size)==r['dimensions'] and h==r['rgba_sha256'] and sha('previews/'+p.name)==r['webp_sha256']
assert not list(A.rglob('*.jpg')) and not list(A.rglob('*.jpeg'))


print('Native QA, archived bindings and five current lossless WebPs verified.')
