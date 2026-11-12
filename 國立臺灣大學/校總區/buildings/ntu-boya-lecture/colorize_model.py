"""Original 1092 triangles; coherent source-bounded faces, not subdivided."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;EXPECTED_STL='5bc3c76a42c666bd6360ab1af6abe5a70795dc6eab512843b66e2e7a4587d85f'
assert hashlib.sha256((R/'model.stl').read_bytes()).hexdigest()==EXPECTED_STL
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1092
pal=[('Photo-bounded brick return','#AE7F6C'),('Concrete portico stair and circular aperture','#A8ADA6'),('Observed lower wing light wall','#D0D3CB'),('Existing discrete window shade','#475B56'),('Coarse existing balcony and recess metal family','#9FAFA7'),('Grass reference only original slope upper face','#758656'),('UNVERIFIED or topology-crossing full plane neutral','#A7ABA5')]
mat=np.full(len(m.faces),6,dtype=np.int32)
for i,(t,(x,y,z),n)in enumerate(zip(m.triangles,m.triangles_center,m.face_normals)):
 lo=t.min(0);hi=t.max(0);nx,ny,nz=n
 if hi[2]<=3.001:continue
 # Entire main front is neutral: its large original faces cross upper brick/lower gray.
 if abs(x+17)<.003 and nx<-.99 and lo[2]>=26.499 and lo[1]>=-27.001 and hi[1]<=-22.499:mat[i]=0
 # Existing lower-wing photographed faces only, no roof/rear extrapolation.
 if abs(x+55.5)<.003 and nx<-.99:mat[i]=2
 if abs(y+14.5)<.003 and ny<-.99 and hi[0]<=-16.499:mat[i]=2
 # Existing entrance portico components, all gray concrete; do not borrow bridge.
 if lo[0]>=-63.501 and hi[0]<=19.501 and lo[1]>=-43.501 and hi[1]<=-20.499 and lo[2]>=23.999 and hi[2]<=26.501:mat[i]=1
 if lo[0]>=-63.001 and hi[0]<=-58.999 and lo[1]>=-43.501 and hi[1]<=-20.499 and hi[2]<=26.001:mat[i]=1
 if lo[0]>=-24.001 and hi[0]<=-19.999 and lo[1]>=-25.501 and hi[1]<=-20.499 and hi[2]<=26.001:mat[i]=1
 if lo[0]>=-62.001 and hi[0]<=20.001 and lo[1]>=-49.851 and hi[1]<=-41.149 and hi[2]<=7.001:mat[i]=1
 # Existing gray balcony lips and parapets (coarse originals, no fine railings added).
 for zz in [26,37,48,59]:
  if lo[0]>=-21.001 and hi[0]<=-14.999 and lo[1]>=-22.501 and hi[1]<=40.501 and lo[2]>=zz-.001 and hi[2]<=zz+4.201:mat[i]=4
 # Main front existing recessed window backs/returns; no new front material boundary.
 if lo[1]>=-27.001 and hi[1]<=-26.099 and abs(ny)<.99:mat[i]=4
 if abs(y+26.1)<.003 and ny<-.99:mat[i]=3
 # Lower wing existing cut backs, returns bounded to original wall thickness.
 if abs(x+54.7)<.003 and nx<-.99:mat[i]=3
 if lo[0]>=-55.501 and hi[0]<=-54.699 and abs(nx)<.99:mat[i]=2
 # Roof greenery only sloping top of the original wedge, not any vertical wall.
 if lo[0]>=-60.501 and hi[0]<=-11.499 and lo[1]>=38.999 and hi[1]<=59.001 and lo[2]>=2.899 and hi[2]<=15.901 and .5<nz<.999:mat[i]=5

t=m.triangles;n=m.face_normals;old=mat.copy();hit=np.zeros(len(t),bool);e=.0001
for xx in [-8,6,20,34,48]:
 for zz in [29,39,49]:
  for side in [-1,1]:
   q=(abs(t[:,:,0]-(xx+side*2.9)).max(1)<e)&(t[:,:,1].min(1)>=-27-e)&(t[:,:,1].max(1)<=-26.1+e)&(t[:,:,2].min(1)>=zz-e)&(t[:,:,2].max(1)<=zz+6+e)&(n[:,0]*side<-.999999);assert q.sum()==2;hit|=q
assert hit.sum()==60 and np.all(old[hit]==4)
ad=m.face_adjacency;cs=trimesh.graph.connected_components(ad[(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(t)),min_len=1);assert all(not hit[c].any()or hit[c].all()for c in cs)
oldmix=[c for c in cs if len(set(old[c]))>1];assert len(oldmix)==2
mat[hit]=6;assert all(np.array_equal(old[c],mat[c])for c in oldmix);assert sum(len(set(mat[c]))>1 for c in cs)==2
assert np.bincount(mat).tolist()==[8,295,181,72,224,6,306]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=mat);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((mat==i).sum())}for i,(name,col)in enumerate(pal)],'withdrawn_face_indices':np.flatnonzero(hit).tolist(),'withdrawn_color_faces':60,'new_color_faces':0,'original_colored_faces':846,'colored_faces':786,'neutral_faces':306,'triangles':1092,'complete_selected_domains':30,'original_mixed_domains':2,'current_mixed_domains':2,'original_mixed_domains_indices_and_materials':[{'faces':c.tolist(),'materials':old[c].tolist()}for c in oldmix],'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1092original triangles;STL/OBJ/build unchanged','limits':['Withdraw insufficiently supported blanketmetal designation of60verticalwindowreturns;not evidence everyjamb is brick or wrong.','Designer side photograph contextual only,not color transfer to oppositefacade.','Mainfront149neutralfaces and all otherindices unchanged; original2mixed domains exact.','No newcolor,geometryfix,calibratedHEX or2026claim.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':EXPECTED_STL,'triangles':1092,'withdrawn':60,'new_color':0,'colored':786,'neutral':306,'mixed_domains_unchanged':2,'color_mesh_sha256':hashlib.sha256((R/'color-mesh.npz').read_bytes()).hexdigest()},indent=2)+'\n');print(q['palette'])
