from pathlib import Path
import ast,json,hashlib
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='490dd16c89baa07009b5edcd648919ecf99a8d715b5324b25867d0d02b9e7142'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];norm=s.face_normals;a=np.full(len(f),3,np.int32);tol=.004
pal=[['Off-white tower and proven arcade','#D8DBD5'],['Recess shadow not glazing','#454945'],['Dark cap','#303837'],['Unverified neutral','#B8BAB6']]
# Execute only original primitive construction, stopping BEFORE Boolean/export/parser.
nodes=[]
for q in ast.parse((R/'build_model.py').read_text()).body:
 if isinstance(q,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='body'for t in q.targets):break
 nodes.append(q)
env={'__file__':str(R/'build_model.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'original-primitive-lookup','exec'),env);parts=env['parts'];cuts=env['cuts'];assert len(parts)==62

def match(p,inverted=False):
 q=p.to_mesh();mesh=trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False);ids=np.flatnonzero(np.all(tri>=mesh.bounds[0]-tol,axis=(1,2))&np.all(tri<=mesh.bounds[1]+tol,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(ids):
  pts=np.concatenate([tri[ids],tri[ids].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,ds,fs=trimesh.proximity.closest_point(mesh,pts);sgn=-1 if inverted else 1;out[ids]=np.all(ds.reshape(-1,4)<tol,axis=1)&(np.einsum('ij,ij->i',norm[ids],mesh.face_normals[fs.reshape(-1,4)[:,-1]])*sgn>.97)
 return out
union=lambda pp:m.Manifold.batch_boolean(pp,m.OpType.Add)
# White original tower parts20..56, including pale lantern drum, not blue glass.
a[match(union(parts[20:57]))]=0
a[match(union(parts[57:60]))]=2
# Lantern's blind engraved panels stay white/pale; tower small openings are shadow.
a[match(union(cuts[12:24]),True)]=0
a[match(union(cuts[-5:]),True)]=1
# Front and photographed perpendicular low building vertical outer planes.
for p in parts[3:18]:
 mask=match(p);a[mask&(((norm[:,1]<-.99)&np.all(tri[:,:,1]<-4.4,axis=1))|((norm[:,0]>.99)&np.all(tri[:,:,0]>5.5,axis=1)))]=0
# Only front parapet/piers, not rear ledges; neutral large horizontal roof.
a[np.all(abs(tri[:,:,1]+6)<.004,axis=1)&(norm[:,1]<-.99)]=0
a[np.all(abs(tri[:,:,0]-7)<.004,axis=1)&(norm[:,0]>.99)&np.all(tri[:,:,2]<24.01,axis=1)]=0
# Original blind arches: white returns, shadow at actual solid recess backing.
arc=match(union(cuts[:8]),True);a[arc]=0
back_y=np.all(abs(tri[:,:,1]+3.6)<.004,axis=1);back_x=np.all(abs(tri[:,:,0]-4.5)<.004,axis=1);a[arc&(back_y|back_x)]=1
# All rear keeper planes and outer perimeter walls remain neutral.
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Original primitive surfaces matched by full vertices+center and normals; no output geometry created. .004mm numerical lookup tolerance, not architectural precision.','limits':'White tower whole-component continuity; lantern pale not blue; keeper front/perpendicular arcade only, rear/roof/paving neutral.'};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
