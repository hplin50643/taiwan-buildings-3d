"""Same original facets only. Roof primitive surfaces identify existing faces, not new geometry."""
from pathlib import Path
import ast,json,hashlib
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(R/'model.stl')=='3eabe204535bf0ec3be8a9693218cbfe6a298372299f74c00de9f426b86603af'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];n=s.face_normals;a=np.full(len(f),7,np.int32);e=.002
pal=[['Terracotta tile family','#AD7857'],['Roof ridge and underside','#6E6556'],['Near front red frame','#A35347'],['Pale existing leaf','#C4C9B9'],['Weathered stone','#A4A391'],['Existing green infill','#6C8C7D'],['Recess shadow','#4E514A'],['Unknown neutral','#A7ABA5']]
# Reuse only original pure primitive function definitions to recognize coplanar
# original skin triangles. Never append these temporary lookup solids to output.
code=ast.parse((R/'build_model.py').read_text());defs=[x for x in code.body if isinstance(x,ast.FunctionDef)and x.name in ['rod','mesh_solid','roof']];env={'np':np,'trimesh':trimesh,'m':m,'parts':[]};exec(compile(ast.Module(body=defs,type_ignores=[]),'original-roof-functions','exec'),env)
def component_tm(part):
 z=part.to_mesh();return trimesh.Trimesh(np.asarray(z.vert_properties[:,:3]),np.asarray(z.tri_verts),process=False)
def surface_match(mesh):
 lo=mesh.bounds[0]-e;hi=mesh.bounds[1]+e;candidate=np.flatnonzero(np.all(tri>=lo,axis=(1,2))&np.all(tri<=hi,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(candidate):
  pts=np.concatenate([tri[candidate],tri[candidate].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,dist,_=trimesh.proximity.closest_point(mesh,pts);out[candidate]=np.all(dist.reshape(-1,4)<e,axis=1)
 return out
for cy,w,d in [(-29,53,42),(32,49,40)]:
 for z,ww,dd,h in [(31.4,w+7,d+5,6.5),(42.8,w-1,d-2,8.1)]:
  env['parts']=[];env['roof'](0,cy,z,ww,dd,h);parts=env['parts'];skin=surface_match(component_tm(parts[0]));a[skin]=np.where(n[skin,2]>.01,0,1)
  ridge=m.Manifold.batch_boolean(parts[1:],m.OpType.Add);a[surface_match(component_tm(ridge))]=1
# Only observed near-front original rectangular/curved components; no fictitious doors.
for i,t in enumerate(tri):
 lo=t.min(axis=0);hi=t.max(axis=0);nx,ny,nz=n[i]
 def inside(x0,x1,y0,y1,z0,z1):return bool(np.all(lo>=np.array([x0,y0,z0])-e)and np.all(hi<=np.array([x1,y1,z1])+e))
 def py(y):return bool(np.all(abs(t[:,1]-y)<e))
 # Retaining front visible stone skin, individual original stele relief and front stair.
 if inside(-36,36,-59.5,-57.45,2.4,15.01)and ny<-.1:a[i]=4
 if inside(22.8,35.2,-74.5,-57.9,2.4,17.71):a[i]=4
 if inside(-37.1,24,-59.24,-57.76,15.75,18.81):a[i]=4
 if py(-59.15)and inside(-37.1,24,-59.16,-59.14,15.8,17.75):a[i]=5
 # Lower full-height columns include unseparated pale/red source regions:
 # keep coherent stone-neutral family, rather than split cylinder triangles.
 for cx in np.linspace(-22,22,6):
  rr=np.sqrt((t[:,0]-cx)**2+(t[:,1]+46.9)**2)
  if inside(cx-1.11,cx+1.11,-48.01,-46.0,17.1,31.4)and np.all(rr<1.102):a[i]=4
  if inside(cx-1.175,cx+1.175,-47.65,-46.15,29.8,31.5):a[i]=2
 # Existing front sign/header only; lower broad wall stays neutral (no actual cut doors).
 if inside(-5.25,5.25,-47.45,-46.75,28,29.9):a[i]=2
 # Upper front slender original columns are red. Window backs actually penetrate .025mm.
 for cx in np.linspace(-19.1,19.1,6):
  rr=np.sqrt((t[:,0]-cx)**2+(t[:,1]+43.35)**2)
  if inside(cx-.651,cx+.651,-44.001,-42.699,34,43.2)and np.all(rr<.652):a[i]=2
 if py(-42.975)and inside(-18,18,-42.977,-42.973,36,42):
  a[i]=6 if lo[0]>-2.2 and hi[0]<2.2 else 3
 # Near-front balcony parapet: real protruding posts remain stone; panel plane green.
 if inside(-22,22,-45.651,-44.349,34.75,37.81):a[i]=4
 if py(-45.575)and inside(-22,22,-45.577,-45.573,34.8,36.75):a[i]=5
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a)
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Whole original surface facets; roof lookup from unchanged original pure primitive definitions, no output geometry added. Full-vertex domain/normal gates; no centroid color borders.'};(R/'appearance-materials.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(q)
