"""3680 original triangles; finite inner vertical coping ellipse chord fields only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d2f6a8a97addc8c6260819dcdb05896d5bc996169f90054384c3939140e5c310';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==3680
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
for k in range(128):
 p0=np.array([48*np.cos(2*np.pi*k/128),10+65*np.sin(2*np.pi*k/128)]);p1=np.array([48*np.cos(2*np.pi*(k+1)/128),10+65*np.sin(2*np.pi*(k+1)/128)]);v=p1-p0;L=np.linalg.norm(v);delta=t[:,:,:2]-p0
 dist=abs(delta[:,:,0]*v[1]-delta[:,:,1]*v[0])/L;u=np.einsum('nvi,i->nv',delta,v)/(L*L)
 fields.append((dist.max(1)<.0001)&(u.min(1)>=-.0001)&(u.max(1)<=1.0001)&(lo[:,2]>=24.5-.0001)&(hi[:,2]<=26.6+.0001)&(lo[:,1]>=-35-.0001)&(hi[:,1]<=58+.0001))
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
pal=[('Observed paired gallery inner upper coping vertical fields offwhite','#D9D8D0'),('UNVERIFIED roofs outerfields mixedwalls openingbacks neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'inner_vertical_coping':int((rail&(a==0)).sum()),'left':int(((a==0)&(t[:,:,0].mean(1)<0)).sum()),'right':int(((a==0)&(t[:,:,0].mean(1)>0)).sum()),'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==136
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'3680 original triangles unchanged; no cuts or newgeometry','limitations':['All vertices on finite original128gon inner vertical chords,rx48/ry65 center0,10,z24.5..26.6.','136 original faces68 per arm;one paired gallery model.','No normal or centroid shortcuts;horizontal roofs outerwalls mixedbase entirelyneutral.','Photo captureunknown;no currentconditionclaim.','Two labels not testedfourfilament.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':3680,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
