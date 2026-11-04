"""Source-bounded color, exact original 2452 triangles, no new faces."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='fbfdb2588ad010d36724ea67d48560a51f941d440e6f84327f973e14e5cff03e'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==2452
pal=[('Photographed left short-end brick','#A8735D'),('Observed front gray grid','#A9B0B0'),('Observed top-frame front darker gray','#717B80'),('Existing window recess generic shade','#424C4F'),('UNVERIFIED entry opposite end rear horizontal roof','#A7ABA5')]
mat=np.full(len(m.faces),4,dtype=np.int32)
for i,(t,(x,y,z),n) in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 # Whole main front plane; no invented side brick margins on triangles crossing boundaries.
 if abs(y+53)<.003 and ny<-.99:mat[i]=1
 # Only the photograph-matched left short-end plane, not its opposite.
 if abs(x+46)<.003 and nx<-.99:mat[i]=0
 # Existing sparse left-end opening backs/returns.
 for zz in [12,29,46,63,80,97,114]:
  if lo[0]>=-46.001 and hi[0]<=-44.999 and lo[1]>=-10.501 and hi[1]<=-3.499 and lo[2]>=zz-.001 and hi[2]<=zz+6.001:
   mat[i]=3 if nx<-.99 else 0
 # Existing discrete front window cavities, no continuous glazing or new frames.
 for zz in [12,29,46,63,80,97,114]:
  for xx in range(-40,41,5):
   if zz==12 and xx in [-35,-30,-25,-20]:continue
   if zz in [29,46] and xx in [-30,-25,-20,-15]:continue
   if lo[0]>=xx-1.451 and hi[0]<=xx+1.451 and lo[1]>=-53.001 and hi[1]<=-51.949 and lo[2]>=zz-.001 and hi[2]<=zz+10.001:
    mat[i]=3 if ny<-.99 else 1
 for zz in [29,46]:
  for xx in [-30,-18]:
   if lo[0]>=xx-4.501 and hi[0]<=xx+4.501 and lo[1]>=-53.001 and hi[1]<=-51.949 and lo[2]>=zz-.001 and hi[2]<=zz+8.001:mat[i]=3 if ny<-.99 else 1
 # Only observed front of top open frame, not horizontal top/back/side returns.
 if abs(y+53)<.003 and ny<-.99 and lo[2]>=129.999:mat[i]=2
 # Entry cavity, original added approach and canopy not source-confirmed: neutral whole domains.
 if lo[0]>=-39.001 and hi[0]<=-15.001 and lo[1]>=-67.101 and hi[1]<=-51.599 and hi[2]<=39.501 and lo[2]>=2.999:
  if hi[1]<-53.001 or (lo[0]>=-32.501 and hi[0]<=-21.499 and lo[2]>=24.999 and hi[2]<=38.001 and lo[1]>=-53.001 and hi[1]<=-51.599 and (ny>-.99 or y>-52.99)):mat[i]=4
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'2452 original triangles unchanged.','limits':['Only one brick end and gray front are photograph-matched.','Entry/stair/opposite end/rear/horizontal roof neutral.','Five labels are not a tested multi-filament project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
