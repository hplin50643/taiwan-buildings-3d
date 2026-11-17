"""Extend only two complete original main roof left hip triangles."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAIN=json.loads((Path(__file__).parent/'left-roof-domain.json').read_text())
def classify(tri):
 c,r=base_classify(tri);u=(tri[:,:,2]-71)/4;eps=3e-5
 cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None]
 m=(abs(tri[:,:,0]-(-64.5+15.82*u))<eps).all(1)&(u>=-eps).all(1)&(u<=1+eps).all(1)&(abs(tri[:,:,1]+26)<=15-14.55*u+eps).all(1)&(norm@np.array(DOMAIN['domain']['normal'])>.99999)
 ids=np.flatnonzero(m).tolist();assert ids==DOMAIN['ids']==[485,486];assert not c[m].any();t=tri[m];assert len(np.unique(t.reshape(-1,3),axis=0))==4
 area=float(np.linalg.norm(cross[m],axis=1).sum()/2);assert abs(area-DOMAIN['domain']['analytic_area_mm2'])<3e-5
 c[m]=1;r[m]='main_roof_complete_left_hip_historical_terracotta_component_inference'
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=2,face_ids=ids,area_mm2=area,analytic_area_mm2=DOMAIN['domain']['analytic_area_mm2'],complete_original_trapezoid=True),indent=2)+'\n')
 return c,r
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Original9frontroof and42windowback faces preserved;2complete mainroof left hip triangles extend samehistorical terracotta by component inference.1389remaining neutral;no other slope or mixedwall recoloring.No2026claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
