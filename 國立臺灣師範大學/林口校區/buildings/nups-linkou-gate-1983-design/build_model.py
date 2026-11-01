"""NUPS main gate, May1983 original-design reconstruction. A5 section controlsheight, not asbuilt/current. Metres."""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold,CrossSection,Mesh64,FillRule
R=Path(__file__).resolve().parent
P=[];LOG=[]
PALETTE=[('neutral wall','#CBC8BC'),('neutral walking surface','#B4B6B2'),('opaque glazing','#526C74'),('neutral frame','#DEDCD0'),('authored display base','#96958D'),('recess','#37464B')]
def box(a,b,c,d,e,f):
 assert b>a and d>c and f>e
 return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def along_x(q,x0,x1):
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(q,q[1:]+q[:1]))<0:q=q[::-1]
 m=CrossSection([q]).extrude(x1-x0).to_mesh64();v=np.asarray(m.vert_properties)[:,:3];v=v[:,[2,0,1]];v[:,0]+=x0
 return Manifold(Mesh64(np.array(v,dtype=np.float64,order="C",copy=True),np.array(m.tri_verts,dtype=np.uint64,order="C",copy=True)))

# A2/A3 overall37.15x13.15;A5 detailedsectionGLroof9.95m.
bx('authored_display_base',-2,39.15,-2,15.15,-.50,-.04,4)
bx('local_grade',-1.5,38.65,-1.5,14.65,-.06,0,4)
# Roof edge shape:45cmupper/lowerchamfers,12cmslab,60cmcofferbeams.
q=[(0,8.10),(.45,7.65),(12.70,7.65),(13.15,8.10),(13.15,9.50),(12.70,9.95),(.45,9.95),(0,9.50)]
outer=along_x(q,0,37.15)
qx=[(0,8.10),(.45,7.65),(36.70,7.65),(37.15,8.10),(37.15,9.50),(36.70,9.95),(.45,9.95),(0,9.50)]
# Rotate second prism toclipendchamfers, q uses negative x forpositive rotatedx.
qneg=[(-x,z) for x,z in qx]
outer=outer ^ along_x(qneg,0,13.15).rotate((0,0,90))
# Coherent slabwithopenparapetabove; inside20cmwall offset simplified atcorners.
roof=outer-box(.65,36.50,.65,12.50,8.37,10.20)
# Cut8x24coffers frombelow; ribs25cm / clear125cm.
for i in range(24):
 for j in range(8):
  x=.70+1.5*i;y=.70+1.5*j
  roof=roof-box(x,x+1.25,y,y+1.25,7.5,8.25)
add('large_coffer_roof_with_chamfered_fascia',roof,0)
# A2 8columns, xaxes5.825/10.325/26.825/31.325, y2.825/10.325.
for x in [5.825,10.325,26.825,31.325]:
 for y in [2.825,10.325]:
  col=box(x-.5,x+.5,y-.5,y+.5,-.02,7.68)
  for ya,yb in [(y-.51,y-.425),(y+.425,y+.51)]:col=col-box(x-.075,x+.075,ya,yb,-.03,7.7)
  for xa,xb in [(x-.51,x-.425),(x+.425,x+.51)]:col=col-box(xa,xb,y-.075,y+.075,-.03,7.7)
  add('one_metre_column_four_15cm_flutes',col)
  bx('column_capital_150cm',x-.75,x+.75,y-.75,y+.75,7.39,8.27)
# A2 independentroomgroups,7.50x4.50grid; interiorsnotyetWIPmodeled.
for xa,xb in [(2.825,11.075),(26.075,34.325)]:
 room=box(xa,xb,4.325,8.825,0,3.50)
 # A4 road-facingwideflattenedarch:363cmclear,50cmroundedcorners.
 yc=6.575;y0=yc-1.815;y1=yc+1.815
 q=[(y0,.15),(y1,.15),(y1,2.25)]
 for a in np.linspace(0,np.pi/2,17)[1:]:q.append((y1-.5+.5*np.cos(a),2.25+.5*np.sin(a)))
 q.append((y0+.5,2.75))
 for a in np.linspace(np.pi/2,np.pi,17)[1:]:q.append((y0+.5+.5*np.cos(a),2.25+.5*np.sin(a)))
 room=room-along_x(q,xb-.45,xb+.05) if xa<10 else room-along_x(q,xa-.05,xa+.45)
 add('doorhouse_shell_with_road_facing_flattened_arch',room,1)

