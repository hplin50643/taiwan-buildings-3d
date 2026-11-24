"""Extend existing opaqueglass proxy onto nine original south narrowwindow back rectangles only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'south-slit-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.001;c[m]=3;w[m]='south_narrow_original_window_back_opaque_glazing_proxy';selected+=ids
 assert len(selected)==len(set(selected))==18;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=18,face_ids=sorted(selected),window_back_groups=9,frames_returns_walls_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve228previous glassproxy faces/reasons,84basefaces,all original native materialdatablocks and unusedslot1. Add18original southnarrow windowback triangles in existing opaqueglass3,9complete rectangles. Other8706faces unchanged. Native linearRGBA/use_nodes exact;3MF8bitsRGB quantization remains disclosed. Original8724triangles4348vertices andSTL unchanged;2001completion not photo date, no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
