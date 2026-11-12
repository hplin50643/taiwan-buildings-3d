"""65686 original triangles; complete south highwall and entrylintel front planes only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='353a5ce7fcd15a798f8bbf932e73d67b95ef856c60623cc3d7831f46dd609897';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==65686
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
# Original S=1.8 BASE=3; full front planes of highwall and entrylintel original add().
for x1,x2,y,z1,z2,n in [(-24.,30.2,-2.9,40.,44.4,46),(-13.,13.,-35.5,7.1,8.,2)]:
 yy=float(np.float32(y*1.8));low=np.array([x1*1.8,yy,3+z1*1.8]).astype('f4').astype(float);high=np.array([x2*1.8,yy,3+z2*1.8]).astype('f4').astype(float)
 whole=np.max(abs(t[:,:,1]-yy),1)<1e-5
 finite=whole&np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2))
 assert whole.sum()==n and np.array_equal(whole,finite),(yy,whole.sum(),finite.sum())
 fields.append(finite)
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
pal=[('CNU Wang Chen Library source observed southwall and lintel graywhite','#D9D9D3'),('CNU Wang Chen Library unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'south_highwall_and_entrylintel':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==48
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'65686 original triangles unchanged; no cuts or newgeometry','limitations':['v2 accepted limited exceptions remain;459opening warnings, directional shortchords,728 junctionpoints with533pair/195triple controls and v1HOLD history. This sourceGO does not recertify printability/support/globalQA. Original homepage preview remains; new variant separate.', 'Original5 preview contrast materials and everyoriginal file remain unchanged. New separate variant assigns48 documented faces light family; all otherfaces unknownneutral, not an assertion original darkpreview was real dark finish.', '48complete original faces only,65638unknownneutral;L only not adjacentQ.', 'Named2017/2020/2025 albumfiles not capture or current2026 certification.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':65686,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
