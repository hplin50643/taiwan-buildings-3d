"""Original curved construction-facet matching; no mesh modification or broad sy mask."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math,struct
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='7519576d2584246bb55c3b159c2226ff2081553c22b70ae74d8f6243feac0103';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5600
scale=150/147;out=m.triangles/scale
v=[]
for j in range(45):
 z=3+144*j/44;w=30-4*(j/44)**2
 for i in range(17):
  x=-w+2*w*i/16;t=(z-3)/144;y=-16-17*math.sin(math.pi*t)-3.5*(1-(x/31)**2)*math.sin(math.pi*t);v.append([x,y,z])
v=np.array(v);tris=[]
for j in range(44):
 for i in range(16):
  k=j*17+i;tris.extend([v[[k,k+17,k+1]],v[[k+1,k+17,k+18]]])
tris=np.array(tris);origin=tris[:,0];u=tris[:,1]-origin;vv=tris[:,2]-origin;cross=np.cross(u,vv);norm=cross/np.linalg.norm(cross,axis=1)[:,None]
def bary(t,idx):
 e=t-origin[idx];uu=u[idx]@u[idx];uv=u[idx]@vv[idx];v2=vv[idx]@vv[idx];eu=e@u[idx];ev=e@vv[idx];den=uu*v2-uv*uv;bb=(v2*eu-uv*ev)/den;cc=(uu*ev-uv*eu)/den
 return min(bb.min(),cc.min(),(1-bb-cc).min())
ids=[];maxerr=0
for k,t in enumerate(out):
 row=int((t.mean(0)[2]-3)/(144/44));cand=np.arange(max(0,row-1)*32,min(44,row+2)*32)
 if not len(cand):continue
 err=np.abs(np.einsum('cvi,ci->cv',t[None,:,:]-origin[cand,None,:],norm[cand])).max(1)
 for idx in cand[err<3e-5]:
  if bary(t,idx)>=-2e-5:ids.append(k);maxerr=max(maxerr,float(abs((t-origin[idx])@norm[idx]).max()));break
assert len(ids)==1298
# Exact original binary triangles only, then independently check documented facet156 boundary.
b=(R/'model.stl').read_bytes();raw=np.array([struct.unpack_from('<12fH',b,84+50*i)[3:12]for i in range(5600)]).reshape(-1,3,3)
def key(t):return tuple(sorted(map(tuple,t)))
lookup={key(t):i for i,t in enumerate(m.triangles)};ex=[]
for rawid in [2708,2711]:
 k=lookup[key(raw[rawid])];t=out[k];err=float(abs((t-origin[156])@norm[156]).max());bc=float(bary(t,156))
 assert k not in ids and err<9e-6 and -.00046<bc<-.00044 and m.face_normals[k,1]<-.9
 assert abs(t[:,2].min()-16.089422454833983)<1e-6
 ex.append(k)
assert lookup[key(raw[5377])] not in ids+ex
assigned=np.ones(5600,np.int32);assigned[ids+ex]=0
p=np.arange(5600)
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(p)):g.setdefault(root(i),[]).append(i)
removed=[]
for ix in g.values():
 if len(set(assigned[ix]))>1:removed.extend(i for i in ix if assigned[i]!=1);assigned[ix]=1
pal=[('Observed original sail layer0 opaque silveroffwhite','#D4D6CF'),('UNVERIFIED innerback thickness braces canopy stairs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=assigned);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'strict_layer0_facets':1298,'documented_boundary_exceptions':len(ex),'outward_layer0_actual':int((assigned==0).sum()),'excluded_step5377':int(assigned[lookup[key(raw[5377])]])==1,'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((assigned==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5600 original triangles unchanged; no perforations or new cuts','limitations':['Layer0 actual finite constructionfacets only, not analyticalsy proximity.','Two explicit originalBoolean edgeexceptions checked on facet156.','Inner layer1 andedge thickness neutral.','Canopy stripes,braces,stairs,body andwindows unverifiedneutral.','Source publication/path years not capture dates;not whole Haoyangbuilding.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5600,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz'),'strict_max_plane_error':maxerr,'domain_counts':domains,'connected_coplanar_domains':len(g)},indent=2));print(domains,np.unique(assigned,return_counts=True))
