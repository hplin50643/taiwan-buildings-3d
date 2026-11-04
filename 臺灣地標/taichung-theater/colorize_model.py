from pathlib import Path
import ast,json,hashlib
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='955fa5a6f1c348668930e03d7cea8edef6b02fae4dab5ee06c192bafa0667b2a'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];norm=s.face_normals;a=np.full(len(f),3,np.int32);tol=.018
pal=[['Source-supported pale shell','#CFD3D0'],['Original glazing backing appearance','#596E70'],['Existing gray mullions','#727B7A'],['Unverified neutral','#B8BAB6']]
# Evaluate original construction only, stop before result/export. Lookup surfaces never added.
nodes=[]
for q in ast.parse((R/'build_model.py').read_text()).body:
 if isinstance(q,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='result'for t in q.targets):break
 nodes.append(q)
env={'__file__':str(R/'build_model.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'original-primitive-lookup','exec'),env)
def match(p,inverted=False):
 q=p.to_mesh();mesh=trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False);ids=np.flatnonzero(np.all(tri>=mesh.bounds[0]-tol,axis=(1,2))&np.all(tri<=mesh.bounds[1]+tol,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(ids):
  pts=np.concatenate([tri[ids],tri[ids].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,ds,fs=trimesh.proximity.closest_point(mesh,pts);out[ids]=np.all(ds.reshape(-1,4)<tol,axis=1)&(np.einsum('ij,ij->i',norm[ids],mesh.face_normals[fs.reshape(-1,4)[:,-1]])*(-1 if inverted else 1)>.97)
 return out
def plane(axis,value):return np.all(abs(tri[:,:,axis]-value)<.008,axis=1)
# Full front/left/right exterior planes, not roof, base or rear.
a[(plane(1,-40)&(norm[:,1]<-.99))|(plane(0,-65)&(norm[:,0]<-.99))|(plane(0,65)&(norm[:,0]>.99))]=0
front=match(env['front_cut'],True);left=match(env['left_cut'],True);right=match(env['right_cut'],True);a[front|left|right]=0
# The low right entry's original complete cut surface; backing below separately.
entry=match(env['box'](64.9,-17,9,4,24,12),True);a[entry]=0
# Original blind front/left glazing backing, not invented transparent space.
a[(front&plane(1,-36))|(left&plane(0,-61))|(entry&plane(0,62.9))]=1
# Existing ribs are recognized exactly, not rectangular fields painted over wall.
a[match(env['union'](env['ribs']))|match(env['union'](env['left_ribs']))]=2
# Original small recesses are pale shell, not random dark material dots.
a[match(env['union'](env['pores']),True)]=0
# Four original funnels only. Stagehouse and unbounded horizontal roof remain neutral.
a[match(env['union'](env['roof'][:4]))]=0
# Original exposed base/threshold is not proven facade material.
a[np.all(tri[:,:,2]<3.01,axis=1)]=3
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Full vertices+center+normal original primitive matching; .018mm tolerance for original simplify(.006), not building precision.','limits':'Front/left/right shell and original closed glazing, four approximate original funnels pale; whole horizontal roof and rear/stagehouse neutral. No grass, environment reflection or yellow interior light.'};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
