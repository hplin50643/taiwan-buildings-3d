"""Extend published pale front canopy color onto two original vertical end rectangles only."""
from pathlib import Path
import json,numpy as np
import build_current as current
old=current.old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'canopy-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.001;c[m]=2;w[m]='original_canopy_two_vertical_end_rectangles_pale_same_component_inference';selected+=ids
 assert len(selected)==len(set(selected))==4;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=4,face_ids=sorted(selected),side_plane_groups=2,top_bottom_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve709published colored faces/reasons including1408/1409 and7colors. Add4original entrycanopy end faces in palegray2 as same-component inference; true hollow canopy not represented by original solid slab. Top,bottom,annexroof,shopfront and all otherfaces unchanged. Original1524triangles764vertices andSTL unchanged; no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
