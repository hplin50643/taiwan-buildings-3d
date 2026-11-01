"""PTIVS external stair addition, August1971 historical design; not as-built.
Only CCRH53623005/006. Metres until final1:50 millimetre export.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=20
PALETTE=[('RC approximate warm grey','#C5C0AD'),('red tile approximate not sampled','#A65F44'),('roof protective coating approximate ivory','#DDD7BF'),('painted steel neutral approximate','#6D7875'),('authored display base not terrain','#A7AD9D')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def profile_xz(n,pts,y0,y1,mat=0):
 # CrossSection extrusion local z rotated into world y.
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 m=CrossSection([pts]).extrude(y1-y0).rotate((90,0,0)).translate((0,y1,0));add(n,m,mat)
def beam(n,a,b,w=.035,mat=3):
 a=np.array(a);b=np.array(b);vec=b-a;L=np.linalg.norm(vec);z=vec/L;aux=np.array([0.,0.,1.]);
 if abs(z@aux)>.95:aux=np.array([0.,1.,0.])
 x=np.cross(z,aux);x/=np.linalg.norm(x);y=np.cross(z,x)
 # square section hull connecting endpoints, overlapped at endpoints.
 pts=[p+sx*x*w/2+sy*y*w/2 for p in [a-z*.01,b+z*.01] for sx in [-1,1] for sy in [-1,1]]
 add(n,Manifold.hull_points(pts),mat)
# Declared support/base; no fabricated classroom volume.
bx('authored_base_not_site_terrain',-.45,6.05,-3.70,3.70,-.22,0,4)
bx('ground_entrance_platform_FL040',-.04,1.03,-3.3,3.3,-.01,.40)
bx('lower_stair_footing_display_ground_slab',.88,5.62,-1.96,1.96,-.01,.18)
# 30cm central wall; tiled faces represented by restrained relief joints.
bx('central_wall_30cm',.90,3.825,-.15,.15,.0,7.46,1)
for z in np.arange(.45,7.35,.065):
 for y in [-.155,.15]:bx('tile_horizontal_course_relief',.91,3.815,y,y+.005,z,z+.006,1)
# Two 200cm-rise flights: ten risers and nine32.5cm treads.
for side in [-1,1]:
 y0,y1=(-1.95,-.14) if side<0 else (.14,1.95)
 # Lower ascending+x; upper ascending-x.12cm structural waist, not solid staircase block.
 if side<0:
  pts=[(.89,.275),(3.835,2.085),(3.835,2.205),(.89,.395)]
 else:pts=[(.89,4.085),(3.835,2.275),(3.835,2.395),(.89,4.205)]
 profile_xz('lower_waist' if side<0 else 'upper_waist',pts,y0,y1)
 for i in range(9):
  a=.90+i*.325;b=a+.325;top=.60+.20*i if side<0 else 4.20-.20*i
  # below tread overlaps sloping waist; upper step lower end uses decreasing profile.
  bottom=(.60+.20*i-.24) if side<0 else (4.20-.20*(i+1)-.14)
  bx(f'flight_{side}_tread_{i}',a-.005,b+.005,y0,y1,bottom,top)
bx('mid_landing_EL240',3.81,5.60,-1.95,1.95,2.25,2.40)
bx('upper_connector_EL440_to_existing_boundary',-.03,1.02,-3.30,3.30,4.25,4.40)
# Railings80cm high. Source10mm square bars thickened to30mm (0.6mm at1:50).
for side in [-1,1]:
 y=side*1.95
 def tz(x):return .40+(x-.9)/2.925*2.0 if side<0 else 4.40-(x-.9)/2.925*2.0
 beam(f'slope_handrail_{side}',(.90,y,tz(.9)+.8),(3.825,y,tz(3.825)+.8),.06)
 for x in np.linspace(.90,3.825,21):beam('slope_baluster', (x,y,tz(x)-.04),(x,y,tz(x)+.80),.03)
 # midlanding edge rails continuing both ends plus farend.
 beam('landing_side_top',(3.81,y,3.20),(5.6,y,3.20),.06)
 for x in np.linspace(3.825,5.60,13):beam('landing_side_bar',(x,y,2.36),(x,y,3.20),.03)
beam('landing_far_top',(5.6,-1.95,3.20),(5.6,1.95,3.20),.06)
for y in np.linspace(-1.95,1.95,27):beam('landing_far_bar',(5.6,y,2.36),(5.6,y,3.20),.03)
# Upper side connector rails terminate at actual boundary; no railing across building access.
for y in [-3.3,3.3]:
 beam('upper_connector_end_rail',(0,y,5.20),(1.0,y,5.20),.06)
 for x in np.linspace(0,1,8):beam('upper_connector_end_bar',(x,y,4.36),(x,y,5.20),.03)
for a,b in [(-3.3,-1.95),(1.95,3.3)]:
 beam('upper_connector_outer_top',(1.0,a,5.2),(1.0,b,5.2),.06)
 for y in np.linspace(a,b,10):beam('upper_connector_outer_bar',(1.,y,4.36),(1.,y,5.2),.03)
# Main12cm canopy slab and structural central spine.
bx('roof_slab_12cm_EL790',0,5.60,-1.95,1.95,7.78,7.90,2)
bx('central_roof_spine',-.01,5.61,-.16,.16,7.45,7.80)
# Two KG2 transverse beams,20x45cm incl slab, graphically divided thirds.
for x in [1.87,3.73]:bx("KG2_transverse_beam",x-.10,x+.10,-1.95,1.95,7.45,7.80)
# Longitudinal scalloped fascia. Lower profile follows explicit R142 arcs.
for y0,y1 in [(-1.95,-1.79),(1.79,1.95)]:
 fascia=box(0,5.60,y0,y1,7.33,7.78)
 for lo,hi in [(.15,1.72),(2.02,3.59),(3.89,5.45)]:
  cx=(lo+hi)/2;r=1.42;hh=(hi-lo)/2
  xs=np.linspace(lo,hi,41);zs=7.33+np.sqrt(r*r-(xs-cx)**2)-np.sqrt(r*r-hh*hh)
  # cutter below arc, extrudedalongy.
  pp=[(lo,7.0),(hi,7.0)]+list(zip(xs[::-1],zs[::-1]));cs=CrossSection([pp]);cut=cs.extrude(y1-y0+.04).rotate((90,0,0)).translate((0,y1+.02,0));fascia=fascia-cut
 add('longitudinal_R142_scalloped_band',fascia,2)
# Transverse scallops on xends. NominalR140 (handwritten±2cm reading uncertainty).
for x0,x1 in [(0,.16),(5.44,5.60)]:
 fascia=box(x0,x1,-1.95,1.95,7.33,7.78)
 for lo,hi in [(-1.80,-.15),(.15,1.80)]:
  cy=(lo+hi)/2;r=1.40;hh=(hi-lo)/2;ys=np.linspace(lo,hi,41);zs=7.33+np.sqrt(r*r-(ys-cy)**2)-np.sqrt(r*r-hh*hh)
  pp=[(lo,7.0),(hi,7.0)]+list(zip(ys[::-1],zs[::-1]));cut=CrossSection([pp]).extrude(x1-x0+.04).rotate((90,0,90)).translate((x0-.02,0,0));fascia=fascia-cut
 add('transverse_R140_scalloped_band',fascia,2)
# 5cm external mouldings and locally raised12cm edge bands (not790wholemax).
for y0,y1 in [(-2.00,-1.90),(1.90,2.00)]:
 bx('roof_5cm_moulding_long',0,5.60,y0,y1,7.73,7.78,2);bx('roof_raised_edge_long',0,5.60,y0,y1,7.88,8.02,2)
for x0,x1 in [(-.05,.05),(5.55,5.65)]:
 bx('roof_5cm_moulding_end',x0,x1,-2.,2.,7.73,7.78,2);bx('roof_raised_edge_end',x0,x1,-2.,2.,7.88,8.02,2)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-2.80,0,.22)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:50','datum':'GL0; authoredsupportnotterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
