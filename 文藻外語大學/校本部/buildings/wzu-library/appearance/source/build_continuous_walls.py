"""Preserve original firstseen vertexorder and external palette; extend finite eave edges only."""
from pathlib import Path
import json,numpy as np
import build_appearance as old
A=old.OUT;base_classify=old.classify;base_model_root=old.model_root
def model_root(title,palette):
 root,res=base_model_root(title,palette)
 for node in root:
  if node.tag==old.TAG('metadata') and node.get('name')=='Description':node.text='Editable unchanged surface colors. Original front palette retained; eight finite outer eave-edge faces extend cream as component inference. Body side/rear and roof tops neutral; no physical print validation.'
 return root,res
DOMAINS=json.loads((Path(__file__).parent/'eave-domains.json').read_text())['groups']
def classify(vs):
 c,r=base_classify(vs)
 if c:return c,r
 t=np.asarray(vs);n=np.cross(t[1]-t[0],t[2]-t[0])
 for d in DOMAINS:
  lo,hi=np.array(d['bounds']);axis=d['axis']
  if np.all((t>=lo-.00003)&(t<=hi+.00003)) and np.all(abs(t[:,axis]-d['value'])<.00003) and n[axis]*d['normal_sign']>0:return 3,'whole_original_eave_outer_side_rear_cream_component_inference'
 return c,r
def main():
 old.classify=classify;old.model_root=model_root;old.main();v,f=old.read_stl(old.ROOT/'model.stl');tri=np.array(v)[np.array(f)];before=[base_classify(t) for t in tri];after=[classify(t) for t in tri];ids=[i for i,(b,a) in enumerate(zip(before,after)) if b!=a];assert ids==sorted(i for d in DOMAINS for i in d['ids']);assert len(ids)==8
 for d in DOMAINS:
  t=tri[d['ids']];assert len(np.unique(t.reshape(-1,3),axis=0))==4;area=float(np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1).sum()/2);assert abs(area-d['analytic_area'])<.0001
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(changed_faces=8,face_ids=ids,finite_rectangles=4,service_tower_and_window_cutout_retained=True),indent=2)+'\n')
 p=A/'face-materials.json';d=json.loads(p.read_text());d['face_reasons']=[r for c,r in after];d['unknown_backside']='Body neutral;only bounded original eave edge receives samecomponent cream inference.';d['roof']='Top/soffit and tower neutral;left/right and two rear eave rectangles cream3. Rightrear startsx66.75 due original towerwindow cutout;no repair.';d['current_extension']='8previouslyneutral eave triangles,5236oldcolored faces and original roles preserved;no2026condition or physicalprint claim.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
