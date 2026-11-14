"""Material-only current wrapper. The historical classifier source stays unchanged."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
S=Path(__file__).resolve().parent; A=S.parent
spec=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py'); old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
original_classify=old.classify
TARGET=[8253,8259]
def classify(tri):
 colors,why=original_classify(tri)
 assert len(tri)==8666 and np.bincount(colors).tolist()==[8652,12,2]
 assert all(colors[i]==0 for i in TARGET)
 assert (abs(tri[TARGET,:,2]-101)<1e-8).all()
 colors[TARGET]=1
 why[TARGET]='bounded_front_cap_underside_existing_brick_family_approximation'
 assert np.bincount(colors).tolist()==[8650,14,2]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main()
 p=A/'palette.json'; j=json.loads(p.read_text())
 j['historical_scope']=j['scope']
 j['scope']='Original 14 classified faces preserved, plus only two complete downward shallow front-cap triangles at z101, x[-61.75,61.75], y[14.5,16], using existing brick-family material. No geometry change; not brick-species or calibrated color certification. Coarse modeled depth and end positions are not surveyed. No extension to side/rear cap, glazing, low wing or roof top.'
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 print('CURRENT_COUNTS', [8650,14,2])
