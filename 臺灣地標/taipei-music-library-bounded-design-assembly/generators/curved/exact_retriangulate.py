from fractions import Fraction as F
import collections

def repair(vertices,faces):
 v=[];ix={};mp={}
 for i,q in enumerate(vertices):
  key=tuple(q)
  if key not in ix:ix[key]=len(v);v.append(q)
  mp[i]=ix[key]
 f=[[mp[i]for i in t]for t in faces];records=[]
 def cross(a,b):return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
 def sub(a,b):return[x-y for x,y in zip(a,b)]
 def dot(a,b):return sum(x*y for x,y in zip(a,b))
 def norm(t):return cross(sub(v[t[1]],v[t[0]]),sub(v[t[2]],v[t[0]]))
 def exact_coplanar(a,b,c,d):
  a,b,c,d=[[F(x)for x in v[i]]for i in [a,b,c,d]];return dot(cross(sub(b,a),sub(c,a)),sub(d,a))==0
 for attempt in range(20):
  zeros=[i for i,t in enumerate(f)if dot(norm(t),norm(t))==0]
  if not zeros:break
  edges=collections.defaultdict(list)
  for i,t in enumerate(f):
   for a,b in zip(t,t[1:]+t[:1]):edges[tuple(sorted((a,b)))].append(i)
  changed=False
  for i in zeros:
   t=f[i]
   for a,b in zip(t,t[1:]+t[:1]):
    c=next(x for x in t if x not in[a,b]);ab=sub(v[b],v[a]);ac=sub(v[c],v[a]);den=dot(ab,ab)
    if not den or not(0<dot(ac,ab)<den):continue
    for j in edges[tuple(sorted((a,b)))]:
     if i==j:continue
     d=next(x for x in f[j]if x not in[a,b])
     if d==c or tuple(sorted((c,d)))in edges or not exact_coplanar(a,b,c,d):continue
     # Directed pair boundary: replace diagonal and orient to surviving nonzero face normal.
     n=norm(f[j]);new=[[a,c,d],[c,b,d]]
     for k,tt in enumerate(new):
      if dot(norm(tt),n)<0:new[k]=list(reversed(tt))
     if any(dot(norm(tt),norm(tt))==0 for tt in new):continue
     def boundary(ts):
      e=collections.Counter((a,b)for t in ts for a,b in zip(t,t[1:]+t[:1]));return sorted((a,b)for (a,b),num in e.items()for _ in range(max(0,num-e[(b,a)])))
     if boundary([f[i],f[j]])!=boundary(new):continue
     records.append({'face_indices':[i,j],'old':[f[i],f[j]],'new':new,'vertices':[a,b,c,d],'strict_dyadic_coplanarity':True,'C_strictly_inside_AB':True,'directed_outer_boundary_exact':True,'new_diagonal_unused':True});f[i],f[j]=new;changed=True;break
    if changed:break
   if changed:break
  if not changed:print('UNRESOLVED',zeros);break
 return v,f,records
