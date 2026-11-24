"""Check current delivery, including equivalence with pinned historical review hashes."""
from pathlib import Path
from PIL import Image
import hashlib, json, zipfile

A=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256((A/p).read_bytes()).hexdigest()
load=lambda p:json.loads((A/p).read_text())
stl=sha('model.stl')
for f,k in [('release.json','stl_sha256'),('qa-topology.json','sha256'),('qa-layers.json','stl_sha256'),('qa/local-features.json','stl_sha256'),('qa/exchange-validation.json','source_STL_SHA256')]:
    assert load(f)[k]==stl,f
assert load('qa/scene-validation.json')['scene_sha256']==sha('scene.blend')
assert zipfile.ZipFile(A/'model.3mf').testzip() is None
render=load('qa/render-manifest.json')
historical={}
current={}
for v in render['files']:
    assert (A/v['path']).stat().st_size==v['bytes'] and sha(v['path'])==v['sha256'],v['path']
    with Image.open(A/v['path']) as im:
        assert list(im.size)==render['resolution'] and im.format=='WEBP'
        assert hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()==v['rgba_sha256']
    archive=v['archival_png'];historical[archive['path']]=archive['sha256'];current[v['path']]=v['sha256']
assert set(current)=={f'previews/{n}-full.webp' for n in ('front','rear','left_oblique','top','elevation')}
assert load('qa/render-reopen-validation.json')['front_sha256']==historical['previews/front.png']
check_historical=lambda p:historical[p] if p in historical else sha(p)
for n,h in load('qa/isolated-rebuild.json')['files_identical'].items():
    assert check_historical(n)==h,n
for r in load('qa/source-visual-review.json')['reviewed_artifacts']:
    assert check_historical(r['path'])==r['sha256'],r['path']
for r in render['prior_lightweight_webps']:
    assert (A/r['path']).stat().st_size==r['bytes'] and sha(r['path'])==r['sha256']
assert len(render['prior_lightweight_webps'])==4
for bad in ('*.pyc','*.png','*.jpg','*.jpeg'):
    assert not list(A.rglob(bad)),bad
for row in (A/'SHA256SUMS').read_text().splitlines():
    h,n=row.split('  ',1);assert sha(n)==h,n
print('Current checksums, native geometry links, all five decoded full-size views and historical review links pass.')
