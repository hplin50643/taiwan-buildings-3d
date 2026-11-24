"""Two complete original 160-gon outward spandrel bands only; no geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b54b57c7c6c824161df9e4b461d02559bb54fbaad566a6d102e1f8a0c04e9949';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==18016
t=m.triangles;n=m.face_normals;lo=t.min(1);hi=t.max(1);e=.00001;a=np.full(len(t),1,np.int32)
pal=[('Observed two complete curved tile bands nominal cream','#D8D4C2'),('UNVERIFIED lettering windows walls roof neutral','#B8BAB5')];D={}
# Test full triangles against every actual outward original regular-polygon facet,
# not radius-of-centroid or arbitrarily clipped face fragments.
for z0,z1 in [(45.7,51),(77.7,83)]:
 mask=np.zeros(len(t),bool)
 for k in range(80,160):
  angle=2*np.pi*(k+.5)/160;normal=np.array([np.cos(angle),np.sin(angle),0]);dist=36*np.cos(np.pi/160)
  tangent=np.array([-np.sin(angle),np.cos(angle),0]);halfspan=36*np.sin(np.pi/160)
  facet=(np.max(abs(t@normal-dist),axis=1)<e)&(np.max(abs(t@tangent),axis=1)<=halfspan+e)&(n@normal>.999999)&(lo[:,2]>=z0-e)&(hi[:,2]<=z1+e)
  mask|=facet
 ids=np.flatnonzero(mask).tolist();assert len(ids)==264;D[f'complete_outward_band_{z0}_{z1}']=ids;a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1)
assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[528,17488]
old=a.copy();new=[]
for k in range(40,56):
 A=np.array([0.,-33.])+2.3*np.array([np.cos(2*np.pi*k/64),np.sin(2*np.pi*k/64)]);B=np.array([0.,-33.])+2.3*np.array([np.cos(2*np.pi*(k+1)/64),np.sin(2*np.pi*(k+1)/64)]);u=(B-A)/np.linalg.norm(B-A);nn=np.array([-u[1],u[0]]);q=t[:,:,:2]-A
 hit=(abs(q@nn)<1e-4).all(1)&((q@u>=-1e-4)&(q@u<=np.linalg.norm(B-A)+1e-4)).all(1)&((t[:,:,2]>=3-1e-4)&(t[:,:,2]<=31.4+1e-4)).all(1)
 ids=np.flatnonzero(hit);gs=[c for c in cs if hit[c].any()];assert len(ids)==2 and len(gs)==1 and set(gs[0])==set(ids);assert (old[ids]==1).all();new.extend(ids.tolist())
a[new]=2;assert len(new)==32 and np.bincount(a).tolist()==[528,17456,32];assert np.array_equal(a[np.setdiff1d(np.arange(len(a)),new)],old[np.setdiff1d(np.arange(len(a)),new)])
pal.append(('Central pier bounded front quarter nominal gray family','#A8AAA5'));D['central_pier_front_quarter']=new
assert all(len(set(a[c]))==1 for c in cs)
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'coplanar_neutralized_faces':[],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'18016 original triangles unchanged','limits':['Only radius36 regular160gon outward planes in entire z45.7..51 and77.7..83 fields,264each;24 tiny original facet triangles restored to their whole coplanar fields by explicit correction.','Lettered middle band61.7..67 neutral; lowest darkedge and upper crown neutral.','Central pier front quarter32 faces nominal gray; remaining posts and glass proxies/frames/wings/steps/roof/rear cut neutral.','Central segment not whole administration building; unknown capture dates,2025conference not capture year.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':18016,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
