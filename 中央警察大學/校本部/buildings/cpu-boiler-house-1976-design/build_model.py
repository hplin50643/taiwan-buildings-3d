"""CCCK375 November1976 boiler-house historical envelope. 1FL=0, NOTGL.
OriginalGL5/10cmconflict retained; no surveyterrain. Printscale1:75.
Roofnotch~220cm derived with±12cmdatumlimit, notstandalone source dimension.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={}
PALETTE=[('plastered wall approximate ivory','#D8D4C5'),('roof waterproof mortar approximate','#B8BBAF'),('roller steel neutral approximate','#8F9997'),('wood louver color not established','#8A8B7B'),('opaque backed vent recess','#444E50'),('authored support NOTGL','#A0A796'),('plain RC framing approximate','#C4C4B6')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
X0=-.12;X1=10.62;Y0=-.12;Y1=8.40;RF=3.50;S=1000/75
# Display support endsatfloorunderside: not reconstructedactualGL.
bx('authored_display_support_NOT_GL',-.80,12.30,-.80,10.10,-.30,-.115,5)
floor=box(X0,X1,Y0,9.40,-.12,0)+box(X1-.01,11.62,7.20,9.40,-.12,0)
add('floor_and_canopy_apron_1FL0_closed_display',floor,6)
body=box(X0,X1,Y0,Y1,-.02,3.38)
# Three350cmfrontbays,24cmcolumns; centerline divides each roller-door drawing.
for b in range(3):body=body-box(b*3.5+.12,(b+1)*3.5-.12,8.27,8.55,0,3.00)
# W1outside80x100; centers graphical beside24cmcentralcolumns.
for side,face,sgn in [('south',X0,-1),('north',X1,1)]:
 for c in [3.68,4.72]:
  a,b=sorted([face-sgn*.14,face+sgn*.08]);body=body-box(a,b,c-.40,c+.40,2.10,3.10)
# NorthD1 only; oppositewall mustnotbe arbitrarilymirrored.
body=body-box(X1-.14,X1+.08,7.35,8.25,0,2.10)
for c in [1.75,5.25,8.75]:body=body-box(c-.10,c+.10,-.20,.02,2.85,3.05)
add('closed_envelope_backed_openings',body,0)
for j in range(4):bx(f'front_RC_column24_{j}',j*3.5-.12,j*3.5+.12,8.28,8.52,-.02,3.50,6)
# Continuous50cmfrontbeam; topmatchesRFL, underside3.00.
bx('front_50cm_beam',X0,X1,8.28,8.52,3.00,3.50,6)
for b in range(3):
 lo=b*3.5+.12;hi=(b+1)*3.5-.12;c=(lo+hi)/2
 bx(f'roller_bay{b}_opaque_backing',lo,hi,8.26,8.30,-.01,3.00,2)
 # Disclosed12cmnominalslatpitch; operationarrowsarenotraiseddiagonalhardware.
 for k in range(25):bx(f'roller_bay{b}_slat{k}',lo,hi,8.29,8.34,k*.12+.025,k*.12+.080,2)
 for x in [lo,hi-.045,c-.0225]:bx(f'roller_bay{b}_edge_and_center_division',x,x+.045,8.29,8.38,-.01,3.00,6)
# Four sloped wooden-louver windows; geometrybacked forclosedprintmesh.
for side,face,sgn in [('south',X0,-1),('north',X1,1)]:
 for c in [3.68,4.72]:
  def xb(n,d0,d1,y0,y1,z0,z1,mat):
   a,b=sorted([face+sgn*d0,face+sgn*d1]);bx(f'{side}_W1_{c}_{n}',a,b,y0,y1,z0,z1,mat)
  xb('back',-.17,.005,c-.4,c+.4,2.10,3.10,4)
  for k,y in enumerate([c-.4,c+.35]):xb('jamb'+str(k),-.14,.065,y,y+.05,2.10,3.10,3)
  for k,z in enumerate([2.10,3.05]):xb('edge'+str(k),-.14,.065,c-.4,c+.4,z,z+.05,3)
  for k in range(12):
   z=2.15+k*.075
   yz=[(face-sgn*.13,z),(face+sgn*.05,z+.08),(face+sgn*.05,z+.105),(face-sgn*.13,z+.025)]
   add(f'{side}_W1_{c}_sloped_louver{k}',Manifold.hull_points([(x,y,zz) for x,zz in yz for y in [c-.36,c+.36]]),3)
# SourceD1single90x210 wooddoor; frame/detail simplifications explicit.
bx('north_D1_single_leaf',X1-.16,X1-.105,7.35,8.25,-.01,2.10,3)
for y in [7.35,8.205]:bx('north_D1_jamb',X1-.14,X1+.025,y,y+.045,-.01,2.10,3)
bx('north_D1_head',X1-.14,X1+.025,7.35,8.25,2.055,2.10,3)
# Three rear20x20 vents (A1plan+section); no inventedrearwindows.
for i,c in enumerate([1.75,5.25,8.75]):
 bx(f'rear_vent{i}_opaque_back',c-.10,c+.10,.005,.045,2.85,3.05,4)
 for x in [c-.15,c+.10]:bx(f'rear_vent{i}_frame',x,x+.05,-.14,.03,2.80,3.10,3)
 for z in [2.80,3.05]:bx(f'rear_vent{i}_edge',c-.15,c+.15,-.14,.03,z,z+.05,3)
# Exact10.74x9.52mainroof +1.00x~2.20side return. Flatdisplay simplification
# ofsource1%drainage topping; roofslab12cm and10cmupstand retained.
roof=box(X0,X1,Y0,9.40,3.38,3.50)+box(X1-.01,11.62,7.20,9.40,3.38,3.50)
add('roof_slab12cm_main1074x952_plus_return',roof,1)
outline=[(X0,Y0),(X1,Y0),(X1,7.20),(11.62,7.20),(11.62,9.40),(X0,9.40)]
for i,((a,b),(c,d)) in enumerate(zip(outline,outline[1:]+outline[:1])):
 if b==d:
  sy=1 if c>a else -1;y0,y1=sorted([b,b+sy*.10]);bx(f'roof_upstand10cm_{i}',min(a,c),max(a,c),y0,y1,3.48,3.60,0)
 else:
  sx=-1 if d>b else 1;x0,x1=sorted([a,a+sx*.10]);bx(f'roof_upstand10cm_{i}',x0,x1,min(b,d),max(b,d),3.48,3.60,0)
# Concaveupstandcorner filledinsideLfootprint toavoidline-onlycontact.
bx('roof_notch_inner_upstand_corner',10.52,10.62,7.20,7.30,3.48,3.60,0)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-5.75,-4.65,.30)).scale((S,S,S)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=12);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();assert t.is_watertight and t.is_winding_consistent;assert len(t.split())==1,[(len(c.faces),c.volume,c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:75','datum':'1FL=0, authoredsupportnotGL','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
