"""Original v2 south crown panel and bounded front cylindrical column sides."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='4fde918dd4060a88e5ed64b03e6a233e8e34d176306fd21f16cbd171e14acb35';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==38898
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,1]+66.3).max(1)<1e-5);assert len(ids)==179
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
assert ((t[ids,:,0]>=-33.63-1e-5)&(t[ids,:,0]<=33.63+1e-5)&(t[ids,:,2]>=79.61-1e-5)&(t[ids,:,2]<=97.87+1e-5)).all()
D['complete_south_short_crown_outward_panel']=ids.tolist();a[ids]=0

# Four existing front columns, selected from their 32 original cylindrical
# facets. No added geometry, caps, glazing, wall returns, or rear columns.
par=json.loads((R/'params.json').read_text());S=par['model_mm_per_drawing_m']
y=-par['column_y_m']*S;r=par['column_radius_m']*S
z0=(par['ground_floor_m']-.01)*S+par['base_mm'][2]-.03
z1=(par['body_top_m']+.03)*S+par['base_mm'][2]-.03
selected=np.zeros(len(t),bool);column_domains={};eps=2e-5
for cx in par['column_x_m']:
 center=np.array([cx*S,y]);xy=t[:,:,:2]-center
 bound=np.all(np.linalg.norm(xy,axis=2)<=r+eps,axis=1)&np.all((t[:,:,2]>=z0-eps)&(t[:,:,2]<=z1+eps),axis=1)
 mask=np.zeros(len(t),bool)
 for k in range(32):
  theta=(k+.5)*2*np.pi/32;normal=np.array([np.cos(theta),np.sin(theta)])
  mask|=bound&np.all(abs(xy@normal-r*np.cos(np.pi/32))<eps,axis=1)
 column_domains[str(cx)]=np.flatnonzero(mask).tolist();selected|=mask
assert [len(column_domains[str(x)]) for x in par['column_x_m']]==[84,80,80,84]
assert selected.sum()==328 and not np.any(selected&(a==0))
a[selected]=0;D['front_column_side_faces']=np.flatnonzero(selected).tolist()
D['front_columns_by_center_m']=column_domains

ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[507,38391]
pal=[('NSYSU south crown and front columns nominal gray brown substrate','#A58F82'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'38898 original triangles unchanged','limits':['Only 328 front-column side faces added to the original 179 south crown faces. Nominal same-family color on back-facing portions of the same columns is inferred. Crown recesses, caps, rear columns, other walls, glazing and roofs remain unchanged.', 'South is original drawing/entry-relative label, not surveyed world orientation.', 'Model bridge connector artificial closure not real facade; remain neutral.', 'Commons2024 original pixels GET403 stopped and not used; 2026 photo only original citation, not read or used as color evidence.', 'Preserve all original v2 geometry/source/printability limits and original previews; no globalQA recertification or current/asbuilt assertion.', 'One existing mainblock; no newbuilding/count increase; still partial.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':38898,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
