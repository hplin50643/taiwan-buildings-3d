"""2984 original triangles unchanged; member-based, whole-face bounded material."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;expected='e441be1ba889649fd965097334f68f597d31b0bdc25fad0fb317e0c6a94cc309';assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2984
t=m.triangles;lo=t.min(1);hi=t.max(1);a=np.full(len(t),2,np.int32)
def span(ax,l,h):return (lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
def box(x0,x1,y0,y1,z0,z1):return span(0,x0,x1)&span(1,y0,y1)&span(2,z0,z1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
front=np.zeros(len(t),bool);right=front.copy();brows=front.copy();fc=[];rc=[]
for x in range(29,67,2):
 s=box(x-.55,x+.55,-32.3,-28.9,30,62);front|=s;fc.append(int(s.sum()))
for y in range(-24,20,2):
 s=box(68.9,72.3,y-.55,y+.55,30,62);right|=s;rc.append(int(s.sum()))
capfront=plane(1,-32)&box(22,72,-32,-32,66,68.8)&(m.face_normals[:,1]<-.99)
capright=plane(0,72)&box(72,72,-32,26,66,68.8)&(m.face_normals[:,0]>.99)
for z in [71,82,93,104]:
 for zz in [z-1.5,z+6]:brows|=plane(0,48)&box(48,48,-12.5,16.5,zz,zz+1.5)&(m.face_normals[:,0]>.99)
assert min(fc)>0 and min(rc)>0 and capfront.sum()==2 and capright.sum()==2 and brows.sum()==16
assert not np.any((front|right)&(capfront|capright|brows))
a[front|right]=0;a[capfront|capright|brows]=1
pal=[('Observed independent front and right fins charcoal','#3D4140'),('Observed cap outer fascia and high eyebrows palegray','#CBCDCA'),('UNVERIFIED mixed green/window walls rear roof neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':n,'hex':c,'faces':int((a==i).sum())}for i,(n,c)in enumerate(pal)],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'2984 original triangles unchanged; no new or split faces','domains':{'front_fins':int(front.sum()),'right_fins':int(right.sum()),'individual_front_fin_counts':fc,'individual_right_fin_counts':rc,'cap_front':int(capfront.sum()),'cap_right':int(capright.sum()),'high_eyebrows_x_front':int(brows.sum())},'limitations':['Only original independent fins, cap outward fascia and high eyebrow end faces.','Green lower band has unmodeled windows; entire backing neutral. Mixed fullheight walls and rails neutral.','Photo capture dates unknown;2023 form and2025 PDF edition not capture dates.','Material labels are not a verified multi-filament slicing job.']},indent=2)+'\n')
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','triangles':2984,'original_STL_sha256':expected,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2));print(np.unique(a,return_counts=True))
