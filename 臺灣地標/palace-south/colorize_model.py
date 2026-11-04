"""Original primitive surface recognition for bounded front appearance only.
Temporary lookup surfaces never join or replace the output mesh.
"""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np,trimesh,manifold3d as m
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert H(R/'model.stl')=='79d4e4dd06a731f5f17ea7feb3b848f0cae04e317acdd1bb64d94383a21dc476'
s=trimesh.load(R/'model.stl',process=True);v=np.asarray(s.vertices);f=np.asarray(s.faces);tri=v[f];norm=s.face_normals;a=np.full(len(f),5,np.int32);tol=.012
pal=[['Local front ink cladding','#424B49'],['Front entry portal','#555D59'],['Local front glass appearance','#859A8C'],['Original front framing','#A9B0A8'],['Bridge structure family','#94978D'],['Unverified neutral','#A7ABA5']]
defs=[x for x in ast.parse((R/'build_model.py').read_text()).body if isinstance(x,ast.FunctionDef)];env={'np':np,'math':math,'m':m,'trimesh':trimesh};exec(compile(ast.Module(body=defs,type_ignores=[]),'original-primitive-functions','exec'),env)
def tm(part):
 q=part.to_mesh();return trimesh.Trimesh(np.asarray(q.vert_properties[:,:3]),np.asarray(q.tri_verts),process=False)
def match(mesh,normal_gate=True):
 lo=mesh.bounds[0]-tol;hi=mesh.bounds[1]+tol;ids=np.flatnonzero(np.all(tri>=lo,axis=(1,2))&np.all(tri<=hi,axis=(1,2)));out=np.zeros(len(f),bool)
 if len(ids):
  pts=np.concatenate([tri[ids],tri[ids].mean(axis=1)[:,None,:]],axis=1).reshape(-1,3);_,ds,fs=trimesh.proximity.closest_point(mesh,pts);good=np.all(ds.reshape(-1,4)<tol,axis=1)
  if normal_gate:good&=np.einsum('ij,ij->i',norm[ids],mesh.face_normals[fs.reshape(-1,4)[:,-1]])>.97
  out[ids]=good
 return out
# Build only one outer SIDE surface (not roof or inward side) of original sweep.
def side_surface(path,first,last,sign):
 verts=[];faces=[]
 for j in range(first,last+1):
  x,y,w,h=path[j];d=path[min(j+1,len(path)-1),:2]-path[max(j-1,0),:2];d/=np.linalg.norm(d);nr=np.array([-d[1],d[0]])*sign
  verts += [[x+nr[0]*w,y+nr[1]*w,2.8],[x+nr[0]*w*.94,y+nr[1]*w*.94,h-1.4]]
 for j in range(last-first):
  q=2*j
  for ff in [[q,q+1,q+3],[q,q+3,q+2]]:
   vv=np.array(verts)[ff];nn=np.cross(vv[1]-vv[0],vv[2]-vv[0]);i=first+j;dd=path[min(i+1,len(path)-1),:2]-path[max(i-1,0),:2];nr=np.array([-dd[1],dd[0]])*sign
   if np.dot(nn[:2],nr)<0:ff=ff[::-1]
   faces.append(ff)
 return trimesh.Trimesh(verts,faces,process=False)
sp=env['sample_path'];ink=sp([(1,66,2.2,9),(-17,53,10.5,18),(-34,35,17,25),(-29,18,16,24),(-5,8,13,20),(16,0,3.1,10)],130);glass=sp([(-1,63,3,14),(12,50,8,20),(33,34,12,25),(43,20,10,26),(34,4,8,22),(17,-6,2.8,17)],130)
inkmask=match(side_surface(ink,78,104,-1));a[inkmask]=0
glassmask=match(side_surface(glass,100,129,1));a[glassmask]=2
# Four original near-entry ribs, outer side only. Do not silver the bowed roof.
for idx in [104,111,118,125]:
 p=glass[idx];d=glass[idx+1,:2]-glass[idx-1,:2];d/=np.linalg.norm(d);w=p[2]+.75;h=p[3]+.65;pair=np.array([[*(p[:2]+d*off),w,h]for off in [-.55,.55]])
 a[match(side_surface(pair,0,1,1))]=3
