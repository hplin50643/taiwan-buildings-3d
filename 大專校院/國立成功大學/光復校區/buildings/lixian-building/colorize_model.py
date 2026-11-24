"""Existing-face material update only. No geometry change, subdivision, or photo texture."""
from pathlib import Path
import hashlib,json,numpy as np,trimesh
R=Path(__file__).resolve().parent
EXPECTED_STL='584bec17ff0addc03e6ec92291dae9f330b66ebc4bc80403d774f03dda7cc297'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==5376 and m.is_watertight
pal=[('Approximate restored red-orange pier brick','#B65E41'),('Approximate restored warm-white arcade and entrance','#E9E5DE'),('Approximate gray-beige balustrade and cornice','#9A998E'),('UNVERIFIED side rear roof and authored base neutral','#AAA99E')]
mat=np.full(len(m.faces),3,dtype=np.int32)
xs=[-62,-50,-23,-11.5,0,11.5,23,50,62]
piers=[-69,-57,-44,-29,-17,-5.8,5.8,17,29,44,57,69]
for i,((x,y,z),(nx,ny,nz)) in enumerate(zip(m.triangles_center,m.face_normals)):
 if z<=2.701:continue
 # Existing facade and recess wall/intrados default warm white. Broad coplanar front
 # triangles cross real white-ring/brick boundaries: deliberately not falsely cut.
 if y<-13.99:mat[i]=1
 # Normal narrow projecting column bellies only; no invented horizontal segmentation.
 if m.triangles[i][:,1].max()<=-15.49 and z<33.45 and any(np.all(np.abs(m.triangles[i][:,0]-a)<=.661) for a in piers):mat[i]=0
 # Front-plane spandrels are not uniformly brick: lack of exact ring topology is retained.
 # Existing balustrades and their incised grooves.
 if -17.01<y<-15.35 and m.triangles[i][:,2].min()>=18.99 and m.triangles[i][:,2].max()<=21.81 and any(np.all(np.abs(m.triangles[i][:,0]-a)<=5.01) for a in xs):mat[i]=2
 # Existing entrance pavilions: tall front columns white, caps gray, beam gray.
 for cx in [-36.5,36.5]:
  if abs(x-cx)<8.51 and y<-13.99:mat[i]=1
  if abs(x-cx)<6.01 and y<-18.49 and 17.99<z<20.21:mat[i]=2
  for dx in [-7,7]:
   if abs(x-cx-dx)<1.31 and y<-17.49 and 2.99<z<35.01:mat[i]=1
   if abs(x-cx-dx)<2.11 and y<-16.89 and 34.79<z<36.81:mat[i]=2
  if abs(x-cx)<6.01 and y<-19 and z<5.1:mat[i]=2
 # Front fascia is known gray, but huge horizontal roof surface stays neutral.
 if y<-15.99 and 33.19<z<35.81:mat[i]=2
 if z>=35.79 and nz>.9:mat[i]=3
 # Unverified end and rear surfaces cannot inherit the front paint observation.
 if abs(x)>=69.99 or y>=-13.99:mat[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'original_STL_unchanged':True,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'vertex_count':len(m.vertices),'watertight':bool(m.is_watertight),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest(),'limitations':'Existing front coplanar triangles lack separate white arch rings; broad crossing faces remain warm white, brick pier bellies are colored. No wood door/window geometry added.'}
assert len(np.unique(mat))==4
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int(np.count_nonzero(mat==i))}for i,(a,b)in enumerate(pal)],'four_color_printing':'Four appearance labels are NOT a verified four-filament slicer project; STL has no color.','geometry_policy':'Original 5376 triangles, no subdivision or movement.','unknown':'Sides, rear, broad roof and base are neutral; not measured original paint.'},indent=2)+'\n');print(q)
