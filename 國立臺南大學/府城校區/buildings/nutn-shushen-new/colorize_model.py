"""Four original surviving finite panel front domains only, no geometry edits."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='511db129ca786dcaedee1d1c5a4bf777945b454b0b53f166eff1e7f8d67f0e28';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==1752
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),3,np.int32);D={}
for name,x0,x1,z0,z1,mat,count in [('top_left',-38,-32,94,111,0,6),('top_right',20,26,94,111,0,6),('middle_left',-13,-7,59,94,1,10),('lower_left',-38,-32,41,57,2,6)]:
 hit=(abs(t[:,:,1]+19.9).max(1)<e)&(t[:,:,0].min(1)>=x0-e)&(t[:,:,0].max(1)<=x1+e)&(t[:,:,2].min(1)>=z0-e)&(t[:,:,2].max(1)<=z1+e);ids=np.flatnonzero(hit);assert len(ids)==count,(name,len(ids));D[name]=ids.tolist();a[ids]=mat
original=a.copy();candidate=np.zeros(len(t),bool);by={}
for z,y,x0,x1,h in [(111,-19.7,-56.5,56.5,2),(94,-19.3,-56.5,54.5,2.3)]:
 q=(abs(t[:,:,1]-y).max(1)<.0001)&(t[:,:,0].min(1)>=x0-.0001)&(t[:,:,0].max(1)<=x1+.0001)&(t[:,:,2].min(1)>=z-.0001)&(t[:,:,2].max(1)<=z+h+.0001)&(n[:,1]<-.99999);by[str(z)]=np.flatnonzero(q).tolist();candidate|=q
ad=m.face_adjacency;cs=trimesh.graph.connected_components(ad[(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999],nodes=np.arange(len(t)),min_len=1)
assert candidate.sum()==20 and np.all(original[candidate]==3) and all(not candidate[c].any()or candidate[c].all()for c in cs)
a[candidate]=4;assert np.bincount(a).tolist()==[12,10,6,1704,20]and all(len(set(a[c]))==1 for c in cs)
pal=[('Observed top panel fronts muted yellow','#C7BA63'),('Observed middle-left panel front pale ochre','#D0BC87'),('Observed lower-left panel front terracotta','#B77858'),('UNVERIFIED treehidden panel walls glass roof neutral','#B8BAB5'),('Observed two upper complete front band fields nominal offwhite','#E0E0D9')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'original_domain_face_indices':D,'new_front_band_domains':by,'new_face_indices':np.flatnonzero(candidate).tolist(),'original_colored_faces':28,'added_colored_faces':20,'colored_faces':48,'neutral_faces':1704,'coplanar_components':len(cs),'mixed_coplanar_domains':0,'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'1752 original triangles and original STL/build bytes unchanged','limits':['Original palette0..3 includingneutral3 unchanged; newoffwhite appendedat4. Original28coloredfaces unchanged.','Only two upper visible front band planes; no top/underside/return/depth or treehidden lower band expansion.','Shallow original band depths/notches remain simplified, not newly measured geometry. Nominal offwhite not calibrated.','Unknown photo capture date, pageyear not capture or2026condition. Only new Shushenbuilding, no adjacent old buildings.','Source private, no photo textures or public source images.']}
(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':1752,'original':28,'added':20,'colored':48,'neutral':1704,'mixed_coplanar_domains':0,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2)+'\n');print(q)
