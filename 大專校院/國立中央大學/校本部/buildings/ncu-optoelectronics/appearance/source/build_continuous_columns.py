"""Inferred same-column material continuity, not a new rear-photo claim."""
from pathlib import Path
import importlib.util,json,numpy as np
S=Path(__file__).resolve().parent;A=S.parent
sp=importlib.util.spec_from_file_location('current',S/'build_current.py');cur=importlib.util.module_from_spec(sp);sp.loader.exec_module(cur)
prior=cur.old.classify
ADDED=[1075,1076,1077,1078,1080,1081,1083,1084,1085,1086,1087,1089,1091,1092,1093,1094,1096,1097]
def classify(tri):
 c,w=prior(tri)
 assert np.bincount(c).tolist()==[2596,1494,42,6]
 selected=np.zeros(len(tri),bool)
 for x in [-22,0,22]:
  selected |= np.all((abs(tri[:,:,0]-x)<=1.202)&(tri[:,:,1]>=-44.502)&(tri[:,:,1]<=-39.498)&(tri[:,:,2]>=2.999)&(tri[:,:,2]<=38.002),axis=1)
 selected &= c==0
 assert np.where(selected)[0].tolist()==ADDED
 c[selected]=3;w[selected]='inferred_continuous_same_central_column_side_rear_material_not_photo_verified'
 assert np.bincount(c).tolist()==[2578,1494,42,24]
 return c,w
cur.old.classify=classify
if __name__=='__main__':
 cur.old.main()
 p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Central three columns: original six front faces plus18 same-column side/rear triangles use existing pale gray #C5C5BB by inferred material continuity. No independent side/rear photo claim. Other4114 triangles and all geometry unchanged; no extension to walls, recesses, roof, soffit or base.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
