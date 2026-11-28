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
arch={r['archive_png']:r['archive_png_sha256'] for r in current.values()}
arch.update({n:v['sha256'] for n,v in evidence['historical_review_files'].items()})
def historic_digest(name):
 return arch[name] if name in arch else sha(name)
sums={name:digest for digest,name in (line.split('  ',1) for line in (A/'SHA256SUMS').read_text().splitlines())}
actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
assert set(sums)|{'SHA256SUMS'}==actual
assert all(sha(name)==digest for name,digest in sums.items())
assert sha(evidence['historical_source_review'])==evidence['historical_source_review_sha256']
stl=sha('model.stl')
for f,k in [('release.json','stl_sha256'),('qa-topology.json','sha256'),('qa-layers.json','stl_sha256'),('qa/local-features.json','stl_sha256'),('qa/exchange-validation.json','source_STL_SHA256')]:assert json.loads((A/f).read_text())[k]==stl,f
assert json.loads((A/'qa/scene-validation.json').read_text())['scene_sha256']==sha('scene.blend')
for r in json.loads((A/'qa/render-manifest.json').read_text())['files']:assert historic_digest(r['path'])==r['sha256']
assert json.loads((A/'qa/render-reopen-validation.json').read_text())['front_sha256']==historic_digest('previews/front.png')
assert zipfile.ZipFile(A/'model.3mf').testzip() is None
for name,h in json.loads((A/'qa/isolated-rebuild.json').read_text())['files_identical'].items():assert historic_digest(name)==h
assert not list(A.rglob('*.pyc'))
assert not list((A/'previews').glob('*.png'))
from PIL import Image,ImageChops,ImageStat
from math import sqrt
assert {p.stem for p in (A/'previews').glob('*.webp')}==set(VIEWS)|{k+'-640' for k in VIEWS}
rs=json.loads((A/'previews/thumbnail-proof.json').read_text())['images']
assert len(rs)==5 and {x['full'] for x in rs}=={'previews/'+k+'.webp' for k in VIEWS}
for row in rs:
 assert hashlib.sha256((A/row['preview']).read_bytes()).hexdigest()==row['preview_sha256']
 assert rgba(A/row['preview'])[1]==row['preview_rgba_sha256']
 with Image.open(A/row['full']) as f0,Image.open(A/row['preview']) as s0:
  f=f0.convert('RGBA'); thumb=s0.convert('RGBA');f.thumbnail((640,640),Image.Resampling.LANCZOS)
  assert list(f.size)==row['preview_size'] and f.size==thumb.size
  assert f.getchannel('A').tobytes()==thumb.getchannel('A').tobytes()
  def util(im):return Image.alpha_composite(Image.new('RGBA',im.size,(255,255,255,255)),im).convert('RGB')
  rms=ImageStat.Stat(ImageChops.difference(util(f),util(thumb))).rms
  assert sqrt(sum(x*x for x in rms)/3)<9

for name,r in current.items():
 p=A/'previews'/(name+'.webp'); size,h=rgba(p)
 assert list(size)==r['dimensions'] and h==r['rgba_sha256'] and sha('previews/'+p.name)==r['webp_sha256']
assert not list(A.rglob('*.jpg')) and not list(A.rglob('*.jpeg'))
print('Native CAD, unchanged historical QA and five current lossless WebP files verified.')
