from pathlib import Path
import json,struct,numpy as np
A=Path(__file__).resolve().parents[1];raw=(A.parent/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);c=np.array(json.loads((A/'face-materials.json').read_text())['face_material_indices']);eps=.00015
roof=t[c==1];glass=t[c==2];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);rn=normal[c==1]
assert len(roof)==24 and len(glass)==22
assert np.all(roof>=[-67-eps,-33-eps,71-eps]) and np.all(roof<=[-37+eps,-5+eps,74.2+eps])
front=np.all(abs(roof[:,:,2]-71-(roof[:,:,1]+33)*3.2/13.58)<eps,axis=1);left=np.all(abs(roof[:,:,2]-71-(roof[:,:,0]+67)*3.2/4.2)<eps,axis=1)
back=np.all(abs(roof[:,:,2]-71-(-5-roof[:,:,1])*3.2/13.58)<eps,axis=1);assert np.all(front|left|back) and np.all(rn[:,2]>0) and np.all(rn[front,1]<0) and np.all(rn[left,0]<0)
assert np.all(abs(glass[:,:,1]+25.5)<eps) and np.all(glass[:,:,0]>=-38.9-eps) and np.all(glass[:,:,0]<=-35.1+eps) and np.all(glass[:,:,2]>=23-eps) and np.all(glass[:,:,2]<=110+eps)
assert np.all(normal[c==2,1]<0)
for z in range(25,111,10):
 # Crossbars occupy full recess width; no selected triangle crosses their solid z interval.
 assert np.all((glass[:,:,2].max(axis=1)<=z+eps)|(glass[:,:,2].min(axis=1)>=z+1.1-eps))
assert (c==3).sum()==2
assert np.all(abs(t[c==3,:,0]+75)<1e-5)
r={'original_fascia_faces':2,'new_rear_slope_faces':int(back.sum()),'full_triangle_membership_only':True,'no_centroid_or_subdivision':True,'original_front_roof_faces':int(front.sum()),'original_left_roof_faces':int(left.sum()),'single_recess_back_wall_faces':len(glass),'crossbar_interiors_excluded':True,'outward_normals_verified':True,'neutral_faces':int((c==0).sum()),'colored_face_indices':{str(k):np.where(c==k)[0].tolist() for k in [1,2]}}
(A/'qa-continuous-lowhiprear/material-boundaries.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

# Check every newly touched original coplanar edge component is selected in full.
import build_appearance as old
bc,_=old.classify(t);ds=list(range(n));edges={};unit=normal/np.linalg.norm(normal,axis=1)[:,None]
def root(i):
 while ds[i]!=i:ds[i]=ds[ds[i]];i=ds[i]
 return i
for i,v in enumerate(t):
 for a,b in zip(v,np.roll(v,-1,axis=0)):
  e=tuple(sorted((tuple(a),tuple(b))))
  if e in edges:
   j=edges[e]
   if unit[i]@unit[j]>.99999 and max(abs((t[i]-t[j,0])@unit[j]))<.00015 and max(abs((t[j]-t[i,0])@unit[i]))<.00015:ds[root(i)]=root(j)
  else:edges[e]=i
groups={}
for i in range(n):groups.setdefault(root(i),[]).append(i)
changed=np.flatnonzero(c!=bc);touched=[g for g in groups.values()if set(g)&set(changed.tolist())];assert sorted(map(len,touched))==[4,4];assert sorted(sum(touched,[]))==changed.tolist()
bmixed=[g for g in groups.values()if len(set(bc[g]))>1];nmixed=[g for g in groups.values()if len(set(c[g]))>1];assert bmixed==nmixed
(A/'qa-continuous-lowhiprear/coplanar-components.json').write_text(json.dumps(dict(point_plane_tolerance_mm=.00015,normal_dot_minimum=.99999,whole_new_components=touched,original_mixed_components=bmixed,new_mixed_components=nmixed,no_new_mixed_components=True),indent=2)+'\n')
