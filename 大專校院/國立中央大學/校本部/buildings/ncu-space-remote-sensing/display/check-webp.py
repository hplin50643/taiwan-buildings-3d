"""Check the current display files. Optionally compare a clean Blender rebuild."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from PIL import Image
import json
p=ArgumentParser()
p.add_argument('--replay-root',type=Path)
p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent.parent)
a=p.parse_args(); root=a.package
m=json.loads((root/'display/webp-proof.json').read_text())
def digest(b):return sha256(b).hexdigest()
def require(x,label):
 if not x:raise RuntimeError(label)
def get(path,z):
 b=path.read_bytes();require(len(b)==z['bytes'] and digest(b)==z['sha256'],str(path))
 im=Image.open(path).convert('RGBA');require(list(im.size)==z['dimensions'] and digest(im.tobytes())==z['rgba_sha256'],str(path))
 return im
for n,z in m['views'].items():
 full=get(root/z['full']['path'],z['full']); assert z['rgba_sha256']==digest(full.tobytes())
 thumb=get(root/z['thumb']['path'],z['thumb']); assert z['thumb']['alpha_sha256']==digest(thumb.getchannel('A').tobytes())
 if a.replay_root:
  alternate=Image.open(a.replay_root/z['source']).convert('RGBA')
  require(alternate.size==full.size and alternate.tobytes()==full.tobytes(),'Rebuild pixels: '+n)
for k,z in m['current_native'].items():
 require(digest((root/k).read_bytes())==z['sha256'],'Native: '+k)
print(len(m['views']),'views, and native file checksums verified')