# Derivedneutralbrickcolour: interpretivedisplay, not fieldcolourmeasurement.
PALETTE[1]=('source brick interpretation','#A87963')
def cyl_y(r,y0,y1,x,z):return Manifold.cylinder(y1-y0,r,r,64).rotate((90,0,0)).translate((x,y1,z))
def arch_void(x,y0,y1,width,top):
 r=width/2;spring=top-r
 return box(x-r,x+r,y0,y1,-.1,spring)+cyl_y(r,y0,y1,x,spring)
def plane_window(n,xa,xb,y,z0,z1,cols=3):
 bx(n,xa,xb,y-.025,y+.025,z0,z1,2)
 for xx in np.linspace(xa,xb,cols+1):bx(n+'_frame',xx-.025,xx+.025,y-.05,y+.05,z0,z1,3)
 for zz in [z0,z1,z1-.50]:bx(n+'_horizontal',xa,xb,y-.05,y+.05,zz-.025,zz+.025,3)
for xc in [8.075,29.075]:
 # HistoricalcirclefrontW4, glazed/backednotthroughroom.
 add('W4_round_opaque_glazing',cyl_y(.75,4.28,4.34,xc,2.0),2)
 add('W4_round_frame',cyl_y(.84,4.25,4.35,xc,2.0)-cyl_y(.75,4.20,4.40,xc,2.0),3)
 plane_window('rear_room_W1',xc-1.5,xc+1.5,8.85,.15,2.75)
 # Narrowcolourjointreliefnotindividuallyinventedbrickdimensions.
 for zz in np.arange(.20,3.35,.24):
  add('brick_course_relief_front',box(xc-2.20,xc+2.20,4.29,4.335,zz,zz+.012)-cyl_y(.85,4.20,4.4,xc,2.0),1)
 # Emblem-bearingpanels betweenfrontcolumns; sketchsimplificationpendingA6.
 bx('front_emblem_panel',xc-2.0,xc+2.0,2.65,3.0,3.48,7.45,0)
 bx('front_emblem_square_frame',xc-1.40,xc+1.40,2.56,2.68,4.25,7.05,3)
 bx('front_emblem_square_inset',xc-1.15,xc+1.15,2.52,2.60,4.50,6.80,0)
 # RearA4 blankpanelwithhorizontalbands,notfrontglobe.
 bx('rear_upper_panel',xc-2.0,xc+2.0,10.15,10.50,3.48,7.45,0)
 for z in [4.25,5.55,6.85]:bx('rear_horizontal_relief',xc-1.40,xc+1.40,10.48,10.56,z,z+.25,3)
for xc in [12.20,24.95]:
 add('arched_pedestrian_portal',box(xc-1.24,xc+1.24,6.30,6.85,0,3.50)-arch_void(xc,6.20,6.95,1.265,2.75),1)
 # Sourcegateleaftemporarilyrepresentedbythinframenotfilledsolid.
 for xx in [xc-.59,xc,xc+.59]:bx('pedestrian_leaf_vertical',xx-.025,xx+.025,6.53,6.60,0,2.05,3)
 bx('pedestrian_leaf_bottom',xc-.615,xc+.615,6.53,6.60,0,.06,3)
 bx('pedestrian_leaf_spring',xc-.615,xc+.615,6.53,6.60,2.00,2.07,3)
# Localfencecutends: authoredextent, not entire380m boundary.
for xa,xb in [(-1.0,2.825),(34.325,38.15)]:bx('truncated_225cm_boundary_wall',xa,xb,6.46,6.69,-.02,2.25,1)

