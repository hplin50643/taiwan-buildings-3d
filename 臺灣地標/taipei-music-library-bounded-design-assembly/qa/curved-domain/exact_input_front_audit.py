#!/usr/bin/env python3
import json,hashlib
from fractions import Fraction as F
from exact_domain_audit import HERE,SOURCE,canonical_plane,exact_num
from exact_boundary_envelope import polygon_subtract,polygon_planes,area2
E=json.loads((SOURCE/'expected-convex-primitives.json').read_text());A={o['id']:o for o in json.loads((SOURCE/'geometry.json').read_text())['objects']};results=[]
def remainder_area(source,targets):
 h,p=source;k=max(range(3),key=lambda i:abs(h[i]));axes=[i for i in range(3) if i!=k];remainder=[[(v[axes[0]],v[axes[1]]) for v in p]]
 for g,q in targets:
  if g!=h:continue
  proj=[(v[axes[0]],v[axes[1]]) for v in q];planes=polygon_planes(proj);new=[]
  for poly in remainder:
   bb=[min(v[i] for v in poly) for i in range(2)]+[max(v[i] for v in poly) for i in range(2)];cc=[min(v[i] for v in proj) for i in range(2)]+[max(v[i] for v in proj) for i in range(2)]
   if any(min(bb[i+2],cc[i+2])<=max(bb[i],cc[i]) for i in range(2)):new.append(poly);continue
   pieces,_=polygon_subtract(poly,planes,dim=2);new+=pieces
  remainder=new
  if not remainder:break
 return sum(F(area2(p),2) for p in remainder)
for name,prims in E.items():
 fronts=[p for p in prims if '_primitive_roof_' in p['id']];floats=[x for p in prims for v in p['vertices_mm'] for x in v]+[x for v in A[name]['vertices_mm'] for x in v];scale=2**max(F(float(x)).denominator.bit_length()-1 for x in floats)
 src=[]
 for p in fronts:
  vv=[tuple(int(F(float(x))*scale) for x in v) for v in p['vertices_mm']];tri=[vv[k] for k in p['triangles'][0]];src.append((canonical_plane(*tri),tri))
 vv=[tuple(int(F(float(x))*scale) for x in v) for v in A[name]['vertices_mm']];actual=[]
 for f in A[name]['triangles']:
  tri=[vv[k] for k in f];actual.append((canonical_plane(*tri),tri))
 missing=[remainder_area(s,actual) for s in src];planes={s[0] for s in src};coplanar=[t for t in actual if t[0] in planes];extra=[remainder_area(t,src) for t in coplanar]
 r={'id':name,'input_front_triangle_count':len(src),'actual_same_oriented_plane_triangle_count':len(coplanar),'each_input_front_triangle_missing_projected_area_mm2':[exact_num(x,scale**2) for x in missing],'actual_extra_on_input_front_planes_projected_area_mm2':exact_num(sum(extra),scale**2),'full_input_front_finite_domains_bidirectionally_exact':all(x==0 for x in missing+extra)};results.append(r);print(name,r['full_input_front_finite_domains_bidirectionally_exact'],flush=True)
(HERE/'EXACT-INPUT-FRONT-DOMAIN-QA.json').write_text(json.dumps({'scope':'Entire finite input skin front triangles (primitive triangle 0) minus union of exactly coplanar same-oriented actual triangles, and inverse difference for every actual triangle on those input front planes. Exact rational 2D clipping, no tolerance, no sampling. This refers to supplied retained hypothesis/reference input fronts, not new claims about original real architecture.','input_geometry_sha256':hashlib.sha256((SOURCE/'geometry.json').read_bytes()).hexdigest(),'input_primitives_sha256':hashlib.sha256((SOURCE/'expected-convex-primitives.json').read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
