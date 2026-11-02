"""TMU oral medicine building historical1973drawing/1975completion exterior, NOT present survey.
Source controls metres; display millimetres at1:250. Post1999curtain wall/elevator excluded.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/250
PALETTE=[('illustrative washed masonry','#CCC6B5'),('illustrative exposed concrete','#AEB0A8'),('illustrative roof finish','#858A82'),('illustrative joinery','#94856F'),('authored support not terrain','#A5AD9C'),('opaque glazing illustration','#628089'),('illustrative timber door','#9E8B73'),('model interface cut NOT historical exterior wall','#76827B')]
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yzsolid(pts,x0,x1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
def xzsolid(pts,y0,y1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(y1-y0).transform(((1,0,0,0),(0,0,1,y0),(0,1,0,0)))
# Axes x0..72 west-east; y0 front to10.4rear. Fourstoreys, openfrontcorridor.
BASE=.50;FLOORS=[.35,3.95,7.55,11.15];RF=14.75
bx('authored_display_support_not_historical_terrain',-2.2,74.2,-4.2,12.5,-BASE,0,4)
bx('building_ground_platform_GL035',-.1,72.1,-.10,10.5,0,.35,1)
# Hiddenbodytop2cmunderroofskinavoidscoplanarmaterialtriangles; exposedRFunchanged.
# Mainoccupiedexterior; openfrontcorridor preserved, no1999curtainwall.
body=box(0,72,2.6,10.4,.33,RF-.02)
for a,b in [(0,16),(56,72)]:body=body+box(a,b,0,2.62,.33,RF-.02)
# SourceA2/A7 eighteenfolds, onlylongdiagonal isopaque.
folds=[]
for k in range(18):
 a=13.5+2.5*k;pts=[(a,10.35),(a+2,11.9),(a+2.5,10.35)]
 body=body+prism(pts,.33,RF-.02)
 folds.append((a,a+2,a+2.5))
# Fourroundopenings; RFupperanchoredcentres. Interior is limited recessedshadow, notfullreconstruction.
for cx in [12,60]:
 for cz in [3.9,11.1]:
  cut=Manifold.cylinder(2.1,2.6,2.6,96).rotate((90,0,0)).translate((cx,1.95,cz))
  body=body-cut
# Generalwindowrecesses normaltoface with printableinfill.
W=[]
def rect_on_plane(cx,cy,dx,dy,w,depth,z0,z1,offset=0):
 nx,ny=-dy,dx
 return prism([(cx+dx*u+nx*v,cy+dy*u+ny*v)for u,v in [(-w/2,offset), (w/2,offset),(w/2,offset+depth),(-w/2,offset+depth)]],z0,z1)
def window(tag,cx,cy,dx,dy,w,z0,z1,cols=3,rows=3):
 global body
 body=body-rect_on_plane(cx,cy,dx,dy,w,.45,z0,z1,-.20)
 W.append((tag,cx,cy,dx,dy,w,z0,z1,cols,rows))
# Classroomfront behind2.6m open corridor. Graphicallyderived5m subbays, notcurtainwall.
for fl in FLOORS:
 for x in range(16,56,5):window('front_recessed_classroom_window',x+2.5,2.6,1,0,4.20,fl+2.30,fl+3,4,1)
for fl in FLOORS:
 for x in [16.7,25.3,26.7,35.3,36.7,45.3,46.7,55.3]:
  window('corridor_classroom_door_graphic',x,2.6,1,0,1.0,fl,fl+2.1,1,1)
# Actualsidefour260bays; outwardfinwalls beyondxaxis handledseparately.
for fl in FLOORS:
 for y in [1.3,3.9,6.5,9.1]:
  window('west_side_window',0,y,0,-1,2.05,fl+.90,fl+3,3,3)
  window('east_side_window',72,y,0,1,2.05,fl+.90,fl+3,3,3)
# Rearfoldshortdiagonalglass, notsolidlongslope.
for a,b,c in folds:
 dx,dy=.5,-1.55;le=(dx*dx+dy*dy)**.5;dx/=-le;dy/=-le
 for fl in FLOORS:window('rear_fold_short_glazing',b+.25,11.125,dx,dy,le-.18,fl+.95,fl+3.0,1,3)
# Rearendtoiletsmallwindows; actualpositions estimatedfromA3±.10m.
for fl in FLOORS:
 for x in [9,10.5,12,60,61.5,63]:window('rear_end_small_window_graphic',x,10.4,-1,0,1.08,fl+1.55,fl+2.25,1,1)
for x in [6,66]:window('rear_1F_extra_outer_window_graphic',x,10.4,-1,0,1.80,1.90,2.60,2,1)
add('historical_occupied_exterior_open_corridor_NOT_current_curtainwall',body,0)
for tag,cx,cy,dx,dy,w,z0,z1,cols,rows in W:
 # normal(-dy,dx) goesinwards foroursurfaces exceptfolds; usecentredshallowlayer tostayconnected.
 add(tag+'_opaque_glazing_illustration',rect_on_plane(cx,cy,dx,dy,w+.03,.16,z0-.02,z1+.02,.10),6 if 'door' in tag else 5)
 fw=.10
 for u in np.linspace(-w/2,w/2,cols+1):
  add(tag+'_frame',rect_on_plane(cx+dx*u,cy+dy*u,dx,dy,fw,.30,z0,z1,-.07),3)
 for z in np.linspace(z0,z1,rows+1):add(tag+'_rail',rect_on_plane(cx,cy,dx,dy,w,.30,z-fw/2,z+fw/2,-.07),3)
# Openfrontcorridor slabs/columns, unobscured inhistoricfrontview.
for fl in FLOORS[1:]+[RF]:bx('front_corridor_floor_slab',15.8,56.2,-.10,2.65,fl-.22,fl-.02 if fl==RF else fl,1)
for fl in FLOORS[1:]+[RF]:bx('front_corridor_65cm_downstand',16,56,-.15,.20,fl-.65,fl-.02 if fl==RF else fl,1)
for x in range(16,57,5):bx('front_corridor_column_graphic40',x-.20,x+.20,-.20,.20,.33,RF-.02,1)
# Upperlowguardwalls, sourceA6. Finepipeadaptedto.10m=.4mm.
for fl in FLOORS[1:]:
 if fl!=3.95:
  bx('open_corridor_guardwall',16,56,-.12,.10,fl,fl+.95,1)
# Secondfloorbalconyonly,not3/4F; central40m x3.5.
bx('secondfloor_balcony_slab_only',16,56,-3.5,0.2,3.73,3.95,1)
bx('balcony_front_guardwall',16,56,-3.5,-3.32,3.95,4.90,1)
for a,b in [(16,16.18),(55.82,56)]:bx('balcony_end_guardwall',a,b,-3.5,.10,3.95,4.90,1)
# Recessedlanding/slimsolidguardwithinroundholes; flooranchored+5cmcoordinationrecorded.
for cx in [12,60]:
 for fl,cz in [(3.95,3.9),(11.15,11.1)]:
  bx('round_aperture_recessed_landing_not_complete_stair',cx-2.55,cx+2.55,.30,2.10,fl-.22,fl,1)
  bx('round_aperture_solid_low_guard',cx-2.58,cx+2.58,.42,.54,fl,fl+.60,1)
  bx('round_aperture_pipe_rail_adapted',cx-2.46,cx+2.46,.43,.53,fl+.90,fl+1.00,3)
  for xx in [cx-2.4,cx+2.4]:bx('round_aperture_rail_end_post',xx-.05,xx+.05,.43,.53,fl+.55,fl+1.00,3)
# Sidewingwalls, true150projection (notextraoccupiedrooms), fourbays.
for yy in np.arange(0,10.41,2.6):
 bx('west_150cm_wingwall',-1.5,.10,yy-.09,yy+.09,.33,15.95,0)
 bx('east_150cm_wingwall',71.90,73.5,yy-.09,yy+.09,.33,15.95,0)
for fl in FLOORS[1:]:
 bx('west_side_60cm_window_canopy',-.60,.10,0,10.4,fl-.15,fl,1)
 bx('east_side_60cm_window_canopy',71.9,72.60,0,10.4,fl-.15,fl,1)
# Roofdrainageslope1/100 noted;nominaldatum doesnotassertfinishedcornerheights.
bx('nominal_main_roof_slab',-1.5,73.5,-.15,10.50,14.55,14.75,2)
bx('front_parapet_RFplus120',-1.5,73.5,-.15,.05,14.70,15.95,0)
for a,b in [(-1.5,-1.3),(73.3,73.5)]:bx('side_parapet',a,b,0,10.5,14.70,15.95,0)
bx('rear_roof_parapet_nominal',-1.5,73.5,10.30,10.50,14.70,15.95,0)
# FoldtopsfinishatRFandremainoutsideparapetline perA3/A7.
for a,b,c in folds:add('fold_top_roof_closure',prism([(a,10.30),(b,11.90),(c,10.30)],14.55,14.75),2)
# Two800x400stairhouses, centreperA2. Mainroofstairshiddenexcluded.
for a in [8,56]:
 bx('roof_stairhouse_800x400axis',a-.075,a+8.075,2.525,6.675,14.70,17.55,0)
 bx('roof_stairhouse_30cm_topslab',a-.15,a+8.15,2.45,6.75,17.55,17.85,1)
 # smallA2roofwindow/doorpositionsgraphicnotfullschedule.
 dc=a+7.0 if a==8 else a+1.0
 bx('roof_stairhouse_rear_door_graphic',dc-.45,dc+.45,6.66,6.72,14.75,16.85,6)
 bx('roof_stairhouse_front_window_graphic',dc-.65,dc+.65,2.49,2.54,15.75,16.75,5)
# NUMERICAL_FINALIZATION
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-36,-4.2,.50)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_NOT_FINAL_SOURCE_OR_PRINT_QA','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:250','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