# A4 sidearchedframe overlays45cm recessedD1/W3 wall(A2plan).
for xp,sgn in [(10.625,1),(26.525,-1)]:
 bx('road_side_recessed_wall',xp-.04,xp+.04,4.555,8.595,.15,3.25,1)
 for name,ya,yb,z0,z1 in [('D1',7.48,8.48,.15,2.75),('W3',4.66,6.16,1.05,2.75)]:
  xx=xp+sgn*.05
  bx(name+'_backed_panel',xx-.025,xx+.025,ya,yb,z0,z1,2)
  for yy in [ya,yb,(ya+yb)/2]:bx(name+'_frame_vertical',xx-.05,xx+.05,yy-.025,yy+.025,z0,z1,3)
  for zz in [z0,z1,z1-.50]:bx(name+'_frame_horizontal',xx-.05,xx+.05,ya,yb,zz-.025,zz+.025,3)

# A6 globe outline, simplifiedmeridians; centralhands/plumdetailomitted.
for xc in [8.075,29.075]:
 zc=5.65
 ring=cyl_y(1.15,2.47,2.56,xc,zc)-cyl_y(1.10,2.43,2.59,xc,zc)
 add('simplified_emblem_outer_globe',ring,3)
 # Ellipticalmeridianscutfromannuli, not inventedgeographicalcontinents.
 for fac in [.35,.68]:
  rr=(Manifold.cylinder(.09,1.15,1.15,64)-Manifold.cylinder(.11,1.10,1.10,64).translate((0,0,-.01))).scale((fac,1,1)).rotate((90,0,0)).translate((xc,2.56,zc))
  add('simplified_emblem_meridian',rr,3)
 bx('emblem_equator',xc-1.10,xc+1.10,2.46,2.56,zc-.025,zc+.025,3)
 for dz in [-.57,.57]:
  width=(1.1**2-dz**2)**.5;bx('simplified_emblem_latitude',xc-width,xc+width,2.46,2.56,zc+dz-.025,zc+dz+.025,3)
# A10 loweruncancelledplan:10.5mvehicleleaf2mhighat+0.10.
for zz in [.10,1.10,2.10]:bx('vehicle_gate_horizontal',13.30,23.85,6.53,6.61,zz-.035,zz+.035,3)
for xx in np.linspace(13.325,23.825,11):bx('vehicle_gate_cell_divider',xx-.035,xx+.035,6.53,6.61,.10,2.10,3)
for j in range(10):
 xc=13.85+1.05*j
 for radius in [.18,.28,.38]:
  # TopU opensupwards; bottomU opensdownwards, 3nestedmotifspercell.
  for zc,up in [(1.62,False),(.58,True)]:
   ann=cyl_y(radius,6.52,6.62,xc,zc)-cyl_y(radius-.035,6.49,6.65,xc,zc)
   clip=box(xc-.5,xc+.5,6.48,6.66,zc if up else zc-.5,zc+.5 if up else zc)
   add('source_nested_U_curve',ann^clip,3)
   for xx in [xc-radius+.0175,xc+radius-.0175]:
    bx('source_nested_U_leg',xx-.0175,xx+.0175,6.52,6.62,.10 if up else zc,zc if up else 2.10,3)
# A2 source-sideW2highwindow; sourcefullglassW1rearalreadyabove.
for xa,sgn in [(2.825,-1),(34.325,1)]:
 bx('outer_side_high_W2',xa-.045,xa+.045,4.44,8.71,2.25,2.75,2)
 for yy in np.linspace(4.44,8.71,9):bx('W2_frame',xa-.07,xa+.07,yy-.025,yy+.025,2.25,2.75,3)
 for zz in [2.25,2.75]:bx('W2_horizontal',xa-.07,xa+.07,4.44,8.71,zz-.025,zz+.025,3)
# A2 historicalright-to-lefttext;A6 saysfontseparatelyspecified.
# NotoSansCJKTC outlines are interpretivetext,not originalcalligraphy.
PALETTE.append(('interpretive gilt lettering','#B9A86A'))
letters=json.loads((R/'letter-contours.json').read_text())
for i,ch in enumerate(reversed('國立僑生大學先修班')):
 shape=CrossSection(letters[ch],FillRule.NonZero).extrude(.065).rotate((90,0,0)).translate((13.175+i*1.25,.025,8.40))
 add('historical_name_interpretive_font_'+ch,shape,6)
