from PIL import Image,ImageDraw
from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['court-oblique','rear-oblique','top','entry-end']:
 im=Image.open(P/(name+'.png')).convert('RGB');o=Image.new('RGB',(im.width,im.height+145),'white');o.paste(im,(0,145));d=ImageDraw.Draw(o)
 for y,t in [(15,'TUNG YUAN - artificial joint relief / separate SOURCE and PROXY research parts'),(40,'Source front contours retained within reported float32 error; RF domains remain UNBUILT'),(65,'0.98 back-depth wedge; proxy end cuts and platform notches are MANUFACTURING DESIGN, not real joints'),(90,'All-pair digital collision check at 1e-5 mm3 threshold; tiny raw numerical residues disclosed'),(115,'NO physical fit / insertion / stability / print test; mixed window proxies have no invented connectors')]:d.text((20,y),t,fill='black')
 o.save(P/('review-'+name+'.png'))
