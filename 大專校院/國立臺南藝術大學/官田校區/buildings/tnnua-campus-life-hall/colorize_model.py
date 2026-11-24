"""Finite original16gon front-facing branch facets only, no geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='3746e1135d20fd342aea955fd9da8090d569d271ebd5120f260ace9ea5a2b88c';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1952
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32)
pal=[('Observed near fork steel outward facets lightgray','#CCD0CC'),('UNVERIFIED shaft canopy rail proxies neutral','#B8BAB5')];D={};evidence=[]
# Reconstruct exact build-code cylinder rotation Ry(theta) then Rz(phi).
start=np.array([42.,-20.,37.])
for end in [np.array([33.,-20.,50-(42-27)*5/36+.5]),np.array([51.,-20.,50-(42-9)*5/36+.5])]:
 v=end-start;length=np.linalg.norm(v);axis=v/length;theta=np.arccos(axis[2]);phi=np.arctan2(axis[1],axis[0]);u=np.array([np.cos(phi)*np.cos(theta),np.sin(phi)*np.cos(theta),-np.sin(theta)]);w=np.array([-np.sin(phi),np.cos(phi),0]);local=t-start;ax=local@axis;mask=np.zeros(len(t),bool);fs=[]
 for k in range(16):
  ang=2*np.pi*(k+.5)/16;normal=u*np.cos(ang)+w*np.sin(ang);tangent=-u*np.sin(ang)+w*np.cos(ang)
  if normal@np.array([0,-1,0])<=1e-6:continue
  # All vertices satisfy SAME finite plane, tangent width and axis interval.
  hit=(np.max(abs(local@normal-np.cos(np.pi/16)),axis=1)<e)&(np.max(abs(local@tangent),axis=1)<=np.sin(np.pi/16)+e)&(ax.min(1)>=-e)&(ax.max(1)<=length+e)
  mask|=hit;fs.append({'k':k,'indices':np.flatnonzero(hit).tolist()})
 ids=np.flatnonzero(mask).tolist();assert len(ids)==23;D[f'near_branch_to_x{end[0]}']=ids;a[ids]=0;evidence.append({'start':start.tolist(),'end':end.tolist(),'u':u.tolist(),'v':w.tolist(),'axis':axis.tolist(),'length':float(length),'facets':fs})
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[46,1906]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'finite_facet_reconstruction':evidence,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1952 original triangles unchanged','limits':['Only two rightfront original16gon branches23+23whole outward front facet triangles.','No rawtriangle normal threshold or centroid cut; finiteplane+tangent+axis allvertices.','Shaft/junction, other supports, solid rail proxies, entire folded roof with omitted grid/shadows neutral.','All mixed walls glazing cone plaza ramps unknownneutral; source builtphotos not woodmodel, PDF2013 metadata not capture.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1952,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
