# Double precision finite solid BSP; no change to input STL bytes.
import numpy as np
EPS=1e-5
class Poly:
 def __init__(self,v):
  self.v=np.array(v,dtype=float);n=np.cross(self.v[1]-self.v[0],self.v[2]-self.v[0]);l=np.linalg.norm(n)
  if l<1e-12:raise ValueError('degenerate polygon')
  self.n=n/l;self.w=float(self.n@self.v[0])
 def flip(self):self.v=self.v[::-1].copy();self.n=-self.n;self.w=-self.w
 def clone(self):return Poly(self.v.copy())
class Node:
 def __init__(self,ps=None):
  self.n=None;self.w=None;self.ps=[];self.f=None;self.b=None
  if ps:self.build(ps)
 def split(self,p,cf,cb,front,back):
  ds=p.v@self.n-self.w;typ=np.where(ds>EPS,1,np.where(ds< -EPS,2,0));t=0
  for x in typ:t|=int(x)
  if t==0:(cf if self.n@p.n>0 else cb).append(p)
  elif t==1:front.append(p)
  elif t==2:back.append(p)
  else:
   f=[];b=[]
   for i,vi in enumerate(p.v):
    j=(i+1)%len(p.v);vj=p.v[j];ti=int(typ[i]);tj=int(typ[j])
    if ti!=2:f.append(vi)
    if ti!=1:b.append(vi)
    if (ti|tj)==3:
     q=vi+(vj-vi)*(self.w-self.n@vi)/(self.n@(vj-vi));f.append(q);b.append(q)
   for vv,out in [(f,front),(b,back)]:
    clean=[]
    for q in vv:
     if not clean or np.linalg.norm(q-clean[-1])>1e-8:clean.append(q)
    if len(clean)>2 and np.linalg.norm(clean[0]-clean[-1])<1e-8:clean.pop()
    if len(clean)>2:
     # rotate to a non-collinear first triple
     for k in range(len(clean)):
      c=clean[k:]+clean[:k]
      if np.linalg.norm(np.cross(c[1]-c[0],c[2]-c[0]))>1e-12:out.append(Poly(c));break
 def invert(self):
  for p in self.ps:p.flip()
  if self.n is not None:self.n=-self.n;self.w=-self.w
  if self.f:self.f.invert()
  if self.b:self.b.invert()
  self.f,self.b=self.b,self.f
 def clip_polys(self,ps):
  if self.n is None:return ps[:]
  f=[];b=[]
  for p in ps:self.split(p,f,b,f,b)
  if self.f:f=self.f.clip_polys(f)
  if self.b:b=self.b.clip_polys(b)
  else:b=[]
  return f+b
 def clip_to(self,b):
  self.ps=b.clip_polys(self.ps)
  if self.f:self.f.clip_to(b)
  if self.b:self.b.clip_to(b)
 def all(self):return self.ps+(self.f.all()if self.f else[])+(self.b.all()if self.b else[])
 def build(self,ps):
  if not ps:return
  if self.n is None:self.n=ps[0].n.copy();self.w=ps[0].w
  f=[];b=[]
  for p in ps:self.split(p,self.ps,self.ps,f,b)
  if f:
   if self.f is None:self.f=Node()
   self.f.build(f)
  if b:
   if self.b is None:self.b=Node()
   self.b.build(b)
def difference(aa,bb):
 a=Node([p.clone()for p in aa]);b=Node([p.clone()for p in bb]);a.invert();a.clip_to(b);b.clip_to(a);b.invert();b.clip_to(a);b.invert();a.build(b.all());a.invert();return a.all()
def intersection(aa,bb):
 a=Node([p.clone()for p in aa]);b=Node([p.clone()for p in bb]);a.invert();b.clip_to(a);b.invert();a.clip_to(b);b.clip_to(a);a.build(b.all());a.invert();return a.all()
def halfspace(n,c,bounds):
 # convex hull of clipped bounding-box corners and crossing edges, scipy is only triangulator.
 from scipy.spatial import ConvexHull
 import itertools
 lo,hi=bounds;v=np.array(list(itertools.product(*zip(lo,hi))));d=v@n+c;pts=[x for x,t in zip(v,d)if t<=0]
 for i,j in itertools.combinations(range(8),2):
  if np.count_nonzero(v[i]!=v[j])==1 and d[i]*d[j]<0:pts.append(v[i]+(v[j]-v[i])*d[i]/(d[i]-d[j]))
 if len(pts)<4:return[]
 pts=np.array(pts);h=ConvexHull(pts);out=[]
 for f,e in zip(h.simplices,h.equations):
  p=Poly(pts[f]);
  if p.n@e[:3]<0:p.flip()
  out.append(p)
 return out
