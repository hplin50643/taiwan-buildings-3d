"""Current bounded column-front appearance; historical classifier remains unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[1086, 1091, 1092, 1103, 1109, 1127, 1136, 1153, 1161, 1162, 1163, 1174]
assert len(old.PALETTE)==2
old.PALETTE=old.PALETTE+[('front_column_gray_stone_background_approximation','#B9BDB3')]
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==3522 and np.bincount(colors).tolist()==[3521, 1]
 assert len(TARGET)==12 and (colors[TARGET]==0).all()
 colors[TARGET]=2;why[TARGET]='complete_front_column_gray_stone_background_only'
 assert np.bincount(colors).tolist()==[3509, 1, 12]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only12 complete front-column triangles additionally use new gray stone-like background material2. Original2 shaders and3510 other indices remain. Four coarse rectangular columns minus stairs; true sloping plinths/granular texture not modeled. Original exposed ears are intersections, not measured real feet. Sides/back/stairs excluded.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
