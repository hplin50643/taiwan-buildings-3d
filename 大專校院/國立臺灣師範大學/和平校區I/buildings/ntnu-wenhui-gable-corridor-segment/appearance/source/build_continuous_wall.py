"""Inferred continuous left wall/base colors; cropped rear stays neutral."""
from pathlib import Path
import importlib.util,json,numpy as np
S=Path(__file__).resolve().parent;A=S.parent
s=importlib.util.spec_from_file_location('original',S/'build_appearance.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old);prior=old.classify
ADDED_BRICK=[57,97,226,227,260,261];ADDED_STONE=[25,31]
def classify(t):
 c,w=prior(t);lo=t.min(1);hi=t.max(1)
 brick=np.all(abs(t[:,:,0]+56)<.0002,axis=1)&(lo[:,2]>=9.7998)&(hi[:,2]<=55.7502)&(lo[:,1]>=-24.5002)&(hi[:,1]<=40.5002)&(c==0)
 stone=np.all(abs(t[:,:,0]+58)<.0002,axis=1)&(lo[:,2]>=2.9998)&(hi[:,2]<=9.8002)&(lo[:,1]>=-24.5002)&(hi[:,1]<=40.5002)&(c==0)
 assert np.where(brick)[0].tolist()==ADDED_BRICK and np.where(stone)[0].tolist()==ADDED_STONE
 c[brick]=1;w[brick]='inferred_same_hall_left_wall_brick_continuity_not_photo_verified'
 c[stone]=2;w[stone]='inferred_same_raised_base_left_side_stone_continuity_not_photo_verified'
 return c,w
old.classify=classify
if __name__=='__main__':
 old.main();p=A/'palette.json';j=json.loads(p.read_text());j['scope']='Original registered front plus inferred continuous left hall wall (6 triangles) and left raised base (2 triangles). Same existing brick/stone palette; no new photograph claim. Artificial rear cut, roof, corridor and side-window recesses unchanged.';p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
