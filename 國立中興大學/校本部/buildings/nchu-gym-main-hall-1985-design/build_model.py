"""NCHU main gym historical1985 revised exterior; not current condition.
Metres source geometry; exported millimetres at1:300. Roofdatum±.15m interpretation.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=1000/300
PALETTE=[('approximate pale plaster','#D8D6CA'),('approximate concrete framing','#B9BDB6'),('opaque backed glazing','#647B82'),('approximate metal roof','#AEB9BA'),('approximate skylight translucent represented opaque','#C8D8D9'),('authored display base NOTsurvey','#989F91'),('recess shadow','#49595D')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def poly(points,z0,z1):return CrossSection([points]).extrude(z1-z0).translate((0,0,z0))
def rectpoints(a,b,c,d,cut=.0):
 return [(a+cut,c),(b-cut,c),(b,c+cut),(b,d-cut),(b-cut,d),(a+cut,d),(a,d-cut),(a,c+cut)] if cut else [(a,c),(b,c),(b,d),(a,d)]
# AtGL a minimal display pad, no surrounding streets or unproven landscaping.
bx('authored_base_NOT_terrain',-6,74,-3,53.6,-.65,-.01,5)
outline=rectpoints(-.45,70.05,-.45,51.05,1.45)
body=poly(outline,-.02,18.20)
# All facade cuts and relief inserted below from floor/window schedules.
# Facadecoordinate helpers: A=y0,F=y50.6,front=x0,rear=x69.6.
# Backedrecesses preserveclosedprintenvelope; glazingopaque, nointeriorclaim.
def sb(side,n,u0,u1,d0,d1,z0,z1,mat=0):
 if side=='A':return box(u0,u1,-d1,-d0,z0,z1)
 if side=='F':return box(u0,u1,50.6+d0,50.6+d1,z0,z1)
 if side=='front':return box(-d1,-d0,u0,u1,z0,z1)
 return box(69.6+d0,69.6+d1,u0,u1,z0,z1)
def relief(side,n,u0,u1,d0,d1,z0,z1,mat=0):add(side+'_'+n,sb(side,n,u0,u1,d0,d1,z0,z1),mat)
def win(side,n,center,width,z,h,div=2,trans=True):
 global body
 a=center-width/2;b=center+width/2
 body=body-sb(side,n,a,b,-.65,.65,z,z+h)
 relief(side,n+'_opaque_glass',a,b,-.68,-.22,z,z+h,2)
 for u in np.linspace(a,b,div+1):relief(side,n+'_mullion',u-.06,u+.06,-.65,-.10,z,z+h,1)
 for zz in [z,z+h]:relief(side,n+'_rail',a-.05,b+.05,-.65,-.10,zz-.06,zz+.06,1)
 if trans:relief(side,n+'_transom',a,b,-.65,-.10,z+h/2-.05,z+h/2+.05,1)
def panel(side,n,center,width,glassz,glassh):
 global body
 a=center-width/2-.18;b=center+width/2+.18
 body=body-sb(side,n,a,b,-.35,.7,12.70,17.20)
 relief(side,n+'_solid_spandrel',a,b,-.40,-.27,12.70,17.20,0)
 for u in [a,b]:relief(side,n+'_vertical_frame',u-.07,u+.07,-.35,.10,12.65,17.25,1)
 for z in [12.70,17.20]:relief(side,n+'_horizontal_frame',a,b,-.35,.10,z-.07,z+.07,1)
 # Pane recessed independentlyinsidefullheightpanel; panelback isremovedhere.
 # Add opaqueglassjustoutboard panel toavoidfullyhidingit.
 relief(side,n+'_actual_glass',center-width/2,center+width/2,-.28,-.18,glassz,glassz+glassh,2)
 for u in [center-width/2,center,center+width/2]:relief(side,n+'_glass_mullion',u-.045,u+.045,-.2,-.12,glassz,glassz+glassh,1)
 for z in [glassz,glassz+glassh/2,glassz+glassh]:relief(side,n+'_glass_rail',center-width/2,center+width/2,-.2,-.12,z-.045,z+.045,1)
xs=[0,8]+[8+6.7*k for k in range(1,9)]+[69.6]
# Lowerfacadecontinuous insetbetweenstrongbays; sourcepostspacingretained.
for side in ['A','F']:
 for i in range(1,9):
  a,b=xs[i],xs[i+1]
  body=body-sb(side,'bay',a+.25,b-.25,-.35,.65,.02,10.8)
  relief(side,'bay_back',a+.25,b-.25,-.45,-.34,-.02,10.8,0)
  relief(side,'bay_head',a+.12,b-.12,-.35,.45,10.3,10.8,1)
  # EachupperbaythreeW3doublepane210cmhigh,notfullheightglazing.
  for k in range(3):panel(side,f'W3_{i}_{k}',a+(k+.5)*(b-a)/3,1.4333,14.90,2.10)
  if i in [1,8]:
   win(side,f'DW2_side_entry{i}',(a+b)/2,6.0,1.40,2.80,6,False)
   # solid40cmhead above240cmdoor
   relief(side,'DW2_solid_upper40',a+.35,b-.35,-.58,-.16,3.8,4.2,1)
  else:win(side,f'W4_first{i}',(a+b)/2,6.0,2.50,1.50,8,False)
  win(side,f'W4_upper{i}',(a+b)/2,6.0,7.40,1.50,8,False)
  # Basementventstrip visibleaboveGL; twosegmentsperbay, notexposedbasement.
  for k in range(2 if i in range(2,8) else 0):win(side,f'W6_7_low{i}_{k}',a+(k+.5)*(b-a)/2,2.85,.35,.80,4,False)
 for x in xs[1:-1]:relief(side,'projecting_RC_pier',x-.25,x+.25,-.43,.60,-.01,10.85,1)
# Endfacades: unequalfront/backcentralpanel, windowgroups5/7/5.
for side in ['front','rear']:
 for a,b,count,w in [(8,18,5,1.30),(18,32.6,7,1.3857),(32.6,42.6,5,1.30)]:
  for j in range(count):panel(side,f'upper{a}_{j}',a+(j+.5)*(b-a)/count,w,14.90 if side=='front' else (14.55 if a==18 else 13.65),2.10 if side=='front' else 1.50)
  if not(side=='rear' and a==18):
   width=13.9 if a==18 else 9.3
   win(side,f'wide_upper{a}',(a+b)/2,width,7.50 if side=='rear' else 7.4,.80 if side=='rear' else 1.50,14 if a==18 else 10,False)
   if side=='rear':win(side,f'W8_thirdfloor{a}',(a+b)/2,9.30,10.10,.80,14,False)
   win(side,f'wide_first{a}',(a+b)/2,width,2.5,1.50,14 if a==18 else 10,False)
   for j in range(0 if a==18 else 3):win(side,f'low{a}_{j}',a+(j+.5)*(b-a)/3,2.90,.35,.80,4,False)
  for u in [a,b]:relief(side,'end_large_pier',u-.25,u+.25,-.4,.60,-.01,11.20 if side=='rear' else 10.85,1)
  relief(side,'end_large_head',a,b,-.4,.60,10.95 if side=='rear' else 10.3,11.20 if side=='rear' else 10.8,1)
# Mainentryonlyfront. Rearcentralpanel intentionallysolid.
win('front','DW1_main_entry',25.3,12.70,1.40,3.40,14,False)
relief('front','DW1_door_transom',18.95,31.65,-.65,-.10,3.75,3.85,1)
# Canopy4.50m projection; chamfered120cmfrontedge simplifiedasclosedslab.
add('front_canopy_folded_edge',Manifold.hull_points([(x,y,z) for x,z in [(-4.5,4.95),(-4.35,4.8),(-.3,4.8),(-.3,6.0),(-4.35,6.0),(-4.5,5.85)] for y in [18.45,32.15]]),1)
# EntrylandingFF+1.4 andeight17.5cmsteps; stylizededgewidthfromA3.
bx('main_entry_landing',-1.5,.01,18.2,32.4,-.02,1.4,1)
for j in range(8):bx('main_entry_step'+str(j),-4.3+j*.35,-1.45,18.2,32.4,-.02,(j+1)*.175,1)
# Sideentranceeightsteps,nominal30cmtreads; coherent1.4rise.
for side in ['A','F']:
 for center in [(8+14.7)/2,(54.9+61.6)/2]:
  for j in range(8):relief(side,'side_entry_step',center-3,center+3,-.45,2.4-j*.30,-.02,(j+1)*.175,1)

# A8/A9 callout is GLASSBRICK, not ventilationlouvers.
# Strippositions/heights graphicestimates; width127.5cm fromadjacentW5reference.
for side,centers in [('A',[7.25,62.35]),('F',[7.25,62.35]),('front',[7.25,43.35]),('rear',[7.25,43.35])]:
 for c in centers:
  for z0,z1 in [(1.6,5.1),(5.9,8.3),(9.1,12.1),(.35,1.15)]:
   relief(side,'glassbrick_backed_strip',c-.6375,c+.6375,.43,.49,z0,z1,2)
   for u in np.linspace(c-.6375,c+.6375,7):relief(side,'glassbrick_vertical_joint',u-.03,u+.03,.47,.55,z0,z1,1)
   for z in np.arange(z0,z1+.001,.25):relief(side,'glassbrick_horizontal_joint',c-.6375,c+.6375,.47,.57,z-.03,z+.03,1)
# OutsideironmeshFW1 onlyFsideaxes3–6 basementwindows; frontshortendFW2.
for i in [2,3,4]:
 a,b=xs[i],xs[i+1]
 for k in range(2):
  c=a+(k+.5)*(b-a)/2
  for u in np.arange(c-1.425,c+1.426,.475):relief('F','FW1_authored_mesh_relief',u-.025,u+.025,-.23,-.09,.35,1.15,1)
for a,b in [(8,18),(32.6,42.6)]:
 for j in range(3):
  c=a+(j+.5)*(b-a)/3
  for u in np.arange(c-1.45,c+1.451,.48333):relief('front','FW2_authored_mesh_relief',u-.025,u+.025,-.23,-.09,.35,1.15,1)
# A12 sixteen55highx120wideACreservedholes deliberatelynotinventedasopenwindows.

add('closed_historical_envelope',body,0)
# Roofcentralpitch: 25.16m halfspan,1mrise; nominalreference21.35±.15.
yc=25.3
def roofz(y):return 21.35-abs(y-yc)/25.16
for side,(a,b) in enumerate([(.14,yc),(yc,50.46)]):
 # Solid internal backing intentionally closes inaccessiblehall volume.
 add('closed_pitched_roof_half'+str(side),Manifold.hull_points([(x,y,z) for x in [-.14,61.60] for y in [a,b] for z in [18.10,roofz(y)]]),3)
# Foldedfascia: underside18.0; RF18.2; top22.0, 65+270+65=400cm.
# Solidouterhullminusinneropening yieldsconnectedfoldedring,notflatfourmetreslab.
outer=Manifold.hull_points([(x,y,z) for inset,z in [(.65,18.0),(0,18.65),(0,21.35),(.65,22.0)] for x,y in rectpoints(-1.75+inset,71.35-inset,-1.75+inset,52.35-inset,.65)])
# Innerface is graphic envelope simplification; retain visiblefoldedouterprofile.
inner=box(-.86,70.46,-.86,51.46,18.21,22.5)
add('folded_fascia_ring_380_above_RF400_total',outer-inner,0)
bx('right_side_RC_roof_band_axes10to11',61.6,69.6,0,50.6,18.08,18.26,1)
# Four staircoreterraces explicitly shownA7 atRF ratherthan guessedmetalroof.
for x0,x1 in [(0,8),(61.6,69.6)]:
 for y0,y1 in [(0,8),(42.6,50.6)]:
  cut=box(x0+.12,x1-.12,y0+.12,y1-.12,18.2,23)
  # Remove pitchedroof fromtheseRCcornerterraces ineach previouslyaddedroofhalf.
  for k in range(len(P)):
   if LOG[k]['name'].startswith('closed_pitched_roof_half'):
    mat=LOG[k]['material'];P[k]=(P[k]-cut).as_original();IDS[P[k].original_id()]=mat
  bx('corner_RC_terrace',x0,x1,y0,y1,18.08,18.26,1)
# A7two203x340stairheads: locationgraphical±.15m, topsfollowadopted
# mainroofpitchasexplicitcoordinationinterpretation, NOTexactsourceheight.
for j,(ya,yb) in enumerate([(8.0,11.4),(39.2,42.6)]):
 xa,xb=65.4,67.43
 head=Manifold.hull_points([(x,y,z) for x in [xa,xb] for y in [ya,yb] for z in [18.18,roofz(y)]])
 add('stairhead_coordinated_roof_'+str(j),head,0)
 # D6source90x180 with13cmstep; W10 90x100, sillgraphicallyapproximate.
 doorc,windowc=(ya+.8,yb-.8) if j==0 else (yb-.8,ya+.8)
 bx('stairhead_D6_backed_wood',xa-.045,xa+.01,doorc-.45,doorc+.45,18.33,20.13,1)
 for k in range(7):bx('stairhead_D6_vertical_relief',xa-.065,xa-.035,doorc-.42+k*.14,doorc-.39+k*.14,18.33,20.13,0)
 bx('stairhead_W10_opaque',xa-.04,xa+.01,windowc-.45,windowc+.45,19.00,20.00,2)
 bx('stairhead_W10_mullion',xa-.065,xa-.025,windowc-.035,windowc+.035,19.0,20.0,1)

# Rightbandtank: A7outer720x215; A8RF+.50+.15+1.50+.15=2.30m.
# PositionC-.575..C+1.575graphicallyread±.10m; hatchadds6cm.Nointernalwaterclaim.
for x in [61.875,68.925]:bx('tank_support_end',x,x+.15,17.425,19.575,18.18,18.72,1)
bx('closed_water_tank720x215',61.875,69.075,17.425,19.575,18.70,20.50,0)
bx('tank_hatch_graphical_position',62.20,63.00,17.60,18.40,20.48,20.56,1)
# Rooflights A7 sevencolumnsbyfourrows. A23base25+louver45+dome35=105cm.
# positions: Xaxis3..9; rows symmetric±3.35,±9.65fromridge.
for i,x in enumerate([14.7+6.7*k for k in range(7)]):
 for j,y in enumerate([yc-9.65,yc-3.35,yc+3.35,yc+9.65]):
  z=roofz(y);bx(f'skylight_{i}_{j}_base25',x-.60,x+.60,y-.4175,y+.4175,z-.06,z+.25,1)
  bx(f'skylight_{i}_{j}_backed_louver45',x-.60,x+.60,y-.4175,y+.4175,z+.24,z+.70,6)
  for h in [.28,.40,.52,.64]:
   bx(f'skylight_{i}_{j}_louver_relief',x-.64,x+.64,y-.455,y+.455,z+h,z+h+.065,1)
  # Ellipsoidcap35,closedsolid; physical opaque approximation,no unsupported canopy.
  cap=Manifold.sphere(1,24).scale((.60,.4175,.35)).translate((x,y,z+.70))
  cap=cap-box(x-1,x+1,y-1,y+1,z-.5,z+.695)
  add(f'skylight_{i}_{j}_curved_dome35',cap,4)
# Thin sheet ribs simplified into shallowbroadreliefat~1.8m pitch, notliteralprofile.
for x in np.arange(8.8,61.6,1.8):
 for a,b in [(.14,yc),(yc,50.46)]:
  add('simplified_roof_rib',Manifold.hull_points([(xx,y,roofz(y)+dz) for xx in [x-.04,x+.04] for y in [a,b] for dz in [-.025,.035]]),3)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-34.8,-25.3,.65)).scale((S,S,S)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=6);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices();
if not t.is_watertight:
 counts=np.bincount(t.edges_unique_inverse);bad=t.edges_unique[counts!=2];print('BAD_EDGES',len(bad),t.vertices[bad[:30]].tolist());np.savez_compressed(R.parent/'debugmesh.npz',vertices=t.vertices,faces=t.faces)
assert t.is_watertight and t.is_winding_consistent
assert len(t.split())==1,[(len(c.faces),c.volume,c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:300','datum':'GL0 assumedlevel architecturaldatum; baseauthored','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
