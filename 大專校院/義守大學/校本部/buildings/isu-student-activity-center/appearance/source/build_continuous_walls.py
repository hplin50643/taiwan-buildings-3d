"""Extend existing opaque brick color onto two original east upper bands only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'east-brick-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.001;c[m]=1;w[m]='east_upper_original_brick_face_same_family_extension_partly_obscured_evidence';selected+=ids
 assert len(selected)==len(set(selected))==164;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=164,face_ids=sorted(selected),outer_plane_groups=2,south_windows_whitebelts_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve238published brickfaces/reasons and2colors. Add164eastupper completeoriginal brickfaces in existing opaque brick1; official poolside photo supports materialfamily with partialobstruction/undated limits. Whitebelts,windows/reveals,lowerwalls,columns,roof,southrear unchanged. Original9626triangles4775vertices andSTL unchanged; no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
