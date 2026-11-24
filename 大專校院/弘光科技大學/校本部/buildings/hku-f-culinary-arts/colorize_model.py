"""4180 original triangles; six complete framing strip front rectangles only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='f6da2b555c5e75e62ea3d166f559cbc01262d42c327104456761decbe0103ee6';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4180
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+24),1)<1e-5
fields=[whole&(t[:,:,0].min(1)>=cx-1-1e-5)&(t[:,:,0].max(1)<=cx+1+1e-5)&(t[:,:,2].min(1)>=12-1e-5)&(t[:,:,2].max(1)<=64+1e-5) for cx in [-63,-46,-29,-12,5,22]]
assert np.array_equal(whole,np.logical_or.reduce(fields))
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
pal=[('Observed six complete front framing strips offwhite','#DEDDD3'),('UNVERIFIED mixed louvers signwall roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'six_complete_framing_fronts':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==12
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4180 original triangles unchanged; no cuts or newgeometry','limitations':['Six complete framing fronts, twelve original triangles, offwhite.','All three vertices finite rectangles; whole infinite plane equals their union.','Awning union naturally hides original lower frame surfaces, not material clipping.','Full width topcap has no proven full correspondence; mixed louvers, lettering wall and marked awning neutral.','F Culinary Arts building is not L event venue or D Food Technology.','Flag2024 is not exact capture date; not2026 condition.','Two labels not verified filament slicing.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':4180,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
