from pathlib import Path
import json,struct,hashlib,collections
import numpy as np
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;O=R;raw=(O/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0]
t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normals/=np.linalg.norm(normals,axis=1)[:,None]
colors=json.loads((O/'appearance/face-materials.json').read_text())['face_material_indices'];edges=collections.defaultdict(list)
for i,tri in enumerate(t):
 for a,b in [(0,1),(1,2),(2,0)]:edges[tuple(sorted((tuple(tri[a]),tuple(tri[b]))))].append(i)
adj=[set() for _ in t]
for fs in edges.values():
 for i in fs:adj[i].update(set(fs)-{i})
res=abs(t[:,:,1]+54.5);mask=np.all(res<1e-5,axis=1)&(normals[:,1]<-.999999)
remaining=set(map(int,np.flatnonzero(mask)));components=[]
while remaining:
 seen={min(remaining)};stack=list(seen)
 while stack:
  for i in adj[stack.pop()]:
   if mask[i] and i not in seen:seen.add(i);stack.append(i)
 remaining-=seen;ids=sorted(seen);ps=[Polygon(t[i][:,[0,2]]) for i in ids];components.append((ids,ps,unary_union(ps)))
patterns=[(46,[(-48,25),(-14,34),(21,26),(50,25)]),(59,[(-51,19),(-24,29),(10,35),(48,30)]),(72,[(-47,31),(-12,28),(19,24),(48,28)]),(85,[(-53,18),(-27,29),(8,35),(46,34)]),(98,[(-46,34),(-8,34),(27,29),(54,17)])]
domains=[]
for row,(z,bays) in enumerate(patterns):
 for j,(xx,w) in enumerate(bays):
  outer=box(xx-w/2,z,xx+w/2,z+11.5);inner=box(xx-(w-8)/2,z+1.4,xx+(w-8)/2,z+9.8)
  support=outer.difference(inner);strips=[]
  for side in ([-1,1] if (row+j)%2==0 else [1]):
   for dz in [2,3.8,5.6,7.4,9.2]:
    sx=xx+side*(w/2-2.5);q=box(sx-1.75,z+dz,sx+1.75,z+dz+.8);strips.append(list(q.exterior.coords));support=support.difference(q)
  hits=[c for c in components if c[2].intersection(support).area>1]
  assert len(hits)==1,(row,j,len(hits));ids,ps,u=hits[0]
  outside=sum(p.difference(support).area for p in ps);missing=support.difference(u).area
  assert outside<.003 and missing<.003,(row,j,outside,missing)
  domains.append({'name':f'row_{row+1}_frame_{j+1}_front','row':row,'bay':j,'original_parameters':{'x':xx,'z':z,'width':w,'depth':7,'height':11.5},'seed':ids[0],'faces':ids,'count':len(ids),'bounds':[t[ids].min(axis=(0,1)).tolist(),t[ids].max(axis=(0,1)).tolist()],'current_indices':[colors[i] for i in ids],'material_counts':dict(collections.Counter(colors[i] for i in ids)),'plane':'y=-54.5','normal':[0,-1,0],'projection_axes':[0,2],'outer_xz':list(outer.exterior.coords),'cut_xz':list(inner.exterior.coords),'subtracted_louvre_xz':strips,'support_area_mm2':support.area,'actual_area_mm2':sum(p.area for p in ps),'outside_mm2':outside,'reverse_missing_mm2':missing,'max_plane_residual_mm':float(res[ids].max())})

d=next(d for d in domains if d['row']==0 and d['bay']==2);ids=d['faces']
import zipfile,xml.etree.ElementTree as E,importlib.util
assert ids==[1214, 1215, 1216, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1242, 1244, 1245, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268] and n==5324
with zipfile.ZipFile(A/'nckuscisouth-appearance.3mf') as z:r=E.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
vs=np.array([[float(x.get(k)) for k in 'xyz'] for x in r.findall('.//m:vertices/m:vertex',ns)]);ts=r.findall('.//m:triangles/m:triangle',ns);fs=np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]);assigned=np.array([int(x.get('p1')) for x in ts]);assert np.array_equal(vs[fs],t) and assigned.tolist()==colors
sp=importlib.util.spec_from_file_location('old',A/'source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old);before,_=old.classify(t)
assert np.flatnonzero(assigned!=before).tolist()==ids and (assigned[ids]==2).all()
result={'status':'PASS_MATERIAL_ONLY','triangles':n,'changed_faces':ids,'counts':np.bincount(assigned).tolist(),'stl_geometry_order_exact':True,'complete_plane_bfs_domains':[d],'actual_area_mm2':d['actual_area_mm2'],'support_area_mm2':d['support_area_mm2'],'outside_mm2':d['outside_mm2'],'reverse_missing_mm2':d['reverse_missing_mm2'],'area_tolerance_mm2_per_domain':.003,'source_stl_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa/current-material-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
