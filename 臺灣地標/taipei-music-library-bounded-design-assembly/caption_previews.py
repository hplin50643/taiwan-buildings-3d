from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
ROOT=Path(__file__).resolve().parent
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
texts={
'assembled':['THREE-MODULE BOUNDED RESEARCH ASSEMBLY | 1:800','Three artificial frames + six removable hypothetical skins/supports + courtyard-hole display base.','B roof cut-position conflict remains. South band has nominal X. Not a complete building or tested print.'],
'exploded':['EXPLODED DISPLAY | NOT AN INSERTION TRAJECTORY','Each hypothetical skin is removed together with its entire dedicated support.','All supports, backing, grooves and base are artificial. Physical fit, strength and printing remain untested.'],
'hypotheses_removed':['HYPOTHESES REMOVED | THREE FRAMES AND ARTIFICIAL BASE','All six hypothetical skin units and their dedicated posts/arms are hidden.','Full-height opaque frame faces are still PROXIES, not certified actual walls. Unknown openings remain unresolved.'],
'source_only':['FINITE REFERENCE LINES ONLY | NO SOLID ARCHITECTURE CLAIM','116 finite plan baselines at nominal levels; no full-height proxies, carriers, base or conditional roofs.','First-floor zero is an artificial display datum. These lines are not complete wall, window or roof boundaries.']}
for name,lines in texts.items():
 im=Image.open(ROOT/'previews'/f'{name}.png').convert('RGB');out=Image.new('RGB',(im.width,im.height+138),'white');out.paste(im,(0,0));d=ImageDraw.Draw(out)
 for i,s in enumerate(lines):d.text((24,im.height+16+i*38),s,font=title if i==0 else font,fill=(25,40,48))
 out.save(ROOT/'previews'/f'review-{name}.png')
(ROOT/'PREVIEW-CAPTIONS.json').write_text(json.dumps({'captions':texts,'original_render_pixels_preserved':True,'caption_area_added_outside_original_canvas':True},indent=2)+'\n')
