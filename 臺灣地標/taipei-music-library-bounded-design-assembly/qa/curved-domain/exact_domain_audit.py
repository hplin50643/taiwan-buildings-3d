#!/usr/bin/env python3
"""Exact rational polyhedral occupied-domain audit. No random or grid sampling.
Uses stdlib only. Float32 coordinates are lifted exactly onto an integer lattice.
Expected convex union is partitioned by exact halfspaces into disjoint convex cells.
Actual closed oriented mesh is integrated by signed tetrahedra against every cell.
"""
from fractions import Fraction as F
from functools import cmp_to_key
from collections import defaultdict,Counter
import itertools,math,json,pathlib,hashlib,struct,time,argparse,decimal
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'curved-build/output-v7'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b,c):return dot(a,cross(b,c))
def canonical_plane(a,b,c,inside=None):
 n=cross(sub(b,a),sub(c,a));d=dot(n,a)
 if not any(n):return None
 if inside is not None and dot(n,inside)>d:n=mul(n,-1);d=-d
 vals=(*n,d);lcm=1
 for x in vals:lcm=math.lcm(lcm,F(x).denominator)
 vals=tuple(int(x*lcm) for x in vals);g=0
 for x in vals:g=math.gcd(g,abs(x))
 return tuple(x//g for x in vals)
def signed(h,v):return dot(h[:3],v)-h[3]
def clean(poly):
 p=[]
 for x in poly:
  if not p or x!=p[-1]:p.append(x)
 if len(p)>1 and p[0]==p[-1]:p.pop()
 if len(p)<3:return []
 change=True
 while change and len(p)>=3:
  change=False
  for i in range(len(p)):
   if not any(cross(sub(p[i],p[i-1]),sub(p[(i+1)%len(p)],p[i]))):p.pop(i);change=True;break
 return p if len(p)>=3 else []
def ring(points,h):
 pts=list(set(points));axis=max(range(3),key=lambda i:abs(h[i]));axes=[k for k in range(3) if k!=axis];center=tuple(sum(p[k] for p in pts)/F(len(pts)) for k in axes)
 def rel(p):return (p[axes[0]]-center[0],p[axes[1]]-center[1])
 def half(v):return 0 if (v[1]>0 or (v[1]==0 and v[0]>=0)) else 1
 def cmp(a,b):
  x,y=rel(a),rel(b);ha,hb=half(x),half(y)
  if ha!=hb:return -1 if ha<hb else 1
  c=x[0]*y[1]-x[1]*y[0]
  if c:return -1 if c>0 else 1
  return (dot(x,x)>dot(y,y))-(dot(x,x)<dot(y,y))
 pts.sort(key=cmp_to_key(cmp));pts=clean(pts)
 if pts and dot(cross(sub(pts[1],pts[0]),sub(pts[2],pts[0])),h[:3])<0:pts.reverse()
 return pts
class Poly:
 __slots__=('faces','points','bounds','vol')
 def __init__(self,faces):
  self.faces=faces;self.points=tuple(set(p for h,f in faces for p in f));self.bounds=tuple(min(p[k] for p in self.points) for k in range(3))+tuple(max(p[k] for p in self.points) for k in range(3));self.vol=None
 def volume(self):
  if self.vol is None:
   total=0
   for h,f in self.faces:
    for i in range(1,len(f)-1):total+=det(f[0],f[i],f[i+1])
   self.vol=F(total,6)
  return self.vol

def clip(P,h):
 ds={p:signed(h,p) for p in P.points};lo=min(ds.values());hi=max(ds.values())
 if hi<=0:return P
 if lo>=0:return None
 faces=[];cutpoints=[]
 for oldh,f in P.faces:
  out=[]
  for a,b in zip(f,f[1:]+f[:1]):
   da,db=ds[a],ds[b]
   if da<=0:out.append(a)
   if da==0:cutpoints.append(a)
   if (da<0<db) or(db<0<da):
    t=F(da,da-db);x=add(a,mul(sub(b,a),t));out.append(x);cutpoints.append(x)
  out=clean(out)
  if out:faces.append((oldh,out))
 cap=ring(cutpoints,h)
 if cap:faces.append((h,cap))
 if len(faces)<4:return None
 return Poly(faces)
def disjoint(a,b):return any(min(a.bounds[k+3],b.bounds[k+3])<=max(a.bounds[k],b.bounds[k]) for k in range(3))
def subtract(P,C):
 if disjoint(P,C):return [P]
 inside=P;outside=[]
 for h,f in C.faces:
  other=clip(inside,tuple(-x for x in h))
  if other is not None:outside.append(other)
  inside=clip(inside,h)
  if inside is None:break
 return outside

def intersection(P,C):
 if disjoint(P,C):return None
 for h,f in C.faces:
  P=clip(P,h)
  if P is None:return None
 return P

def primitive(p,scale):
 vv=[tuple(int(F(float(x))*scale) for x in v) for v in p['vertices_mm']];groups=defaultdict(set)
 for f in p['triangles']:
  h=canonical_plane(*(vv[k] for k in f))
  assert h is not None
  assert max(signed(h,v) for v in vv)<=0,('NONCONVEX',p['id'],h)
  groups[h].update(vv[k] for k in f)
 faces=[(h,ring(list(v),h)) for h,v in groups.items()];P=Poly(faces);assert P.volume()>0,p['id'];return P

def tetra(vertices):
 center=mul(tuple(sum(v[k] for v in vertices) for k in range(3)),F(1,4));faces=[]
 for inds in [(0,1,2),(0,3,1),(0,2,3),(1,3,2)]:
  pts=[vertices[k] for k in inds];h=canonical_plane(*pts,inside=center)
  if h is None:return None
  if dot(cross(sub(pts[1],pts[0]),sub(pts[2],pts[0])),h[:3])<0:pts.reverse()
  faces.append((h,pts))
 return Poly(faces)

def exact_num(x,scale=1):
 q=F(x,scale);decimal.getcontext().prec=65
 dec=decimal.Decimal(q.numerator)/decimal.Decimal(q.denominator)
 # Exact fractions are hashed to avoid huge report fields; decimal carries an explicit rounding bound.
 return {'decimal_65_significant_digits':str(dec),'float':float(q),'rational_numerator_bits':q.numerator.bit_length(),'rational_denominator_bits':q.denominator.bit_length(),'rational_sha256':hashlib.sha256((str(q.numerator)+'/'+str(q.denominator)).encode()).hexdigest(),'decimal_absolute_rounding_bound':str(decimal.Decimal(10)**(dec.adjusted()-64)) if dec else '0'}

def stl_triangles(path):
 data=path.read_bytes();count=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*count;out=[]
 for i in range(count):
  v=struct.unpack_from('<12fH',data,84+50*i);out.append(tuple(tuple(v[k:k+3]) for k in [3,6,9]))
 return out

def run_unit(name,expected,actual,outdir):
 start=time.time();floats=[x for p in expected for v in p['vertices_mm'] for x in v]+[x for v in actual['vertices_mm'] for x in v];exponent=max(F(float(x)).denominator.bit_length()-1 for x in floats);scale=2**exponent
 vv=[tuple(int(F(float(x))*scale) for x in v) for v in actual['vertices_mm']];ff=actual['triangles'];origin=tuple(F(sum(v[k] for v in vv),len(vv)) for k in range(3))
 prims=[primitive(p,scale) for p in expected];cells=[]
 for i,P in enumerate(prims):
  remains=[P]
  for C in prims[:i]:
   tmp=[]
   for Q in remains:tmp.extend(subtract(Q,C))
   remains=tmp
   if not remains:break
  cells.extend(remains)
  print(name,'primitive',i,'union_cells',len(cells),'seconds',round(time.time()-start,1),flush=True)
 unionvol=sum(P.volume() for P in cells)
 actualvol=0;inter=0;tetcount=0;intercount=0
 for ti,face in enumerate(ff):
  a,b,c=[vv[k] for k in face];six=det(sub(a,origin),sub(b,origin),sub(c,origin))
  if six==0:continue
  actualvol+=F(six,6);sgn=1 if six>0 else -1;T=tetra([origin,a,b,c]);tetcount+=1
  for C in cells:
   J=intersection(T,C)
   if J is not None:inter+=sgn*J.volume();intercount+=1
  if ti%20==0:print(name,'triangle',ti,'intersections',intercount,'seconds',round(time.time()-start,1),flush=True)
 extra=actualvol-inter;missing=unionvol-inter
 assert extra>=0 and missing>=0,('NEGATIVE_EXACT_DIFFERENCE',name,float(extra/scale**3),float(missing/scale**3))
 stl=stl_triangles(SOURCE/(name+'.stl'));geotri=[tuple(tuple(float(x) for x in actual['vertices_mm'][k]) for k in face) for face in ff]
 match=stl==geotri
 result={'id':name,'method':'Exact rational signed-tetrahedron integration against a disjoint exact convex decomposition of expected union. IEEE754 coordinate conversion exact; no sampling and no numerical clipping tolerance. Requires actual mesh to be embedded, closed and consistently outward oriented; independent embedding audit reported separately.','integer_lattice_exponent':exponent,'primitive_count':len(prims),'expected_disjoint_convex_cells':len(cells),'actual_triangles':len(ff),'nonzero_signed_tetrahedra':tetcount,'positive_convex_intersections_evaluated':intercount,'actual_geometry_equals_binary_stl_ordered_triangle_coordinates':match,'expected_union_volume_mm3':exact_num(unionvol,scale**3),'actual_signed_volume_mm3':exact_num(actualvol,scale**3),'intersection_signed_integral_mm3':exact_num(inter,scale**3),'actual_extra_outside_expected_mm3':exact_num(extra,scale**3),'expected_missing_from_actual_mm3':exact_num(missing,scale**3),'symmetric_difference_mm3':exact_num(extra+missing,scale**3),'exact_domain_equal':extra==0 and missing==0,'elapsed_seconds':time.time()-start}
 (outdir/(name+'.exact-domain.json')).write_text(json.dumps(result,indent=2)+'\n');return result

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--unit');args=parser.parse_args();expected=json.loads((SOURCE/'expected-convex-primitives.json').read_text());actual={x['id']:x for x in json.loads((SOURCE/'geometry.json').read_text())['objects']};out=[]
 for name in expected:
  if args.unit and name!=args.unit:continue
  out.append(run_unit(name,expected[name],actual[name],HERE))
 (HERE/('SUMMARY-'+(args.unit or 'ALL')+'.json')).write_text(json.dumps({'inputs':{n:hashlib.sha256((SOURCE/n).read_bytes()).hexdigest() for n in ['expected-convex-primitives.json','geometry.json']},'results':out},indent=2)+'\n')
if __name__=='__main__':main()
