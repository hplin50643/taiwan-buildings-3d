"""5500 original triangles; both bounded rooftop cross broad profiles; narrow returns unchanged."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='2b7f6bae46e83a82ee78eb99707daad1387d7b3849b7f4996c76623fb0fa8565';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5500
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]-14.1),1)<1e-5
finite=whole&np.all((t[:,:,0]>=-58-1e-5)&(t[:,:,0]<=-48+1e-5)&(t[:,:,2]>=77.9-1e-5)&(t[:,:,2]<=86.5+1e-5),1)
assert whole.sum()==10 and np.array_equal(whole,finite)
fields=[finite]
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
pal=[('CJCU Administration approach-facing rooftop cross off-white','#DDDCD5'),('CJCU Administration unverified walls windows neutral','#B8BAB5')]
original=a.copy();opposite=np.max(abs(t[:,:,1]-11.9),1)<1e-5
bounded=opposite&np.all((t[:,:,0]>=-58-1e-5)&(t[:,:,0]<=-48+1e-5)&(t[:,:,2]>=77.9-1e-5)&(t[:,:,2]<=86.5+1e-5),1)
assert opposite.sum()==10 and np.array_equal(opposite,bounded) and np.all(original[opposite]==1)
assert all(not opposite[c].any() or opposite[c].all() for c in g.values())
a[opposite]=0;assert all(len(set(a[c]))==1 for c in g.values())
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'cross_whole_profile_component':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g),'opposite_profile_faces':int(opposite.sum()),'new_face_indices':np.flatnonzero(opposite).tolist()}
assert (a==0).sum()==20
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5500 original triangles unchanged; no cuts or newgeometry','limitations':['Original10 approach-facing plus10 opposite whole-profile triangles off-white; originalpalette name is historical.','Whole y14.1 originalprofile preserved; newwhole y11.9 oppositeprofile added; narrowreturns stillneutral.','Stone tower crosses dark base with no material boundary, so whole tower neutral.','Brick arcade glazing roof and all unlisted faces neutral; neighboring left library excluded.','Source URL201807 is not verified capture date; not2026 survey or tested filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5500,'new_faces':10,'colored':20,'neutral':5480,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
