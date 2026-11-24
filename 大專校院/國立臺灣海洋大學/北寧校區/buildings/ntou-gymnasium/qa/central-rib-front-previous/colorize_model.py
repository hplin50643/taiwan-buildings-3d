"""5630 original triangles; complete small left-door canopy front fascia only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='752b4c147bd18874b1c49890596c260e58015520f71f60cebc6ee6144700ef49';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5630
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,1]+32.45),1)<1e-5
finite=whole&np.all((t[:,:,0]>=-42-1e-5)&(t[:,:,0]<=-35+1e-5)&(t[:,:,2]>=11.7-1e-5)&(t[:,:,2]<=12.7+1e-5),1)
assert whole.sum()==2 and np.array_equal(whole,finite)
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
pal=[('NTOU Gymnasium small door canopy front nominal gray','#B4B7B5'),('NTOU Gymnasium unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'small_door_canopy_front_whole_component':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==2
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'5630 original triangles unchanged; no cuts or newgeometry','limitations':['2 complete small left-door canopy front triangles nominal gray;5628 neutral.','Original single display material retained unchanged, no geometry repair.','Original strict false/run_checks exit1 and60 polygons opening loss above1percent,1227 short chords and12 along-face rays remain retained finite exceptions.','Color geometry identity PASS is not a global minimum-wall, zero-warning or physical-print certification.','Small canopy solid top is a proxy for photographed open grid, top/underside/returns remain neutral.','EXIF2026-04-21/page2026-04-22 not independently authenticated capture; original2026-03-19 attribution retained unverified.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':5630,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
