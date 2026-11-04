from pathlib import Path
import json,struct,numpy as np
P=Path(__file__).resolve().parent;O=P/'reference-nominal'
def read(p):
 b=p.read_bytes();return np.array([struct.unpack_from('<12fH',b,84+50*i)[3:12]for i in range(struct.unpack_from('<I',b,80)[0])]).reshape(-1,3,3)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def area(p):return abs(sum(cross(a,b)for a,b in zip(p,np.roll(p,-1,axis=0))))/2 if len(p)>2 else 0

def intersect(poly,clip):
 if sum(cross(a,b)for a,b in zip(clip,np.roll(clip,-1,axis=0)))<0:clip=clip[::-1]
 out=list(poly)
 for a,b in zip(clip,np.roll(clip,-1,axis=0)):
  inp=out;out=[]
  if not inp:break
  for u,v in zip(inp,inp[1:]+inp[:1]):
   du=cross(b-a,u-a);dv=cross(b-a,v-a)
   if du>=-1e-10:out.append(u)
   if (du>=-1e-10)!=(dv>=-1e-10):out.append(u+(v-u)*du/(du-dv))
 return out
rows=[]
for name in ['SOURCE_NORMALIZED_A_END','SOURCE_NORMALIZED_F_GABLE','SOURCE_NORMALIZED_ROOF_left','SOURCE_NORMALIZED_ROOF_right']:
 old=read(O/'parts'/(name+'.stl'));new=read(P/'parts'/(name+'.stl'))
 if 'ROOF'in name:n=np.array([1 if name.endswith('left')else-1,0,-1])/np.sqrt(2);c=76.2/np.sqrt(2);axis=[0,1];factor=np.sqrt(2)
 else:n=np.array([0,1,0]);c=1.5147540983606558 if'A_END'in name else-174.91685393258427;axis=[0,2];factor=1
 a=old[np.max(np.abs(old@n+c),axis=1)<1e-5][:,:,axis];b=new[np.max(np.abs(new@n+c),axis=1)<1e-5][:,:,axis]
 aa=sum(area(x)for x in a)*factor;bb=sum(area(x)for x in b)*factor;common=sum(area(intersect(x,y))for x in a for y in b)*factor
 rows.append({'id':name,'old_front_triangles':len(a),'new_front_triangles':len(b),'old_area_mm2':aa,'new_area_mm2':bb,'overlap_area_mm2':common,'symmetric_difference_area_mm2':max(0,aa+bb-2*common),'old_minus_new_area_mm2':max(0,aa-common),'new_minus_old_area_mm2':max(0,bb-common)})
print(json.dumps(rows,indent=2));(P/'SOURCE-FRONT-SYMMETRIC-DIFFERENCE.json').write_text(json.dumps({'method':'all-pair convex triangle intersection in source plane; includes hole and outer boundaries rather than area equality only','results':rows,'not_yet_independent_review':True},indent=2)+'\n')
# Boundary verification: merge collinear adjacent boundary fragments before endpoint bounds.
from collections import Counter

def boundary(tri):
 vv,ii=np.unique(tri.reshape(-1,2),axis=0,return_inverse=True);es=Counter(tuple(sorted((int(a),int(b))))for f in ii.reshape(-1,3)for a,b in zip(f,np.roll(f,-1)))
 segs=[[vv[a],vv[b]]for(a,b),n in es.items()if n==1]
 return segs
 changed=True
 while changed:
  changed=False
  for i in range(len(segs)):
   a,b=segs[i];d=b-a;L=np.linalg.norm(d)
   if L<1e-12:continue
   d=d/L
   for j in range(i+1,len(segs)):
    c,e=segs[j]
    if max(abs(cross(d,c-a)),abs(cross(d,e-a)))>2e-5:continue
    ts=sorted([float((c-a)@d),float((e-a)@d)])
    if ts[0]>L+2e-5 or ts[1]< -2e-5:continue
    segs[i]=[a+d*min(0,ts[0]),a+d*max(L,ts[1])];segs.pop(j);changed=True;break
   if changed:break
 return segs

def distpoint(p,a,b):
 d=b-a;t=np.clip((p-a)@d/(d@d),0,1);return float(np.linalg.norm(p-a-t*d))
def bound(sa,sb):
 result=0
 for a,b in sa:
  v=b-a;ll=v@v;ts=sorted(set([0.,1.]+[float(np.clip((q-a)@v/ll,0,1))for pair in sb for q in pair]))
  for t,u in zip(ts,ts[1:]):
   x=a+t*v;y=a+u*v
   result=max(result,min(max(distpoint(x,c,d),distpoint(y,c,d))for c,d in sb))
 return result
bs=[]
for rr in rows:
 name=rr['id'];old=read(O/'parts'/(name+'.stl'));new=read(P/'parts'/(name+'.stl'))
 if'ROOF'in name:n=np.array([1 if name.endswith('left')else-1,0,-1])/np.sqrt(2);c=76.2/np.sqrt(2);axis=[0,1];factor=np.sqrt(2)
 else:n=np.array([0,1,0]);c=1.5147540983606558 if'A_END'in name else-174.91685393258427;axis=[0,2];factor=1
 a=boundary(old[np.max(np.abs(old@n+c),axis=1)<1e-5][:,:,axis]);b=boundary(new[np.max(np.abs(new@n+c),axis=1)<1e-5][:,:,axis]);bs.append({'id':name,'old_raw_boundary_segments':len(a),'new_raw_boundary_segments':len(b),'bidirectional_full_segment_distance_upper_bound_mm':max(bound(a,b),bound(b,a))*factor})
(P/'SOURCE-BOUNDARY-DISTANCE.json').write_text(json.dumps({'method':'Unmerged raw boundary edges subdivided at opposite endpoint projections; per-subsegment endpoint distances to one opposite straight segment bound its convex distance. Both directions; outer plus holes.','results':bs},indent=2)+'\n');print(bs)
