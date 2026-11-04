#!/usr/bin/env python3
"""Exact whole-surface coverage by Minkowski sums of convex boundary patches and cubes.
Normal candidates for planar polygon + axis cube are polygon face normals, cube
face normals, and every polygon-edge x cube-edge direction. Their support planes
are the complete Minkowski normal-fan refinement; redundant candidates are safe.
"""
import json,math,time,hashlib,itertools
from fractions import Fraction as F
from exact_domain_audit import HERE,SOURCE,primitive,canonical_plane,dot,cross,sub,exact_num
from exact_boundary_envelope import expected_boundary,polygon_subtract as raw_subtract,nonzero3,bounds
OUT=HERE/'final-envelope'
OUT.mkdir(exist_ok=True)
def polygon_subtract(poly,planes,dim=3):
 for h in planes:
  values=[sum(h[k]*p[k] for k in range(len(p)))-h[-1] for p in poly]
  if min(values)>=0 and max(values)>0:return [poly],[]
 return raw_subtract(poly,planes,dim)
DELTA_MM=F(1,200000)
def normalize(v):
 if not any(v):return None
 den=1
 for x in v:den=math.lcm(den,F(x).denominator)
 iv=[int(x*den) for x in v];g=0
 for x in iv:g=math.gcd(g,abs(x))
 return tuple(x//g for x in iv)
def hull_planes(poly,h,delta):
 axes=[(1,0,0),(0,1,0),(0,0,1)];normals=set(axes+ [tuple(-x for x in n) for n in axes]);normals.add(tuple(h[:3]));normals.add(tuple(-x for x in h[:3]))
 for a,b in zip(poly,poly[1:]+poly[:1]):
  e=sub(b,a)
  for axis in axes:
   n=normalize(cross(e,axis))
   if n:normals.add(n);normals.add(tuple(-x for x in n))
 return [(*n,max(dot(n,p) for p in poly)+delta*sum(abs(x) for x in n)) for n in sorted(normals)]
def covered(src,dst,scale):
 delta=DELTA_MM*scale;targets=[{'patch':p,'bbox':bounds(p['poly']),'planes':hull_planes(p['poly'],p['plane'],delta),'planes0':hull_planes(p['poly'],p['plane'],0)} for p in dst]
 missing=[];changed=[];maxnormal2=F(0);maxcomponent2=F(0)
 for si,S in enumerate(src):
  remaining=[S['poly']];bb=bounds(S['poly']);h=S['plane'];sourcechanged=[];smax=F(0);destowners=set()
  # First remove the union of ALL exactly coincident finite target patches.
  # A nearby patch's dilation must not pre-empt an exact adjacent match.
  for T in targets:
   if T['patch']['plane']!=h:continue
   tb=T['bbox']
   if any(min(bb[k+3],tb[k+3])<max(bb[k],tb[k]) for k in range(3)):continue
   nextrem=[]
   for p in remaining:
    pieces,_=polygon_subtract(p,T['planes0']);nextrem.extend(pieces)
   remaining=nextrem
   if not remaining:break
  if not remaining:continue
  # Exact coplanar targets first prevents assigning unchanged interior patches to nearby tilted planes.
  candidates=sorted(range(len(targets)),key=lambda j:targets[j]['patch']['plane']!=h)
  for ti in candidates:
   T=targets[ti];g=T['patch']['plane'];tb=T['bbox']
   if dot(h[:3],g[:3])<=0:continue
   if any(min(bb[k+3],tb[k+3])+delta<max(bb[k],tb[k]) for k in range(3)):continue
   nextrem=[]
   for p in remaining:
    pieces,inside=polygon_subtract(p,T['planes']);nextrem.extend(pieces)
    if inside:
     is_exact=all(all(dot(q[:3],x)<=q[3] for q in T['planes0']) for x in inside)
     if not is_exact:
      sourcechanged.extend(inside);destowners.add(str(T['patch'].get('owner')))
      for x in inside:
       nn=F((dot(g[:3],x)-g[3])**2,dot(g[:3],g[:3]));smax=max(smax,nn);maxnormal2=max(maxnormal2,nn)
   remaining=nextrem
   if not remaining:break
  for p in remaining:
   if not nonzero3(p):continue
   axis=max(range(3),key=lambda k:abs(h[k]));inds=[k for k in range(3) if k!=axis];ar2=abs(sum(a[inds[0]]*b[inds[1]]-a[inds[1]]*b[inds[0]] for a,b in zip(p,p[1:]+p[:1])))
   missing.append({'source_patch':si,'owner':S.get('owner'),'primitive_id':S.get('primitive_id'),'face_indices':S.get('primitive_face_indices'),'projected_area_mm2':float(ar2/(2*scale**2)),'bbox_mm':[float(x/scale) for x in bounds(p)]})
  if sourcechanged:
   changed.append({'source_patch':si,'owner':S.get('owner'),'primitive_id':S.get('primitive_id'),'face_indices':S.get('primitive_face_indices'),'boundary_role':S.get('boundary_role'),'assigned_target_owners':sorted(destowners),'nonzero_envelope_source_bbox_mm':[float(x/scale) for x in bounds(sourcechanged)],'maximum_support_plane_distance_mm_upper':math.nextafter(math.sqrt(float(smax))/scale,math.inf)})
 bb=None
 if changed:
  bb=[min(c['nonzero_envelope_source_bbox_mm'][k] for c in changed) for k in range(3)]+[max(c['nonzero_envelope_source_bbox_mm'][k] for c in changed) for k in range(3,6)]
 return {'all_source_boundary_covered':not missing,'source_patches':len(src),'target_patches':len(dst),'Linf_point_to_surface_distance_bound_mm':float(DELTA_MM),'euclidean_point_to_surface_distance_bound_mm_upper':math.nextafter(math.sqrt(3)*float(DELTA_MM),math.inf),'uncovered_fragments':missing,'uncovered_projected_area_mm2':sum(x['projected_area_mm2'] for x in missing),'nonzero_boundary_envelope_bbox_mm':bb,'maximum_assigned_support_plane_distance_mm_upper':math.nextafter(math.sqrt(float(maxnormal2))/scale,math.inf),'changed_patch_ledger':changed}
def main():
 E=json.loads((SOURCE/'expected-convex-primitives.json').read_text());A={o['id']:o for o in json.loads((SOURCE/'geometry.json').read_text())['objects']};results=[]
 for name,pp in E.items():
  start=time.time();floats=[x for p in pp for v in p['vertices_mm'] for x in v]+[x for v in A[name]['vertices_mm'] for x in v];exp=max(F(float(x)).denominator.bit_length()-1 for x in floats);scale=2**exp;prims=[primitive(p,scale) for p in pp];expected=expected_boundary(prims)
  for patch in expected:
   original=pp[patch['owner']];vs=[tuple(int(F(float(x))*scale) for x in v) for v in original['vertices_mm']];patch['primitive_id']=original['id'];patch['primitive_face_indices']=[i for i,f in enumerate(original['triangles']) if canonical_plane(*(vs[k] for k in f))==patch['plane']]
  for patch in expected:
   if 'primitive_roof' not in patch['primitive_id']:patch['boundary_role']='artificial_support_or_cap'
   elif 0 in patch['primitive_face_indices']:patch['boundary_role']='retained_skin_input_front'
   elif 1 in patch['primitive_face_indices']:patch['boundary_role']='artificial_skin_backing_face'
   else:patch['boundary_role']='artificial_skin_extrusion_side'
  vv=[tuple(int(F(float(x))*scale) for x in v) for v in A[name]['vertices_mm']];actual=[{'plane':canonical_plane(*(vv[k] for k in f)),'poly':[vv[k] for k in f],'owner':i} for i,f in enumerate(A[name]['triangles'])]
  r={'id':name,'actual_to_expected':covered(actual,expected,scale),'expected_to_actual':covered(expected,actual,scale),'elapsed_seconds':time.time()-start};results.append(r);(OUT/(name+'.minkowski-envelope.json')).write_text(json.dumps(r,indent=2)+'\n');print(name,'cover',r['actual_to_expected']['all_source_boundary_covered'],r['expected_to_actual']['all_source_boundary_covered'],'seconds',time.time()-start,flush=True)
 (OUT/'MINKOWSKI-ENVELOPE-ALL.json').write_text(json.dumps({'status':'EXACT_POLYGON_COVERAGE_NO_SAMPLING','input_geometry_sha256':hashlib.sha256((SOURCE/'geometry.json').read_bytes()).hexdigest(),'input_primitives_sha256':hashlib.sha256((SOURCE/'expected-convex-primitives.json').read_bytes()).hexdigest(),'method':'Every entire source boundary patch is successively clipped against a complete halfspace representation of every target convex boundary patch plus an axis-aligned +/-0.000005mm cube. All rational inequalities exact. Full two-way coverage bounds surface Hausdorff distance; separate exact embedded-solid and signed volume audits remain required.','normal_fan_basis':'Minkowski facet normals arise from a polygon face, cube face, or polygon-edge/cube-edge pair. Enumerating both polygon normals, six cube normals, and all +/- cross products of polygon edges with cube axes gives a complete supporting halfspace representation.','bbox_scope':'Reported bboxes enclose nonzero matched boundary-envelope regions, not exact interior symmetric-difference cells.','results':results},indent=2)+'\n')
if __name__=='__main__':main()
