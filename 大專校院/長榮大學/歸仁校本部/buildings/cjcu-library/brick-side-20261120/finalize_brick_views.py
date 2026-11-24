from pathlib import Path
from PIL import Image
import sys
P=Path(sys.argv[1]);D=P/'previews'
for n in ('front','rear','elevation','top','right-side'):
 p=D/(n+'.png')
 with Image.open(p) as im:
  pix=im.tobytes(); mode=im.mode; size=im.size
 clean=Image.frombytes(mode,size,pix);tmp=p.with_suffix('.tmp')
 clean.save(tmp,format='PNG');tmp.replace(p)
 with Image.open(p) as re:assert re.tobytes()==pix and not re.info
with Image.open(D/'front.png') as a,Image.open(D/'rear.png') as b:
 assert a.size==b.size==(1000,800);out=Image.new('RGB',(2000,800));out.paste(a.convert('RGB'),(0,0));out.paste(b.convert('RGB'),(1000,0));out.save(D/'front-rear.png')
