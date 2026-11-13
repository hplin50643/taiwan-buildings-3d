"""25704 original triangles; two complete front120cm canopy underside components only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='07fe1f62fa94da4bb0dc3dc1c9fd2d8873e69e95e8e793a80a2025f79faf4be3';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==25704
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
# Original rows(n,x0,y0), canopy120cm, transform(-17.1,-14.5,+.55)*5.
whole=np.max(abs(t[:,:,2]-(3.30+.55)*5),1)<1e-5
for n,x0,y0,expected_count in [(6,0,0,35),(4,5.7,19,22)]:
 low=np.array([(x0-.12-17.1)*5,(y0-.12-1.21-14.5)*5,(3.30+.55)*5]).astype('f4').astype(float)
 high=np.array([(x0+n*5.7+.12-17.1)*5,(y0-.12+.01-14.5)*5,(3.30+.55)*5]).astype('f4').astype(float)
 finite=whole&np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2))
 assert finite.sum()==expected_count,(low,high,finite.sum())
 fields.append(finite)
assert np.logical_or.reduce(fields).sum()==57 # remaining same-z rear soffits are unobserved neutral
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
pal=[('NTU Scholar Residence Two Rows 1965 Design 1963 1965 design white cement soffit','#D9D9D0'),('NTU Scholar Residence Two Rows 1965 Design unverified walls windows neutral','#B8BAB5')]
# A2 section4 rear120cm canopy underside explicit whitecement design.
prior=a.copy();added=[];rear_counts=[]
for n,x0,y0,cnt in [(6,0,0,37),(4,5.7,19,24)]:
 low=np.array([(x0-.12-17.1)*5,(y0+7.62-.01-14.5)*5,19.25]).astype('f4').astype(float)
 high=np.array([(x0+n*5.7+.12-17.1)*5,(y0+7.62+1.21-14.5)*5,19.25]).astype('f4').astype(float)
 hit=np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2));ids=np.flatnonzero(hit)
 assert len(ids)==cnt and (prior[ids]==1).all()
 assert any(set(ids)==set(q) for q in g.values()),'not entire connected coplanar domain'
 a[ids]=0;added.extend(ids.tolist());rear_counts.append(len(ids))
assert len(set(added))==61 and (a==0).sum()==118
other=np.setdiff1d(np.arange(len(a)),added);assert np.array_equal(a[other],prior[other])
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'two_complete_front_canopy_soffits':int((rail&(a==0)).sum()),'front_per_rectangle':[int(x.sum())for x in fields],'two_complete_rear_canopy_soffits':len(added),'rear_per_rectangle':rear_counts,'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==118
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'25704 original triangles unchanged; no cuts or newgeometry','limitations':['two authored separate bases not site reconstruction', 'onlysix+fourcurrentphase; not four whole motherplan rows', 'exact current location unproven; not1970WangDaHong', 'all original dimension conflicts/heightapproximations/printthickening unchanged', 'not new printability or global QA approval', '118 complete canopy underside faces:57front+61rear,not fascia/top/upper roof.', '1963–1965 DESIGN finish whitecement,not current or asbuilt color.', 'Original eight illustrative materials and37originalfiles retained unchanged.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':25704,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
