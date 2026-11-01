"""NCHU CCCK240 shelter, March1985 revision. Single uncrossed18.48m canopy.
Metres, GL=0. Printscale1:100. Sourcepixels excluded. Not current/as-built.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={}
PALETTE=[('mosaic concrete neutral approximate','#C9C5B6'),('roof waterproofing neutral approximate','#D8D5C7'),('rack painted steel color not established','#747D7A'),('paving neutral approximate','#B9B9AC'),('authored displaybase','#969F92')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def prism_x(n,x0,x1,yz,mat=0):add(n,Manifold.hull_points([(x,y,z) for x in [x0,x1] for y,z in yz]),mat)
def rod(n,a,b,w=.06):
 a=np.array(a);b=np.array(b);u=(b-a)/np.linalg.norm(b-a);v=np.cross(u,[0,0,1] if abs(u[2])<.9 else [0,1,0]);v=v/np.linalg.norm(v);t=np.cross(u,v)
 add(n,Manifold.hull_points([p+iv*v*w/2+it*t*w/2 for p in [a,b] for iv in [-1,1] for it in [-1,1]]),2)
L=18.48;COLS=[3.08,9.24,15.40]
bx('authored_displaybase_not_foundations',-.75,L+.75,-3.10,3.10,-.30,-.10,4)
bx('ground_display',-.75,L+.75,-3.10,3.10,-.11,0,4)
# Source pavement10cmPC, centralcrown+5cm; concealedaggregate/footings omitted.
bx('pavement_10cm_PC_flattened_plus5',0,L,-2.5,2.5,-.05,.05,3)
for i,x in enumerate(COLS):bx(f'C1_square35_column_{i+1}',x-.175,x+.175,-.175,.175,.03,2.12,0)
# Explicit10cm slab, separated from structuralupstands. Outer slabtop2.50,
# valleytop2.20; centralbeamtop2.50 andoutercurbtop2.60 are different.
for sign,side in [(-1,'south'),(1,'north')]:
 prism_x('RS_10cm_slab_'+side,0,L,[(0,2.10),(sign*2.5,2.40),(sign*2.5,2.50),(0,2.20)],1)
 a,b=sorted([sign*2.30,sign*2.50]);bx('RG4_edge20x20_'+side,0,L,a,b,2.40,2.60,0)
# Central longitudinal beams. RG1 depth conflict reviewed beforefreeze.
bx('RG2_center25x40_two616spans',3.08,15.40,-.125,.125,2.10,2.50,0)
# RG1 type25x40~20 conflicts with its schematicconstant-depthprofile.
# Adopt20cmend→40cmsupport taper, explicitly disclosedinterpretation.
for nm,poly in [('west',[(0,2.30),(3.08,2.10),(3.08,2.50),(0,2.50)]),('east',[(15.40,2.10),(L,2.30),(L,2.50),(15.40,2.50)])]:
 add('RG1_interpreted40to20_'+nm,Manifold.hull_points([(x,y,z) for x,z in poly for y in [-.125,.125]]),0)
# Five transverseRG5 lines: twoends andthreecolumns, width25cm.
for i,x in enumerate([0]+COLS+[L]):
 a=max(0,x-.125);b=min(L,x+.125)
 if i==0:b=.25
 if i==4:a=L-.25
 for sign,side in [(-1,'south'),(1,'north')]:prism_x(f'RG5_taper40to20_{i}_{side}',a,b,[(0,2.10),(sign*2.5,2.40),(sign*2.5,2.60),(0,2.50)],0)
# Four open triangular rack runs:4,10,10,4modules at56cm pitch.
# Original1inch tubes simplified as6cm square rods for0.6mm displaythickness.
# 87.6cm width/43.8cm height are nominal reference-centreline geometry.
for run,(start,count) in enumerate([(.56,4),(3.36,10),(9.52,10),(15.68,4)]):
 end=start+count*.56
 for y,z in [(-.438,.0627),(.438,.0627),(0,.0627),(0,.5007)]:rod(f'rack_{run}_longitudinal_{y}_{z}',(start,y,z),(end,y,z))
 for k in range(count+1):
  x=start+k*.56
  rod(f'rack_{run}_{k}_diagonal_s',(x,-.438,.0627),(x,0,.5007));rod(f'rack_{run}_{k}_diagonal_n',(x,.438,.0627),(x,0,.5007))
  rod(f'rack_{run}_{k}_middle',(x,0,.0627),(x,0,.5007))
# No parked bicycles, enclosingwalls, inventedfoundationpedestals or canceledpipes.
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-L/2,0,.30)).scale((10,10,10)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:100','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
