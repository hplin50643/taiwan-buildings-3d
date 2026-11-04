from pathlib import Path
import ast,json,hashlib,math
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='8d71508dea4ad2d0de0cdd69ec14cecca8791ca21530602c01f3ffc05ed21f17'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];norm=s.face_normals;a=np.full(len(f),6,np.int32);tol=.012
pal=[['Front pink-gray stone','#CDBFBC'],['Crown and existing gold trim','#BEA65D'],['Front dark roof','#55574F'],['Front lotus window appearance','#536A7C'],['Pale existing framing','#D5CEAF'],['Recess shadow','#414B46'],['Unverified neutral','#A7ABA5']]
env={'np':np,'math':math,'m':m,'trimesh':trimesh};defs=[x for x in ast.parse((R/'build_model.py').read_text()).body if isinstance(x,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),'original-functions','exec'),env)
def tm(p):
 q=p.to_mesh();return trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False)
def match(p):
 mesh=tm(p);ids=np.flatnonzero(np.all(tri>=mesh.bounds[0]-tol,axis=(1,2))&np.all(tri<=mesh.bounds[1]+tol,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(ids):
  pts=np.concatenate([tri[ids],tri[ids].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,ds,fs=trimesh.proximity.closest_point(mesh,pts);out[ids]=np.all(ds.reshape(-1,4)<tol,axis=1)&(np.einsum('ij,ij->i',norm[ids],mesh.face_normals[fs.reshape(-1,4)[:,-1]])>.97)
 return out
box=env['box'];roof=env['roof'];flame=env['flame'];union=env['union']
def plane_y(y):return np.all(abs(tri[:,:,1]-y)<.008,axis=1)&(norm[:,1]<-.99)
# Only complete source-supported front vertical wall planes. No side/back propagation.
for y in [-34,-12.5,-13.5,-9,-38,-46.5,-29]:a[plane_y(y)&np.all(tri[:,:,2]>7,axis=1)]=0
# Original front window and entrance recess backs, not invented glazing.
for y in [-33.6,-45.4,-28.55]:a[plane_y(y)]=5
# Front tower lotus backing and original discrete mullions.
a[plane_y(-10.7)&np.all((tri[:,:,2]>=47.9)&(tri[:,:,2]<=80.1),axis=1)]=3
ribs=[box(x,-10.9,63,.65,1.1,31)for x in [-6,-3,0,3,6]]+[box(0,-10.9,z,16,1.1,.65)for z in [53,58,63,68,73]]
a[match(union(ribs))]=4
frame=flame(0,-12.2,47,22,34,1.6)-flame(0,-11.5,48,19,32,3);a[match(frame)]=1
# Only front-facing surfaces of already modeled roofs and copings.
roofs=[roof(x,-20,40,22,22,4.1)for x in [-57,57]]+[roof(0,-25,43,42,30,4.2),roof(0,-39,28,35,19,4)]
for z,w,d in [(45,39,39),(88,40,40),(95,34,34),(101,29,29)]:
 roofs.append(roof(0,5,z+1,w+1.5,d+1.5,3.5));a[match(box(0,5,z,w,d,2))&(norm[:,1]<-.99)]=4
for p in roofs:a[match(p)&(norm[:,1]<-.15)]=2
a[match(box(0,-26,25,135,18,2))&(norm[:,1]<-.99)]=4
# Gold crown is an explicit same-component continuation from front photograph.
crown=[]
for angle in range(0,360,45):
 ts=np.linspace(0,1,30);outside=[[5+10*t-3*t*t,99+15*t]for t in ts];inside=[[3+9*t-2*t*t,99+13*t]for t in ts[::-1]];crown.append(m.CrossSection([outside+inside]).extrude(6).rotate((90,0,0)).translate((0,3,0)).rotate((0,0,angle)).translate((0,5,0)))
crown += [m.Manifold.cylinder(11,7,6,64).translate((0,5,98)),m.Manifold.sphere(7.9,80).scale((1,1,1.06)).translate((0,5,114)),m.Manifold.cylinder(10,1.65,.9,40).translate((0,5,121)),m.Manifold.sphere(1,32).translate((0,5,131))];a[match(union(crown))]=1
for x in [-57,57]:
 staff=[m.Manifold.cylinder(21,1.35,1.15,32).translate((x,-20,44)),m.Manifold.sphere(1.8,32).translate((x,-20,65)),m.Manifold.cylinder(2,1,.85,24).translate((x,-20,66)),m.Manifold.cylinder(1.4,2.3,2.3,40).rotate((90,0,0)).translate((x,-19.3,63))];a[match(union(staff))]=4
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Whole original facet planes or full vertices+center+normal match against original primitive surfaces; tolerance .012mm for original simplify(.005), not real-world accuracy.','limits':'Front only except explicitly inferred complete crown/staff components. Rear lotus, shoulders, unverified sides and roofs neutral.'};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
