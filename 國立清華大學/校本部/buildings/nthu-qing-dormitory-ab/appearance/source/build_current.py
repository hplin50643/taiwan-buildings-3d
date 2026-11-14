"""Material-only wrapper around the byte-preserved historical classifier."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
classify_original=old.classify; TARGET=[33143,33153,33155]
assert len(old.PALETTE)==5
old.PALETTE=old.PALETTE+[('AB_crown_light_khaki_background_approximation','#C6C1A7')]
def classify(tri):
 color,why=classify_original(tri)
 assert len(tri)==33320 and np.bincount(color).tolist()==[30946,940,138,1032,264]
 assert (color[TARGET]==0).all();color[TARGET]=5
 why[TARGET]='bounded_front_V_crown_pale_khaki_background_not_complete_real_component'
 assert np.bincount(color).tolist()==[30943,940,138,1032,264,3]
 return color,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Historical five-material assignments preserved. Only three complete front V-crown triangles use a new pale khaki display-background approximation. Original polygon and depth are coarse; gray curved border, soffit and detailed material subdivisions are absent and not reconstructed. Not a claim of a homogeneous real crown, measured color, or current condition. Other towers are excluded.';j['materials'][5]['roughness']=.88;p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
