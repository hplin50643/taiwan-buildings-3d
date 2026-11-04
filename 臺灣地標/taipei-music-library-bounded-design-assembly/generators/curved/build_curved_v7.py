import bpy,json,sys,math,struct,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
OUT=Path(sys.argv[sys.argv.index('--')+1])if '--'in sys.argv else ROOT/'output-v7'
OUT.mkdir(parents=True,exist_ok=True)
p=json.loads((ROOT/'inputs/curved-parameters-v2.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)

def signed_volume(v,f):
 return sum((v[a][0]*(v[b][1]*v[c][2]-v[b][2]*v[c][1])+v[a][1]*(v[b][2]*v[c][0]-v[b][0]*v[c][2])+v[a][2]*(v[b][0]*v[c][1]-v[b][1]*v[c][0]))/6 for a,b,c in f)
def obj(name,v,f):
 if signed_volume(v,f)<0:f=[list(reversed(t))for t in f]
 m=bpy.data.meshes.new(name);m.from_pydata(v,[],f);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);return o

def prism(s):
 v=s['reference_vertices_mm'];axis=s['extrusion_axis'];delta=s['artificial_delta_mm'];proj=[i for i in range(3)if i!=axis];v1=[];lookup={};mapping={}
 for i,p in enumerate(v):
  key=tuple(round(x,9)for x in p)
  if key not in lookup:lookup[key]=len(v1);v1.append(p)
  mapping[i]=lookup[key]
 ff=[]
 for f in s['faces']:
  f=[mapping[i]for i in f];a,b,c=[[v1[i][j]for j in proj]for i in f];cross=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
  if cross<0:f=list(reversed(f))
  ff.append(f)
 n=len(v1);vv=v1+[[x+(delta if k==axis else 0)for k,x in enumerate(q)]for q in v1];faces=[];edges={}
 for f in ff:
  faces += [f if delta<0 else list(reversed(f)),[i+n for i in (list(reversed(f))if delta<0 else f)]]
  for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 for e,pairs in edges.items():
  if len(pairs)==1:
   a,b=pairs[0];q=[b,a,a+n,b+n]if delta<0 else[a,b,b+n,a+n];faces += [[q[0],q[1],q[2]],[q[0],q[2],q[3]]]
  else:assert len(pairs)==2
 return obj(s['id'],vv,faces)

def box(name,b):
 x,y,z,X,Y,Z=b;v=[[x,y,z],[X,y,z],[X,Y,z],[x,Y,z],[x,y,Z],[X,y,Z],[X,Y,Z],[x,Y,Z]];qs=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]];return obj(name,v,[[q[0],q[1],q[2]]for q in qs]+[[q[0],q[2],q[3]]for q in qs])
def cap_post(name,b,corners):
 v=[[c[0],c[1],b[2]]for c in corners]+corners;qs=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]];return obj(name,v,[[q[0],q[1],q[2]]for q in qs]+[[q[0],q[2],q[3]]for q in qs])

