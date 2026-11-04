from pathlib import Path
import numpy as np,json,struct,hashlib
from collections import Counter,defaultdict
P=Path(__file__).resolve().parent;rows=[];errors=[]
for p in sorted((P/'parts').glob('*.stl')):
 b=p.read_bytes();n=struct.unpack_from('<I',b,80)[0];assert len(b)==84+n*50
 tri=np.array([[struct.unpack_from('<12fH',b,84+50*i)[k:k+3]for k in[3,6,9]]for i in range(n)]);v,idx=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);fs=idx.reshape(-1,3);es=Counter();ds=Counter();eowners=defaultdict(list)
 for i,f in enumerate(fs):
  for a,c in zip(f,np.roll(f,-1)):e=tuple(sorted((int(a),int(c))));es[e]+=1;ds[(int(a),int(c))]+=1;eowners[e].append(i)
 areas=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2;volume=np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()/6
 adj=[set()for _ in range(n)]
 for vv in eowners.values():
  for i in vv:adj[i].update(vv)
 seen=set();components=0
 for i in range(n):
  if i in seen:continue
  components+=1;todo=[i];seen.add(i)
  while todo:
   k=todo.pop()
   for j in adj[k]-seen:seen.add(j);todo.append(j)
 linkbad=[]
 for vi in range(len(v)):
  adjv=defaultdict(set)
  for f in fs:
   if vi in f:
    other=[int(x)for x in f if x!=vi]
    if len(other)==2:a,c=other;adjv[a].add(c);adjv[c].add(a)
  if any(len(x)!=2 for x in adjv.values()):linkbad.append(vi)
  elif adjv:
   ss={next(iter(adjv))};stack=list(ss)
   while stack:
    a=stack.pop()
    for c in adjv[a]-ss:ss.add(c);stack.append(c)
   if len(ss)!=len(adjv):linkbad.append(vi)
 ok=all(x==2 for x in es.values())and all(ds[(a,c)]==ds[(c,a)]==1 for a,c in es)and areas.min()>1e-10 and volume>0 and not linkbad
 if not ok:errors.append(p.name)
 rows.append({'file':str(p.relative_to(P)),'sha256':hashlib.sha256(b).hexdigest(),'triangles':n,'vertices':len(v),'edges':len(es),'euler':len(v)-len(es)+n,'components':components,'volume_mm3':float(volume),'min_triangle_area':float(areas.min()),'edge_manifold_oriented':all(x==2 for x in es.values())and all(ds[(a,c)]==ds[(c,a)]==1 for a,c in es),'vertex_link_bad_count':len(linkbad),'pass':bool(ok)})
(P/'BINARY-QA.json').write_text(json.dumps({'status':'PASS_EACH_EXPORTED_PART'if not errors else'FAIL','parts':rows,'errors':errors,'whole_assembly_not_certified':True},indent=2)+'\n');print(len(rows),'parts',sum(x['triangles']for x in rows),'triangles',errors)
