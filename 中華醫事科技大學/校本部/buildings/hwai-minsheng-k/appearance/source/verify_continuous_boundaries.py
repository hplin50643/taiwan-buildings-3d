'''Read-only complete original grey upper-front band vertical end returns; no model edits.'''
from pathlib import Path
import numpy as np,json,hashlib,struct,importlib.util
A=Path(__file__).resolve().parents[1];R=A.parent;raw=(R/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i)for i in range(n)]).reshape(-1,3,3)
s=importlib.util.spec_from_file_location('old',R/'appearance/source/build_appearance.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old);c,why=old.classify(t);stored=json.load(open(R/'appearance/face-materials.json'));assert hashlib.sha256(raw).hexdigest()==old.SOURCE_SHA
normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);unit=normal/np.linalg.norm(normal,axis=1)[:,None];eps=.00015
# Group original adjacent coplanar faces using symmetric point-to-plane tests, robust to float32.
par=list(range(n));edges={}
def root(i):
 while par[i]!=i:par[i]=par[par[i]];i=par[i]
 return i
for i,v in enumerate(t):
 for a,b in zip(v,np.roll(v,-1,axis=0)):
  e=tuple(sorted((tuple(a),tuple(b))))
  if e in edges:
   j=edges[e]
   if unit[i]@unit[j]>.99999 and max(abs((t[i]-t[j,0])@unit[j]))<eps and max(abs((t[j]-t[i,0])@unit[i]))<eps:par[root(i)]=root(j)
  else:edges[e]=i
grouped={}
for i in range(n):grouped.setdefault(root(i),[]).append(i)
records=[];ids=[]
for x in [-40,26]:
 for z in [49.2,59.2,69.2,79.2,89.2,99.2,109.2]:
  lo=np.array([x,-21.3,z]);hi=np.array([x,-19,z+2.1]);sgn=-1 if x<0 else 1
  mask=(abs(t[:,:,0]-x)<eps).all(1)&(normal[:,0]*sgn>0)&(t>=lo-eps).all((1,2))&(t<=hi+eps).all((1,2));ix=np.flatnonzero(mask);assert len(ix)==2 and not c[ix].any();assert grouped[root(int(ix[0]))]==ix.tolist()
  uv=np.unique(t[ix].reshape(-1,3),axis=0)[:,1:];expected=np.array([[-21.3,z],[-21.3,z+2.1],[-19,z],[-19,z+2.1]]);assert len(uv)==4 and np.max(abs(np.array(sorted(uv.tolist()))-np.array(sorted(expected.tolist()))))<eps
  area=np.linalg.norm(normal[ix],axis=1).sum()/2;assert abs(area-4.83)<.00003
  # Existing front of same band is already grey and shares one vertical edge with return.
  front=(abs(t[:,:,1]+21.3)<eps).all(1)&(t[:,:,0].min(1)>=-40-eps)&(t[:,:,0].max(1)<=26+eps)&(t[:,:,2].min(1)>=z-eps)&(t[:,:,2].max(1)<=z+2.1+eps)&(normal[:,1]<0)
  oldids=np.flatnonzero(front);assert len(oldids)==2 and(c[oldids]==2).all()
  shared=set(map(tuple,t[ix].reshape(-1,3)))&set(map(tuple,t[oldids].reshape(-1,3)));assert len(shared)==2
  records.append(dict(axis=0,plane=x,normal_sign=sgn,low_mm=lo.tolist(),high_mm=hi.tolist(),faces=ix.tolist(),adjacent_original_grey_front_faces=oldids.tolist(),shared_front_edge_points=sorted(map(list,shared)),complete_coplanar_component=grouped[root(int(ix[0]))],finite_rectangle_area_mm2=4.83,mesh_area_mm2=float(area),all_three_vertices_and_full_rectangle=True));ids+=ix.tolist()
ids=sorted(ids);assert len(ids)==28;new=c.copy();new[ids]=2;assert np.array_equal(c[c!=0],new[c!=0]);assert np.bincount(c).tolist()==[2882,108,14];assert np.bincount(new).tolist()==[2854,108,42]
bmix=[g for g in grouped.values()if len(set(c[g]))>1];nmix=[g for g in grouped.values()if len(set(new[g]))>1];assert bmix==nmix
assert new.tolist()==stored['face_material_indices']
for i in range(n):
 if i not in ids:assert why[i]==stored['face_reasons'][i]
assert len(bmix)==len(nmix)==36
q=dict(new_face_ids=ids,full_rectangle_groups=records,all_original122_materials_and_reasons_preserved=True,baseline_mixed_coplanar_groups=bmix,new_mixed_coplanar_groups=nmix,all36baseline_mixed_components_identical=True,no_new_mixed_coplanar_component=True,only_vertical_returns=True,top_and_soffit_unchanged=True,point_plane_tolerance_mm=.00015,normal_dot_minimum=.99999)
(A/'qa-continuous-bandreturns/material-boundaries.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('PASS 14 complete rectangles; 36 unchanged baseline mixed components')
