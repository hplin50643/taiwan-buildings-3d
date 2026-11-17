"""Extend east entablature pale stone onto its own short lateral ends only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'entablature-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();tri=tri.copy();tri[:,:,:2]/=(150/68);tri[:,:,2]=(tri[:,:,2]-2.4)/(150/68);cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  lo,hi=np.array(d['local_bounds']);axis=d['axis'];m=np.all((tri>=lo-.00003)&(tri<=hi+.00003),axis=(1,2))&np.all(abs(tri[:,:,axis]-d['value'])<.00003,1)&(cr[:,axis]*d['normal_sign']>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_local_area'])<.001;c[m]=1;w[m]='east_original_entablature_cornice_shortends_pale_same_component_inference';selected+=ids
 assert len(selected)==len(set(selected))==8;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=8,face_ids=sorted(selected),outer_plane_groups=4,tops_bottoms_west_dome_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve4677published colored faces/reasons including6insetreturn updates and6colors. Add8eastentablature/cornice shortend faces in pale1,4complete rectangles,samecomponent inference on coarseoriginal geometry. Dome,westportico,tops/bottoms/soffits/rotunda/clock unchanged. Original32106triangles16031vertices andSTL unchanged; no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
