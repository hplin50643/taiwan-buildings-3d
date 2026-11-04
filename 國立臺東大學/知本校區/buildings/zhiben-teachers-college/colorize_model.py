"""Whole original finite front roof-slope planes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='6bd3e91f0d0feb8401baeea03181e6f1efcef14bdc295f1253e5f7c41a5c3217';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3626
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,aa,bb,xlo,xhi in [('left_front',[-11.5,31.6],[2,37],-64.5,4.5),('right_front',[-11.5,36.2],[4,41.6],9,63)]:
 aa=np.array(aa);bb=np.array(bb);length=np.linalg.norm(bb-aa);tangent=(bb-aa)/length;normal=np.array([-tangent[1],tangent[0]]);v=t[:,:,1:]-aa
 plane=np.abs(v@normal).max(1)<e;along=v@tangent
 hit=plane&(along.min(1)>=-e)&(along.max(1)<=length+e)&(t[:,:,0].min(1)>=xlo-e)&(t[:,:,0].max(1)<=xhi+e)
 ids=np.flatnonzero(hit);assert len(ids)==2 and np.array_equal(ids,np.flatnonzero(plane))
 edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
 assert len(trimesh.graph.connected_components(edges,nodes=ids,min_len=1))==1
 D[name]=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[4,3622]
pal=[('Observed complete front roof slopes nominal gray metal','#727B80'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3626 original triangles unchanged','limits':['All main rear slopes and rear perpendicular wing roofs, not transferred from repeated roof function.', 'Asymmetric tower cap, its solid side/thickness and other flat top pieces; actual shelter and model simplified mass are not proven identical material domains.', 'All roof fascia, gables, undersides and thickness edges: white trim is not the gray upper roof skin.', 'Main walls and piers, facade/window backs, lettering areas and stair tower: white, dark panels/glazing, red accent strips and gold text remain mixed or incompletely delimited.', 'Stairs, base, hidden and rear surfaces remain neutral.', 'Principal photographed connected teaching block only, not all Teachers College courtyard wings; no material borrowed from Jinsin Academy or the upper engineering photo.', 'Capture dates unverified; no 2026 current-condition claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':3626,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
