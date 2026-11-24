"""Complete original1969 design underside whitecement domain only."""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='a67695b2eb747c0a90b62e3a8fe586db969250437e6194793a329e8a0edcb1f1';assert H(R/'model.stl')==expected
m=trimesh.load(R/'model.stl',force='mesh',process=True);assert len(m.faces)==12154
t=m.triangles;n=m.face_normals;e=.0001;a=np.full(len(t),1,np.int32);D={}
ids=np.flatnonzero(np.abs(t[:,:,2]-112.5).max(1)<1e-5);assert len(ids)==142
edges=m.face_adjacency;edges=edges[np.isin(edges[:,0],ids)&np.isin(edges[:,1],ids)]
pcs=trimesh.graph.connected_components(edges,nodes=ids,min_len=1);assert len(pcs)==1
angles=(np.arange(128)+.5)*2*np.pi/128;norms=np.column_stack([np.cos(angles),np.sin(angles)])
assert (t[ids,:,:2]@norms.T<=19.4*np.cos(np.pi/128)+1e-5).all()
D['complete_exposed_tank_bottom_underside']=ids.tolist();a[ids]=0
ad=m.face_adjacency;cop=(n[ad[:,0]]*n[ad[:,1]]).sum(1)>.999999;cs=trimesh.graph.connected_components(ad[cop],nodes=np.arange(len(t)),min_len=1);assert all(len(set(a[c]))==1 for c in cs);assert np.bincount(a).tolist()==[142,12012]
pal=[('NCU Water Tower 1969 Design documented underside white cement design family','#DFE0D4'),('UNVERIFIED main walls entrance windows roofs neutral','#B8BAB5')]
np.savez_compressed(R/'color-mesh.npz',vertices=m.vertices,faces=m.faces,materials=a);(R/'palette.json').write_text(json.dumps(pal,indent=2)+'\n');q={'palette':[{'id':i,'name':name,'hex':col,'faces':int((a==i).sum())}for i,(name,col)in enumerate(pal)],'domain_face_indices':D,'coplanar_components':len(cs),'partial_color_incomplete':True,'fully_colored_exterior':False,'geometry_policy':'12154 original triangles unchanged','limits':['All vertical tank skin/ribs/supports and B4 chord beams remain outside this bounded recommendation.', 'Pipe, ladder, cover, roof/rim, author base and hidden solid print core not assigned source white.', 'No new texture, line, geometry or mirrored material domain.', 'Historical1969design not as-built/current; exact present site/preservation unverified.', 'T1 clear inner diameter3.66m takes priority; T2 3.60m discrepancy retained without averaging.', '16radialribs22.5deg, slab/height chain/ring geometry unchanged.', 'Tank interior solid print core, closed25mm display lid, rectangularized ladder and .8mm printed return-pipe enlargement remain disclosed fabrication approximations.', 'Base not terrain/foundation; underground and unknown services excluded; no physical print test.', 'Sourcecolor recommendation does not rewrite or independently reapprove original QA.']};(R/'appearance-materials.json').write_text(json.dumps(q,indent=2)+'\n');(R/'COLOR-ASSIGNMENT-QA.json').write_text(json.dumps({'status':'PASS','original_STL_sha256':expected,'triangles':12154,'color_mesh_sha256':H(R/'color-mesh.npz')},indent=2));print(q['palette'],'components',len(cs))
