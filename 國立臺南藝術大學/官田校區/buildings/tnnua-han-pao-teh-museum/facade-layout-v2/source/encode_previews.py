"""Encode the current inspection renders as lossless WebP; compare decode and source bytes."""
from pathlib import Path
from PIL import Image
import json, sys
src,dst=map(Path,sys.argv[1:])
dst.mkdir(parents=True,exist_ok=True)
receipt={}
for n in ('front','stairs','rear','top','stair-door'):
    p=src/(n+'.png'); out=dst/(n+'.webp')
    with Image.open(p) as f: im=f.convert('RGB')
    im.save(out,format='WEBP',lossless=True,method=6,exact=True)
    with Image.open(out) as got:
        assert got.format=='WEBP' and not {'xmp','exif','icc_profile'}&got.info.keys()
        assert got.convert('RGB').tobytes()==im.tobytes() and got.size==im.size
    a,b=p.stat().st_size,out.stat().st_size
    receipt[n]={'size_px':im.size,'png_bytes':a,'webp_bytes':b,'smaller_bytes':a-b,'decoded_rgb_equal':True}
print(json.dumps(receipt,indent=2))
