#!/usr/bin/env python3
import json,itertools
from fractions import Fraction as F
from exact_domain_audit import HERE,primitive,subtract,intersection,tetra,det,sub
from exact_embedding_audit import audit
FACES=[[0,3,2],[0,2,1],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]
def box(x):return {'id':'box'+str(x),'vertices_mm':[[x,0,0],[x+2,0,0],[x+2,2,0],[x,2,0],[x,0,2],[x+2,0,2],[x+2,2,2],[x,2,2]],'triangles':FACES}
a=primitive(box(0),1);b=primitive(box(1),1);c=primitive(box(2),1);tests={}
tests['cube_volume_8']=a.volume()==8
tests['half_overlap_volume_4']=intersection(a,b).volume()==4
tests['subtraction_volume_4']=sum(x.volume() for x in subtract(a,b))==4
tests['identical_subtraction_empty']=subtract(a,a)==[]
tests['face_touch_intersection_empty']=intersection(a,c) is None
tests['face_touch_union_volume_16']=a.volume()+sum(x.volume() for x in subtract(c,a))==16
T=tetra([(0,0,0),(2,0,0),(0,2,0),(0,0,2)]);tests['tetra_volume_4over3']=T.volume()==F(4,3);tests['tetra_halfclip_volume_1over6']=intersection(T,b).volume()==F(1,6)
origin=(-3,5,7);obj=box(0);vv=[tuple(v) for v in obj['vertices_mm']];signedint=0
for face in FACES:
 p,q,r=[vv[k] for k in face];sg=det(sub(p,origin),sub(q,origin),sub(r,origin));U=tetra([origin,p,q,r]);J=intersection(U,b)
 if J is not None:signedint+=(1 if sg>0 else -1)*J.volume()
tests['outside_origin_signed_tetra_overlap_4']=signedint==4
tests['cube_embedded_audit']=audit(obj)['embedded_closed_oriented_single_surface_pass']
report={'tests':tests,'all_pass':all(tests.values()),'scope':'Analytic unit tests for volume, clipping, disjoint subtraction, touch-only exclusion, outside-origin signed integration and embedding.'};(HERE/'SELFTEST-EXACT-GEOMETRY.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
assert all(tests.values())