def grid_union(name,bb):
 import numpy as np
 coords=[sorted(set(b[k]for b in bb for k in [i,i+3]))for i in range(3)];ix=[{x:i for i,x in enumerate(c)}for c in coords];solid=np.zeros(tuple(len(c)-1 for c in coords),dtype=bool)
 for b in bb:solid[tuple(slice(ix[k][b[k]],ix[k][b[k+3]])for k in range(3))]=True
 verts=[];faces=[];lookup={}
 def put(q):
  ff=[]
  for key in q:
   if key not in lookup:lookup[key]=len(verts);verts.append([coords[k][key[k]]for k in range(3)])
   ff.append(lookup[key])
  faces.extend([[ff[0],ff[1],ff[2]],[ff[0],ff[2],ff[3]]])
 for i,j,k in np.argwhere(solid):
  i,j,k=int(i),int(j),int(k)
  qs=[[(i,j,k),(i,j,k+1),(i,j+1,k+1),(i,j+1,k)],[(i+1,j,k),(i+1,j+1,k),(i+1,j+1,k+1),(i+1,j,k+1)],[(i,j,k),(i+1,j,k),(i+1,j,k+1),(i,j,k+1)],[(i,j+1,k),(i,j+1,k+1),(i+1,j+1,k+1),(i+1,j+1,k)],[(i,j,k),(i,j+1,k),(i+1,j+1,k),(i+1,j,k)],[(i,j,k+1),(i+1,j,k+1),(i+1,j+1,k+1),(i,j+1,k+1)]]
  for n,(di,dj,dk)in enumerate([(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]):
   a,b,c=i+di,j+dj,k+dk
   if not(0<=a<solid.shape[0]and 0<=b<solid.shape[1]and 0<=c<solid.shape[2])or not solid[a,b,c]:put(qs[n])
 return obj(name,verts,faces)

records=[];all_primitives={}
sys.path.insert(0,str(ROOT));from exact_retriangulate import repair
from planar_patch_repair import repair_patch
def capture(o):
 o.data.calc_loop_triangles();return {'id':o.name,'vertices_mm':[list(v.co)for v in o.data.vertices],'triangles':[list(t.vertices)for t in o.data.loop_triangles]}
for s in p['skins']:
 o=prism(s);inputs=[];axisboxes=[];primitive_records=[]
 for fi,f in enumerate(s['faces']):
  part=dict(s);part['id']=s['id']+'_primitive_roof_'+str(fi);part['reference_vertices_mm']=[s['reference_vertices_mm'][i]for i in f];part['faces']=[[0,1,2]];tmp=prism(part);primitive_records.append(capture(tmp));bpy.data.objects.remove(tmp,do_unlink=True)
 for i,t in enumerate(s['supports']):
  for k in ['post_bounds_mm','arm_bounds_mm','cap_bounds_mm']:
   if k not in t:continue
   name=s['id']+f'_support{i}_{k}'
   angled='angled_post_cap_corners_mm'in t and (k=='cap_bounds_mm'or(k=='post_bounds_mm'and 'cap_bounds_mm'not in t))
   if angled:
    bounds=t[k][:]
    if k=='post_bounds_mm':bounds[2]=-1.2
    tmp=cap_post(name,bounds,t['angled_post_cap_corners_mm']);inputs.append(tmp);primitive_records.append(capture(tmp))
   else:axisboxes.append(t[k])
 for b in p['boxes']:
  if b['unit']==s['id']and b['kind']=='actual_designed_peg_extension':
   if s['id']in ['A_NOMINAL_ROOF_SUPPORT_1','B_FINITE_UPPER_CANDIDATE_PROXY']:continue
   axisboxes.append(b['bounds_mm'])
 for bi,bounds in enumerate(axisboxes):
  tmp=box(s['id']+'_primitive_axis_'+str(bi),bounds);primitive_records.append(capture(tmp));bpy.data.objects.remove(tmp,do_unlink=True)
 all_primitives[s['id']]=primitive_records
 if axisboxes:inputs.insert(0,grid_union(s['id']+'_axis_support_union',axisboxes))
 if s['id']=='A_NOMINAL_ROOF_SUPPORT_0':
  roof=o;o=inputs[0];inputs=inputs[1:]+[roof]
 for a in inputs:
  bpy.context.view_layer.objects.active=o;o.select_set(True);mod=o.modifiers.new('artificial_union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=a;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(a,do_unlink=True)
 # Triangulate deterministic final evaluated union.
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('triangulate','TRIANGULATE');mod.quad_method='FIXED';mod.ngon_method='CLIP';bpy.ops.object.modifier_apply(modifier=mod.name)
 import bmesh
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges));bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='FIXED',ngon_method='BEAUTY');bm.to_mesh(o.data);bm.free();o.data.update()
 o.data.calc_loop_triangles();v=[list(x.co)for x in o.data.vertices];f=[list(t.vertices)for t in o.data.loop_triangles];vol=signed_volume(v,f)
 if vol<0:
  for poly in o.data.polygons:poly.flip()
  o.data.update();o.data.calc_loop_triangles();f=[list(t.vertices)for t in o.data.loop_triangles];vol=signed_volume(v,f)
 v,f,flips=repair(v,f);v,f,patchproof=repair_patch(s['id'],v,f);(OUT/(s['id']+'-planar-patch-proof.json')).write_text(json.dumps(patchproof,indent=2)+'\n');o.name=s['id'];mesh=bpy.data.meshes.new(s['id']+'_exact_retriangulated');mesh.from_pydata(v,[],f);mesh.update();old=o.data;o.data=mesh;bpy.data.meshes.remove(old);vol=signed_volume(v,f)
 (OUT/(s['id']+'-exact-flip-proof.json')).write_text(json.dumps({'records':flips,'scope':'Strict dyadic coplanarity and directed boundary preservation; no coordinate movement.'},indent=2)+'\n')
 rec={'id':s['id'],'vertices_mm':v,'triangles':f,'signed_volume_mm3':vol,'role':'Hypothetical display front with artificial backing and dedicated support, not actual architecture','assembly_matrix':[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]};records.append(rec)
 stl=bytearray(b'Bounded hypothetical display study; millimetres'.ljust(80,b' ')+struct.pack('<I',len(f)))
 for a,b,c in f:
  va,vb,vc=Vector(v[a]),Vector(v[b]),Vector(v[c]);n=(vb-va).cross(vc-va);n.normalize();stl+=struct.pack('<12fH',*n,*va,*vb,*vc,0)
 (OUT/(s['id']+'.stl')).write_bytes(stl);print('BUILT',s['id'],len(v),len(f),vol,flush=True)
(OUT/'expected-convex-primitives.json').write_text(json.dumps(all_primitives,indent=2)+'\n')
(OUT/'geometry.json').write_text(json.dumps({'objects':records},indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'curved-parts.blend'))
