"""65686 original triangles; south highwall front and complete bounded entrance lintel and piers."""
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
a[rail]=0
# The original entrance lintel and two piers form one light-colored frame in
# official album image 5962. Only their original finite box-boundary faces
# are colored. Side/back/soffit continuity is explicitly an inference.
entry_domains={};entry_frame=np.zeros(len(t),bool);eps=2e-5
for name,bounds in [
 ('lintel',[-13,13,-35.5,-34.4,7.1,8.0]),
 ('left_pier',[-12.95,-11.65,-35.2,-33.5,0,7.3]),
 ('right_pier',[11.65,12.95,-35.2,-33.5,0,7.3])]:
 low=np.array([bounds[0]*1.8,bounds[2]*1.8,3+bounds[4]*1.8])
 high=np.array([bounds[1]*1.8,bounds[3]*1.8,3+bounds[5]*1.8])
 within=np.all((t>=low-eps)&(t<=high+eps),axis=(1,2));mask=np.zeros(len(t),bool)
 for axis in range(3):
  for value in [low[axis],high[axis]]:
   mask|=within&(np.max(abs(t[:,:,axis]-value),axis=1)<eps)
 entry_domains[name]=int(mask.sum());entry_frame|=mask
assert entry_domains=={'lintel':34,'left_pier':27,'right_pier':32}
assert entry_frame.sum()==93 and (entry_frame&(a==1)).sum()==91
a[entry_frame]=0
p=np.arange(len(a))
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
pal=[('CNU south highwall and entrance frame graywhite; returns inferred','#D9D9D3'),('CNU Wang Chen Library unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'original_south_highwall_and_lintel_front':int((rail&(a==0)).sum()),'entrance_frame':int((entry_frame&(a==0)).sum()),'entrance_parts':entry_domains,'added_faces':91,'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==139 and len(removed)==0
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'65686 original triangles unchanged; no cuts or newgeometry','limitations':['v2 accepted limited exceptions remain;459opening warnings, directional shortchords,728 junctionpoints with533pair/195triple controls and v1HOLD history. This sourceGO does not recertify printability/support/globalQA. Original homepage preview remains; new variant separate.', 'Original five preview contrast materials and historical files remain unchanged. Entrance-frame fronts are supported by the official photo; side, rear, top and soffit continuity is inferred, not directly verified as current condition.', '139 original faces have nominal graywhite, including 91 added entrance-frame faces; 65547 faces remain unknown neutral. The original 48 observed south-wall/lintel faces are retained. Only building L, not adjacent Q.', 'Named2017/2020/2025 albumfiles not capture or current2026 certification.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':65686,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
