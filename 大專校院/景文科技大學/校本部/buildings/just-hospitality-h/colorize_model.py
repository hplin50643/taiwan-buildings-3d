"""Whole original right tower uppermost cap front fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='ae110755183d79ba5b17b45ec048529ca0730eff43a91c68dab1e5b7ed482a13';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1476
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+21).max(1)<e)
assert len(ids)==2
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert sorted(map(len,pcs))==[2]
D['whole_right_tower_cap_front']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,1474]
pal=[('JUST Hospitality H observed tower cap front light gray','#CBCDC8'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1476 original triangles unchanged','limits':['Tower front includes banner/lettering and slit-window details; not full gray.', 'Tower glazed return mixes glass and framework; no full blue/gray backing.', 'Cap top, underside, side returns, supports and rear are not inferred from the front fascia.', 'Main facade has window frames, AC units, wall variation and low-level transitions not isolated as original material domains; no blanket tan facade.', 'Rooftop stair/mechanical enclosure, roof surface, terrace/landscape proxy and base remain neutral.', 'Unseen rear and neighboring background building excluded; all unlisted faces remain neutral.', 'Preserve1476 original faces; no geometry edits, new openings, face boundaries or OBJ generation.', 'Use actual five-rank photographic building evidence, not official273illustration as color evidence.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1476,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
