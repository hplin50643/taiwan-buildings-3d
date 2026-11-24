"""Whole original long rooftop fascia front plane only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='662a2e1b078e24446b4f6ab1d5758be8553d33824e5d82cead51aad301612439';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3336
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+10.5).max(1)<e)
assert len(ids)==2
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1;assert all(len(c)==2 for c in pcs)
D['whole_long_roof_fascia_front']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[2,3334]
pal=[('Meiho B observed long roof fascia pale gray','#D3D6D2'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3336 original triangles unchanged','limits':['Roof upper skin and dark underside are not approved by this fascia-only recommendation.', 'Left gabled shelter, its glass backing and all rooftop posts/screens remain neutral; left and right shelters are one building, not separate models.', 'Broad front wall contains circular openings and transitions to lower material/occluded base; no all-wall white or triangular material split.', 'Window backing contains frames/reflection and equipment; neutral.', 'Ground canopy, side/rear walls, hidden base, steps and all other faces remain neutral.', 'Preserve all3336 original triangles; no geometry modifications, new source retrieval, Git changes or OBJ generation.', 'Nominal limited material-family mapping, not complete coloring or 2026 condition confirmation.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3336,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
