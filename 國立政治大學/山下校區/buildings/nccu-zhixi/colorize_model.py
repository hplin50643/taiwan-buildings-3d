"""Existing Zhixi geometry; lower portal structural-pier front material correction only."""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
R=Path(__file__).resolve().parent;EXPECTED_STL='8708e06528a5e6287650b16b1ca37473c3fe9941156243aab04bb27b1024f1b8'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1026 and m.is_watertight
pal=[('Observed gray washed aggregate, approximate','#999A90'),('Observed light aluminum frame, approximate','#BCC0BB'),('Opaque dark recess / glazing illustration','#4D585A'),('Observed darker projecting eave and eyebrow','#6C716B'),('UNVERIFIED roof and rear neutral','#A5AAA7'),('Authored display plinth','#AAA9A3')]
mat=np.zeros(len(m.faces),dtype=np.int32)
for i,((x,y,z),(nx,ny,nz))in enumerate(zip(m.triangles_center,m.face_normals)):
 if z<=3.001:mat[i]=5;continue
 if z>=27.599:mat[i]=4;continue
 # Existing connected eave fascia, not all hipped roof skin.
 if 26.39<z<27.61:mat[i]=3
 # Explicitly unverified blank rear and outer long sides.
 if abs(y-24.5)<.002 and ny>.9:mat[i]=4
 if abs(abs(x)-66)<.002 and abs(nx)>.9:mat[i]=4
 # Original recessed five central high windows: exposed back surface, not added panes.
 if -1.01<y<-.99 and 14<z<23 and any(abs(x-c)<2.66 for c in [-13.6,-6.8,0,6.8,13.6]):mat[i]=2
 # Original central crossbars, side jambs and horizontal entrance eyebrows.
 if -4.01<y<-1.99 and 17.99<z<19.01 and any(abs(x-c)<2.66 for c in [-13.6,-6.8,0,6.8,13.6]):mat[i]=1
 if any(abs(x-c)<1.01 for c in [-17,17]) and -4.51<y<-1.49 and 3<z<28.01:mat[i]=1
 if -6.56<y<-.99 and 11.99<z<13.31 and abs(x)<19.51:mat[i]=3
 # Existing entrance is a single recessed opening, not reconstructed doors.
 if abs(y)<.002 and 3<z<12.59 and abs(x)<16.51:mat[i]=2
 # Courtyard rear-bar window recesses (y8.8 backs).
 if abs(y-8.8)<.003 and any(abs(x-c)<4.01 for c in [-27,27]) and any(a<z<a+6 for a in [6,18]):mat[i]=2
 # Wing inner recess backs x32.5 / -32.5.
 if abs(abs(x)-32.5)<.003 and any(abs(y-c)<4.01 for c in [4,-8]) and any(a<z<a+6 for a in [6,18]):mat[i]=2
 # Front end-wall windows, two per floor per wing, recess back y-27.
 if abs(y+27)<.003 and any(abs(x-c)<3.51 for c in [-56,-44,44,56]) and any(a<z<a+6 for a in [6,18]):mat[i]=2
 if 13.99<z<15.21 and abs(abs(x)-34)<.76:mat[i]=3
 if y<-7 and z<5.1:mat[i]=1
 # Unphotographed rear/outside projecting fascia is not source-observed dark eave.
 if mat[i]==3 and (y>24.51 or abs(x)>66.01):mat[i]=4
# Correct only finite lower structural pier front faces, not aluminum doorway frames.
t=m.triangles
selected=(np.abs(t[:,:,1]+4.5).max(1)<1e-4)&(t[:,:,2].min(1)>=3-1e-4)&(t[:,:,2].max(1)<=12+1e-4)&(np.abs(t[:,:,0]).min(1)>=16.5-1e-4)&(np.abs(t[:,:,0]).max(1)<=18+1e-4)
assert np.flatnonzero(selected).tolist()==[507,509,523,525]
original=mat.copy();assert (original[selected]==1).all()
mat[selected]=0;assert np.array_equal(mat[~selected],original[~selected])
ad=m.face_adjacency;cs=trimesh.graph.connected_components(ad[(m.face_normals[ad[:,0]]*m.face_normals[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(mat)),min_len=1)
assert all(not selected[c].any() or selected[c].all() for c in cs)
assert np.bincount(mat).tolist()==[491,169,44,116,150,56]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.count_nonzero(mat==i))}for i,(a,b)in enumerate(pal)],'geometry_policy':'1026 original triangles unchanged','limits':['2021 inventory exterior photo version, not earlier red entrance.','Neutral large roof surfaces and blank rear; no inferred tile color.','No new doorway, frames, or photo texture.','Six-material appearance is not a tested four-filament print project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'watertight':bool(m.is_watertight),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};assert len(np.unique(mat))==6;(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
