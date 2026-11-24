"""Current bounded positive-x beam end; historical classifier unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[922, 923, 924, 925]
assert len(old.PALETTE)==8
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==1678 and np.bincount(colors).tolist()==[416, 232, 774, 58, 72, 64, 36, 26]
 assert len(TARGET)==4 and (colors[TARGET]==0).all()
 colors[TARGET]=2;why[TARGET]='complete_positive_x_portico_beam_end_only'
 assert np.bincount(colors).tolist()==[412, 232, 778, 58, 72, 64, 36, 26]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only positive-x front-portico beam end four faces to existing warm_ochre_stone2. Original eight shaders unchanged. Exclude opposite end, top, underside, front, columns and main roof. Original 2mm height/11.5mm exposed depth and rear cap intersection step are coarse proxies; multilayer mouldings absent, not survey/color/stone-species certification. Source0 directly supports exterior brown-gray family distinct from white inner soffit; sources1/2/3 do not authorize other domains. PNG create/modify metadata not exposure dates. Historical QA/manufacturing limits retained.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
