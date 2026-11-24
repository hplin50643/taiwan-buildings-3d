"""7854 original triangles; finite original48gon column sides, reverse side continuity inferred."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='01277bf8746a2ae19b5abe792d334756caa2e22db1252f5d586e1951069ec7a0';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==7854
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
K=.1378645278805804;S=150/132;BASE=2.4
fa=np.array([(730-930)*K,(790-775)*K]);fb=np.array([(1195-930)*K,(790-750)*K]);u=(fb-fa)/np.linalg.norm(fb-fa);north=np.array([-u[1],u[0]]);rad=.9*S
fields=[];column_fields=[];observed=[]
for fraction in [.10,.25,.40,.55,.70,.85]:
 center=(fa+(fb-fa)*fraction+north*(8.2-4*fraction))*S;delta=t[:,:,:2]-center;cf=[]
 for j in range(48):
  theta=2*np.pi*(j+.5)/48;n=np.array([np.cos(theta),np.sin(theta)]);tangent=np.array([-n[1],n[0]])
  q=(np.max(abs(np.einsum('nvi,i->nv',delta,n)-rad*np.cos(np.pi/48)),1)<.0001)&(np.max(abs(np.einsum('nvi,i->nv',delta,tangent)),1)<=rad*np.sin(np.pi/48)+.0001)&(lo[:,2]>=BASE-.05*S-.0001)&(hi[:,2]<=BASE+21.15*S+.0001)
  fields.append(q);cf.append(q)
  if np.dot(n,north)>1e-8:observed.append(q)
 column_fields.append(np.logical_or.reduce(cf))
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
pal=[('Original column sides; observed north and inferred reverse silvergray','#AEB4B5'),('UNVERIFIED caps canopy mixedglazing rails roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
original=np.logical_or.reduce(observed);added=(a==0)&~original
assert original.sum()==327 and added.sum()==335 and (a==0).sum()==662
assert np.all(a[original]==0) and len(removed)==0
assert all(len(set(a[ids]))==1 for ids in g.values())
domains={'observed_north_column_faces':327,'inferred_reverse_faces':335,'colored_faces':662,'neutral_faces':7192,'per_column':[int(x.sum())for x in column_fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g),'original_face_indices':np.flatnonzero(original).tolist(),'new_inferred_face_indices':np.flatnonzero(added).tolist(),'per_column_face_indices':[np.flatnonzero(x).tolist() for x in column_fields]}
assert domains['per_column']==[178,96,96,96,96,100]
limits=['All triangle vertices lie on finite original 48-gon side facets, original tangent and axial bounds.','327 original observed north-facing faces retained; 335 reverse-facing original faces inferred as continuous same-column silvergray, not individually photograph verified.','First and last columns include original Boolean fragments; no new cuts or added geometry.','Caps, canopy, glazing, rails, roofs, courtyard and all other 7192 faces remain unknown-neutral.','Official daylight photos support material family; night photo is not material color evidence.','Capture dates unknown; URL 2016/04 is not confirmed capture date or evidence of 2026 condition.','Nominal HEX, not measured color; not test printed or validated filament slicing.']
q={'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'count_delta':0,'geometry_policy':'7854 original triangles unchanged; no cuts or new geometry','limitations':limits}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':7854,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz'),'domains':domains},indent=2)+'\n');print(domains)
