"""NCU science hall 1968 original design, not later observatory/current condition.
Source A2/A5/A6/A9; metres. Printable exterior interpretation at1:300.
"""
from pathlib import Path
import numpy as np,json,hashlib,trimesh
from manifold3d import Manifold,OpType
R=Path(__file__).resolve().parent
P=[];LOG=[];DARK=[]
PALETTE=[('source white aggregate exterior, neutral interpretation','#CBCAC2'),('dark glazed recess interpretation','#526265'),('authored display base','#9C9F96')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def union(ms):return Manifold.batch_boolean(ms,OpType.Add)
# Axis length18*4.5+6=87m. 100cm end dimensions refer to exterior apron, not building extension.
add('authored_display_base_not_terrain',box(-2.5,89.5,-13,44,-.45,0),2)
add('source_100cm_apron',box(-1,88,-1,17,-.01,.10))
main=box(-.225,87.225,-.10,16.10,0,11.30)
cut=[];frames=[]
# A9 each450bay: three120mm fins with992.5mm glazed widths; intermediate grid at1125mm.
xs=list(np.arange(0,40.5001,4.5))+list(np.arange(46.5,87.0001,4.5))
bays=[(float(x),4.5) for x in np.arange(0,40.5,4.5)]+[(float(x),4.5) for x in np.arange(46.5,87,4.5)]
for side in ['front','rear']:
 yy=0 if side=='front' else 16
 def ypair(front,rear):return front if side=='front' else rear
 for bi,(x,w) in enumerate(bays):
  # A5 rear outermost stair bays are predominantly opaque; retain upper small openings.
  stair=side=='rear' and (bi==0 or bi==17)
  for j in range(4):
   x0=x+j*1.125+.08;x1=x+(j+1)*1.125-.08
   for lev in range(3):
    z=.8+lev*3.5+1.0;zt=z+1.9
    if stair:
     if j not in [1,2] or lev==0:continue
     z+=.9
    y0,y1=ypair((-.12,.16),(15.84,16.12));cut.append(box(x0,x1,y0,y1,z,zt));DARK.append([x0,x1,y0,y1,z,zt])
    # Two by two panes shown A9; explicit printable120mm ->0.4mm mullions.
    ym0,ym1=ypair((-.04,.18),(15.82,16.04))
    frames.extend([box((x0+x1)/2-.06,(x0+x1)/2+.06,ym0,ym1,z,zt),box(x0,x1,ym0,ym1,(z+zt)/2-.06,(z+zt)/2+.06)])
  for j in [1,2,3]:
   xj=x+j*1.125
   add('A9_12cm_vertical_fin_'+side,box(xj-.06,xj+.06,*ypair((-.35,.12),(15.88,16.35)),0,11.30))
 for x in xs:
  add('A9_35cm_column_'+side,box(x-.175,x+.175,*ypair((-.35,.25),(15.75,16.35)),0,11.30))
# A12 AW6 end windows280x200cm, four columns/two rows. A10 AD3 door277x290,
# central pair160x215 plus75cm transom. Position uses A5 side elevation alignment.
for side in [0,87]:
 xx=(-.25,-.02) if side==0 else(87.02,87.25)
 fx=(-.23,.02) if side==0 else(86.98,87.23)
 for z in [5.3,8.8]:
  cut.append(box(*xx,8.1,10.9,z,z+2));DARK.append([*xx,8.1,10.9,z,z+2])
  for yy in [8.8,9.5,10.2]:add('A12_AW6_end_window_vertical_mullion',box(*fx,yy-.06,yy+.06,z,z+2))
  add('A12_AW6_end_window_horizontal_mullion',box(*fx,8.1,10.9,z+.94,z+1.06))
 cut.append(box(*xx,8.115,10.885,.8,3.70));DARK.append([*xx,8.115,10.885,.8,3.70])
 for yy in [8.7,9.5,10.3]:add('A10_AD3_end_door_leaf_and_sideframe',box(*fx,yy-.06,yy+.06,.8,2.95 if yy==9.5 else 3.70))
 add('A10_AD3_end_door_transom',box(*fx,8.115,10.885,2.89,3.01))
 # A2/A5 short external stair; five rises chosen to span80cm, run1.50m scaled reading.
 for i in range(5):
  x0,x1=(-1.725+i*.30,-.20) if side==0 else(87.20,88.725-i*.30)
  add('A5_end_entry_steps_scaled_run1p5m_five_rises',box(x0,x1,8.1,10.9,0,(i+1)*.16))
# Central entrance and stair feature, not a fabricated open tunnel.
cut.extend([box(40.675,46.325,-.12,.4,.8,3.70),box(40.8,46.2,15.6,16.12,.8,3.25)])
DARK.extend([[40.675,46.325,-.12,.4,.8,3.70],[40.8,46.2,15.6,16.12,.8,3.25]])
for xx in [41.6375,42.6,43.5,44.4,45.3625]:add('A10_AD1_front_door_leaves_and_fixed_sidelights',box(xx-.06,xx+.06,-.04,.42,.8,3.7 if xx in [42.6,44.4] else 2.95))
add('A10_AD1_75cm_transom',box(40.675,46.325,-.04,.42,2.89,3.01))
# A5 central stair bay is not a typical A9 450cm bay: front two bands,
# rear single offset band; extents and five120cm intervals are elevation readings.
for side,bands,yp,fp in [('front',[(5.3,7.2),(8.8,10.7)],(-.12,.18),(-.04,.20)),('rear',[(7.7,8.9)],(15.82,16.12),(15.80,16.04))]:
 for z,zt in bands:
  cut.append(box(40.675,46.325,*yp,z,zt));DARK.append([40.675,46.325,*yp,z,zt])
  for xx in [41.1,42.3,43.5,44.7,45.9]:add('A5_central_'+side+'_scaled_window_vertical_frame',box(xx-.045,xx+.045,*fp,z,zt))
  if side=='front':add('A5_central_front_scaled_window_midrail',box(40.675,46.325,*fp,(z+zt)/2-.06,(z+zt)/2+.06))
  add('A5_central_'+side+'_window_sill_no_ground_door_crossing',box(40.675,46.325,*((-0.40,.2) if side=='front' else (15.8,16.4)),z-.10,z))
# A5/A12 end elevation facing joints; shallow0.2mm print engraving, not structural openings.
for xx in [(-.24,-.18),(87.18,87.24)]:
 for yy in np.linspace(0,16,13)[1:-1]:cut.append(box(*xx,yy-.03,yy+.03,.12,11.28))
main=main-union(cut)
add('main_exterior_solid_backing_no_interior_claim',main)
for m in frames:add('A9_printable_window_cross_mullion',m)
# 190cm windows and 100cm sills controlled by A6. Continuous slab/sill edges remain visible.
for y0,y1 in [(-.40,.10),(15.90,16.40)]:
 for z in [.8+1,.8+3.5+1,.8+7+1]:
  for x0,x1 in [(-.20,40.5),(46.5,87.20)]:add('A6_projected_sill_edge_excluding_central_bay',box(x0,x1,y0,y1,z-.10,z))
add('roof_slab',box(-.4,87.4,-.4,16.4,11.15,11.30))
for a,b,c,d in [(-.4,87.4,-.4,-.25),(-.4,87.4,16.25,16.4),(-.4,-.25,-.4,16.4),(87.25,87.4,-.4,16.4)]:add('A5_100cm_roof_parapet',box(a,b,c,d,11.29,12.30))
# Center stair facade fins at600cm bay (five intervals), differing from450cm bays.
for x in np.linspace(40.5,46.5,6):
 add('A5_central_front_fins_from4p3',box(x-.06,x+.06,-.36,.1,4.3,11.3))
 add('A5_central_rear_fins_from6p4',box(x-.06,x+.06,15.9,16.36,6.4,11.3))
# A4 600x554cm plan control; A7 roof210+35+25=270cm above mainroof.
tower=box(40.5,46.5,10.46,16.0,11.29,14.00)
tower=tower-box(43.0,44.0,10.44,10.65,11.30,13.4)
tower=tower-box(40.7,46.3,15.82,16.02,13.40,13.75)
add('A4_A7_roof_stair_6x5p54_height_2p70m',tower)
DARK.append([43,44,10.44,10.65,11.3,13.4])
DARK.append([40.7,46.3,15.82,16.02,13.40,13.75])
for xx in [41.1,41.6,42.1,42.6,43.1,43.6,44.1,44.6,45.1,45.6,46.1]:add('glassbrick_band_aggregated_relief_not_actual_block_size',box(xx-.045,xx+.045,15.90,16.03,13.4,13.75))
add('roof_stair_cap',box(40.35,46.65,10.31,16.15,13.75,14.00))
# A13 detailed entrance supersedes schematic A2 projection:11m wall to lowest step,
# 180cm run and70cm rise above10cm apron. 600cm tread width;100/400/100 are substructure dashed supports.
add('A13_entrance_platform_10cm_slab',box(40.5,46.5,-9.2,0,.70,.8))
add('A13_central_400cm_compacted_fill',box(41.5,45.5,-9.2,0,0,.71))
add('A13_lowest_apron',box(40.5,46.5,-11.1,-9.15,0,.1))
for i in range(5):add('A13_entry_14cm_riser_45cm_run',box(40.5,46.5,-11+i*.45,-9.15,0,.10+(i+1)*.14))
# Attached stepped lecture room: A3 external datum 10+910+25+110=1055cm over sharedGL.
# Detailed A8 interior steps are intentionally not fabricated inside solid-backed exterior.
hall=box(34.5,52.5,22,42,0,9.20)
# A8 recurring85/115cm plan with50cm inset.15cm skin is below print thickness and represented by solid exterior.
for i in range(10):
 y=22+2*i
 hall=hall-box(34.48,35.0,y+.175,y+1.025,0.10,9.20)
 hall=hall-box(52.0,52.52,y+.175,y+1.025,0.10,9.20)
# Front elevation A4: upper6m glazed banks, low flanking windows and central connection.
hc=[]
for z,h in [(1.90,.80),(4.10,1.60),(6.95,1.60)]:
 for a,b in ([(34.775,40.225),(46.775,52.225)] if z>6 else [(34.775,39.115),(47.885,52.225)]):
  hc.append(box(a,b,21.97,22.22,z,z+h));DARK.append([a,b,21.97,22.22,z,z+h])
for a,b in [(40.775,46.225)]:
 hc.append(box(a,b,21.97,22.22,6.95,8.55));DARK.append([a,b,21.97,22.22,6.95,8.55])
# A3 back elevation has TWO low side doors; scaled1.05x2.10m, not an all-solid rear.
for a,b in [(35.25,36.30),(50.70,51.75)]:
 hc.append(box(a,b,41.80,42.03,.10,2.20));DARK.append([a,b,41.80,42.03,.10,2.20])
# Staggered facing joints shown on back elevation, engraved0.2mm at1:300 for visibility.
for zz in [2.375,4.65,6.925]:hc.append(box(34.51,52.49,41.94,42.03,zz-.03,zz+.03))
for row in range(4):
 for xx in np.arange(34.5+(0 if row%2==0 else .6),52.5,1.2):
  if xx>34.55:hc.append(box(xx-.03,xx+.03,41.94,42.03,.1+row*2.275,.1+(row+1)*2.275))
add('A3_A8_stepped_lecture_hall_closed_exterior',hall-union(hc))
# Flat roof and110cm parapet, separate from910cm wall/25cm band.
add('A3_lecture_hall_25cm_roof_band',box(34.35,52.65,21.85,42.15,9.20,9.45))
for a,b,c,d in [(34.35,52.65,21.85,22.0),(34.35,52.65,42,42.15),(34.35,34.50,21.85,42.15),(52.5,52.65,21.85,42.15)]:add('A3_lecture_hall_110cm_parapet',box(a,b,c,d,9.44,10.55))
# A5 three roof fans at3,9,15m across hall and2m from connecting bridge end.
for x in [37.5,43.5,49.5]:
 add('A5_vent_80cm_plinth',box(x-.4,x+.4,23.6,24.4,9.44,9.74))
 add('A5_vent_neck',Manifold.cylinder(.35,.31,.31,32).translate((x,24,9.73)))
 add('A5_vent_cap_profile',Manifold.cylinder(.25,.48,.38,32).translate((x,24,10.05)))
 add('A5_vent_taper',Manifold.cylinder(.51,.38,.24,32).translate((x,24,10.29)))
# A8 bridge:600cm clear distance between blocks,600cm width; neutral solid-backed thin-frame sides; material not evidenced,
# GL+.10+3.00 floor3.10; external3.10+top.30 yields6.50. Inner313 vs outer310 remains3cm discrepancy.
# Lower beam edge2.75 is drawing-scaled estimate (+/-5cm), not explicit dimension.
bridge=box(40.5,46.5,15.95,22.05,2.75,6.50)
bridgecuts=[]
for x0,x1 in [(40.48,40.70),(46.30,46.52)]:
 bridgecuts.append(box(x0,x1,16.15,21.85,4.10,5.95))
add('A8_bridge_90cm_wall_10cm_cap_neutral_upper_screen',bridge-union(bridgecuts))
for x0,x1 in [(40.50,40.73),(46.27,46.50)]:
 for yy in np.linspace(16.15,21.85,7):add('A8_bridge_neutral_frame_not_glass_claim',box(x0,x1,yy-.06,yy+.06,4.1,5.95))
# Source-defined mullions on attached hall facade, enlarged120mm for printable relief.
for z,h in [(1.90,.80),(4.10,1.60),(6.95,1.60)]:
 for a,b in ([(34.775,40.225),(46.775,52.225),(40.775,46.225)] if z>6 else [(34.775,39.115),(47.885,52.225)]):
  for x in np.linspace(a,b,11 if z>6 else 9)[1:-1]:add('hall_facade_print_mullion',box(x-.06,x+.06,22.05,22.24,z,z+h))
  if h>1:add('hall_facade_horizontal_mid_mullion',box(a,b,22.05,22.24,z+h/2-.06,z+h/2+.06))
solid=union(P).simplify(1e-7).translate((-43.5,-18,.45)).scale((10/3,10/3,10/3))
m=solid.to_mesh64();t=trimesh.Trimesh(np.array(m.vert_properties[:,:3]),np.array(m.tri_verts),process=True)
assert t.is_watertight and t.is_winding_consistent and len(t.split(only_watertight=False))==1
assert (t.area_faces>0).all()
cent=t.triangles_center/(10/3)+np.array([43.5,18,-.45]);mat=np.zeros(len(t.faces),int);mat[cent[:,2]<0]=2
for a,b,c,d,e,f in DARK:
 hit=(cent[:,0]>=a-.001)&(cent[:,0]<=b+.001)&(cent[:,1]>=c-.001)&(cent[:,1]<=d+.001)&(cent[:,2]>=e-.001)&(cent[:,2]<=f+.001);mat[hit]=1
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat);t.export(R/'model.stl')
(R/'components.json').write_text(json.dumps(LOG,indent=2));(R/'palette.json').write_text(json.dumps(PALETTE));q={'status':'PASS_GEOMETRY','triangles':len(t.faces),'watertight':True,'winding':True,'components':1,'scale':'1:300','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'bounds_mm':t.bounds.tolist()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(q)
