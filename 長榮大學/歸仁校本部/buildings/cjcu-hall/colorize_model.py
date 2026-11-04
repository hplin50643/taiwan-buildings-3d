"""Complete original main and lantern frustum upper skins only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='eda523c703513c0d20fdbfed8d0d8472183a6b89e1b9638ab610eebf4d88bebf';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==4734
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
for label,N,r0,r1,z0,z1,count in [('main',144,59.5,10.5,21,40.4,448),('lantern',96,13.4,1.4,49.6,51.6,192)]:
 wholeunion=set();finiteunion=set()
 for k in range(N):
  u=2*np.pi*k/N;v=2*np.pi*(k+1)/N
  p=np.array([[r0*np.cos(u)-12,r0*np.sin(u),z0],[r0*np.cos(v)-12,r0*np.sin(v),z0],[r1*np.cos(v)-12,r1*np.sin(v),z1],[r1*np.cos(u)-12,r1*np.sin(u),z1]])
  norm=np.cross(p[1]-p[0],p[2]-p[0]);norm/=np.linalg.norm(norm)
  dist=np.abs((t-p[0])@norm).max(1);whole=np.flatnonzero(dist<e);wholeunion.update(whole.tolist())
  inside=np.ones(len(t),bool)
  for j in range(4):
   edge=p[(j+1)%4]-p[j]
   side=np.cross(edge,t-p[j])@norm/np.linalg.norm(edge)
   inside&=side.min(1)>=-e
  finite=np.flatnonzero((dist<e)&inside);finiteunion.update(finite.tolist())
 assert wholeunion==finiteunion and len(finiteunion)==count
 D[label+'_complete_frustum_skin']=sorted(finiteunion);a[list(finiteunion)]=0
assert len(set(D['main_complete_frustum_skin'])&set(D['lantern_complete_frustum_skin']))==0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[640,4094]
pal=[('CJCU Hall observed conical roof skins metal gray','#A4ADB0'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'4734 original triangles unchanged','limits':['Vertical eave fascia, main roof underside, tiny lantern central flat apex disk and cap vertical rim remain neutral.', 'Lantern vertical ribs and glass/vent backing are mixed and not blanket gray/black.', 'Main24post glass drum is a solid-glass proxy with recessed openings, not transparent reconstructed interior; no broad blue/gray backing or invented bamboo trusses.', 'Low side service annex contains wall details and lettering; no all-white dome/side.', 'Steps, base, clock tower, neighboring canopy and landscaping excluded/uncolored.', 'All unlisted original triangles remain neutral.', 'Preserve4734 original faces and approximate conical geometry; no rib texture, new material boundaries or export files.', 'Use correct name長榮堂; not a separately invented chapel or bell tower model.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':4734,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
