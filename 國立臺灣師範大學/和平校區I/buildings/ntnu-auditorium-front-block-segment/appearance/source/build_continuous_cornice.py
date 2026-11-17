"""Inferred same-cornice lateral faces, preserving cut backs and roofs."""
from pathlib import Path
import importlib.util,json,numpy as np
S=Path(__file__).resolve().parent;A=S.parent
s=importlib.util.spec_from_file_location('original',S/'build_appearance.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old);prior=old.classify
ADDED=[740,742,743,746,748,1682,1684,1685,1701,1704]
def classify(t):
 c,w=prior(t);lo=t.min(1);hi=t.max(1);mask=np.zeros(len(t),bool)
 for sign in [-1,1]:
  outer=np.all(abs(t[:,:,0]-sign*71.5)<.0002,axis=1)
  inner=np.all(abs(t[:,:,0]-sign*42.5)<.0002,axis=1)&(hi[:,1]<=-3.4998)
  mask|=(outer|inner)&(lo[:,1]>=-12.5002)&(hi[:,1]<=28.5002)&(lo[:,2]>=73.9998)&(hi[:,2]<=76.1002)&(c==0)
 assert np.where(mask)[0].tolist()==ADDED
 c[mask]=2;w[mask]='inferred_same_tower_cornice_lateral_stone_continuity_not_photo_verified'
 return c,w
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Original front appearance plus10 lateral faces of twin-tower cornice bands using existing stone by inferred material continuity. Cropped rear planes, rear corner slivers, roof tops, mixed-material tower side walls and all other indices unchanged. Not independently photo verified.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
