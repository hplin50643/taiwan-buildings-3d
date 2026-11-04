"""5406 original triangles; finite front curved coping andtwo original birdfronts only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='c65460645b2c2633d27ee4938aa5c80ab2d642b179d0a0ff759edb78a09d36b2';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5406
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
# Reconstruct finite original128ellipse chord facets, not radius/normal shortcut.
canopy=np.zeros(len(t),bool)
for k in range(65,127):
 ang=np.array([k,k+1])*2*np.pi/128;uv=np.column_stack([42*np.cos(ang),-28+17.5*np.sin(ang)])
 edge=uv[1]-uv[0];q=t[:,:,:2]-uv[0];u=np.einsum('ijk,k->ij',q,edge)/np.dot(edge,edge)
 dist=abs(q[:,:,0]*edge[1]-q[:,:,1]*edge[0])/np.linalg.norm(edge)
 canopy|=(dist.max(1)<.0001)&(u.min(1)>=-.0001)&(u.max(1)<=1.0001)&span(2,24,25.8)&(abs(m.face_normals[:,2])<.0001)
piers=plane(1,-27)&span(0,-16,16)&span(2,47,57)
a[canopy]=0;a[piers]=2;p=np.arange(len(a))
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
pal=[('Observed front curved coping outward vertical offwhite','#D9D7C9'),('UNVERIFIED multicolor crest mixedwalls roof rear neutral','#B8BAB5'),('Observed two simplified bird profile fronts nominalgold','#BE984F')]
assert (a==0).sum()==124 and(a==2).sum()==16
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'finite_coping_facets65to126':int((canopy&(a==0)).sum()),'two_original_bird_fronts':int((piers&(a==2)).sum()),'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5406 original triangles unchanged; no cuts or newgeometry','limitations':['Coping outervertical finite62facets only;top bottom rear neutral.','Bird originalfront only;no feather beak tail geometry added.','Entire multicolor crest slab neutral.','Mixedbrickgraywalls glazing stairs roof rear neutral.','Captureunknown;EXIFmodify2022 not capture proof.','Three labels not testedfourfilament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5406,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
