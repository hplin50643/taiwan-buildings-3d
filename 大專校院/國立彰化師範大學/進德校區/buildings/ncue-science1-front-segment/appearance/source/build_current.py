"""Current bounded entrance-step background; original classifier unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[1005, 1006, 1007, 1008, 1014, 1017, 1018, 1019, 1028, 1029, 1031, 1032]
assert len(old.PALETTE)==3
old.PALETTE=old.PALETTE+[('entrance_step_gray_background_approximation','#90958C')]
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==2450 and np.bincount(colors).tolist()==[2391,33,26]
 assert len(TARGET)==12 and (colors[TARGET]==0).all()
 colors[TARGET]=3;why[TARGET]='complete_entrance_tread_riser_gray_background_only'
 assert np.bincount(colors).tolist()==[2379,33,26,12]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Only12 entrance tread/riser triangles additionally use new gray background material3. Original3 shaders and2438 other indices unchanged. Yellow fine nosings not modeled: this does not imply uniform real gray stairs. Coarse3step count and original5.1 gap retained. Side skirts/door/platform excluded.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
