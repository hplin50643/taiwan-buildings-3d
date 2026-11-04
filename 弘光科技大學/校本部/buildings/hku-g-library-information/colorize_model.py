"""Whole original exposed clerestory fin fronts only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='c6a397ca8dde8d4492c6228a378c443fa54fda7760e9afc14a1f04196ff7413c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2492
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+25.1).max(1)<e)
assert len(ids)==50
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==25;assert all(len(c)==2 for c in pcs)
D['whole_25_exposed_fin_fronts']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[50,2442]
pal=[('Observed25 exposed clerestory fin front faces offwhite','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2492 original triangles unchanged','limits':['Glazing/window backs include frames, reflection and interior contents; no blanket dark.', 'Lettered圖書館 wall and broad body mix inscription, stone and shadow domains; neutral.', 'Terracotta upper roof-canopy, its underside and far roof are not selected without further precise domain proof.', 'Left gray block, steps, entrance, base and unseen rear remain neutral.', 'Higher rear teaching volume and right tower not supported by this newly inspected front image remain neutral; no new Commons retrieval or inferred current colors.', 'One existing front-library/rear-information group; only lower front fin material reviewed. No separate duplication of library and information names.', 'Photography date unknown; source publication date does not guarantee2026 state.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':2492,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
