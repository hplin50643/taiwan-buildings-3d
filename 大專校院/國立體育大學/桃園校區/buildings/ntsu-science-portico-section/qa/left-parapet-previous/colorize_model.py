"""Whole original lower slab outer chord facets only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='93cb3e2b361f55b50301286b8b4242ce8e538814a084d95871cd37780adfa224';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5086
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
angles=np.linspace(-np.deg2rad(42),np.deg2rad(42),65)
pts=np.c_[88.5*np.sin(angles),49-88.5*np.cos(angles)]
for j,(p,q) in enumerate(zip(pts[:-1],pts[1:])):
 u=q-p;L=np.linalg.norm(u);u/=L;normal=np.array([-u[1],u[0]])
 delta=t[:,:,:2]-p;dist=delta@normal;along=delta@u
 plane=np.abs(dist).max(1)<e
 finite=plane&(along.min(1)>=-e)&(along.max(1)<=L+e)&(t[:,:,2].min(1)>=17.6-e)&(t[:,:,2].max(1)<=19.8+e)
 ids=np.flatnonzero(finite);assert len(ids)==2;assert np.array_equal(ids,np.flatnonzero(plane))
 assert len(set(m.faces[ids[0]])&set(m.faces[ids[1]]))==2
 D[f'lower_slab_outer_facet_{j:02d}']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[128,4958]
pal=[('Observed lower slab outer curved vertical edge pale gray','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5086 original triangles unchanged','limits':['All upper parapet faces including text field and openings: lettering has no independent material boundary in original mesh.', 'All cylindrical columns: stickers/notices and patterned feet mix within full-height original facets.', 'Slab top, dark underside, inner edge and end caps do not inherit front-edge color.', 'Main wing walls mix brick, pale upper bands and base/obscured regions without matching original boundaries; all remain neutral.', 'Glass, window proxies, stair/ground surfaces, plain side/rear section cuts and all unknown faces neutral.', 'Concave-corner science portico and cropped wing sections only, not entire complex or interior.', 'Retain original README older appearance and2021 wall/2024 AC context. These source dates and planning notes do not certify2026 current facade; exact photography dates unknown.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':5086,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
