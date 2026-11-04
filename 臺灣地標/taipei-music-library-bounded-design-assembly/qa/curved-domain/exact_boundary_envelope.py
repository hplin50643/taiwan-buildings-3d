#!/usr/bin/env python3
"""Full, bidirectional, exact-rational boundary coverage inside 1e-5mm axis envelope.
Expected union exterior patches are obtained from every primitive face, subtracting
other primitive interiors and resolving same-facing coplanar duplicates by ownership.
Actual and expected patches then cover each other through orthogonal projection.
"""
import json,itertools,math,time,hashlib
from fractions import Fraction as F
from exact_domain_audit import HERE,SOURCE,primitive,canonical_plane,signed,dot,cross,sub,add,mul,exact_num,subtract
TOL_MM=F(1,100000)
def area2(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))) if len(poly)>2 else 0

def clip_poly(poly,coef):
 if not poly:return []
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=sum(coef[k]*a[k] for k in range(len(a)))-coef[-1];db=sum(coef[k]*b[k] for k in range(len(b)))-coef[-1]
  if da<=0:out.append(a)
  if (da<0<db) or(db<0<da):out.append(add(a,mul(sub(b,a),F(da,da-db))))
 pp=[]
 for p in out:
  if not pp or p!=pp[-1]:pp.append(p)
 if len(pp)>1 and pp[0]==pp[-1]:pp.pop()
 return pp

def nonzero3(poly):return len(poly)>=3 and any(any(cross(sub(poly[i],poly[0]),sub(poly[i+1],poly[0]))) for i in range(1,len(poly)-1))
def polygon_subtract(poly,planes,dim=3):
 remain=poly;out=[]
 for h in planes:
  values=[sum(h[k]*p[k] for k in range(len(p)))-h[-1] for p in remain]
  if max(values)<=0:continue
  if min(values)>=0:
   out.append(remain);return out,[]
  plus=clip_poly(remain,tuple(-x for x in h))
  if (nonzero3(plus) if dim==3 else area2(plus)>0):out.append(plus)
  remain=clip_poly(remain,h)
  if not (nonzero3(remain) if dim==3 else area2(remain)>0):return out,[]
 return out,remain

def expected_boundary(prims):
 out=[]
 for i,P in enumerate(prims):
  for hi,face in P.faces:
   remains=[face]
   for j,C in enumerate(prims):
    if i==j:continue
    # If the face plane coincides with a same-facing outer plane of C, only
    # subtract duplicate ownership when C's input index precedes P's.
    same=any(h==hi for h,f in C.faces)
    if same and j>i:continue
    temp=[]
    for poly in remains:
     pieces,_=polygon_subtract(poly,[h for h,f in C.faces]);temp.extend(pieces)
    remains=temp
    if not remains:break
   for f in remains:out.append({'plane':hi,'poly':f,'owner':i})
 return out

def ccw(poly):
 signedarea=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))
 return poly if signedarea>=0 else list(reversed(poly))
def polygon_planes(poly):
 p=ccw(poly);out=[]
 for a,b in zip(p,p[1:]+p[:1]):
  dx,dy=b[0]-a[0],b[1]-a[1];out.append((dy,-dx,dy*a[0]-dx*a[1]))
 return out

def bounds(poly):return tuple(min(p[k] for p in poly) for k in range(3))+tuple(max(p[k] for p in poly) for k in range(3))
def height(h,p,axes,k):return F(h[3]-h[axes[0]]*p[0]-h[axes[1]]*p[1],h[k])
def point3(p,h,axes,k):
 out=[0,0,0];out[axes[0]],out[axes[1]]=p;out[k]=height(h,p,axes,k);return tuple(out)

