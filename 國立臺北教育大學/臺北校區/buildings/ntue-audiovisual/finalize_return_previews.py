from pathlib import Path
import sys,json,hashlib
from PIL import Image
R=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent);records=[]
for name in ['preview','rear','front','back','west','east','top','entry-detail','facade-detail','roof-detail']:
 p=R/(name+'.png');im=Image.open(p);assert im.size==(1200,900);im.load();before=hashlib.sha256(im.tobytes()).hexdigest();im.save(p);re=Image.open(p);assert re.size==im.size and hashlib.sha256(re.tobytes()).hexdigest()==before and not re.text;records.append({'file':p.name,'size':list(im.size),'pixel_sha256':before,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'png_text':False})
(R/'RETURN-PREVIEW-RECEIPTS.json').write_text(json.dumps(records,indent=2)+'\n')
