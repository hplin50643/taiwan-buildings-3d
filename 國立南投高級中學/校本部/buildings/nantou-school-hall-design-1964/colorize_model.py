from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='e991e8d40fd2b86acb95e78ff5cb2c4ea695c6508cea7aec2f96bb4584a416ac'
assert H(R/'model.stl')==expected
d=np.load(R/'mesh.npz');m=trimesh.Trimesh(d['vertices'],d['faces'],process=False);t=m.triangles;a=d['materials'].copy();old=a.copy();assert len(t)==35618
whole=np.max(abs(t[:,:,0]-(-23.5*5)),axis=1)<1e-5;assert whole.sum()==88
fields=[]
for ya,yb in [(9.12,13.63),(13.87,18.38)]:
 low=(np.array([0,ya,.5])+[-23.5,-13.75,1])*5;high=(np.array([0,yb,4.02])+[-23.5,-13.75,1])*5
 finite=whole & np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2));assert finite.sum()==10;fields.append(finite)
sel=np.logical_or.reduce(fields);assert sel.sum()==20 and np.all(old[sel]==0)
p=np.arange(len(t))
def root(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
for i,j in m.face_adjacency:
 if np.dot(m.face_normals[i],m.face_normals[j])>.999999:p[root(i)]=root(j)
g={}
for i in range(len(t)):g.setdefault(root(i),[]).append(i)
assert all(not sel[ids].any()or sel[ids].all()for ids in g.values());assert len({root(i)for i in np.flatnonzero(sel)})==2
a[sel]=6;assert np.array_equal(a[~sel],old[~sel])
pal=[('neutral wall','#CBC8BC'),('unverified roof finish','#AEB6B4'),('opaque glazing','#526C74'),('simplified frame','#DEDCD0'),('authored base','#96958D'),('backed screen recess','#777C75'),('Nantou1964 A5 nominal DESIGN black door surrounds','#333333')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
report={'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'domains':{'selected_complete_surround_faces':20,'whole_x_candidates':88,'excluded_other_faces':68,'selected_components':2,'per_rectangle':[int(x.sum())for x in fields],'coplanar_domains':len(g)},'partial_color_incomplete':True,'fully_colored_exterior':False,'design_color_only':True,'geometry_policy':'35618 original NPZ triangles/vertices/order unchanged; original STL retained byteexact','limitations':['1964 A5 nominalblack DESIGN finish only,not asbuilt/current.','Only clearly written black family used; uncertain intermediate method characters not asserted;red ink rendering isnot redmaterial evidence.','20 original mat0faces to appendedmat6;35598 original six illustrative assignments and RGB EXACT,not newly certified.','Original LOCAL_READY_PUBLICATION_HOLD metadata retained as history,not removed by sourcecolorGO.','Unconfirmed identity to1965built Zhongzhenghall/1989or1990buildings unresolved.','Original15cm door discrepancy,datums/±.10m estimates,backed decorative brickproxy and printlimits retained.']}
(R/'appearance-materials.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':35618,'original_STL_sha256':expected,'color_mesh_sha256':H(R/'color-mesh.npz'),'only_20_assignments_changed':True,'remaining_original_material_assignments_exact':True},indent=2));print(np.unique(a,return_counts=True),report['domains'])
