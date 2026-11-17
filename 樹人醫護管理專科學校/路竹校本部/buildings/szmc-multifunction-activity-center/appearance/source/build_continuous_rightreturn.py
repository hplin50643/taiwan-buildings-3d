from pathlib import Path
import json,hashlib,numpy as np,collections
from build_appearance import read_stl,model_root,add_mesh,sub,write_zip
S=Path(__file__).resolve().parent;A=S.parent;Q=A/'qa-continuous-rightreturn';Q.mkdir(exist_ok=True);r=json.load(open(S/'rightreturn-domain.json'));H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(A.parent/'model.stl')==r['source_stl_sha256'];assert H(S/'baseline-face-materials.json')==r['source_face_materials_sha256'];assert H(A/'palette.json')==r['source_palette_sha256']
v,f=read_stl(A.parent/'model.stl');v=np.array(v);f=np.array(f);t=v[f];old=json.load(open(S/'baseline-face-materials.json'));a=np.array(old['face_material_indices']);before=a.copy();assert np.bincount(a).tolist()==r['baseline_counts'];ids=r['face_ids'];assert ids==[928,941];g=r['groups'][0];normal=np.array(g['normal']);cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n=cross/np.linalg.norm(cross,axis=1)[:,None];sel=np.flatnonzero((abs((t-t[928,0])@normal)<1e-5).all(1)&(n@normal>.999999)).tolist();assert sel==ids;assert np.array_equal(np.unique(t[ids].reshape(-1,3),axis=0),np.array(g['float_corners']));assert abs(np.linalg.norm(cross[ids],axis=1).sum()/2-g['analytic_area_mm2'])<1e-4;assert(a[ids]==0).all();a[ids]=1;assert np.bincount(a).tolist()==r['counts_after'];assert np.array_equal(a[before!=0],before[before!=0]);assert a[916]==before[916]==0
# Preserve historical mixed domains exactly; do not repair old classifier decisions.
par=list(range(len(f)));edges={}
def root(i):
 while par[i]!=i:par[i]=par[par[i]];i=par[i]
 return i
for i,face in enumerate(f):
 for k in range(3):
  e=tuple(sorted([int(face[k]),int(face[(k+1)%3])]))
  if e in edges:
   j=edges[e]
   if np.dot(n[i],n[j])>.999999:par[root(i)]=root(j)
  edges[e]=i
groups={}
for i in range(len(f)):groups.setdefault(root(i),[]).append(i)
mb=[g for g in groups.values()if len(set(before[g]))>1];ma=[g for g in groups.values()if len(set(a[g]))>1];assert mb==ma and len(mb)==21
np.savez_compressed(A/'mesh-data.npz',vertices=v,faces=f,materials=a);pal=json.load(open(A/'palette.json'))['materials'];out=dict(old);out['face_material_indices']=a.tolist();out['material_face_counts']={pal[i]['id']:int(c)for i,c in enumerate(np.bincount(a))};out['current_continuity_extension']={'changed_faces':ids,'target_material':1,'scope':'Only two original rightendfold slantedreturn faces; samepanel inference. Original965colors,21historicalmixed domains,allother3170faces and bottom916 unchanged.'};(A/'face-materials.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
r3,res=model_root('SZMC original right folded-panel limited color continuation',pal);add_mesh(res,1,'SZMC original3172 triangles',v.tolist(),f.tolist(),a.tolist());sub(sub(r3,'build'),'item',objectid=1);write_zip(A/'szmc-appearance.3mf',r3)
(Q/'selection-preservation.json').write_text(json.dumps(dict(changed_faces=ids,original965colors_preserved=True,other3170faces_unchanged=True,original_STL_geometry_order_exact=True,palette_original_bytes=True,baseline_counts=np.bincount(before).tolist(),counts=np.bincount(a).tolist(),coplanar_domains=len(groups),historical21mixed_domains_unchanged=mb,new_mixed_domains=0,bottom916_unchanged=True),indent=2)+'\n')
