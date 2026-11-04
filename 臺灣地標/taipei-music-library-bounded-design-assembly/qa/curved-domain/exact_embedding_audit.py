#!/usr/bin/env python3
"""Exact triangle-pair embedding and edge/vertex-link audit of actual float32 meshes."""
import json,math,itertools,hashlib,time
from collections import defaultdict
from fractions import Fraction as F
from exact_domain_audit import HERE,SOURCE,sub,add,mul,dot,cross,det,canonical_plane,signed

def dedup(poly):
 out=[]
 for p in poly:
  if not out or p!=out[-1]:out.append(p)
 if len(out)>1 and out[0]==out[-1]:out.pop()
 return out

def slice_triangle(t,h):
 out=[];ss=[signed(h,p) for p in t]
 for i,(a,b) in enumerate(zip(t,t[1:]+t[:1])):
  da,db=ss[i],ss[(i+1)%3]
  if da==0:out.append(a)
  if (da<0<db) or (db<0<da):out.append(add(a,mul(sub(b,a),F(da,da-db))))
 return list(set(out))
def point_on_segment(p,a,b):
 return not any(cross(sub(p,a),sub(b,a))) and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in range(3))
def shared_allowed(points,shared):
 if not points:return True
 if len(shared)==0:return False
 if len(shared)==1:return all(p==shared[0] for p in points)
 if len(shared)==2:return all(point_on_segment(p,*shared) for p in points)
 return False

def coplanar_intersection(t,s,h):
 axis=max(range(3),key=lambda i:abs(h[i]));i,j=[k for k in range(3) if k!=axis]
 ori=(s[1][i]-s[0][i])*(s[2][j]-s[0][j])-(s[1][j]-s[0][j])*(s[2][i]-s[0][i]);ori=1 if ori>0 else -1
 p=list(t)
 for a,b in zip(s,s[1:]+s[:1]):
  if not p:break
  dx,dy=b[i]-a[i],b[j]-a[j]
  def value(x):return ori*(dx*(x[j]-a[j])-dy*(x[i]-a[i]))
  out=[]
  for P,Q in zip(p,p[1:]+p[:1]):
   f,g=value(P),value(Q)
   if f>=0:out.append(P)
   if (f<0<g) or (g<0<f):out.append(add(P,mul(sub(Q,P),F(f,f-g))))
  p=dedup(out)
 area2=abs(sum(P[i]*Q[j]-P[j]*Q[i] for P,Q in zip(p,p[1:]+p[:1]))) if len(p)>=3 else 0
 return p,area2

def pair_intersection(t,s,ht,hs):
 ds=[signed(ht,p) for p in s];dt=[signed(hs,p) for p in t]
 if min(ds)>0 or max(ds)<0 or min(dt)>0 or max(dt)<0:return None
 shared=list(set(t)&set(s));line=cross(ht[:3],hs[:3])
 if not any(line):
  if any(ds):return None
  pp,area2=coplanar_intersection(t,s,ht)
  if area2:return {'kind':'positive_coplanar_overlap','projected_twice_area_integer_units':str(area2),'shared_vertices':len(shared)}
  if not shared_allowed(pp,shared):return {'kind':'coplanar_noncombinatorial_contact','points':[[str(x) for x in p] for p in pp],'shared_vertices':len(shared)}
  return None
 a=slice_triangle(t,hs);b=slice_triangle(s,ht)
 if not a or not b:return None
 axis=max(range(3),key=lambda i:abs(line[i]));lo=max(min(p[axis] for p in a),min(p[axis] for p in b));hi=min(max(p[axis] for p in a),max(p[axis] for p in b))
 if lo>hi:return None
 aa=min(a,key=lambda p:p[axis]);ab=max(a,key=lambda p:p[axis])
 if aa[axis]==ab[axis]:points=[aa]
 else:points=[add(aa,mul(sub(ab,aa),F(x-aa[axis],ab[axis]-aa[axis]))) for x in set([lo,hi])]
 if not shared_allowed(points,shared):return {'kind':'noncoplanar_noncombinatorial_intersection','points':[[str(x) for x in p] for p in points],'shared_vertices':len(shared)}
 return None

def audit(obj):
 start=time.time();exp=max(F(float(x)).denominator.bit_length()-1 for v in obj['vertices_mm'] for x in v);scale=2**exp;v=[tuple(int(F(float(x))*scale) for x in a) for a in obj['vertices_mm']];f=obj['triangles'];tris=[[v[k] for k in face] for face in f];planes=[canonical_plane(*t) for t in tris];bounds=[tuple(min(p[k] for p in t) for k in range(3))+tuple(max(p[k] for p in t) for k in range(3)) for t in tris]
 bad=[];candidates=0
 for i,j in itertools.combinations(range(len(f)),2):
  a,b=bounds[i],bounds[j]
  if any(min(a[k+3],b[k+3])<max(a[k],b[k]) for k in range(3)):continue
  candidates+=1;x=pair_intersection(tris[i],tris[j],planes[i],planes[j])
  if x:x['triangles']=[i,j];bad.append(x)
 edges=defaultdict(list);links=[[] for _ in v];adj=[set() for _ in v]
 for ti,(a,b,c) in enumerate(f):
  for x,y in [(a,b),(b,c),(c,a)]:edges[tuple(sorted((x,y)))].append((ti,1 if x<y else -1));adj[x].add(y);adj[y].add(x)
  links[a].append((b,c));links[b].append((c,a));links[c].append((a,b))
 edgefail=[list(e) for e,h in edges.items() if len(h)!=2 or sum(x[1] for x in h)!=0];linkfail=[]
 for vi,lnk in enumerate(links):
  g=defaultdict(list)
  for a,b in lnk:g[a].append(b);g[b].append(a)
  seen=set();todo=[next(iter(g))] if g else []
  while todo:
   x=todo.pop()
   if x in seen:continue
   seen.add(x);todo+=g[x]
  if len(seen)!=len(g) or any(len(a)!=2 for a in g.values()):linkfail.append(vi)
 remaining=set(range(len(v)));components=[]
 while remaining:
  todo=[remaining.pop()];n=0
  while todo:
   a=todo.pop();n+=1
   for b in adj[a]:
    if b in remaining:remaining.remove(b);todo.append(b)
  components.append(n)
 vol=sum(det(*t) for t in tris);result={'id':obj['id'],'method':'All triangle-pair candidates after exact inclusive AABB exclusion tested with exact rational coplanar clipping or exact plane-line intersections. Only the corresponding shared indexed vertex/edge is allowed. No tolerance or sampling.','triangle_pairs_total':len(f)*(len(f)-1)//2,'triangle_pairs_requiring_exact_intersection':candidates,'noncombinatorial_intersections':bad,'edge_or_orientation_failures':edgefail,'vertex_link_cycle_failures':linkfail,'surface_components':len(components),'signed_volume_positive':vol>0,'embedded_closed_oriented_single_surface_pass':not(bad or edgefail or linkfail) and len(components)==1 and vol>0,'elapsed_seconds':time.time()-start};return result

def main():
 objects=json.loads((SOURCE/'geometry.json').read_text())['objects'];results=[]
 for o in objects:
  r=audit(o);results.append(r);print(r['id'],'pass',r['embedded_closed_oriented_single_surface_pass'],'intersections',len(r['noncombinatorial_intersections']),'seconds',r['elapsed_seconds'],flush=True)
 (HERE/'EXACT-EMBEDDING-QA.json').write_text(json.dumps({'geometry_sha256':hashlib.sha256((SOURCE/'geometry.json').read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
if __name__=='__main__':main()
