"""Extend front aggregate-gray to original outer parapet planes only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'parapet-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.001;c[m]=1;w[m]='original_outer_roof_parapet_vertical_pale_wall_family_inference';selected+=ids
 assert len(selected)==len(set(selected))==20;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=20,face_ids=sorted(selected),outer_plane_groups=4,inner_cap_shortends_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve2934published colored faces/reasons and5colors. Add20original outer parapet vertical faces in palegray1 as bounded same-wall-family inference; rear segment not separately photographed. Inner parapet,top,shortends,collectors,roof,balcony and window proxies unchanged. Original4240triangles2108vertices andSTL unchanged; no2026current condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
