"""2025 front bounded palette, unchanged original mesh and no texture."""
from pathlib import Path
import ast,json,hashlib
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='ee873a03173ee2ada7fde6cf9a6c590a8e7fc0839c361c4fac525db8a487d15b'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];norm=s.face_normals;a=np.full(len(f),4,np.int32);e=.007
pal=[['Restored front pink gray','#C8B3B0'],['Pale cream trim','#D9D4BD'],['Front soffit blue gray','#485B6B'],['Recess shadow','#404942'],['Unverified neutral','#A7ABA5']]
for i,t in enumerate(tri):
 lo=t.min(axis=0);hi=t.max(axis=0);nx,ny,nz=norm[i]
 def inside(x0,x1,y0,y1,z0,z1):return bool(np.all(lo>=np.array([x0,y0,z0])-e)and np.all(hi<=np.array([x1,y1,z1])+e))
 def py(y):return bool(np.all(abs(t[:,1]-y)<e))
 if py(-20)and ny<-.99 and lo[2]>=16.9 and hi[2]<=130.2:a[i]=0
 # Only original front corner pilasters, not repeated four-side color.
 for cx in [-20,20]:
  if inside(cx-1.6,cx+1.6,-20.057,-19.993,14.95,130.45):a[i]=1
 for z,w,d,h in [(14,46,43,2.2),(17,45.5,42.5,1.1),(92,46,43,1.8),(94,45,42,1),(130,47,44,2.3)]:
  if inside(-w/2,w/2,-d/2,-19.993,z-h/2,z+h/2)and ny<-.01:a[i]=1
 # Front outward coping/terrace/parapet face, unseen roof floor remains neutral.
 if ny<-.1 and inside(-25.01,25.01,-24.51,-21.0,132,150.01):a[i]=1
 # Front projecting underside only, not a blue terrace or complete roof.
 if nz<-.01 and inside(-25.01,25.01,-24.01,-19.993,124.99,132.31):a[i]=2
 for z in [82,113]:
  if inside(-4.25,4.25,-21.3,-19.5,z-3.7,z+3.7):a[i]=1
  for cx in [-12,12]:
   rr=np.sqrt((t[:,0]-cx)**2+(t[:,2]-z)**2)
   if np.all(rr<=2.607)and inside(cx-2.607,cx+2.607,-21.307,-19.793,z-2.607,z+2.607):a[i]=1
   if py(-19)and np.all(rr<=1.407):a[i]=3
  if py(-19.4)and inside(-2.45,2.45,-19.407,-19.393,z-2.4,z+2.4):a[i]=3
 for cx in [-20,-13,-6,6,13,20]:
  if py(-22.85)and inside(cx-1,cx+1,-22.857,-22.843,142.45,144.55):a[i]=3
# Match original curved eyebrow surfaces including simplification tolerance;
# lookup primitives never become new output geometry.
defs=[x for x in ast.parse((R/'build_model.py').read_text()).body if isinstance(x,ast.FunctionDef)and x.name in ['ball','path']];env={'m':m,'parts':[]};exec(compile(ast.Module(body=defs,type_ignores=[]),'original-eyebrow-functions','exec'),env)
for z in [88.4,119.5]:
 env['parts']=[];env['path']([[float(x),-20.65,z+2.2*np.cos(float(x)*np.pi/13)**2]for x in np.linspace(-13,13,41)],.9);part=m.Manifold.batch_boolean(env['parts'],m.OpType.Add);q=part.to_mesh();tm=trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False);cand=np.flatnonzero(np.all(tri>=tm.bounds[0]-.01,axis=(1,2))&np.all(tri<=tm.bounds[1]+.01,axis=(1,2)))
 if len(cand):
  pts=np.concatenate([tri[cand],tri[cand].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,dist,_=trimesh.proximity.closest_point(tm,pts);a[cand[np.all(dist.reshape(-1,4)<.011,axis=1)]]=1
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Complete original triangles plus normals; curved original relief surface matching for identification only. No added output geometry.'};(R/'appearance-materials.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(q)