# Existing front horizontal frame segments; exact original line samples only.
bars=[]
for z in [8,13,18,23]:
 ids=[i for i,p in enumerate(glass)if p[3]>z+2.2][::4];line=[]
 for i in ids:
  p=glass[i];d=glass[min(i+1,len(glass)-1),:2]-glass[max(i-1,0),:2];d/=np.linalg.norm(d);nr=np.array([-d[1],d[0]]);w=p[2]*(1-.06*(z-2.8)/(p[3]-4.2));xy=p[:2]+nr*w;line.append([xy[0],xy[1],z])
 for j in range(len(ids)-1):
  if ids[j]>=100:bars.append(env['bar'](line[j],line[j+1],.43))
if bars:a[match(tm(m.Manifold.batch_boolean(bars,m.OpType.Add)))]=3
portal=env['prism_poly']([(-3,3),(20,3),(17,25),(2,25)],9,7)-env['prism_poly']([(-.8,5),(17.4,5),(14.9,22.5),(3.8,22.5)],2.4,-.7)
pm=match(tm(portal));portal_rear=np.all(abs(tri[:,:,1]-7)<.008,axis=1);a[pm&(norm[:,2]<.2)&~portal_rear]=1
back=np.all(abs(tri[:,:,1]+.7)<.008,axis=1)&pm;a[back]=2
# All actual bridge arch/hanger/parapet lookup solids are existing code components.
arch=[]
for t in np.linspace(0,1,70):arch.append([4+21*math.sin(math.pi*t)-1.5*t+3.4,-67+69*t,5.6+12.4*math.sin(math.pi*t)**.88])
bridgeparts=[env['bar'](aa,bb,1.05)for aa,bb in zip(arch[:-1],arch[1:])]
for t in np.linspace(.06,.94,19):
 x=4+21*math.sin(math.pi*t)-1.5*t+3.4;y=-67+69*t;z=5.6+12.4*math.sin(math.pi*t)**.88;bridgeparts.append(env['bar']([x,y,4.9],[x,y,z],.7))
rail=[[4+21*math.sin(math.pi*t)-1.5*t-3.2,-67+69*t,6.2+.7*math.sin(math.pi*t)]for t in np.linspace(0,1,65)];bridgeparts += [env['bar'](aa,bb,.66)for aa,bb in zip(rail[:-1],rail[1:])];a[match(tm(m.Manifold.batch_boolean(bridgeparts,m.OpType.Add)))]=4
bp=np.array([[4+21*math.sin(math.pi*t)-1.5*t,-67+69*t,3.9,5.1+.7*math.sin(math.pi*t)]for t in np.linspace(0,1,110)]);deck=match(tm(env['sweep_mass'](bp)));a[deck&(norm[:,2]>.2)]=4
# Vertical filled bridge support and unrelated base stay neutral.
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n');q={'original_STL_sha256':H(R/'model.stl'),'triangles':len(f),'materials':{str(k):{'name':pal[k][0],'hex':pal[k][1],'face_count':int(np.sum(a==k))}for k in range(len(pal))},'geometry_changed':False,'assignment_method':'Full facet vertices+center and outward normal match to original primitive surface patches, tolerance .012 mm for original simplify(.004). No new output geometry.','bounded_curve_scope':{'ink_path_side':-1,'ink_path_samples':[78,104],'glass_path_side':1,'glass_path_samples':[100,129],'front_rib_indices':[104,111,118,125]},'matched_counts':{'ink_front':int(inkmask.sum()),'glass_front':int(glassmask.sum()),'portal':int(pm.sum()),'portal_back':int(back.sum())}};(R/'appearance-materials.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(q)
