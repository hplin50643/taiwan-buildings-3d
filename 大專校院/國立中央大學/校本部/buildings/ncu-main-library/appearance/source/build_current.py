"""Existing-material extension, preserving historical classifier source bytes."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[6650, 6651, 6652, 6653, 6663, 6664, 6665, 6666, 6678, 6679, 6681, 6683]
assert len(old.PALETTE)==4 and old.PALETTE[3][1]=='#BEB7AE'
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==6688 and np.bincount(colors).tolist()==[2285, 506, 2642, 1255]
 assert len(TARGET)==12 and (colors[TARGET]==0).all()
 colors[TARGET]=3;why[TARGET]='bounded_original_three_step_warm_gray_tile_family_approximation'
 assert np.bincount(colors).tolist()==[2273, 506, 2642, 1267]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only12 original three-step tread/front-riser faces additionally use existing warm-gray front tile-family approximation. Original four shaders and other6676 faces unchanged. First riser starts at basez3; upper tread endsy=-47.35, with2.85mm gap to porch retained. Original3steps/nosing/proportions are not measured count or calibrated uniform material. Skirts, base, rear and platform excluded.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
