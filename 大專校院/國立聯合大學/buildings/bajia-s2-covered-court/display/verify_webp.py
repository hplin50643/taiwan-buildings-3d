"""Verify distributed WebP files; optionally reconcile an independent renderer output."""
import argparse,json
from hashlib import sha256
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--replay-root',type=Path,help='Independent copy of model folder, after running current renderer')
arg=parser.parse_args()
manifest=json.loads((P/'archive-png.json').read_text())
def require(ok,msg):
 if not ok:raise SystemExit(msg)
def pixels(path):
 with Image.open(path) as im:return list(im.size),sha256(im.convert('RGBA').tobytes()).hexdigest()
for png,row in manifest['views'].items():
 webp=P.parent/row['webp']; expect=(row['size'],row['rgba_sha256'])
 require(sha256(webp.read_bytes()).hexdigest()==row['webp_sha256'],f'WebP SHA-256 mismatch: {webp}')
 require(pixels(webp)==expect,f'WebP decoded RGBA mismatch: {webp}')
 if arg.replay_root:
  require(pixels(arg.replay_root/png)==expect,f'Rendered PNG decoded RGBA mismatch: {png}')
print(f"Verified {len(manifest['views'])} full-size WebP images"+(' and independent re-renders' if arg.replay_root else ''))
