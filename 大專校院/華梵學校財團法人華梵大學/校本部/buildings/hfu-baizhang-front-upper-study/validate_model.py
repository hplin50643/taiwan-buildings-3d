"""Independent binary STL topology checks, standard Python only; not a print test."""
import argparse,struct,math,json,hashlib,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('stl',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();data=a.stl.read_bytes();count=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*count
vertices=[];lookup={};faces=[];edgeuses=collections.defaultdict(list);fans=collections.defaultdict(list);areas=[];volume=0
for i in range(count):
 raw=struct.unpack_from('<12fH',data,84+50*i);tri=[tuple(raw[j:j+3]) for j in (3,6,9)];assert all(math.isfinite(x) for v in tri for x in v)
 ids=[]
 for v in tri:
  if v not in lookup:lookup[v]=len(vertices);vertices.append(v)
  ids.append(lookup[v])
 faces.append(ids)
 def sub(x,y):return tuple(a-b for a,b in zip(x,y))
 def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
 cr=cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]));areas.append(math.sqrt(sum(x*x for x in cr))/2);volume+=sum(x*y for x,y in zip(tri[0],cross(tri[1],tri[2])))/6
 for j in range(3):
  u,v=ids[j],ids[(j+1)%3];edgeuses[tuple(sorted((u,v)))].append((u,v));fans[u].append((ids[(j+1)%3],ids[(j+2)%3]))
adj=collections.defaultdict(set)
for u,v in edgeuses:adj[u].add(v);adj[v].add(u)
unseen=set(range(len(vertices)));components=0
while unseen:
 components+=1;stack=[unseen.pop()]
 while stack:
  for v in adj[stack.pop()]:
   if v in unseen:unseen.remove(v);stack.append(v)
badfans=0
for center,edges in fans.items():
 graph=collections.defaultdict(set)
 for u,v in edges:graph[u].add(v);graph[v].add(u)
 rem=set(graph);stack=[rem.pop()]
 while stack:
  for v in graph[stack.pop()]:
   if v in rem:rem.remove(v);stack.append(v)
 if rem or any(len(x)!=2 for x in graph.values()):badfans+=1
checks={'finite_coordinates':True,'standard_binary_length':True,'nondegenerate_faces':min(areas)>0,'two_faces_per_edge':all(len(v)==2 for v in edgeuses.values()),'consistent_winding':all(len(v)==2 and v[0]==v[1][::-1] for v in edgeuses.values()),'single_component':components==1,'single_cycle_vertex_links':badfans==0,'positive_volume':volume>0}
r={'passed':all(checks.values()),'checks':checks,'stl_sha256':hashlib.sha256(data).hexdigest(),'triangles':count,'vertices':len(vertices),'components':components,'volume_mm3':volume,'minimum_triangle_area_mm2':min(areas),'bbox_mm':[[min(v[i] for v in vertices) for i in range(3)],[max(v[i] for v in vertices) for i in range(3)]],'limitations':['No comprehensive self-intersection test.','No minimum thickness, slicing or physical print certification.','Source-bounded artificial relief, not complete or measured building.']};a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(0 if r['passed'] else 1)