def coverage(src,dst,scale,require_orientation):
 delta=TOL_MM*scale;dstbounds=[bounds(x['poly']) for x in dst];uncovered=[];maxaxis=F(0);maxnormal2=F(0);wedgepoints=[];coveredcount=0;sourceprojectedarea=F(0)
 for si,S in enumerate(src):
  h=S['plane'];k=max(range(3),key=lambda k:abs(h[k]));axes=[j for j in range(3) if j!=k];projection=[(p[axes[0]],p[axes[1]]) for p in S['poly']];remaining=[projection];bb=bounds(S['poly']);sourceprojectedarea+=F(area2(projection),2)
  for ti,D in enumerate(dst):
   g=D['plane'];dd=dstbounds[ti]
   if g[k]==0 or (require_orientation and dot(h[:3],g[:3])<=0):continue
   if any(min(bb[j+3],dd[j+3])+delta<max(bb[j],dd[j]) for j in range(3)):continue
   dproj=[(p[axes[0]],p[axes[1]]) for p in D['poly']]
   if not area2(dproj):continue
   # Actual source height minus target height, an exact affine form in projected coords.
   dx=F(-h[axes[0]],h[k])+F(g[axes[0]],g[k]);dy=F(-h[axes[1]],h[k])+F(g[axes[1]],g[k]);dc=F(h[3],h[k])-F(g[3],g[k])
   planes=polygon_planes(dproj)+[(dx,dy,delta-dc),(-dx,-dy,delta+dc)];nextrem=[]
   for p in remaining:
    pieces,inside=polygon_subtract(p,planes,dim=2);nextrem.extend(pieces)
    if inside:
     coveredcount+=1
     differences=[dx*x+dy*y+dc for x,y in inside];mx=max(abs(x) for x in differences);maxaxis=max(maxaxis,mx)
     # Plane distance of source point to destination plane = |heightdiff * g[k]|/|g.normal|.
     maxnormal2=max(maxnormal2,F(mx*mx*g[k]*g[k],dot(g[:3],g[:3])))
     if any(differences):
      for p in inside:wedgepoints.extend([point3(p,h,axes,k),point3(p,g,axes,k)])
   remaining=nextrem
   if not remaining:break
  for p in remaining:
   a=F(area2(p),2)
   if a:uncovered.append({'source_patch_index':si,'source_owner':S.get('owner'),'projected_area_mm2':float(a/scale**2),'bounds_mm':[float(x/scale) for x in bounds([point3(q,h,axes,k) for q in p])],'plane':list(h)})
 b=[float(x/scale) for x in bounds(wedgepoints)] if wedgepoints else None
 nr=math.sqrt(float(maxnormal2))/scale
 return {'source_patch_count':len(src),'destination_patch_count':len(dst),'require_matching_orientation':require_orientation,'axis_distance_limit_mm':float(TOL_MM),'all_positive_area_source_patches_covered':not uncovered,'uncovered_projected_area_mm2':sum(x['projected_area_mm2'] for x in uncovered),'uncovered_fragments':uncovered,'exact_max_assigned_axis_separation_mm':exact_num(maxaxis,scale),'maximum_assigned_support_plane_distance_mm_upper':math.nextafter(nr,math.inf),'covered_fragment_count':coveredcount,'conservative_nonzero_boundary_bridge_bbox_mm':b,'bbox_limitation':'Bounds all nonzero source-to-assigned-target boundary bridges; not asserted to be the exact symmetric-difference solid bbox.'}

def main():
 E=json.loads((SOURCE/'expected-convex-primitives.json').read_text());A={o['id']:o for o in json.loads((SOURCE/'geometry.json').read_text())['objects']};results=[]
 for name,pp in E.items():
  start=time.time();floats=[x for p in pp for v in p['vertices_mm'] for x in v]+[x for v in A[name]['vertices_mm'] for x in v];exp=max(F(float(x)).denominator.bit_length()-1 for x in floats);scale=2**exp;prims=[primitive(p,scale) for p in pp];expected=expected_boundary(prims);vv=[tuple(int(F(float(x))*scale) for x in v) for v in A[name]['vertices_mm']];actual=[{'plane':canonical_plane(*(vv[k] for k in f)),'poly':[vv[k] for k in f],'owner':i} for i,f in enumerate(A[name]['triangles'])]
  # Prove expected exterior patches integrate to the independently computed union volume.
  six=sum(dot(p['poly'][0],cross(p['poly'][i],p['poly'][i+1])) for p in expected for i in range(1,len(p['poly'])-1));boundary_volume=F(six,6*scale**3)
  cells=[]
  for pi,P in enumerate(prims):
   remains=[P]
   for C in prims[:pi]:remains=[piece for Q in remains for piece in subtract(Q,C)]
   cells.extend(remains)
  exact_union_volume=sum(P.volume() for P in cells)/scale**3
  assert boundary_volume==exact_union_volume, ('EXPECTED_BOUNDARY_EXTRACTION_MISMATCH',name,float(boundary_volume-exact_union_volume))
  result={'id':name,'expected_boundary_exactly_integrates_to_union_volume':True,'expected_exterior_patch_count':len(expected),'expected_boundary_signed_volume_mm3':exact_num(boundary_volume),'actual_to_expected_oriented':coverage(actual,expected,scale,True),'expected_to_actual_oriented':coverage(expected,actual,scale,True),'actual_to_expected_unoriented':coverage(actual,expected,scale,False),'elapsed_seconds':time.time()-start}
  results.append(result);(HERE/(name+'.boundary-envelope.json')).write_text(json.dumps(result,indent=2)+'\n');print(name,'patches',len(expected),'oriented',result['actual_to_expected_oriented']['all_positive_area_source_patches_covered'],result['expected_to_actual_oriented']['all_positive_area_source_patches_covered'],'unoriented',result['actual_to_expected_unoriented']['all_positive_area_source_patches_covered'],'seconds',time.time()-start,flush=True)
 (HERE/'BOUNDARY-ENVELOPE-ALL.json').write_text(json.dumps({'inputs':{n:hashlib.sha256((SOURCE/n).read_bytes()).hexdigest() for n in ['expected-convex-primitives.json','geometry.json']},'scope':'Exact rational polygon coverage for entire surfaces, no sampling. Projection displacement is along one coordinate axis, so its absolute magnitude is a rigorous Euclidean point-to-surface upper bound. Oriented and unoriented results separated. An embedding failure still blocks ordinary occupied-solid equivalence.','results':results},indent=2)+'\n')
if __name__=='__main__':main()
