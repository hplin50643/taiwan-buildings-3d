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
# Existing rounded platform thin front edge only; not tall parapet or panelled soffit.
t=m.triangles;old=mat.copy();hit=np.zeros(len(t),bool);ap=11*np.cos(np.pi/48)
for k in range(24,48):
 th=(k+.5)*2*np.pi/48;n2=np.array([np.cos(th),np.sin(th)])
 d=np.einsum('fvi,i->fv',t[:,:,:2]-[-27,-55],n2)
 q=np.all(abs(d-ap)<.001,axis=1)&(m.face_normals[:,:2]@n2>.999999)&np.all(t[:,:,2]>=24.599,axis=1)&np.all(t[:,:,2]<=27.001,axis=1)&np.all(t[:,:,1]<=-58.499,axis=1);hit|=q
assert np.flatnonzero(hit).tolist()==[2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2206, 2207, 2208, 2209, 2211, 2212, 2213, 2229, 2230, 2231, 2232, 2236, 2237, 2238, 2241, 2242, 2243, 2246, 2248, 2249, 2252, 2253, 2264, 2265, 2267, 2269, 2271, 2272, 2273] and np.all(mat[hit]==4)
e=m.face_adjacency;groups=trimesh.graph.connected_components(e[np.einsum('ij,ij->i',m.face_normals[e[:,0]],m.face_normals[e[:,1]])>.999999],nodes=np.arange(len(t)),min_len=1)
assert all(not hit[g].any()or hit[g].all()for g in groups)
mat[hit]=1;assert np.array_equal(mat[~hit],old[~hit]);assert np.bincount(mat).tolist()==[100,1596,14,242,500]
assert all(np.array_equal(old[g],mat[g])for g in groups if len(set(old[g]))>1)
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
(R/'appearance-materials.json').write_text(json.dumps({'palette':[{'id':i,'name':a,'hex':b,'faces':int((mat==i).sum())}for i,(a,b)in enumerate(pal)],'geometry_policy':'2452 original triangles unchanged.','limits':['Only one brick end and gray front are photograph-matched.','40 original thin round-platform front edge faces gray; rest of entry/stair/opposite end/rear/horizontal roof remain neutral.','Five labels are not a tested multi-filament project.']},indent=2)+'\n')
q={'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':len(m.faces),'materials_used':np.unique(mat).tolist(),'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()};(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps(q,indent=2));print(q)
