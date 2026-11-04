from pathlib import Path
import numpy as np,json,struct,hashlib
from scipy.spatial import cKDTree
P=Path(__file__).resolve().parent;O=P/'reference-nominal'
polys=json.load(open(P/'CSG64-POLYGONS.json'));records=json.load(open(O/'BUILD-RECORD.json'))['parts'];out=[];mapping={};details=[]
plan=json.load(open(P/'interface-design.json'))
affected={x[k]for x in plan['interfaces']for k in ['a','b']}
for rr in records:
 if rr['id'] not in affected:
  data=(O/rr['file']).read_bytes();(P/rr['file']).write_bytes(data);out.append({**rr,'original_part_sha256':rr['sha256'],'artificial_relief':False});details.append({'id':rr['id'],'unchanged_exact_original_STL':True});continue
 name=rr['id'];ps=[np.array(x,dtype=float)for x in polys[name]];allv=np.concatenate(ps).astype(np.float32).astype(float);tree=cKDTree(allv);parent=list(range(len(allv)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for a,b in tree.query_pairs(2e-5):parent[root(b)]=root(a)
 groups={}
 for i in range(len(allv)):groups.setdefault(root(i),[]).append(i)
 # Keep an existing coordinate, never average source boundaries.
 reps={k:allv[min(v)].copy()for k,v in groups.items()};vs=np.array(list(reps.values()));new=[];offset=0;maxmove=0
 for p in ps:
  seq=[]
  for i in range(len(p)):
   v=reps[root(offset+i)];maxmove=max(maxmove,float(np.linalg.norm(v-p[i])))
   if not seq or np.linalg.norm(v-seq[-1])>1e-8:seq.append(v)
  offset+=len(p)
  if len(seq)>2 and np.linalg.norm(seq[0]-seq[-1])<1e-8:seq.pop()
  if len(seq)<3:continue
  # All incident segment points, including T-junctions made by BSP.
  ring=[]
  for a,b in zip(seq,seq[1:]+seq[:1]):
   d=b-a;ll=d@d
   if ll<1e-16:continue
   t=(vs-a)@d/ll;dist=np.linalg.norm(vs-(a+t[:,None]*d),axis=1);idx=np.where((t>=-1e-8)&(t<1-1e-8)&(dist<2e-5))[0]
   ring.extend(vs[i]for i in sorted(idx,key=lambda i:t[i]))
  if len(ring)<3:continue
  normalarea=np.linalg.norm(sum((np.cross(a,b)for a,b in zip(ring,ring[1:]+ring[:1])),np.zeros(3)))/2
  longest=max(np.linalg.norm(a-b)for a in ring for b in ring)
  if normalarea/max(longest,1e-20)<2e-5:continue
  center=np.mean(ring,axis=0).astype(np.float32).astype(float)
  for a,b in zip(ring,ring[1:]+ring[:1]):
   tri=np.array([center,a,b]);area=np.linalg.norm(np.cross(a-center,b-center))/2
   if area>1e-10:new.append(tri)
 data=bytearray(b'FLOAT64 BSP FINITE MITER RESEARCH NO PHYSICAL FIT'.ljust(80,b' '));data+=struct.pack('<I',len(new))
 for tri in new:
  normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=np.linalg.norm(normal);data+=struct.pack('<12fH',*normal,*tri.reshape(-1),0)
 path=P/rr['file'];path.write_bytes(data);vv=np.concatenate(new);out.append({**rr,'sha256':hashlib.sha256(data).hexdigest(),'original_part_sha256':rr['sha256'],'triangles':len(new),'bbox':[vv.min(0).tolist(),vv.max(0).tolist()],'artificial_relief':True});details.append({'id':name,'max_numeric_vertex_cluster_move_mm':maxmove,'polygons':len(ps),'triangles':len(new)})
(P/'BUILD-RECORD.json').write_text(json.dumps({'status':'BSP_RELIEF_AWAITING_QA','parts':out},indent=2)+'\n');(P/'NUMERICAL-CONFORMING-TRIANGULATION.json').write_text(json.dumps({'epsilon_mm':2e-5,'not_physical_clearance':True,'parts':details},indent=2)+'\n')
print('exported',len(out),sum(x['triangles']for x in out))
