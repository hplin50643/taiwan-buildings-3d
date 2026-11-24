"""Current bounded column-front appearance; historical classifier remains unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[1074, 1079, 1082, 1088, 1090, 1095]
assert len(old.PALETTE)==3
old.PALETTE=old.PALETTE+[('central_column_front_pale_gray_background_approximation','#C5C5BB')]
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==4138 and np.bincount(colors).tolist()==[2602, 1494, 42]
 assert len(TARGET)==6 and (colors[TARGET]==0).all()
 colors[TARGET]=3;why[TARGET]='complete_central_column_front_light_gray_background_only'
 assert np.bincount(colors).tolist()==[2596, 1494, 42, 6]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only6 complete central three-column front faces additionally use pale-gray background approximation. Original3 shaders and4132 other indices unchanged. Original rectangular column count/proportions and lower railing occlusion are coarse proxies, not measured pillar geometry or stone certification. Sides, backs, host, soffit, steps excluded.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
