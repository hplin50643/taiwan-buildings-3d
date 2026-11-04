"""6892 original triangles; upper four original screen tier finfronts only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='d2722ddd9101bceb87ef8540d46127b753451052b5d1e6ec0b0ef0a6963fb3f0';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==6892
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
slabs=np.zeros(len(t),bool)
for z in [34,44,54,64]:
 for x in [-30,-12,6,24,42,60]:
  for dx in [-5.4,-2.7,0,2.7,5.4]:slabs|=plane(1,-8.3)&span(0,x+dx-.575,x+dx+.575)&span(2,z,z+6.5)&(m.face_normals[:,1]<-.99)
a[slabs]=0;p=np.arange(len(a))
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
pal=[('Observed fouruppertiers true finfront offwhite','#D4D1C5'),('UNVERIFIED lowrows mainwalls windowbacks roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'four_visible_screen_tiers_front_fins':int((slabs&(a==0)).sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6892 original triangles unchanged; no cuts or addedgeometry','limitations':['Only four uppertiers120finfront rectangles at y-8.3.','Lowest2tiers treeobscured and allwindowbacks neutral.','All mixedwalls roof sides rearbacking neutral.','One official highview EXIF2009 with unknown timezone;not2026.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':6892,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
