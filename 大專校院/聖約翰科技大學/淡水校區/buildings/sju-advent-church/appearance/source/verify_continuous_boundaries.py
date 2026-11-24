'''Read-only: six complete vertical jamb domains of three existing rear upper shell slots.'''
from pathlib import Path
import sys,json,hashlib,importlib.util,numpy as np
from shapely.geometry import Polygon,Point,mapping
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];R=A.parent;sys.path.insert(0,str(R/'appearance/source'));import geometry_io as gio
sp=importlib.util.spec_from_file_location('old',R/'appearance/source/build_appearance.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
v,f=gio.read_original(R/'model.stl');t=np.array(v)[f];p=t/4.55;p[:,:,2]=(t[:,:,2]-3)/4.55;stored=json.load(open(R/'appearance/face-materials.json'));labels=[old.classify(q)for q in t];palette=[q['id']for q in old.MATERIALS];c=np.array([palette.index(old.REGIONS[l]['material'])for l in labels])
cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);unit=cross/np.linalg.norm(cross,axis=1)[:,None];eps=2e-5
parent=list(range(len(t)));edges={}
def root(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
for i,tri in enumerate(t):
 for a,b in zip(tri,np.roll(tri,-1,axis=0)):
  key=tuple(sorted((tuple(a),tuple(b))))
  if key in edges:
   j=edges[key]
   if unit[i]@unit[j]>.99999 and max(abs((t[i]-t[j,0])@unit[j]))<.0001 and max(abs((t[j]-t[i,0])@unit[i]))<.0001:parent[root(i)]=root(j)
  else:edges[key]=i
groups={}
for i in range(len(t)):groups.setdefault(root(i),[]).append(i)
# Independently retain original piecewise roof curve and slot-back curve knots, not a centroid or infinite plane.
zs=sorted(set([10.65,12.45]+[4.4+.1*k for k in range(101)if 10.65<4.4+.1*k<12.45]+[10.65+.06*k for k in range(31)]))
outer=[(old.interp(z,4.4,.1,100),z)for z in zs];inner=[(old.interp(z,10.65,.06,30)-.25,z)for z in zs];expected=Polygon(outer+inner[::-1]);analytic=expected.area*4.55**2
records=[];ids=[]
for off in [-.9,0,.9]:
 for sign in [-1,1]:
  xx=off+sign*.2
  mask=(abs(p[:,:,0]-xx)<eps).all(1)&(p[:,:,2].min(1)>=10.65-eps)&(p[:,:,2].max(1)<=12.45+eps)&(p[:,:,1].min(1)>0)&(cross[:,0]*-sign>0);ix=np.flatnonzero(mask)
  assert len(ix)==49 and(c[ix]==0).all();assert groups[root(int(ix[0]))]==ix.tolist()
  polys=[Polygon(q[:,1:])for q in p[ix]];actual=unary_union(polys);diff=actual.symmetric_difference(expected).area*4.55**2;overlap=(sum(q.area for q in polys)-actual.area)*4.55**2;area=np.linalg.norm(cross[ix],axis=1).sum()/2
  assert all(expected.buffer(eps).covers(poly)for poly in polys);assert all(expected.buffer(eps).covers(Point(*q[1:]))for tri in p[ix]for q in tri);assert diff<.00002 and abs(overlap)<1e-9 and abs(area-analytic)<.00002
  assert set(labels[j]for j in ix)=={'unmatched_original_faces'}
  records.append(dict(slot_center_design_x=off,side_sign=sign,plane_design_x=xx,plane_mm_x=xx*4.55,outward_into_slot_normal_x=-sign,faces=ix.tolist(),entire_original_coplanar_edge_component=groups[root(int(ix[0]))],finite_polygon_design_yz=mapping(expected),analytic_area_mm2=analytic,mesh_area_mm2=float(area),symmetric_difference_mm2=diff,overlap_mm2=overlap,all_vertices_and_complete_triangles_in_domain=True));ids+=ix.tolist()
ids=sorted(ids);new=c.copy();new[ids]=2;assert len(ids)==294;assert np.array_equal(c[c!=0],new[c!=0]);bmix=[g for g in groups.values()if len(set(c[g]))>1];nmix=[g for g in groups.values()if len(set(new[g]))>1];assert bmix==nmix
assert new.tolist()==stored['material_indices'];assert np.bincount(new).tolist()==[1393,67,1598,67,97,16,720,14]
for i in range(len(t)):
 if i not in ids:assert labels[i]==stored['region_by_face'][i]
r=dict(new_face_ids=ids,groups=records,original_coplanar_mixed=bmix,new_coplanar_mixed=nmix,no_new_mixed_groups=True,complete_original_components=True,analytic_area_mm2=6*analytic,mesh_area_mm2=sum(g['mesh_area_mm2']for g in records),all_original_nonzero2285_faces_preserved=True,old720darkbacks_preserved=True,original_region_labels_unchanged_except294=True)
(A/'qa-continuous-rearjamb/material-boundaries.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS six complete49face strips; originalcolors andregionlabels retained')
