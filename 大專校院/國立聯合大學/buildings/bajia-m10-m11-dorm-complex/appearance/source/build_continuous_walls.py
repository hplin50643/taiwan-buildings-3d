"""Bounded same-fin-family inference on existing rear fins; not rear photographic proof."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'rear-fin-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();selected=[]
 for d in DOMAINS:
  side=d['wing'];ang=np.deg2rad(-side*24);q=tri.copy();q[:,:,0]-=side*38;q[:,:,1]-=8;u=q.copy();u[:,:,0]=q[:,:,0]*np.cos(ang)+q[:,:,1]*np.sin(ang);u[:,:,1]=-q[:,:,0]*np.sin(ang)+q[:,:,1]*np.cos(ang)
  cr=np.cross(u[:,1]-u[:,0],u[:,2]-u[:,0]);lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((u>=lo-.00003)&(u<=hi+.00003),axis=(1,2))&np.all(abs(u[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];c[m]=1;w[m]='original_rear_fin_outward_vertical_faces_pale_same_family_inference_not_rear_photo';selected+=ids
 assert len(selected)==len(set(selected))==3252;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=len(selected),face_ids=sorted(selected),groups=162,rear_fins=54,only_original_outward_vertical_planes=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve all8174published colored faces and reasons. Add3252original outward vertical fin triangles on54rear fins in palegray1,explicit same-family inference only,not rear photographic evidence. Rear infill,windows,roof,ground and fin horizontal/back planes unchanged. All28008faces,13884vertices,6materials and originalSTL unchanged. Simplified symmetric rear fins are existing geometry,not newly surveyed. No2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
