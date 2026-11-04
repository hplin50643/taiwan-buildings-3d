"""NUPS archives, four paired groups, 1983 historical exterior interpretation.
Metres; x across each paired group; y from paper-bottom mainwall towards terraces.
No site terrain/roads/perimeter walls or interiors. Derived rear roof endpoints are not source ELs.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,Mesh64,CrossSection
from geometry_helpers import box,prism,perimeter_band
R=Path(__file__).resolve().parent
S=1000/350;BASE=.70;P=[];LOG=[];IDS={};OFF=0
PALETTE=[('illustrative plaster','#DDD6C5'),('illustrative concrete','#B5B5AC'),('illustrative roof finish','#7B817D'),('print-thickened metal frame','#9FAAAA'),('authored display support not terrain','#A3AA9B'),('opaque glazing illustration','#6D929B'),('illustrative timber door','#94765B')]
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.translate((OFF,0,0)).as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':('group'+str(round(OFF/22.63)+1)+'_'+n)if OFF>=0 else n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def yzsolid(pts,x0,x1):
 if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0:pts=pts[::-1]
 return CrossSection([pts]).extrude(x1-x0).transform(((0,0,1,x0),(1,0,0,0),(0,1,0,0)))
def rear_z(y):return 6.20-(y-4.615)*2/4.885
# Display slab is deliberately not historical site paving or measuredterrain.
OFF=-.0000001;bx('authored_display_base',-1.8,86.3,-2.2,11.3,-BASE,0,4)
for gi in range(4):
 OFF=gi*22.63;W=[]
 body=box(5.785,10.615,-.115,7.06,0,5.02)
 # Groundclosedrooms are6.80mdeep; hiddenbodytop3.18 leaves terracefloor3.20 the unique visiblematerial, avoiding coplanar materialtriangles. Both1Fporches remain exterior.
 for a,b in [(0,5.9),(10.5,16.4)]:
  body=body+box(a-.115,b+.115,1.20,8.00,0,3.18)
  body=body+yzsolid([(-.115,3.17),(4.615,3.17),(4.615,7.05),(-.115,6.208)],a-.115,b+.115)
  bx('ground_platform',a-.115,b+.115,-.115,9.615,0,.20,1)
  bx('terrace_floor_open_overhead',a-.115,b+.115,4.45,9.615,2.80,3.20,1)
  # Frontporch sourcecolumns/beam supporting overhangingupperfloor.
  for xx in [a,b]:bx('ground_porch_column',xx-.16,xx+.16,-.115,.205,.18,3.20,1)
  bx('front_porch_beam',a-.115,b+.115,-.115,.15,2.85,3.22,1)
  bx('rear_terrace_parapet_detail_priority420',a-.115,b+.115,9.40,9.615,3.18,4.20,0)
 # Centralupperstairbody follows broken roof, not fictitious full gable.
 body=body+yzsolid([(-.115,5.00),(7.06,5.00),(7.06,rear_z(7.06)-.12),(4.615,6.05),(4.615,7.05),(-.115,6.208)],5.785,10.615)
 # All roof widths controlled1663; main plane low6.20 high7.20, thin skin15cm.
 add('main_roof_620_to720',yzsolid([(-1,6.05),(4.615,7.05),(4.615,7.20),(-1,6.20)],-.115,16.515),2)
 bx('roof_vertical_step100',-.115,16.515,4.49,4.615,6.05,7.20,0)
 add('central_rear_roof_derived_end5111',yzsolid([(4.49,rear_z(4.49)-.15),(7.275,rear_z(7.275)-.15),(7.275,rear_z(7.275)),(4.49,rear_z(4.49))],5.785,10.615),2)
 for a,b in [(0,5.9),(10.5,16.4)]:
  add('rear_short_canopy140_not_full_terrace_roof',yzsolid([(4.49,rear_z(4.49)-.15),(6.015,rear_z(6.015)-.15),(6.015,rear_z(6.015)),(4.49,rear_z(4.49))],a-.115,b+.115),2)
 # Bothendterracesidewalls have actual roundholes; source10cm terracewall thickenedto23cm for1:350print;bar thickenedto.14m.
 for xx in [0,16.4]:
  wall=yzsolid([(0,0),(9.615,0),(9.615,4.20),(9.50,4.20),(4.615,6.20),(4.615,7.20),(0,6.378)],xx-.115,xx+.115)
  hole=Manifold.cylinder(.8,.75,.75,64).rotate((0,90,0)).translate((xx-.4,5.33,4.10))
  add('end_wall_with_true150cm_circle',wall-hole,0)
  bx('round_aperture_print_thickened_horizontal_bar',xx-.13,xx+.13,4.56,6.10,4.03,4.17,3)
 # Openingsare subtractive shallowrecesses; opaqueinfill isrendering/printing convention.
 def op(n,x,y,w,z0,z1,cols=2,rows=2,normal=1,mat=5):
  global body
  body=body-box(x-w/2,x+w/2,y-.30,y+.30,z0,z1)
  W.append((n,x,y,w,z0,z1,cols,rows,normal,mat))
 # Paperbottom side: closedroomfaceat1.2 forgroundwings,centralfaceat0.
 for x in [3.35,13.05]:op('W1_ground',x,1.20,2.4,1.10,2.80,4,2,-1)
 for x in [6.60,9.80]:op('W2_ground_central',x,-.115,1.4,1.10,2.80,2,2,-1)
 # Upperfourroomwindowpositions graphicalfromA2, widths/heights directA6.
 for x in [1.90,6.60,9.80,14.50]:op('W2_upper',x,-.115,1.4,4.10,5.80,2,2,-1)
 for x in [4.0,12.4]:op('W4_upper_bath',x,-.115,1.,5.20,5.80,2,1,-1)
 for x in [.50,15.90]:
  op('AC_reserved_FIXED_glass_not_equipment',x,-.115,.68,5.20,5.63,1,1,-1)
  bx('AC_reserved_external_support_graphic60',x-.44,x+.44,-.60,.02,5.06,5.20,1)
 # Paper-top terraceside doors: lowerDW1 vs upperDW1prime, not samewidth.
 for x in [3.20,13.20]:op('DW1_ground_280',x,8.00,2.80,.20,2.80,4,2,1)
 for x in [1.80,14.60]:op('DW1prime_upper_210',x,4.615,2.10,3.20,5.70,3,2,1)
 for x in [5.30,11.10]:
  op('D1_ground_entry',x,8.00,1.,.20,2.45,1,1,1,6)
  for k in range(3):bx('near_entry_graphic_short_step',x-.60,x+.60,9.50+k*.27,9.78+k*.27,0,.20-(k+1)*.045,1)
 for x in [4.35,12.05]:op('W5_upper',x,4.615,.80,4.80,5.80,1,2,1)
 for x in [.50,15.90]:op('W3_ground_kitchen',x,1.20,.70,1.20,2.20,1,2,-1)
 for x in [1.30,15.10]:op('D4_ground_kitchen',x,1.20,.90,.20,2.30,1,1,-1,6)
 for x in [6.40,10.00]:
  op('W6_central_vertical',x,7.06,.50,2.2625,4.3625,1,3,1)
  op('W7_central_lower',x,7.06,.50,1.2625,1.8625,1,1,1)
 add('enclosed_rooms_and_stair_external_envelope',body,0)
 for n,x,y,w,z0,z1,cols,rows,normal,mat in W:
  #Infill extendsinto solidbehindrecess toavoidfreeinternal shell.
  cy=y-normal*.20
  bx(n+'_infill',x-w/2-.01,x+w/2+.01,cy-.13,cy+.13,z0-.01,z1+.01,mat)
  for u in np.linspace(x-w/2,x+w/2,cols+1):bx(n+'_frame',u-.07,u+.07,y-.09,y+.09,z0,z1,3)
  zs=np.linspace(z0,z1,rows+1)
  if n.startswith(('DW1','W1_','W2_')):zs=[z0,z1-.50,z1] #A6uppertransom50,notarbitraryequaldivision
  for z in zs:bx(n+'_rail',x-w/2,x+w/2,y-.09,y+.09,z-.07,z+.07,3)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.set_tolerance(.0001).simplify(.0001).translate((-42.25,-4.55,BASE)).scale((S,S,S))
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
m=Manifold(Mesh64(v.astype(np.float32).astype(np.float64),f.astype(np.uint64),face_id=np.arange(len(f),dtype=np.uint64),tolerance=.00001)).simplify(.00001).to_mesh64();materials=materials[np.asarray(m.face_id,dtype=int)]
t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3].astype(np.float32).astype(np.float64),np.asarray(m.tri_verts),process=False);t.merge_vertices(digits_vertex=5);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'WIP_SOURCE_PLACEMENT_NOT_RELEASE','triangles':len(t.faces),'watertight':bool(t.is_watertight),'scale':'1:350','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
