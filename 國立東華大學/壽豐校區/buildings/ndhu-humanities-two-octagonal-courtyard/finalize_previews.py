"""Losslessly remove PNG text metadata and join original front/rear frames. Python+Pillow."""
from pathlib import Path
from PIL import Image
import sys
R=Path(sys.argv[1]);P=R/'previews'
for n in ['front','rear','top','courtyard']:
 p=P/(n+'.png');im=Image.open(p);im.load();im.save(p)
a=Image.open(P/'front.png');b=Image.open(P/'rear.png');out=Image.new('RGB',(a.width+b.width,max(a.height,b.height)));out.paste(a,(0,0));out.paste(b,(a.width,0));out.save(P/'front-rear.png')
