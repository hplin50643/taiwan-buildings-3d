"""Seven complete original central short rib end rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='99578e16887d6d610bd1b7a1f132337bb002a133f816ff6cdce136b34ebc5e3d';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3438
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+10).max(1)<e)
assert len(ids)==18
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2]*9
selected=[]
for c in pcs:
 q=t[c];center=(q[:,:,0].min()+q[:,:,0].max())/2
 if any(abs(center-v)<e for v in [-48,-32,-16,0,16,32,48]):
  assert len(c)==2 and abs(q[:,:,0].max()-q[:,:,0].min()-1.5)<e
  D['complete_central_rib_end_'+str(round(center))]=c.tolist();selected.extend(c)
assert len(selected)==14;a[selected]=0
original=a.copy();candidate=np.zeros(len(t),bool)
for cx in [-32,-16,0,16,32]:
 inside=(t[:,:,0].min(1)>=cx-.7501)&(t[:,:,0].max(1)<=cx+.7501)&(t[:,:,1].min(1)>=-10.0001)&(t[:,:,1].max(1)<=2.0001)&(t[:,:,2].min(1)>=64.9999)&(t[:,:,2].max(1)<=69.1001)
 bottom=(abs(t[:,:,2]-65).max(1)<.0001)&(n[:,2]<-.99)
 side=(abs(t[:,:,0]-(cx+(.75 if cx<0 else -.75))).max(1)<.0001)&((n[:,0]>.99)if cx<0 else(n[:,0]<-.99)) if cx else np.zeros(len(t),bool)
 candidate|=inside&(bottom|side)
ad=m.face_adjacency;cs=trimesh.graph.connected_components(ad[(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(t)),min_len=1)
assert candidate.sum()==18 and np.all(original[candidate]==1)
assert all(not candidate[c].any() or candidate[c].all() for c in cs)
a[candidate]=0;assert np.bincount(a).tolist()==[32,3406] and all(len(set(a[c]))==1 for c in cs)
pal=[('Observed rib fronts and bounded five rib bottom four inward sides pale cream','#D3D0C0'),('Unverified other original geometry neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'original_domain_face_indices':D,'new_face_indices':np.flatnonzero(candidate).tolist(),'original_colored_faces':14,'added_colored_faces':18,'colored_faces':32,'neutral_faces':3406,'coplanar_components':len(cs),'mixed_coplanar_domains':0,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3438 original triangles and STL/build bytes unchanged','limits':['Only five central rib bottoms plus inward-facing sides of four noncentral ribs; nominal uncalibrated pale-cream family, not per-pixel colors.','Same official photograph re-examined at native pixels; not a newly discovered angle. Exact simplified depth remains an inference, not a survey.','Ribs x=+/-48 have different real bracket junctions: no new color there. Central rib sides, outward sides, outer ribs, broad canopy and artificial rear cut stay unchanged.','Original illustrative20mm entrance section not entire gym or measured rear.','Photograph capture date unknown, no2026 condition claim; source private.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3438,'original':14,'added':18,'colored':32,'neutral':3406,'mixed_coplanar_domains':0,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2)+'\n');print(q)
