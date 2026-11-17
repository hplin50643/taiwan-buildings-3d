"""Extend existing tile-family color to original opaque wall planes, no geometry edits."""
from pathlib import Path
import importlib.util,json,hashlib,struct
import numpy as np
S=Path(__file__).resolve().parent;A=S.parent;R=A.parent
sp=importlib.util.spec_from_file_location('current',S/'build_current.py');current=importlib.util.module_from_spec(sp);sp.loader.exec_module(current)
prior=current.classify
def classify(tri):
 colors,why=prior(tri);lo=tri.min(1);hi=tri.max(1);eps=.00015
 wall=np.zeros(len(tri),dtype=bool)
 for axis,value in [(0,-63),(0,63),(1,43)]:
  wall |= np.all(abs(tri[:,:,axis]-value)<eps,axis=1)
 mask=wall&(lo[:,2]>=3-eps)&(hi[:,2]<=107+eps)&(colors==0)
 assert mask.sum()==42
 colors[mask]=3;why[mask]='inferred_continuous_main_body_opaque_wall_tile_family_not_reverse_photo_verified'
 return colors,why
if __name__=='__main__':
 current.old.classify=classify;current.old.main()
 p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Existing front, glazing, crossbars and 12 step faces preserved. Additional 42 complete opaque main-body exterior wall faces on x=+-63 and y=43 use existing material 3 #BEB7AE by explicitly inferred material continuity. Not separately photo-verified side/rear colors. Roof, cornice, base, side slot recesses and mixed ground bays remain unchanged. No geometry change.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
