"""18548 original triangles; complete analytical dry pool floor only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='4b7f69e59b76e32cee16be3402f990cd72c9a429df253c8553f070549359b5dd';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==18548
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.ones(len(t),np.int32)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
whole=np.max(abs(t[:,:,2]+(.18/50.1)*t[:,:,0]-2.84),1)/np.sqrt(1+(.18/50.1)**2)<1e-5
finite=whole&np.all((t[:,:,0]>=-100.2-1e-5)&(t[:,:,0]<=100.2+1e-5)&(t[:,:,1]>=-24.9-1e-5)&(t[:,:,1]<=75.5+1e-5),1)
assert whole.sum()==144 and np.array_equal(whole,finite)
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
pal=[('NKNU Pool Stand 1985 Design 1985 design specified water blue tile nominal shade','#78B9CC'),('NKNU Pool Stand 1985 Design unverified walls windows neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
domains={'complete_dry_floor_1985_design_tile':int((rail&(a==0)).sum()),'per_rectangle':[int(x.sum())for x in fields],'whole_coplanar_withdrawals':len(removed),'coplanar_domains':len(g)}
assert (a==0).sum()==144
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':domains,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'18548 original triangles unchanged; no cuts or newgeometry','limitations':['OriginalA2-2stand58.90m vsA2-1 58.75m difference preserved;GLheights9.37mvs9.40m remain.', 'Original50.10x25.10mstructuralbasin vs50x25mfinishedtileclear size stays; nofinishthicknessgeometriccorrection. Slopedfloor0to−.18m/local−.20drain omitted remains.', 'Tenlanes,20blocks and6simplifiedladderpositions remainoriginalgeometry; whitecross18designnote not used tochange counts.', 'Originalsite51.25vs51.30m discrepancy,glassopaque/hiddenstairs/pipesomissions andsupportbase notsurvey remain.', 'FormatQA originalzeroarea0,mintrianglearea5.25e−9mm2,watertightonecomponent androundtrip do notguaranteephysicalprint,minwall/support/strength. No QA reapproval orrepair.', 'Originalhistoricalidentity1985designnot1987verifiedcompletion,notpostrenovationor2026conditions. Onegroupcount0.', '1985 DESIGN COLOR ONLY;not observed/current asbuilt color,not water.', '144 complete dryfloor triangles;18404 unknownneutral. Original6classification materials and all history retained.', 'Waterblue tile requires sample approval;HEX is nominal not approved swatch.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':18548,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(np.unique(a,return_counts=True),domains)
