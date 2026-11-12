"""6520 original triangles; observed framefront with bounded inferred same-frame returns."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='7fb891cfc398172c7d835d08a2a84e71bd092dfa5d044135e4e0522d41949a11';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6520
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
slabs=plane(1,-50.5)&(((lo[:,0]>=-26.253)&(hi[:,0]<=-23.747)&span(2,14,93))|(span(0,-31,61)&span(2,66,67.4)))&(m.face_normals[:,1]<-.99)
frame_volume=span(1,-50.5,-47.5)&((span(0,-26.25,-23.75)&span(2,14,93))|(span(0,-31,61)&span(2,66,67.4)))
a[frame_volume]=0;p=np.arange(len(a))
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
pal=[('Observed framefront and inferred same-frame returns offwhite','#D4D1C5'),('UNVERIFIED mixedwalls windows tower curvedwing roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'projecting_frame_front':int((slabs&(a==0)).sum()),'inferred_same_frame_returns':int((~slabs&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6520 original triangles unchanged; no cuts or addedgeometry','limitations':['Observed framefront retained. Side returns, top, underside and recess-exposed back faces within the same bounded projecting frame use an explicitly inferred same-material extension.','Mixed pink/pale mainwalls and thick windowgrids neutral.','Tower, curved wing, stairs, roofs, main side/rear walls and unrelated window backs remain neutral. Same-frame return color is inferred, not a measured all-facade finish.','All four official photos capturedateunknown;1998completion not photo date.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':6520,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
