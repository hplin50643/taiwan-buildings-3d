from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
DOMAINS=json.loads((Path(__file__).parent/'rear-roof-domains.json').read_text())['groups']
def classify(tri):
 c,r=base_classify(tri);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);selected=[];areas=[];eps=.00003
 for g in DOMAINS:
  u=(tri[:,:,1]-g['y0'])/(g['y1']-g['y0']);m=(abs(tri[:,:,2]-(g['z0']+(g['z1']-g['z0'])*u))<eps).all(1)&(u>=-eps).all(1)&(u<=1+eps).all(1)&(tri[:,:,0]>=-15.5-eps).all(1)&(tri[:,:,0]<=15.5+eps).all(1)&(cross[:,2]>0)
  ids=np.flatnonzero(m).tolist();assert ids==g['ids'];assert len(ids)==2 and not c[m].any();assert len(np.unique(tri[m].reshape(-1,3),axis=0))==4;area=float(np.linalg.norm(cross[m],axis=1).sum()/2);assert abs(area-g['analytic_area'])<.0002
  c[m]=3;r[m]='central_rear_roof_original_profile_strip_same_charcoal_tile_inference';selected.extend(ids);areas.append(area)
 assert len(selected)==18
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=18,face_ids=sorted(selected),complete_original_strips=9,area_mm2=sum(areas),ridge_gables_and_sidehips_excluded=True),indent=2)+'\n')
 return c,r
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Preserve all5775publishedcolored faces and originalreasons. Extend18complete centralrear roofstrip triangles samecharcoal tile3 by same-rooffamily inference. Ridge,gables,sidehips andall otherfaces unchanged.No2026claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