for xx in [12.50,24.65]:bx('name_side_bar',xx-.06,xx+.06,-.04,.04,8.30,9.30,6)
# Unifiedmesh exportWIP in1:150mm.
solid=P[0]
for part in P[1:]:solid=solid+part
solid=solid.simplify(1e-7).translate((-18.575,-6.575,.5)).scale((1000/150,)*3)
m=solid.to_mesh64();vp=np.asarray(m.vert_properties);tri=np.asarray(m.tri_verts)
verts,inv=np.unique(np.round(vp[:,:3],5),axis=0,return_inverse=True);faces=inv[tri];mat=np.zeros(len(faces),dtype=int)
valid=(faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2])
areas=np.linalg.norm(np.cross(verts[faces[:,1]]-verts[faces[:,0]],verts[faces[:,2]]-verts[faces[:,0]]),axis=1)
valid &= areas>0
print('removed_numeric_zero_area',int((~valid).sum()),flush=True)
faces=faces[valid];mat=mat[valid]
# Conform numeric collinear seam edges after 0.00001mm coordinate snapping.
for iteration in range(5):
 t=trimesh.Trimesh(verts,faces,process=False)
 if t.is_watertight:break
 edges=np.sort(t.edges,axis=1);ue,c=np.unique(edges,axis=0,return_counts=True);bad=ue[c==1]
 print('seam_iteration',iteration,'boundary',len(bad),'nonmanifold',int((c>2).sum()),flush=True)
 candidates=np.unique(bad);splits={}
 for a,b in bad:
  av,bv=verts[a],verts[b];v=bv-av;den=v@v
  if den<1e-14:continue
  ts=(verts[candidates]-av)@v/den
  dist=np.linalg.norm(verts[candidates]-(av+ts[:,None]*v),axis=1)
  pick=(ts>1e-6)&(ts<1-1e-6)&(dist<1.1e-5)
  ids=candidates[pick][np.argsort(ts[pick])]
  if len(ids):splits[(int(a),int(b))]=ids.tolist()
 if not splits:break
 newfaces=[];newmat=[];vv=verts.tolist()
 for f,ma in zip(faces,mat):
  polygon=[];changed=False
  for a,b in zip(f,np.roll(f,-1)):
   polygon.append(int(a));ids=splits.get(tuple(sorted((int(a),int(b)))),[])
   if ids:
    changed=True;polygon.extend(ids if a<b else ids[::-1])
  if changed:
   center=len(vv);vv.append(np.mean(verts[f],axis=0).tolist())
   for a,b in zip(polygon,polygon[1:]+polygon[:1]):newfaces.append([a,b,center]);newmat.append(ma)
  else:newfaces.append(f.tolist());newmat.append(ma)
 verts=np.asarray(vv);faces=np.asarray(newfaces);mat=np.asarray(newmat)
t=trimesh.Trimesh(verts,faces,process=False)
print('watertight',t.is_watertight,'winding',t.is_winding_consistent,flush=True)

assert t.is_watertight and t.is_winding_consistent
cent=t.triangles_center/(1000/150)+np.array([18.575,6.575,-.5]);mat=np.zeros(len(t.faces),dtype=int)
for a in LOG:
 lo=np.array(a['bounds_m'][:3]);hi=np.array(a['bounds_m'][3:]);inside=((cent>=lo-1e-4)&(cent<=hi+1e-4)).all(axis=1);surface=np.minimum(abs(cent-lo),abs(cent-hi)).min(axis=1)<1e-4;mat[inside&surface]=a['material']
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat)
t.export(R/'model.stl');(R/'components.json').write_text(json.dumps(LOG,indent=2));(R/'palette.json').write_text(json.dumps(PALETTE))
q={'status':'PASS_GEOMETRY','triangles':len(t.faces),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'components':len(t.split()),'scale':'1:150','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(q,flush=True)
