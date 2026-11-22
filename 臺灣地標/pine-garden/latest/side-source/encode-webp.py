"""Encode seven exact full-scale previews and proof-source catalog thumbnail using Pillow."""
from pathlib import Path
from PIL import Image
import sys
root=Path(sys.argv[1]);out=root/'webp';out.mkdir(exist_ok=True)
for n in ('front','rear','front-elevation','rear-elevation','right-end','left-end','top'):
 with Image.open(root/(n+'.png')) as im: img=im.convert('RGBA')
 p=out/(n+'.webp');img.save(p,method=6,lossless=True,exact=True)
 with Image.open(p) as read: assert read.convert('RGBA').tobytes()==img.tobytes()
 if n=='front':
  img.thumbnail((640,640),Image.Resampling.LANCZOS)
  img.save(out/'front-640.webp',method=6,quality=92,exact=True)
