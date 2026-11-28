"""Verify delivered files and evidence binding for 法鼓文理學院金山校本部大願橋."""
from pathlib import Path
import hashlib,json,subprocess,sys
A=Path(__file__).resolve().parent
import sys
sys.dont_write_bytecode=True
from export_display_webp import rgba, VIEWS
evidence=json.loads((A/'qa/preview-webp.json').read_text())
current=evidence['views']
arch={r['archive_png']:(r['archive_png_sha256'],r['archive_png_bytes']) for r in current.values()}
def identity(name):
 if name in arch:return arch[name]
 if name in evidence['historical_review_files']:return evidence['historical_review_files'][name]['sha256'],(A/name).stat().st_size
 p=A/name
 return hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size
sums={name:digest for digest,name in (line.split('  ',1) for line in (A/'SHA256SUMS').read_text().splitlines())}
assert set(sums)|{'SHA256SUMS'}=={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
assert hashlib.sha256((A/evidence['historical_source_review']).read_bytes()).hexdigest()==evidence['historical_source_review_sha256']

for line in (A/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((A/n).read_bytes()).hexdigest()==h,n
sha=hashlib.sha256((A/'model.stl').read_bytes()).hexdigest()
for n,key in [('release.json','stl_sha256'),('qa-topology.json','sha256'),('qa-layers.json','stl_sha256'),('qa/feature-validation.json','stl_sha256'),('qa/exchange-validation.json','source_STL_SHA256')]:assert json.loads((A/n).read_text())[key]==sha,n
assert json.loads((A/'qa/scene-validation.json').read_text())['scene_sha256']==hashlib.sha256((A/'scene.blend').read_bytes()).hexdigest()
for n,h in json.loads((A/'qa/isolated-rebuild.json').read_text())['files_identical'].items():assert identity(n)[0]==h,n
for r in json.loads((A/'qa/render-manifest.json').read_text())['files']:assert identity(r['path'])[0]==r['sha256']
assert json.loads((A/'qa/render-reopen-validation.json').read_text())['front_sha256']==identity('previews/front.png')[0]
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
 assert list(size)==r['dimensions'] and h==r['rgba_sha256'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['webp_sha256']
assert json.loads((A/'qa/identity-validation.json').read_text())['all_text_names_consistent']
review=json.loads((A/'qa/independent-appearance-review.json').read_text());assert review['status']=='PASS_SOURCE_BOUND_EXTERIOR_APPROXIMATION'
for r in review['artifacts']:
 assert identity(r['path'])[1]==r['bytes'] and identity(r['path'])[0]==r['sha256'],r['path']
print('Native model, historical evidence and signed WebP verified.')
