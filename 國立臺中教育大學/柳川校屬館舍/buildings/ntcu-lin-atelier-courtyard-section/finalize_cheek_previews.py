from pathlib import Path
import sys,json,hashlib
from PIL import Image
R=Path(sys.argv[1]).resolve();rows=[]
for name in ['preview','rear','front','back','west','east','top','entry-detail','facade-detail','roof-detail']:
 p=R/(name+'.png');im=Image.open(p);assert im.size==(1200,900);pixels=im.tobytes();out=Image.new(im.mode,im.size);out.putdata(list(im.getdata()));out.save(p);assert Image.open(p).tobytes()==pixels and not Image.open(p).text;rows.append(dict(file=p.name,size=[1200,900],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pixel_preserved_text_metadata_removed=True))
(R/'CHEEK-PREVIEW-RECEIPTS.json').write_text(json.dumps(rows,indent=2))
