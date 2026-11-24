"""Whole original clerestory cap front and left components."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='dd7530e7ab3e3dcacf5bc643059055688ea1c9b81e12f0126c85780feb93a149';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3096
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ax,p,count in [('cap_front',1,-39.5,86),('cap_left',0,-29,2)]:
 ids=np.flatnonzero(np.abs(t[:,:,ax]-p).max(1)<e)
 edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
 pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);selected=[]
 for c in pcs:
  v=t[c];inside=(v[:,:,0].min()>=-29-e and v[:,:,0].max()<=29+e and v[:,:,1].min()>=-39.5-e and v[:,:,1].max()<=-4.5+e and v[:,:,2].min()>=43.5-e and v[:,:,2].max()<=46.1+e)
  if inside:selected.extend(c.tolist())
 assert len(selected)==count;D[name]=sorted(selected);a[selected]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[88,3008]
pal=[('Observed elevated cap front and left vertical fascia pale gray','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3096 original triangles unchanged','limits':['Entire lower main roof fascia bears gold and black lettering without corresponding original material boundaries; keep neutral.', 'Cap top, back and right edges, underside and separate dentil faces remain neutral; only front and visible left vertical faces are recommended.', 'Corner lattice is thick solid-backed relief approximating open frame plus pink/red filled triangles; do not color the entire backing or arbitrary triangles pink.', 'Clerestory window backs, pier fluting, portico piers and other walls have mixed depths, contents or uncertain fine boundaries; remain neutral.', 'Rear barrel roof and its ends are not expanded in this limited review.', 'Base, entry steps, unknown/rear and concealed surfaces neutral.', 'Former Chung-Cheng Hall converted to Food Biotechnology Pilot Plant, Taitung city campus; one building group, no equipment/interior representation.', 'Photo capture dates unknown; no assertion of unchanged2026 condition.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3096,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
