"""6892 original triangles; upper four screen tiers plus bounded lower-left finfronts."""
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
original=a.copy();added=np.zeros(len(a),bool)
for z in [14,24]:
 for x in [-30,-12,6]:
  for dx in [-5.4,-2.7,0,2.7,5.4]:
   hit=plane(1,-8.3)&span(0,x+dx-.575,x+dx+.575)&span(2,z,z+6.5)&(m.face_normals[:,1]<-.99)
   assert hit.sum()==2;added|=hit
assert added.sum()==60 and np.all(original[added]==1)
assert all(not added[c].any() or added[c].all() for c in g.values())
a[added]=0
assert (original==0).sum()==240 and (a==0).sum()==300 and np.array_equal(a[~added],original[~added])
assert all(len(set(a[c]))==1 for c in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'four_visible_screen_tiers_front_fins':int((slabs&(a==0)).sum()),'lower_left_fin_added_faces':int(added.sum()),'whole_coplanar_withdrawals':len(removed)}
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'6892 original triangles unchanged; no cuts or addedgeometry','limitations':['Original120 upper finfront rectangles plus30 lower-left rectangles at y-8.3.','Lowest2tiers only left3 screened bays added; right3 remain neutral; allwindowbacks neutral.','All mixedwalls roof sides rearbacking neutral.','Official highview2009 and frontal2010 EXIF clocks unverified; not2026.','Two material labels not tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_colored':240,'new_faces':60,'new_face_indices':np.flatnonzero(added).tolist(),'colored':300,'neutral':6592,'triangles':6892,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
