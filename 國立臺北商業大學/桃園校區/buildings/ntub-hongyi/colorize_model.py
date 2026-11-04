"""Whole original front stair-tower cap edge plane y-64, two complete rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='e5c014bb143e5c8682be55e3bfb4022121c06a6594ad28cfcfeb12f3cddd7153';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==21916
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+64).max(1)<e)
assert len(ids)==4
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2,2]
D['whole_front_tower_cap_edges']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[4,21912]
pal=[('NTUB Hongyi observed front tower caps pale warm gray','#C9C5BB'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'21916 original triangles unchanged','limits':['Cap horizontal top skins, undersides and side/back returns remain neutral.', 'Tower shafts carry lettering, fixtures and tree-obscured lower zones; do not extend pale color down full walls.', 'Glazing contains reflections, frames and floors; no blanket blue glazing backing.', 'Outer shallow hips, rear service caps and roof equipment/PV location remain unverified and neutral.', 'Terrace canopy, solid balcony proxies, brick/gray mixed walls, other fascias, supports and all unlisted triangles remain neutral.', 'Preserve21916 original faces and geometry.', 'Original overall massing/evidence-backed facade approximation, not a measured full-condition reconstruction.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':21916,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
