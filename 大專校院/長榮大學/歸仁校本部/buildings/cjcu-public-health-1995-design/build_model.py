"""CJCU Public Health College1995 historical design exterior. Not as built.
Source metres -> millimetres at1:400. Original scans remain private.
Window relief is opaque backed fabrication interpretation, not full interiors.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib,math
from manifold3d import Manifold,CrossSection
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={};S=2.5
PALETTE=[('approximate pale tile plaster','#D6D1C4'),('approximate concrete stone trim','#B5B8AF'),('opaque glazing representation','#5E7B84'),('approximate waterproof roof','#8A9390'),('opaque glass cover representation','#A9C8CC'),('authored display base NOT terrain','#959E90'),('recess shadow','#394E56')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def poly(points,z0,z1):
 if sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))<0:points=list(reversed(points))
 return CrossSection([points]).extrude(z1-z0).translate((0,0,z0))
def rp(a,b,c,d):return [(a,c),(b,c),(b,d),(a,d)]
def mass(n,a,b,c,d,h):bx(n,a,b,c,d,-.05,h)
def rim(n,a,b,c,d,z,h=1.3,t=.22):add(n,poly(rp(a,b,c,d),z-.08,z+h)-poly(rp(a+t,b-t,c+t,d-t),z-.15,z+h+.1),0)
# Source axes1..18 x0..108.8 and A..Q y0..76.8.
# Small exterior wall offsets .20m taken as representational wall thickness.
bx('display_pad_not_surveyed_terrain',-7.0,114.5,-5,81.8,-.8,-.015,5)
# Main U shaped7F: lower gallery enclosure retained as backed facade.
mass('main_west_spine7F',25.4,41.8,12.6,64.2,29.04)
mass('main_south_bar7F',31.8,83.4,3.0,19.4,29.04)
mass('main_north_bar7F',31.8,83.4,57.4,73.8,29.04)
# Four stair/service towers are unequal byplan, not detached sheet insets.
for a,b,c,d,n in [(25.4,32.2,-.2,12.95,'SW'),(25.4,32.2,63.85,77.0,'NW'),(83,89.8,6.2,13.15,'SE'),(83,89.8,63.65,70.6,'NE')]:
 mass(n+'_stair_tower',a,b,c,d,35.65)
 for z in [5.46,9.6,13.56,17.52,21.48,25.26,29.04,31.7,35.3]:bx(n+'_floor_trim',a-.08,b+.08,c-.08,d+.08,z-.13,z+.03,1)
# Lower east five-storey wing; recessed I-axis atrium betweentwo rooms.
mass('east_north_classrooms5F',83.0,109.0,44.6,55.4,21.48)
mass('east_south_classrooms5F',83.0,109.0,21.4,32.2,21.48)
mass('east_gallery5F',76.6,83.5,19.0,57.8,21.48)
mass('east_atrium_backed_envelope',83.0,105.9,32,44.8,21.48)
# West phaseII four floor wings and link passages, not same1F datum.
for c,d,n in [(-.2,13.0,'SW'),(63.8,77,'NW')]:mass(n+'_phaseII_low_wing',6.2,25.7,c,d,17.52);rim(n+'_low_parapet',6.2,25.7,c,d,17.52)
for c,d,n in [(6.2,12.9,'S'),(63.9,70.6,'N')]:mass(n+'_west_stair',-.2,6.5,c,d,17.52);rim(n+'_west_stair_parapet',-.2,6.5,c,d,17.52)
# Lightwell boxesare voids in actual building; narrow linking galleriesalong edges.
for c,d,n in [(12.7,17.6,'S'),(59.2,64.1,'N')]:mass(n+'_low_link',-.1,25.7,c,d,17.52)
for c,d,n in [(19.2,25.6,'S'),(51.2,57.6,'N')]:mass(n+'_low_side_link',-.2,6.55,c,d,17.52)
# Auditorium steppedroof polygon replaced below by source-digitalized outlines.
# Initial trace from A8-13 grid, curvedwestprofile polyline ratherthan circular assumption.
curve=[(-.1,27.2),(-.85,30),(-1.45,33),(-1.75,36),(-1.85,38.4),(-1.75,41),(-1.45,44),(-.85,47),(-.1,49.6)]
aud0=[[-0.432, 49.94], [5.976, 50.318], [5.976, 52.561], [12.41, 52.964], [12.664, 49.764], [6.154, 46.035], [6.154, 30.715], [12.614, 26.835], [12.41, 23.786], [5.976, 24.214], [5.976, 26.431], [-0.432, 26.86], [-0.915, 28.926], [-1.348, 31.194], [-1.729, 33.587], [-1.984, 35.981], [-2.085, 38.4], [-1.984, 40.769], [-1.729, 43.162], [-1.348, 45.556], [-0.915, 47.824]]
aud1=[(6.05,30.65),(12.85,26.65),(12.85,50.15),(6.05,46.1)]
aud2=[(12.6,26.8),(19.4,26.4),(19.4,50.4),(12.6,50)]
aud3=[(19.2,26.4),(25.7,26),(25.7,50.8),(19.2,50.4)]
for i,(pts,z) in enumerate(zip([aud0,aud1,aud2,aud3],[25.62,21.365,19.665,17.965])):
 if i==0:
  add(f'auditorium_stepped_volume_{i}',poly(pts,-.04,z),0)
  add(f'auditorium_roof_{i}',poly(pts,z-.09,z+.02),3)
 else:
  from shapely.geometry import Polygon,box as sbox
  add(f'auditorium_stepped_volume_{i}',poly(pts,-.04,z-.35),0)
  for low,high in [(0,38.4),(38.4,80)]:
   shape=Polygon(pts).intersection(sbox(-10,low,120,high));coords=list(shape.exterior.coords)[:-1]
   add(f'auditorium_drainage_1in50_{i}',Manifold.hull_points([(x,y,zz) for x,y in coords for zz in [z-.37,z-abs(y-38.4)/50]]),3)
# Small flankingserviceheads A8-13top+22.02.
for c,d in [(23.5,26.5),(50.3,53.3)]:mass('auditorium_side_service_head',12.5,19.5,c,d,22.02)
# Courtyardwestfoyer projection: shallowfacetedcurve sourceestimated, roof5FL+17.52.
foyer=[(41.4,25.6),(44.8,27.2),(46.2,30),(47.3,34),(47.7,38.4),(47.3,42.8),(46.2,46.8),(44.8,49.6),(41.4,51.2)]
add('courtyard_west_projecting_foyer',poly(foyer,-.04,17.52),0)
# Facade helpers: u horizontal alongglobal x ory; vout positiveoutward.
def slab(axis,at,sign,u0,u1,d0,d1,z0,z1):
 lo,hi=sorted([at+sign*d0,at+sign*d1])
 return box(u0,u1,lo,hi,z0,z1) if axis=='y' else box(lo,hi,u0,u1,z0,z1)
def rel(n,axis,at,sign,a,b,d0,d1,z0,z1,mat=0):add(n,slab(axis,at,sign,a,b,d0,d1,z0,z1),mat)
def window(n,axis,at,sign,u,w,z,h,panes=2):
 a,b=u-w/2,u+w/2
 rel(n+'_opaque_backed_glazing',axis,at,sign,a,b,-.08,.035,z,z+h,2)
 for x in np.linspace(a,b,panes+1):rel(n+'_frame',axis,at,sign,x-.045,x+.045,-.07,.13,z,z+h,1)
 for zz in [z,z+h*.7,z+h]:rel(n+'_rail',axis,at,sign,a-.04,b+.04,-.07,.135,zz-.045,zz+.045,1)
 # actual minimum relief~.34mm at1:400, not asserted printable allprocesses.
def narrowrow(n,axis,at,sign,a,b,z,count):
 for j in range(count):window(n+str(j),axis,at,sign,a+(j+.5)*(b-a)/count,.85,z,1.94,1)
# Main north/south 15bayswidewindow and30 upperwindows.
levels=[.96,5.46,9.6,13.56,17.52,21.48,25.26]
for side,at,sgn in [('south',3.0,-1),('north',73.8,1)]:
 for fl,z in enumerate(levels[:5]):
  for j in range(15):
   u=35.2+(j+.5)*3.2
   window(f'{side}_F{fl+1}_AW3_{j}', 'y',at,sgn,u,2.43,z+.78,1.36,4)
   window(f'{side}_F{fl+1}_AW4_{j}', 'y',at,sgn,u,2.43,z+2.25,.56,4)
 for z in levels[5:]:narrowrow(side+'_upperAW16','y',at,sgn,35.2,83.2,z+.80,30)
 for x in np.arange(35.2,83.21,3.2):rel(side+'_projecting_pier','y',at,sgn,x-.18,x+.18,-.1,.95,.8,21.15,1)
 for z in levels[1:6]:rel(side+'_floorband','y',at,sgn,35,83.4,-.08,.27,z-.28,z+.03,1)
 # roofsetbackparapet30.34; no invented continuous3.2m deepglass.
 rel(side+'_roof_parapet','y',at,sgn,32.1,83.4,-.05,.22,29.0,30.34)
 # Basement windows only visible narrowstrip, not underground rooms.
 for j in range(15):window(side+'_lowvent'+str(j),'y',at,sgn,35.2+(j+.5)*3.2,2.30,.12,.55,4)
# Westlowwing exteriornorth/south horizontalwindows fourfloorpattern.
for n,at,sgn in [('low_south',-.2,-1),('low_north',77,1)]:
 for fl,z in enumerate([.60,5.10,9.24,13.38]):
  for j in range(6):window(n+str(fl)+str(j),'y',at,sgn,6.4+(j+.5)*3.2,2.43,z+.85,1.92,4)
 for u in np.arange(6.4,25.7,3.2):rel(n+'_pier','y',at,sgn,u-.18,u+.18,-.07,.7,.4,17.4,1)
# Eastelevationmostlysolid exceptslenderverticalfenestration,glassspineandrelief fins.
for fl,z in enumerate(levels[:5]):
 for u in [34.4,35.4,41.4,42.4]:window('east_slit'+str(fl)+str(u),'x',105.9,1,u,.42,z+.85,2.10,1)
 for u in [23.2,53.6]:
  if fl==4:window('east_top_square'+str(u),'x',109,1,u,2.20,z+1.0,2.0,1)
for u in [27.2,28.5,29.8,47.0,48.3,49.6]:rel('east_tall_vertical_recess','x',109,1,u-.38,u+.38,-.05,.04,2.0,22.25,6)
for u in [27.2,28.5,29.8,47.0,48.3,49.6]:
 for du in [-.45,.45]:rel('east_fins','x',109,1,u+du-.07,u+du+.07,-.1,.5,1.9,22.4,1)
# East side classroombanks, fivelevels;5Fsmallerband ratherthanblindclone.
for n,at,sgn in [('east_northside',55.4,1),('east_southside',21.4,-1)]:
 for fl,z in enumerate(levels[:5]):
  for j in range(8):window(n+str(fl)+str(j),'y',at,sgn,83.2+(j+.5)*3.2,2.43,z+(1.8 if fl==4 else .85),(.95 if fl==4 else 1.92),4)
 for u in np.arange(83.2,109,3.2):rel(n+'_pier','y',at,sgn,u-.18,u+.18,-.08,.75,.8,22.3,1)
 rim(n+'_roofparapet',82.98,109.02,44.58 if sgn==1 else 21.38,55.42 if sgn==1 else 32.22,21.48,1.10)
# Towerssparseverticalwindows onlongsides;smallpanelsavoidall-glass falseheads.
for a,b,c,d,n in [(25.4,32.2,-.2,12.95,'SW'),(25.4,32.2,63.85,77,'NW'),(83,89.8,6.2,13.15,'SE'),(83,89.8,63.65,70.6,'NE')]:
 for fl,z in enumerate(levels):
  positions=[(84.49,.43),(85.11,.43)] if n=='SE' else [(a+1.9,.85),(b-1.65,.43)]
  for u,w in positions:window(n+'_stair'+str(fl)+str(u),'y',c if 'S'in n else d,-1 if 'S'in n else 1,u,w,z+.9,1.42,1)
  if n=='SE':
   rel('SE_AW10prime_100x30_backed'+str(fl),'y',c,-1,84.3,85.3,-.05,.08,z+2.8,z+3.1,6)
   for h in [2.84,2.92,3.00,3.08]:rel('SE_AW10prime_louver'+str(fl),'y',c,-1,84.3,85.3,-.03,.15,z+h,z+h+.025,1)
# Courtyardfacades: doubleheightgroundarcade, upperglazed gallery, 6/7Fwindows.
def archsection(width,spring,rise):
 r=width/2;return [(-r,0),(r,0),(r,spring)]+[(r*math.cos(t),spring+rise*math.sin(t)) for t in np.linspace(0,math.pi,20)][1:]+[(-r,0)]
def archsolid(axis,at,sgn,u,width,z,spring,rise,depth):
 # CrossSection local(x,z) extrudedlocal-y thenrotate90 aboutX.
 m=CrossSection([archsection(width,spring,rise)]).extrude(depth).rotate((90,0,0))
 if axis=='y':return m.translate((u,at+(depth if sgn==1 else 0),z))
 return m.rotate((0,0,90)).translate((at-(depth if sgn==-1 else 0),u,z))
for n,axis,at,sgn,a,b,count in [('court_south','y',19.4,1,41.6,76.8,6),('court_north','y',57.4,-1,41.6,76.8,6),('court_east','x',76.6,-1,19.2,57.6,6)]:
 for j in range(count):
  u=a+(j+.5)*(b-a)/count
  # backed archedrecess, no unseenfullinterior claim.
  add(n+'_arched_shadow',archsolid(axis,at,sgn,u,4.65,.96,5.5,2.15,.07),6)
  for du in [-2.55,2.55]:rel(n+'_arcade_pier',axis,at,sgn,u+du-.20,u+du+.20,-.08,.45,.80,8.3,1)
  # Crown outline ring in2D, relief only.
  ring=archsolid(axis,at,sgn,u,5.1,.8,5.65,2.35,.30)-archsolid(axis,at-.01*sgn,sgn,u,4.65,.80,5.65,2.13,.4)
  if not ring.is_empty():add(n+'_arch_trim',ring,1)
 for fl,z in enumerate([9.60,13.56,17.52]):
  for j in range(count*2):window(n+'_gallery'+str(fl)+str(j),axis,at,sgn,a+(j+.5)*(b-a)/(count*2),2.55,z+.35,3.10,2)
 if axis=='y':
  for z in levels[5:]:narrowrow(n+'_AW16',axis,at,sgn,a,b,z+.80,22)
  rel(n+'_upper_parapet',axis,at,sgn,a,b,-.05,.22,29.0,30.34)
# Westspineupperrowsvisibleaboveauditoriumandcourtyard.
for axis,at,sgn,n in [('x',25.4,-1,'westspine'),('x',41.8,1,'courtwest')]:
 for z in levels[5:]:narrowrow(n+'_AW16',axis,at,sgn,13.1,63.7,z+.8,32)
 rel(n+'_parapet',axis,at,sgn,12.8,64,-.06,.22,29.0,30.34)
# Westlowfacade fourfloor slits andsourcebigarchedmainentry.
for c,d in [(6.4,12.8),(64,70.4)]:
 for z in [.6,5.1,9.24,13.38]:
  for u in np.linspace(c+1,d-1,4):window('westlow_slit','x',-.2,-1,u,.45,z+.75,2.8,1)
# Curvedwestauditoriumfrontentry atmidpoint; opaque backedarch avoids fictitious through tunnel.
# A4-13supplement:opening580wide,ground+.30,top11.30;innerheadstep11.66;outerdecorativeprofilesimplifiedtoit,notexactmaximum.
add('west_main_arched_entry',archsolid('x',-1.80,-1,38.4,5.90,.25,8.1,2.95,.45),2)
entryframe=archsolid('x',-1.90,-1,38.4,6.52,.30,8.1,3.26,1.30)-archsolid('x',-1.80,-1,38.4,5.8,.29,8.11,2.9,1.60)
add('west_A4_13_arch_projecting_frame',entryframe,1)
# Headerat655datum andfineverticalglazingframe: actualimprintedacrylicscreenrepresentedopaque.
rel('west_entry_transom655','x',-2.24,-1,35.5,41.3,-.05,.12,6.49,6.61,1)
for u in [36.35,37.35,38.4,39.45,40.45]:rel('west_entry_vertical_glazing_bar','x',-2.24,-1,u-.045,u+.045,-.04,.12,.30,8.4,1)
# Entrance2x15cmsteps;ovaloutlinegraphicapproximation,notR1250wallclaim.
for rx,ry,z in [(3.2,6.4,.15),(2.95,6.15,.30)]:
 pts=[(-3.2+rx*math.cos(t),38.4+ry*math.sin(t)) for t in np.linspace(0,2*math.pi,64,endpoint=False)]
 add('west_entrance_step',poly(pts,-.04,z),1)
# A8-13 digitizedwesternedgeinterpolation: keepwindowsonthecurve,notburied.
westedge=sorted([p for p in aud0 if p[0]<0],key=lambda p:p[1])
def westx(y):return float(np.interp(y,[p[1] for p in westedge],[p[0] for p in westedge]))
for u in [28,29.6,31.2,32.8,34.4,42.4,44,45.6,47.2,48.8]:window('west_foyer_slit','x',westx(u)-.04,-1,u,.65,.65,5.6,1)
# Tile horizontalbands followthefacetedcurve ratherthancuttingthroughit.
for z in [5.10,9.24,13.38,17.52,18.82,25.4]:
 for (x1,y1),(x2,y2) in zip(westedge[:-1],westedge[1:]):
  add('west_curved_facade_band',poly([(x1-.13,y1),(x2-.13,y2),(x2+.10,y2),(x1+.10,y1)],z-.12,z+.03),1)
# Main courtyardwestprojectingfoyer: glazedverticalscreen andsidearchedportals.
for (x1,y1),(x2,y2) in zip(foyer[:-1],foyer[1:]):
 add('west_courtyard_foyer_glass',poly([(x1-.07,y1),(x2-.07,y2),(x2+.045,y2),(x1+.045,y1)],.96,13.25),2)
 for frac in np.linspace(0,1,4):
  x=x1+(x2-x1)*frac;y=y1+(y2-y1)*frac
  bx('foyer_vertical_frame',x-.12,x+.17,y-.07,y+.07,.90,17.3,1)
 for z in [5.46,9.6,13.56,17.4]:
  add('foyer_curved_horizontal_frame',poly([(x1-.1,y1),(x2-.1,y2),(x2+.20,y2),(x1+.20,y1)],z-.15,z+.04),1)
for u in [23.5,53.3]:add('courtyard_west_side_arch',archsolid('x',41.8,1,u,3.0,.96,5.5,1.5,.14),6)
# Roofcorridorstrips: actualmono-pitch opaqueforms3; notprotectiontriangles.
def wedge(n,a,b,c,d,zlow,zhigh,highaxis,highsign):
 def zz(x,y):
  t=(x-a)/(b-a) if highaxis=='x' else(y-c)/(d-c)
  return zlow+(zhigh-zlow)*(t if highsign==1 else 1-t)
 pts=[(x,y,z) for x,y in [(a,c),(b,c),(b,d),(a,d)] for z in [29.02,zz(x,y)]]
 add(n+'_opaque_mass',Manifold.hull_points(pts),0)
 roofpts=[(x,y,zz(x,y)+dz) for x,y in [(a,c),(b,c),(b,d),(a,d)] for dz in [-.10,.015]]
 add(n+'_waterproof_roof',Manifold.hull_points(roofpts),3)
for n,c,d,sgn in [('south',10.35,13.90,-1),('north',62.90,66.45,1)]:
 wedge(n+'_roof_corridor',50.4,76.8,c,d,30.65,32,'y',sgn)
 for i in range(12):
  u=50.4+(i+.5)*2.2
  window(n+'_AW19roof','y',d if sgn==1 else c,sgn,u,1.65,29.65,1.70,2)
  window(n+'_AW20roof','y',c if sgn==1 else d,-sgn,u,1.65,29.65,.60,2)
wedge('west_roof_corridor',31.83,35.37,25.2,51.6,30.65,32,'x',1)
for i in range(12):
 u=25.2+(i+.5)*2.2;window('west_AW19roof','x',35.37,1,u,1.65,29.65,1.70,2);window('west_AW20roof','x',31.83,-1,u,1.65,29.65,.60,2)
# EastI-axis narrowglassgable atopRF21.48 +170support+100rise.
bx('east_glass_support',86.27,106.53,37.4,39.4,21.40,23.18,0)
add('east_glass_gable',Manifold.hull_points([(x,y,z) for x in [86.27,106.53] for y,z in [(37.4,23.15),(39.4,23.15),(38.4,24.18)]]+[(107.53,38.4,23.15),(107.53,38.4,24.18)]),4)
for x in np.arange(86.4,106.53,.8):
 for a,b in [((37.4,23.18),(38.4,24.18)),((38.4,24.18),(39.4,23.18))]:add('glass_gable_rib',Manifold.hull_points([(xx,y,z+dz) for xx in [x-.035,x+.035] for y,z in [a,b] for dz in [-.02,.045]]),1)
# A4-10:14prime86.4;17prime105.6+80cmgrid+113cmtip=107.53.
# Shoulderouterframe93cm=>106.53, distinctfrom106.40centerline.
tippts=[(105.80,37.4),(106.53,37.4),(107.53,38.4),(106.53,39.4),(105.80,39.4)]
add('east_triangular_glass_front_backed',poly(tippts,-.04,23.18),4)
for a,b in [((106.53,37.4),(107.53,38.4)),((107.53,38.4),(106.53,39.4))]:
 x1,y1=a;x2,y2=b
 for f in [0,.5,1]:
  x=x1+(x2-x1)*f;y=y1+(y2-y1)*f;bx('east_glass_front_vertical_frame',x-.06,x+.08,y-.06,y+.06,.96,24.18-abs(y-38.4),1)
 for z in np.arange(.96,23.18,1.32):add('east_glass_front_horizontal_frame',poly([(x1-.06,y1),(x2-.06,y2),(x2+.08,y2),(x1+.08,y1)],z-.04,z+.04),1)
# Clock tower plan450cmchamferedsquare centered~X13.56/I; exactA8-25sectiondatumpreference.
ct=[(79.7, 36.15), (83.2, 36.15), (83.7, 36.65), (83.7, 40.15), (83.2, 40.65), (79.7, 40.65), (79.2, 40.15), (79.2, 36.65)]
add('clock_lower_machine_room',poly(ct,21.4,25.66),0)
add('clock_upper_body',poly(ct,25.6,30.16),0)
add('clock_pyramid_roof',Manifold.hull_points([(x,y,30.12) for x,y in ct]+[(81.45,38.4,32.54)]),1)
# Stylized clockdialandhandsbasedspecifieddesign,notclaimactualmechanisminstalled.
for at,sgn in [(79.2,-1),(83.7,1)]:
 window('clock_face_frame','x',at,sgn,38.4,3,26.96,3,1)
 disc=Manifold.cylinder(.10,1.0,1.0,48).rotate((0,90,0)).translate((at-.01 if sgn==1 else at-.09,38.4,28.46));add('clock_face_disc',disc,0)
 rel('clock_vertical_hand','x',at,sgn,38.35,38.45,.08,.17,28.46,29.1,6)
 rel('clock_horizontal_hand','x',at,sgn,37.75,38.45,.08,.17,28.41,28.51,6)
# roofheadsminimalcapandchosenlightningrods(notcoveragecones);thickened.16m->.4mm.
for x,y in [(25.6,12.8),(25.6,64),(83.2,12.8),(83.2,64)]:add('lightning_rod_design_thickened',Manifold.cylinder(2.06,.08,.08,12).translate((x,y,35.59)),1)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-54.4,-38.4,.8)).scale((S,S,S)).simplify(.0001)
m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=6);keep=t.nondegenerate_faces();materials=materials[keep];t.update_faces(keep);t.remove_unreferenced_vertices()
if not t.is_watertight:np.savez_compressed(R.parent/'debugmesh.npz',vertices=t.vertices,faces=t.faces)
assert t.is_watertight and t.is_winding_consistent
assert len(t.split())==1,[(len(c.faces),c.volume,c.bounds.tolist()) for c in t.split()]
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:400','datum':'GL0 architecturaldatum; authoredpad notterrain','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
