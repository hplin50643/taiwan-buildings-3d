from pathlib import Path
import numpy as np,json,struct,math
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
A=Path(__file__).resolve().parents[1];b=(A.parent/'model.stl').read_bytes();t=np.array([struct.unpack_from('<9f',b,96+50*i) for i in range(9614)]).reshape(-1,3,3);ids=json.loads((A/'qa/continuous-rim-verification.json').read_text())['changed_faces'];domains=[];seen=[]
for j in range(72):
 p=np.array([61.5*math.cos(j*2*math.pi/144),41.5*math.sin(j*2*math.pi/144)]);q=np.array([61.5*math.cos((j+1)*2*math.pi/144),41.5*math.sin((j+1)*2*math.pi/144)]);d=q-p;L=np.linalg.norm(d);u=d/L;out=np.array([u[1],-u[0]])
 lo,hi=0.,1.
 if d[0]>0:hi=min(hi,(-20.5-p[0])/d[0])
 elif d[0]<0:lo=max(lo,(-20.5-p[0])/d[0])
 elif p[0]>-20.5:continue
 if hi-lo<1e-9:continue
 ff=[i for i in ids if np.max(abs((t[i,:,:2]-p)@out))<1e-5]
 assert ff
 polys=[Polygon(np.column_stack(((t[i,:,:2]-p)@u,t[i,:,2]))) for i in ff];un=unary_union(polys);support=box(lo*L,83,hi*L,84.8)
 outside=un.difference(support).area;missing=support.difference(un).area
 assert outside<.001 and missing<.001
 seen+=ff;domains.append({'facet':j,'faces':ff,'outside_mm2':outside,'missing_mm2':missing,'support_area_mm2':support.area})
assert sorted(seen)==ids
(A/'qa/continuous-rim-support.json').write_text(json.dumps({'passed':True,'facets':domains,'all58_faces_independently_covered':True,'per_facet_area_tolerance_mm2':.001},indent=2)+'\n');print('INDEPENDENT RIM SUPPORT PASS',len(domains))
