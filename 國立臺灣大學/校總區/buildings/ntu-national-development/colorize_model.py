from pathlib import Path
import ast,json,hashlib
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='f6054555c12e1a38add4290d852c4a8b6b4b11720a90e643367e8e92174b6d3d'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);u=v.copy();u[:,2]/=.9;tri=u[f];n=s.face_normals;a=np.full(len(f),4,np.int32);tol=.004
pal=[['Bounded brick infill','#A17C69'],['Existing stone grid and entry','#969B97'],['Original window backing','#536567'],['Recess shadow','#3F4745'],['Unverified or mixed plane neutral','#B8BAB6']]
nodes=[]
for q in ast.parse((R/'build_model.py').read_text()).body:
 if isinstance(q,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='solid'for t in q.targets):break
 nodes.append(q)
e={'__file__':str(R/'build_model.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'original-lookup','exec'),e)
# Geometry remains original scaled coordinates. Only lookup restores pre-scale Z.
lookup=trimesh.Trimesh(u,f,process=False);norm=lookup.face_normals
union=lambda pp:m.Manifold.batch_boolean(pp,m.OpType.Add)
def match(p,inverted=False):
 q=p.to_mesh();mesh=trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False);ids=np.flatnonzero(np.all(tri>=mesh.bounds[0]-tol,axis=(1,2))&np.all(tri<=mesh.bounds[1]+tol,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(ids):
  pts=np.concatenate([tri[ids],tri[ids].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,ds,fs=trimesh.proximity.closest_point_naive(mesh,pts);out[ids]=np.all(ds.reshape(-1,4)<tol,axis=1)&(np.einsum('ij,ij->i',norm[ids],mesh.face_normals[fs.reshape(-1,4)[:,-1]])*(-1 if inverted else 1)>.97)
 return out
def plane(ax,z):return np.all(abs(tri[:,:,ax]-z)<.004,axis=1)
# Coherent connected coplanar wall regions: NEVER paint upper triangles alone.
regions=[]
for ax,z,normal in [(1,-22.5,-1),(0,-68,-1),(0,68,1)]:
 ids=np.flatnonzero(plane(ax,z)&(norm[:,ax]*normal>.99));selected=set(ids);adj=lookup.face_adjacency;edges=adj[np.isin(adj[:,0],ids)&np.isin(adj[:,1],ids)];neighbors={int(i):[]for i in ids}
 for aa,bb in edges:neighbors[int(aa)].append(int(bb));neighbors[int(bb)].append(int(aa))
 while selected:
  start=selected.pop();comp=[start];stack=[start]
  while stack:
   for j in neighbors[int(stack.pop())]:
    if j in selected:selected.remove(j);stack.append(j);comp.append(j)
  lo=tri[comp,:,2].min();hi=tri[comp,:,2].max();allowed=lo>=19-.004
  if allowed:a[comp]=0
  regions.append({'axis':ax,'plane':z,'faces':len(comp),'z_min':float(lo),'z_max':float(hi),'brick':bool(allowed)})
# Existing central tower, copings, side grids and steps: original parts except base/main body.
a[match(union(e['parts'][2:]))]=1
# Original cut returns use recess shadow; actual rectangular backing gray-green.
cm=match(union(e['cuts']),True);a[cm]=3
back=plane(1,-26.35)|plane(1,-21)|plane(0,-66.5)|plane(0,66.5);a[cm&back]=2
# Original arch and existing mullions/trim are stone. No new ornament.
a[match(union(e['details']))]=1
# Low ground/window circle backing retains shadow; mixed outer walls neutral.
# Independent scope correction: unproven crown rear/top, whole original faces.
crown_unknown=[845, 846, 899, 900, 1858, 1859, 1866, 1867, 1876, 1886, 1887, 842, 843, 896, 897, 1854, 1856, 1862, 1865, 1868, 1869, 1870, 1875, 1880, 1883, 1884, 1885]
assert len(f)==4112 and np.all(a[crown_unknown]==1)
a[crown_unknown]=4


# Narrow withdrawal: lower tower front crosses unmodeled brick bands.
old=a.copy()
hit=np.all(abs(tri[:,:,1]+28)<tol,axis=1)&np.all(tri[:,:,2]>=3-tol,axis=1)&np.all(tri[:,:,2]<=20+tol,axis=1)&(np.all(tri[:,:,0]<=-9.5+tol,axis=1)|np.all(tri[:,:,0]>=9.5-tol,axis=1))&np.all(abs(tri[:,:,0])<=20.5+tol,axis=1)
assert hit.sum()==20 and np.all(a[hit]==1)
ad=lookup.face_adjacency;groups=trimesh.graph.connected_components(ad[(norm[ad[:,0]]*norm[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(f)),min_len=1)
affected=[c for c in groups if hit[c].any()];assert len(affected)==2 and all(len(c)==10 and hit[c].all() for c in affected)
a[hit]=4;assert np.array_equal(a[~hit],old[~hit])
assert np.bincount(a,minlength=5).tolist()==[376,1985,126,1170,455]
old_mixed=[c for c in groups if len(set(old[c]))>1];assert len(old_mixed)==19 and all(np.array_equal(a[c],old[c]) for c in old_mixed)
assert len([c for c in groups if len(set(a[c]))>1])==19
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'lookup_transform':'Only lookup coordinates z/0.9; output vertices unchanged.','assignment_method':'Complete connected coplanar regions, then exact original primitive surfaces by all vertices/center/normals; no new faces.','wall_regions':regions,'limits':'Large original wall regions crossing plinth remain neutral. 2010 E10 original building, not relocated premises. Roof/back neutral.'};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
