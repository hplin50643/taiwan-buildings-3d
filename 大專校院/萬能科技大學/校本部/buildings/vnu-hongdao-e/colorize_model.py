"""Whole original raised central cap front plane only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='849ff897b43e89109e8fdc6d750fe8fa80505b84b0763cfb4f7277d4bd04ebfb';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1094
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+57.5).max(1)<e)
assert len(ids)==2
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1;assert all(len(c)==2 for c in pcs)
D['whole_high_cap_front']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,1092]
pal=[('VNU Hongdao E observed high cap gray brown','#918B82'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1094 original triangles unchanged','limits':['Cap upper surface, underside, left/right returns and broad main roof remain neutral.', 'Tall front pilasters extend through low regions and meet multiple facade elements; no blanket nominal tan coloring from partial visibility.', 'Entry entablature contains gold lettering; do not uniformly color it.', 'Main front/side wall fields, windows with frames/reflections, hidden ground and vegetation-obscured base remain neutral.', 'All other original faces remain neutral.', 'Preserve1094 original triangles, no geometry editing or new material cut. No OBJ generated.', 'Local review only: no new download, Git mutation, photo publication or formal GO.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1094,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
