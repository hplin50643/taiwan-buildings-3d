import json, pathlib, hashlib, itertools, time, struct
from fractions import Fraction as F
from collections import Counter
import numpy as np
import sys
R=pathlib.Path(__file__).resolve().parent
O=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else R/'qa-recheck'
O.mkdir(parents=True,exist_ok=True)
p=R/'inputs/physical-meshes.json';hashes={'inputs/physical-meshes.json':hashlib.sha256(p.read_bytes()).hexdigest()}
objects={o['id']:o for o in json.loads(p.read_text())['objects']}
order=['ARTIFICIAL_SHARED_BASE','CENTRAL','A','B','C8_NOMINAL_PLATFORM','L5_NOMINAL_PLATFORM','A_NOMINAL_ROOF_SUPPORT_0','A_NOMINAL_ROOF_SUPPORT_1','B_FINITE_UPPER_CANDIDATE_PROXY','SOUTH_UPPER_BAND_NOMINAL_REFERENCE_PLANE']
D={};mesh_validation={};stl_validation={}
for name in order:
 d=objects[name]; v=np.array(d.get('vertices_mm',d.get('vertices')),dtype=float); f=np.array(d['triangles']); ts=v[f];n=np.cross(ts[:,1]-ts[:,0],ts[:,2]-ts[:,0]); edges=Counter(); directions=Counter()
 for face in f:
  for a,b in zip(face,np.roll(face,-1)):
   edges[tuple(sorted((int(a),int(b))))]+=1;directions[(int(a),int(b))]+=1
 # Exact dyadic integer normal classification. All stored numbers are finite binary floats.
 ratios=[[float(x).as_integer_ratio() for x in p] for p in v]; den=max(q for p in ratios for a,q in p); iv=[[a*(den//q) for a,q in p] for p in ratios]
 exact_n=[]
 for face in f:
  a,b,c=[iv[int(i)] for i in face];u=[b[k]-a[k] for k in range(3)];w=[c[k]-a[k] for k in range(3)]; exact_n.append([u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]])
 signs=np.array([(x[2]>0)-(x[2]<0) for x in exact_n]); assert np.array_equal(signs,np.sign(n[:,2])); assert all(any(a!=0 for a in x) for x in exact_n)
 sp=R/'parts'/f'{name}.stl'; raw=sp.read_bytes();count=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*count
 st=np.array([struct.unpack_from('<12fH',raw,84+i*50)[3:12] for i in range(count)]).reshape(-1,3,3)
 # Compare oriented triangle multisets modulo cyclic vertex shifts; do not allow reversal.
 def canonical(t):
  pts=tuple(tuple(float(x) for x in p) for p in t);return min(pts,pts[1:]+pts[:1],pts[2:]+pts[:2])
 match=Counter(map(canonical,st))==Counter(map(canonical,ts));assert match
 stl_validation[name]={'path':str(sp.relative_to(R)),'sha256':hashlib.sha256(raw).hexdigest(),'triangles':count,'oriented_triangle_multiset_exactly_matches_json':match,'exact_integer_normal_signs_match':True};hashes[str(sp.relative_to(R))]=hashlib.sha256(raw).hexdigest()
 vol=np.einsum('ij,ij->i',ts[:,0],np.cross(ts[:,1],ts[:,2])).sum()/6
 mesh_validation[name]={'vertices':len(v),'triangles':len(f),'closed_edge_manifold':all(x==2 for x in edges.values()),'consistent_orientation':all(directions[(b,a)]==c for (a,b),c in directions.items()),'nondegenerate_triangles':bool(np.all(np.any(n!=0,axis=1))),'signed_volume_mm3':float(vol),'assembly_matrix':d.get('assembly_matrix','identity declared in orthogonal JSON')}
 D[name]={}
 for label,mask in [('up',signs>0),('down',signs<0)]:
  t=ts[mask];D[name][label]=(t,t.min(axis=1),t.max(axis=1),np.where(mask)[0])

def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return [a[i]-b[i] for i in range(len(a))]
def clip(poly,P,Q):
 out=[]; edge=sub(Q,P)
 for a,b in zip(poly,poly[1:]+poly[:1]):
  fa=cross(edge,sub(a,P));fb=cross(edge,sub(b,P))
  if fa>=0:out.append(a)
  if (fa<0<fb) or (fb<0<fa):out.append([a[i]+(b[i]-a[i])*fa/(fa-fb) for i in range(2)])
 return out

def plane(t):
 a,b,c=t; u=sub(b,a);w=sub(c,a);nz=cross(u,w);nx=u[1]*w[2]-u[2]*w[1];ny=u[2]*w[0]-u[0]*w[2]
 return [-nx/nz,-ny/nz,a[2]+nx/nz*a[0]+ny/nz*a[1]]
cache={}
def exact_triangle(name,label,i):
 key=(name,label,i)
 if key not in cache:
  t=[[F(float(x)) for x in p] for p in D[name][label][0][i]]; poly=[p[:2] for p in t]
  if cross(sub(poly[1],poly[0]),sub(poly[2],poly[0]))<0:poly.reverse()
  cache[key]=(poly,plane(t))
 return cache[key]
results=[];allhits=[]
for later in range(1,len(order)):
 moving=order[later];mt,ml,mh,mi=D[moving]['down']
 for fixed in order[:later]:
  ft,fl,fh,fi=D[fixed]['up']; candidates=0; positive_xy=0; xy_envelopes=0; min_gap=None; hits=[];start=time.time()
  for i in range(len(mt)):
   maskxy=(fl[:,0]<mh[i,0])&(fh[:,0]>ml[i,0])&(fl[:,1]<mh[i,1])&(fh[:,1]>ml[i,1]);xy_envelopes+=int(maskxy.sum())
   if maskxy.any():
    gap=float((ml[i,2]-fh[maskxy,2]).min());min_gap=gap if min_gap is None else min(min_gap,gap)
   mask=maskxy&(fh[:,2]>ml[i,2])
   for j in np.where(mask)[0]:
    candidates+=1;mp,mz=exact_triangle(moving,'down',i);fp,fz=exact_triangle(fixed,'up',int(j));poly=mp[:]
    for P,Q in zip(fp,fp[1:]+fp[:1]):
     poly=clip(poly,P,Q)
     if not poly:break
    if len(poly)<3:continue
    area=sum(cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))/2
    if area<=0:continue
    positive_xy+=1
    vals=[sum((mz[k]-fz[k])*p[k] for k in range(2))+mz[2]-fz[2] for p in poly]
    if min(vals)<0:
     h={'moving_face':int(mi[i]),'fixed_face':int(fi[j]),'xy_intersection_area_mm2':float(area),'min_bottom_minus_top_mm':float(min(vals)),'max_bottom_minus_top_mm':float(max(vals))}
     hits.append(h)
  r={'moving':moving,'fixed':fixed,'total_oriented_triangle_pairs':len(mt)*len(ft),'xy_envelope_overlapping_pairs':xy_envelopes,'minimum_triangle_envelope_vertical_gap_mm':min_gap,'aabb_candidates':candidates,'positive_xy_pairs':positive_xy,'obstructing_surface_pairs':len(hits),'hits':hits,'elapsed_seconds':time.time()-start};results.append(r);allhits.extend([dict(moving=moving,fixed=fixed,**h) for h in hits]);print(moving,fixed,'candidates',candidates,'HITS',len(hits),flush=True)
  (O/'ACTUAL-MESH-CONTINUOUS-SWEEP-PROGRESS.json').write_text(json.dumps({'mesh_validation':mesh_validation,'results':results,'hashes':hashes},indent=2))
report={'scope':'All 45 ordered actual serialized mesh solid pairs including base; continuous common-axis vertical downward insertion from arbitrary positive height to assembly identity. Exact dyadic-integer triangle orientation; exhaustive per-triangle projected-envelope and one-sided height separation, with exact rational XY clipping and affine height comparisons for any surviving candidates. Here all candidates are excluded by exact coordinate inequalities, so no rational clipping is needed. This is not a whole-object bounding-box test. No positional sampling or positive penetration tolerance. Interior-volume collisions only; boundary contact is allowed. Conditional on embedded closed consistently outward-oriented solids; self-intersection and material strength require separate validation.','method':'An upward-facing stationary boundary triangle has solid locally below it. A downward-facing moving boundary triangle has solid locally above it. A common XY open region with moving bottom lower than stationary top exists iff the moving solid interior intersects the stationary solid interior for some nonnegative upward translation. Exact rational projected triangle intersections and affine minima over their vertices establish this over the entire translation ray. Removing parts in reverse order follows the same ray. No qualifying triangle pair implies final static interior disjointness too.','assembly_order':order,'mesh_validation':mesh_validation,'hashes':hashes,'stl_validation':stl_validation,'pair_count':len(results),'results':results,'obstructing_surface_pair_count':len(allhits),'verdict':'PASS_NO_POSITIVE_VOLUME_INTERFERENCE' if not allhits else 'FAIL_ORIENTATION_ASSUMPTIONS_OR_INTERFERENCE_REQUIRES_REVIEW','limits':['No physical printing, material stiffness, fit, or installed load approval.','Touching surfaces, zero clearances, and nominal fit tolerances are not positive-volume collisions.','Any modified mesh, including C8 reduction, needs re-bound input hashes and rerun.','No claim of formal proof against self-intersecting or inconsistently embedded surfaces; edge checks alone do not establish embedding.']}
(O/'ACTUAL-MESH-CONTINUOUS-SWEEP-REPORT.json').write_text(json.dumps(report,indent=2));print('DONE',len(allhits),flush=True)
