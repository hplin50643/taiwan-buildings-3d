"""4426 original triangles; two complete finite low cap upper skins only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a378a3f5d2ddd8370a40f2a3f3ec48df6c414c62dded17920a1eb4bc9f7770c5';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4426
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[];infinite=[]
for x0,x1 in [(-62,-44),(28,46)]:
 aa=np.array([-57,23]);bb=np.array([-37,36]);d=bb-aa;L=np.linalg.norm(d);u=d/L;n=np.array([-u[1],u[0]]);q=t[:,:,1:]-aa
 plane_mask=np.max(abs(q@n),1)<1e-5;along=q@u
 finite=plane_mask&(along.min(1)>=-1e-5)&(along.max(1)<=L+1e-5)&(t[:,:,0].min(1)>=x0-1e-5)&(t[:,:,0].max(1)<=x1+1e-5)
 fields.append(finite);infinite.append(plane_mask)
assert np.array_equal(infinite[0],np.logical_or.reduce(fields))
rail=np.logical_or.reduce(fields)
a[rail]=0;p=np.arange(len(a))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(a)):g.setdefault(root(i),[]).append(i)
removed=[]
for ids in g.values():
 if len(set(a[ids]))>1:removed.extend(i for i in ids if a[i]!=1);a[ids]=1
pal=[('Observed two front low cap upper skins terracotta','#A47565'),('UNVERIFIED main roofs walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_complete_front_low_cap_upper_skins':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==16
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4426 original triangles unchanged; no cuts or newgeometry','limitations':['Two complete front low cap upper skins8+8Boolean triangles; muted terracotta tilefamily.','All3vertices finite tangent andfull extrusion; entire infiniteplane equals union ofboth finite components.','OriginalBoolean occlusion at y-50 not artificial clipping; notches retained.','Allthree mainroofs,walls,windows andothercaps neutral;diningexcluded.','Captureunknown;not2026condition.','Two labels not verifiedfilament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':4426,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
