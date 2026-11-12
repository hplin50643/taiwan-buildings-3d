"""Same-item color study of the EXISTING simplified NTU main-library geometry.
Never rebuild, displace, subdivide, or replace the original STL here.
Face material boundaries follow available original triangles; photo is not a texture.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
R=Path(__file__).resolve().parent
EXPECTED_STL='80f25ad47c6aa3c2918840a275709a07aeba024e064db20aaad97a4bd9d4c909'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True)
assert m.is_watertight and len(m.faces)==3264
pal=[('source-observed reddish brown brick, approximate','#A3664C'),('source-observed pale gray stone, approximate','#B7BCB8'),('source-observed dark gray blue glazing, opaque illustration','#45545C'),('source-observed dark gray sloped roofing','#4A5153'),('source-observed muted blue green tower cap','#56858A'),('UNVERIFIED rear mass and authored support neutral','#99998F')]
c=m.triangles_center;n=m.face_normals;mat=np.zeros(len(c),dtype=np.int32)
def in_arch(x,z,cx,z0,w,h,margin=0):
 r=w/2+margin;s=z0+h-w/2
 return abs(x-cx)<=r and z>=z0-margin and (z<=s or (x-cx)**2+(z-s)**2<=r*r)
for i,((x,y,z),(nx,ny,nz)) in enumerate(zip(c,n)):
 # Neutral support and unresolved original broad back block. No source claim.
 if z<=3.001:mat[i]=5;continue
 tower=-67.1<=x<=-52.9 and -6.6<=y<=12.6
 if (y>0 and not tower) or (tower and y>11.5) or (x>61.9 and y>-20):mat[i]=5
 # Front modeled masses are brick by default. Central frontispiece is pale stone.
 if -7.6<=x<=19.6 and y<-30.4 and 17.8<=z<=46.1:mat[i]=1
 # Existing sloped front roof faces (not the rear flat mass whose roof is unverified).
 if z>50.9 and -11.2<x<23.2 and -31.6<y<-18.4 and nz>.15:mat[i]=3
 if z>41.4 and -7.6<x<19.6 and y<-30.4 and abs(nz)>.15:mat[i]=3
 if tower:
  if z>=60.0:mat[i]=4
  elif 57.45<=z<60.01 or any(a-.02<=z<=a+1.22 for a in [16,33,46]):mat[i]=1
  # Existing belfry aperture edge: pale cap/trim, void remains void.
  if z>=48.9 and (abs(x+60)>3.9 or abs(y-3)>5.9):mat[i]=1
  for z0 in [9,22,36]:
   if y<-4.8 and in_arch(x,z,-60,z0,5,10,margin=.65):mat[i]=1
   if -5.30<y<-4.40 and in_arch(x,z,-60,z0,5,10,margin=-.05):mat[i]=2
 # Roof/parapet trims on two front piers.
 for cx in [-26,38]:
  if abs(x-cx)<=8.1 and y<-16.4 and 48.95<=z<=50.25:mat[i]=1
  if abs(x-cx)<=4.6 and y<-28.4 and 38.9<=z<=48.1:mat[i]=1
  if y<-28.2 and in_arch(x,z,cx,19,6.6,19,margin=.90):mat[i]=1
  if -28.9<y<-28.1 and in_arch(x,z,cx,19,6.6,19,margin=-.05):mat[i]=2
  if abs(x-cx)<2.48 and -28.4<y<-28.15 and 40.02<z<45.98:mat[i]=2
 # Central arched glazed recess, excluding original mullion/rail faces.
 if -33.05<y<-32.54 and in_arch(x,z,6,19,12,21,margin=-.02):mat[i]=2
 if y<-33.40 and in_arch(x,z,6,19,12,21,margin=-.05):mat[i]=2
 # Existing relief mullions: face surfaces at y~-33.6, not recolored glass.
 if -33.62<y<-32.58 and 18.9<z<34.6 and -0.1<x<12.1:
  if any(abs(x-a)<.51 for a in [2,6,10]) or any(abs(z-a)<.51 for a in [24,29,34]):mat[i]=1
 # Entrance arches are dark open/recess studies, not invented doors or interiors.
 for cx in [-8,6,20]:
  if y<-37.1 and in_arch(x,z,cx,3,7,11.5,margin=.95):mat[i]=1
  if -36.05<y<-35.65 and in_arch(x,z,cx,3,7,11.5,margin=-.03):mat[i]=2
 # Shallow flanking ground passages and small existing front windows.
 for cx in [-20,32]:
  if y<-29.5 and in_arch(x,z,cx,3,5,9,margin=.50):mat[i]=1
  if -29.2<y<-28.8 and in_arch(x,z,cx,3,5,9,margin=-.03):mat[i]=2
 for cx in [-43,-36,48,56]:
  for z0 in [9,20,31]:
   if abs(x-cx)<1.82 and -21.25<y<-21.15 and z0-.01<z<z0+5.01:mat[i]=2
 # Separate actual sloping cap faces from the existing gray horizontal/vertical cap seat.
 if tower and z>=57.45:
  mat[i]=1
  if (z>60.5 and .05<nz<.999) or (z>62.95 and nz>=.999):mat[i]=4
 # Uniform existing planar tower surfaces; no centroid-created triangular stone patches.
 if tower and abs(z-49.0)<.002 and nz>.9:mat[i]=1
 if tower and abs(y+6.0)<.002 and ny<-.9 and z<48.9:mat[i]=0
 # Entire unverified planar surfaces remain neutral; no centroid-created diagonal color patches.
 if abs(z-45.8)<.002 and nz>.9:mat[i]=5
 if (abs(x+50)<.002 or abs(x-62)<.002) and abs(nx)>.9:mat[i]=5
 if abs(y-38)<.002 and ny>.9:mat[i]=5
 # Source observed broad stone entrance steps; support remains explicitly neutral.
 if y<-38 and z>3.001:mat[i]=1
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'appearance-materials.json').write_text(json.dumps({'status':'PHOTO_REFERENCED_APPROXIMATE_APPEARANCE_NOT_SURVEY_COLOR','palette':[{'id':i,'name':a,'hex':b,'faces':int(np.count_nonzero(mat==i))}for i,(a,b)in enumerate(pal)],'unverified_rear':'neutral material index5, not claimed measured facade color','four_color_printing':'This six-material appearance is NOT a tested four-filament slicer project. STL itself has no color.','geometry_policy':'3264 original triangles, no displacement/subdivision/geometry edits.'},ensure_ascii=False,indent=2)+'\n')
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
qa={'status':'PASS','original_STL_sha256':EXPECTED_STL,'original_STL_unchanged':hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'vertex_count':len(m.vertices),'watertight':bool(m.is_watertight),'bounds_mm':m.bounds.tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest(),'limitations':'Triangle-level material masks preserve original simplified geometry; fine color boundaries may be coarser than real facade.'}
assert qa['original_STL_unchanged'] and len(np.unique(mat))==6
(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(qa,indent=2)+'\n');print(qa)
