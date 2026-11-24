"""Extend metal canopy upper-family color onto original outward perimeter profiles only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'canopy-edge-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.001;c[m]=7;w[m]='original_thickened_roofcanopy_outer_edge_graymetal_family_inference';selected+=ids
 assert len(selected)==len(set(selected))==268;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=268,face_ids=sorted(selected),outer_plane_groups=4,notch_walls_horizontal_internal_seams_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve18685published colored faces/reasons and8colors. Add268original outer metalcanopy edge faces in graymetal7 as same-component inference on original printability-thickened solid backing. Roof top/internal seams,walls and inferred notch cutfaces unchanged. Original21246triangles10419vertices andSTL unchanged; noPV,no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
