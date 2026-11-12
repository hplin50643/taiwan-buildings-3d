"""Original 48-sample finite roof facets after inverse original transforms; no geometry change."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='167ad46cb6da38ceb84ef62dfedabc8aac461d8581357f96f51047168e833a94';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==9662
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={};xs=np.linspace(-18,18,49);zs=23.2+4.4*np.cos(xs/18*np.pi/2)
for side in [-1,1]:
 theta=np.radians(side*18);dx=t[:,:,0]-side*39;dy=t[:,:,1]-26;x=np.cos(theta)*dx+np.sin(theta)*dy;y=-np.sin(theta)*dx+np.cos(theta)*dy;allids=[];facets={}
 for j in range(48):
  k=(zs[j+1]-zs[j])/(xs[j+1]-xs[j]);b=zs[j]-k*xs[j]
  hit=(abs(t[:,:,2]-(k*x+b)).max(1)<=e)&(x.min(1)>=xs[j]-e)&(x.max(1)<=xs[j+1]+e)&(y.min(1)>=-47.5-e)&(y.max(1)<=47.5+e)
  ids=np.flatnonzero(hit);allids.extend(ids.tolist())
  if len(ids):facets[str(j)]=ids.tolist()
 assert len(allids)==len(set(allids))==130;assert len(facets)==45;a[allids]=0;D[str(side)]={'indices':allids,'finite_facets':facets}
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[260,9402]
pal=[('Observed two original factory upper roof skins nominal gray metal','#777D7E'),('UNVERIFIED mixed walls eaves windows towers neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'9662 original triangles unchanged','limits':['Only original roof finite top facets, inverse rotation +/-18 degrees; each 130 original Boolean-clipped triangles.','No roof end thickness, underside, mixed yellow-white teaching wall or window backing colors.','Whole connected teaching and factory group remains one model; no split deliveries.','Capture dates unknown; no current-condition claim.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':9662,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
