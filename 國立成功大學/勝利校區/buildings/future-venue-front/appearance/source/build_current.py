"""Current bounded portal returns, original classifier and shader values unchanged."""
from pathlib import Path
import importlib.util,json
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('historical_build',S/'build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
original_classify=old.classify
TARGET=[4101, 4102, 4104, 4106, 4112, 4114, 4116, 4117, 4122, 4123, 4126, 4127, 4128, 4129, 4137, 4138, 4154, 4158]
assert len(old.PALETTE)==5
def classify(tri):
 q=A/'qa/material-boundaries.json';saved=q.read_bytes() if q.exists() else None
 try:colors,why=original_classify(tri)
 finally:
  if saved is not None:q.write_bytes(saved)
  elif q.exists():q.unlink()
 assert len(tri)==5044 and np.bincount(colors).tolist()==[4533, 372, 120, 17, 2]
 assert len(TARGET)==18 and (colors[TARGET]==0).all()
 colors[TARGET]=3;why[TARGET]='complete_portal_inner_cheeks_and_top_underside_only'
 assert np.bincount(colors).tolist()==[4515, 372, 120, 35, 2]
 return colors,why
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['historical_scope']=j['scope'];j['scope']='Current adds18 complete portal inner-cheek/top-underside faces to existing white material3. Original5 shader values unchanged. Material id front_only and historical511face statement are historical, current529colored/4515neutral. Bottom floor, stairs, rear glazing excluded. Original7.2 exposed depth and left3 window notches retained; coarse proxy, fine columns/luminaires absent.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
