from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'rib-side-domains.json').read_text())
def classify(tri):
 c,r=base_classify(tri);t=tri/1.5-np.array([17,2,0]);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];knots=np.array([(-12.5,30.8),(-7,31.5),(-1,31.8),(1,31.8),(7,31.5),(12.5,30.8)]);selected=[];total=0
 for g in DOMAINS:
  ids=[]
  for i in np.flatnonzero(np.all(abs(t[:,:,1]-g['working_y'])<1e-5,axis=1)&(norm[:,1]*g['side']>.9999)):
   p=t[i][:,[0,2]];samples=list(p)
   for a,b in zip(p,np.roll(p,-1,axis=0)):
    if abs(a[0]-b[0])<1e-7:continue
    for x in knots[:,0]:
     f=(x-a[0])/(b[0]-a[0])
     if 0<f<1:samples.append(a+f*(b-a))
   q=np.array(samples);off=q[:,1]-np.interp(q[:,0],knots[:,0],knots[:,1])
   if min(q[:,0])>=-12.5-1e-5 and max(q[:,0])<=12.5+1e-5 and min(off)>=-1e-5 and max(off)<=.28+1e-5:ids.append(int(i))
  assert ids==g['faces'];assert len(ids)==10 and not c[ids].any();area=float(np.linalg.norm(cross[ids],axis=1).sum()/2);assert abs(area-g['analytic_area_mm2'])<.0001
  c[ids]=1;r[ids]='whole_original_white_rib_thin_side_same_component_material_inference';selected.extend(ids);total+=area
 assert len(selected)==len(set(selected))==180
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=180,face_ids=sorted(selected),nine_ribs_both_sides=True,all_vertex_and_edge_polyline_intersections_checked=True,area_mm2=total,analytic_area_mm2=283.5),indent=2)+'\n')
 return c,r
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['scope']='All190oldwhite and14oldredfaces/reasons preserved.180complete original thin ribside faces extend samewhite materialfamily by explicit inference;3994othersneutral. No wholewall,mainroofendcap orunderside expansion.No2026claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
