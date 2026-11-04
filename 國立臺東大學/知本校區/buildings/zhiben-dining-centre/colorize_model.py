"""Finite original sampled upper roof skins only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b727d519d2c5c8b1cb27664ad31134a5ec633cbc898b03c7f49e18de867e282c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1656
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for name,ry,rise,z0,N,halfwidth,expected_count in [('main',41,9,24,40,66,120),('cap',13,1.8,39.7,20,55,40)]:
 idsall=[]
 for j in range(N):
  aa=np.array([ry*np.cos(j*np.pi/N),z0+rise*np.sin(j*np.pi/N)]);bb=np.array([ry*np.cos((j+1)*np.pi/N),z0+rise*np.sin((j+1)*np.pi/N)])
  tangent=(bb-aa)/np.linalg.norm(bb-aa);normal=np.array([-tangent[1],tangent[0]]);v=t[:,:,1:]-aa
  plane=np.abs(v@normal).max(1)<e;along=v@tangent
  hit=plane&(along.min(1)>=-e)&(along.max(1)<=np.linalg.norm(bb-aa)+e)&(t[:,:,0].min(1)>=-halfwidth-e)&(t[:,:,0].max(1)<=halfwidth+e)
  ids=np.flatnonzero(hit);assert np.array_equal(ids,np.flatnonzero(plane));idsall.extend(ids.tolist())
 idsall=sorted(set(idsall));assert len(idsall)==expected_count;D[name]=idsall;a[idsall]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[160,1496]
pal=[('Observed complete sampled upper roof skins pale gray','#D3D6D3'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1656 original triangles unchanged','limits':['Tree-hidden lower exterior walls and entire left sign block with lettering.', 'Clerestory glazing/frames and opaque backed windows; no uniform dark or glass material.', 'Main roof end faces, thickness/underside and uppercap endfaces/underside.', 'Ground/base/platform/stairs, all unverified walls, piers and hidden surfaces.', 'One independent dining building, not dormitory ground-floor wing, not athletic facility.', 'Only nominal pale-gray upper-skin material color, not exact reflectance or panel texture.', 'Dates unverified; no2026 current-state claim.', 'Original coarse facets and Boolean recess approximation remain, no new geometry or cut.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1656,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
