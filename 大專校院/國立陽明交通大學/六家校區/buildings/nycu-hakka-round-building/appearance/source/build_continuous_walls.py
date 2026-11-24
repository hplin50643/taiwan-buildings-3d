"""Extend existing silver roof color onto highest central fan outer edge only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'fan-edge-domains.json').read_text())['groups']
def classify(tri):
 c,w=base_classify(tri);before=c.copy();cr=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[]
 for d in DOMAINS:
  ends=np.array(d['endpoints_xy']);direction=ends[1]-ends[0];length=np.linalg.norm(direction);direction/=length;out=np.array(d['normal_xy']);along=(tri[:,:,:2]-ends[0])@direction;plane=tri[:,:,:2]@out
  m=np.all(abs(plane-d['plane_offset'])<.00002,1)&np.all((along>=-.00002)&(along<=length+.00002),1)&np.all((tri[:,:,2]>=d['z_min']-.00002)&(tri[:,:,2]<=d['z_max']+.00002),1)&(cr[:,:2]@out>0)&(c==0)
  ids=np.flatnonzero(m).tolist();assert ids==d['ids'];assert len(np.unique(tri[m].reshape(-1,3),axis=0))==4;assert abs(float(np.linalg.norm(cr[m],axis=1).sum()/2)-d['analytic_area'])<.00002;c[m]=2;w[m]='highest_central_fan_original_outer_chord_silver_same_roof_inference';selected+=ids
 assert len(selected)==len(set(selected))==66;assert np.array_equal(c[before!=0],before[before!=0]);(A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=66,face_ids=sorted(selected),finite_chord_groups=33,all_other_roof_and_body_faces_unchanged=True),indent=2)+'\n');return c,w
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['historical_scope']=d['scope'];d['scope']='Preserve29603published colored faces/reasons and6colors. Add66highestcentral fan outeredge faces in silver2,33complete original chordrectangles r51 angle57..123deg z48.4..50.4. Same-roof inference only on original thick stepped approximation,not exact sheetedge survey. Top/bottom/radialends/innerarc/lowersidefans/supports/body unchanged. Original35084triangles17374vertices andSTL unchanged; no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
