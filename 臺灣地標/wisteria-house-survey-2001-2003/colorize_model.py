"""12920 original triangles; six complete upper north/south outer-window outward surrounds only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='40aebcdd46b43c3ba9066c6031b0c07855f4184cdf83e51b56108cf2a4d78fde';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==12920
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
# Derive exact centimetre rounding and add() +6mm datum from original window()/box().
for pl,cx,w in [(3.45,18.85,2.30),(3.45,22.10,2.30),(1.35,27.30,2.05)]:
 low=(np.round(np.array([cx-w/2-.055,pl-.06,5.02-.055])*100)+[0,0,60])*.1
 high=(np.round(np.array([cx+w/2+.055,pl+.025,5.02+1.74+.055])*100)+[0,0,60])*.1
 low=low.astype('f4').astype(float);high=high.astype('f4').astype(float)
 whole=np.max(abs(t[:,:,1]-low[1]),1)<1e-5
 finite=whole&np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2))
 assert finite.sum()==16,(low.tolist(),high.tolist(),finite.sum())
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
pal=[('Wisteria House Survey 2001 2003 survey deep coffee timber outer surrounds','#594137'),('Wisteria House Survey 2001 2003 unverified walls windows neutral','#B8BAB5')]
# Bounded continuation: three entire northern upper outer-surround planes.
prior=a.copy();added=[];north_counts=[]
for pl,cx,w,zz,hh in [(9.10,21.45,2.50,4.92,1.78),(9.10,18.65,1.18,5.00,1.70),(6.65,27.30,2.00,5.00,1.72)]:
 low=((np.round(np.array([cx-w/2-.055,pl-.025,zz-.055])*100)+[0,0,60])*.1).astype('f4').astype(float)
 high=((np.round(np.array([cx+w/2+.055,pl+.06,zz+hh+.055])*100)+[0,0,60])*.1).astype('f4').astype(float)
 hit=(np.max(abs(t[:,:,1]-high[1]),1)<1e-5)&np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2))&(m.face_normals[:,1]>.99)
 ids=np.flatnonzero(hit);assert len(ids)==16 and (prior[ids]==1).all()
 assert any(set(ids)==set(q) for q in g.values()),'not whole connected coplanar domain'
 a[ids]=0;added.extend(ids.tolist());north_counts.append(len(ids))
assert len(set(added))==48 and (a==0).sum()==96
assert np.array_equal(a[np.setdiff1d(np.arange(len(a)),added)],prior[np.setdiff1d(np.arange(len(a)),added)])
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'three_upper_south_outer_surrounds':int((rail&(a==0)).sum()),'three_upper_north_outer_surrounds':len(added),'north_per_rectangle':north_counts,'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==96
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'12920 original triangles unchanged; no cuts or newgeometry','limitations':['Survey exterior not1920s original or post2008/current restoration; multiple survey dates preserved.', 'West timber wing, east two-storey addition and low service/flower roofs form one study; no garden/perimeter/interior/furniture.', 'Right-angle simplification, scan-registered dimensions, common display datum, approximate footings/steps/roof valleys and sparse tilecourses remain.', 'Glass is opaque backed geometry; no hidden equipment or detailed construction fidelity.', 'Original digitalQA12920faces/singlecomponent/watertight/15checks not newly reapproved. Manufacturing risks thinpergola/frames/supports remain; no trialprint.', '96 complete outer surround outwardfaces only:48south+48north;12824neutral,not mullions rails or reveals.', 'Original10materials retained;white-painted timber board source evidence remains valid,not denied.', '2001/06 and2003/03 surveycoat colorfamily,not calibrated RGB or post2008/current condition.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':12920,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
