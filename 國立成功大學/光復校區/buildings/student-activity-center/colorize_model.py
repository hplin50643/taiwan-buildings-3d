"""Color-family assignment to original 2284 triangles, no geometry changes."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='2531748ccbcdc18d006d7501e590834df96fa5fc4aa17a11094fa23d43dc1211'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2284
pal=[('Observed main light frame and bands','#D0D1C9'),('West front dark gray-brown screen family','#77776F'),('Recess shade not asserted blue glass','#424E4E'),('UNVERIFIED neutral roof rear and display base','#A7ABA5')];mat=np.full(len(m.faces),3,dtype=np.int32)
for i,(t,(x,y,z),n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 # Coherent western front plane only; unknown long western side stays neutral.
 if abs(y+42)<.003 and ny<-.99:mat[i]=1
 for zz in [10,17,24,31]:
  if lo[0]>=-67.501 and hi[0]<=-32.499 and lo[1]>=-42.401 and hi[1]<=-40.399 and lo[2]>=zz-.001 and hi[2]<=zz+1.101:mat[i]=0
 if abs(y+41.2)<.003 and ny<-.99:mat[i]=2
 # Main front parapet, existing columns, exposed terrace/slab edges.
 if lo[0]>=-37.001 and hi[0]<=67.001 and lo[1]>=-23.501 and hi[1]<=-.499 and lo[2]>=16.999 and hi[2]<=19.201:mat[i]=0
 if lo[0]>=-37.001 and hi[0]<=67.001 and lo[1]>=-22.701 and hi[1]<=-20.699 and lo[2]>=18.899 and hi[2]<=23.901:mat[i]=0
 for zz,yy,ww,dd in [(25,-3,96,10),(33,6,80,5)]:
  if lo[0]>=18-ww/2-.001 and hi[0]<=18+ww/2+.001 and lo[1]>=yy-dd/2-.001 and hi[1]<=yy+dd/2+.001 and lo[2]>=zz-.001 and hi[2]<=zz+1.501:mat[i]=0
  if lo[0]>=18-ww/2-.001 and hi[0]<=18+ww/2+.001 and lo[1]>=yy-3.051 and hi[1]<=yy-1.749 and lo[2]>=zz+1.299 and hi[2]<=zz+4.301:mat[i]=0
 for xx in [-30,0,31,61]:
  if lo[0]>=xx-1.301 and hi[0]<=xx+1.301 and lo[1]>=-20.401 and hi[1]<=-17.599 and hi[2]<=18.801:mat[i]=0
 # Existing recessed wall fields and opaque shallow backs, not open-space reconstruction.
 if abs(y+5)<.003 and ny<-.99 and lo[0]>=-33.001:mat[i]=0
 if abs(y-1)<.003 and ny<-.99 and lo[0]>=-22.001:mat[i]=0
 if (abs(y+4.1)<.003 or abs(y-1.9)<.003) and ny<-.99:mat[i]=2
 # Actual modeled near-front stair and plinth; no new success-hall columns.
 if lo[0]>=-7.501 and hi[0]<=13.501 and lo[1]>=-28.001 and hi[1]<=-17.999 and hi[2]<=17.001:mat[i]=0
 if lo[0]>=-39.001 and hi[0]<=69.001 and lo[1]>=-36.001 and hi[1]<=-25.499 and hi[2]<=5.601:mat[i]=0
 # Main broad roof planes have no photograph color control.
 if nz>.99 and z>=23.9 and (hi[1]-lo[1])>5:mat[i]=3
 if nz>.99 and abs(z-26.5)<.003 and lo[1]>=-4.751:mat[i]=3
 if nz>.99 and abs(z-34.5)<.003:mat[i]=3
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat)
(R/'palette.json').write_text(json.dumps(pal,ensure_ascii=False,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'Original2284 triangles unchanged; no surface subdivision.','limits':['No yellow panels: original solid bands lack panel topology.','No gray-blue success-hall columns mapped onto main light columns.','West outside long wall, rear and broad roofs neutral.','Four material labels do not establish a tested four-filament slicer project.']},ensure_ascii=False,indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
