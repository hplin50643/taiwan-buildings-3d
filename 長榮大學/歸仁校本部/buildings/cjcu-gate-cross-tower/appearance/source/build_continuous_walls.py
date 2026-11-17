from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.A;base_classify=old.classify
REVIEW=json.loads((Path(__file__).parent/'reverse-panel-domains.json').read_text())['candidate']
def classify(tri):
 c,r=base_classify(tri);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];selected=[];total=0
 for g in REVIEW['groups']:
  eps=.00002;m=(abs(tri[:,:,0]-g['value'])<eps).all(1)&(tri[:,:,1]>=-12-eps).all(1)&(tri[:,:,1]<=12+eps).all(1)&(tri[:,:,2]>=5-eps).all(1)&(tri[:,:,2]<=150+eps).all(1)&(norm[:,0]<-.999)
  ids=np.flatnonzero(m).tolist();assert ids==g['faces'];assert not c[m].any();area=float(np.linalg.norm(cross[m],axis=1).sum()/2);assert abs(area-g['analytic_area_mm2'])<.0001
  c[m]=1;r[m]='same_original_slab_reverse_broad_face_light_brick_red_material_inference';selected.extend(ids);total+=area
 assert sorted(selected)==REVIEW['faces'] and len(selected)==126
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=126,face_ids=sorted(selected),area_mm2=total,analytic_area_mm2=REVIEW['analytic_area_mm2'],apertures_tie_contacts_caps_edges_retained=True),indent=2)+'\n')
 return c,r
def main():
 old.classify=classify;old.main();p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Preserve126oldpositiveXbroadredfaces/reasons;126originalnegativeXbroadfaces extend same slab redfamilybyexplicitinference.248neutral,252red. Narrowedges,caps,aperturereveals,ties,base unchanged.No2026claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
