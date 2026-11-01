"""NCTU Guangfu North Gate, undated original design. Not current/as-built.
Metres local A1/A2 coordinates; approximate terrain, A3-digitized curved wall.
Detailed roof and linear chains govern; source angle/fill conflicts documented.
"""
from pathlib import Path
import numpy as np,trimesh,json,hashlib
from manifold3d import Manifold,CrossSection,Mesh64
from shapely.geometry import LineString,Polygon
from scipy.interpolate import PchipInterpolator,CubicHermiteSpline
R=Path(__file__).resolve().parent;P=[];LOG=[];IDS={}
PALETTE=[('approximate yellow Italian marble','#DDD0A3'),('approximate Kinmen granite','#AEB1A2'),('opaque backed glazing','#4D6971'),('neutral aluminum frame','#C8C9BE'),('authored approximate terrain','#A9ACA2'),('roof cover height475 not exact soil layer','#8C8D76'),('substitute old name patinated bronze','#3C5749')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def poly(q,z0,z1):
 if Polygon(q).exterior.is_ccw is False:q=q[::-1]
 return CrossSection([q]).extrude(z1-z0).translate((0,0,z0))
def add(n,m,mat=0):
 assert not m.is_empty(),n
 m=m.as_original();IDS[m.original_id()]=mat;P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
def bx(n,a,b,c,d,e,f,mat=0):add(n,box(a,b,c,d,e,f),mat)
def linewall(n,a,b,w,z0,z1,mat=0):
 a=np.array(a);b=np.array(b);d=b-a;nn=np.array([-d[1],d[0]])/np.linalg.norm(d)*w/2
 add(n,poly([tuple(a+nn),tuple(b+nn),tuple(b-nn),tuple(a-nn)],z0,z1),mat)
# A3 grid-derived centerline. A1 context placement is graphically scaled, not a site survey.
c=np.array(json.loads((R/'CURVE-DIGITIZATION.json').read_text())['local_xy_m']);arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(c,axis=0),axis=1))];ss=np.linspace(0,arc[-1],140);ix=PchipInterpolator(arc,c[:,0]);iy=PchipInterpolator(arc,c[:,1]);dx=ix.derivative()(arc);dy=iy.derivative()(arc);dx[-1]=np.cos(np.deg2rad(56));dy[-1]=np.sin(np.deg2rad(56));cc=np.c_[CubicHermiteSpline(arc,c[:,0],dx)(ss),CubicHermiteSpline(arc,c[:,1],dy)(ss)];raw=np.c_[ix(ss),iy(ss)];smoothing_shift=float(np.max(np.linalg.norm(cc-raw,axis=1)));assert smoothing_shift<.03;cc+=np.array([21.1,-25.1]);tangent=np.array([np.cos(np.deg2rad(56)),np.sin(np.deg2rad(56))]);ext=cc[-1]+np.linspace(.2,19.3,80)[:,None]*tangent;path=np.vstack([cc,ext]);wallline=LineString(path)
# Surface only interpolates local source elevation controls; the cropped display base is authored.
def grade(x,y):
 z=float(np.interp(y,[-25.1,-2.6,float(path[-1,1])],[1.25,2.4,4.25]))
 if -8<=x<=10 and -6<=y<=4.4:z=min(z,2.4)
 return z
xs=np.linspace(-10,34,23);ys=np.linspace(-28,17,24);v=[]
for y in ys:
 for x in xs:v.append([x,y,grade(x,y)])
nx=len(xs);ny=len(ys);f=[]
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;f.extend([[a,a+1,a+nx+1],[a,a+nx+1,a+nx]])
edge=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range(ny*nx-2,(ny-1)*nx-1,-1))+[j*nx for j in range(ny-2,0,-1)]
base=[]
for k in edge:base.append(len(v));v.append([v[k][0],v[k][1],-.5])
for i,a in enumerate(edge):j=(i+1)%len(edge);f.extend([[a,base[i],base[j]],[a,base[j],edge[j]]])
bc=len(v);v.append([12,-5.5,-.5])
for i in range(len(base)):f.append([bc,base[(i+1)%len(base)],base[i]])
t=trimesh.Trimesh(v,f,process=True);t.fix_normals();assert t.is_watertight
add('authored_coarse_interpolated_sloping_terrain',Manifold(Mesh64(np.array(t.vertices,dtype=np.float64,order='C'),np.array(t.faces,dtype=np.uint64,order='C'))),4)
# Wall lower parts merge into terrain; constant EL490 top preserves changing visible wall height.
wallpoly=wallline.buffer(.125,cap_style=2,join_style=1);add('A3_digitized_25cm_name_wall_top_EL490',poly(list(wallpoly.exterior.coords)[:-1],.6,4.90),0)
# Tower blade, detailed A3: 15.00m above EL240, not above lowest road.
bx('tower_320cm_plan_55cm_estimated_thickness',-.475,.075,-4.2,-1.0,2.35,17.40,0)
bx('tower_terrace_at_EL240',-1.1,.8,-4.65,-.55,1.8,2.40,1)
# Thin seams on the blade: graphical cladding pattern, not exact fabrication layout.
for yy in [-4.2,-3.4,-2.6,-1.8,-1.0]:bx('tower_long_face_vertical_joint',-.486,-.469,yy-.008,yy+.008,2.40,17.40,1)
for zz in np.arange(3.4,17.4,1.0):bx('tower_long_face_horizontal_joint',-.486,-.469,-4.2,-1.0,zz-.008,zz+.008,1)
# Guardroom footprint governed by dimension chains, not contradictory printed67degrees.
q=[(0,0),(4.65,0),(7.60,3.90),(0,3.90)];qp=Polygon(q)
add('guardroom_closed_exterior_backing',poly(q,2.35,4.51),1)
add('roof_structural_slab_EL450_465',poly(list(qp.buffer(.08,join_style=2).exterior.coords)[:-1],4.50,4.65),1)
add('roof_surface_EL475_direct_label_10cm_cover',poly(q,4.64,4.75),5)
linewall('front_high_parapet_EL520',(0,0),(4.65,0),.25,4.60,5.20,0)
linewall('west_side_parapet_EL495',(0,0),(0,3.90),.20,4.60,4.95,0)
linewall('east_side_parapet_EL495',(4.65,0),(7.60,3.90),.25,4.60,4.95,1)
# Back adjoins hillside in section; no invented raised north parapet.
# Source forecourt wall and left angled retaining strip, cropped to detailed-plan extent.
add('guard_forecourt_EL240',poly([(-2.8,0),(0,0),(0,3.9)],1.8,2.40),1)
linewall('west_forecourt_low_wall_EL465',(-2.8,0),(0,0),.25,1.25,4.65,0)
linewall('existing_wall_interface_shown_extent',(-6.39,-5.0),(0,3.9),.25,1.1,4.90,0)
# A2 front face W2, west W1/W3, diagonal W4 and P1. Opaque backing disclosed.
def facade_rect(n,a,b,z0,z1,mat=2,frame=True,middle=True):
 a=np.array(a);b=np.array(b);d=b-a;u=d/np.linalg.norm(d);normal=np.array([u[1],-u[0]])
 linewall(n,a,b,.12,z0,z1,mat)
 if frame:
  for p in [a,b]:linewall(n+'_jamb',p-normal*.07,p+normal*.07,.08,z0-.04,z1+.04,3)
  for z in [z0,z1]:linewall(n+'_head_sill',a,b,.16,z-.04,z+.04,3)
  mid=(a+b)/2
  if middle:linewall(n+'_middle_mullion',mid-normal*.07,mid+normal*.07,.06,z0,z1,3)
facade_rect('W1_100x120',(-.035,1.58),(-.035,.58),3.30,4.50)
facade_rect('W3_60x50',(-.035,3.30),(-.035,2.70),3.40,3.90)
facade_rect('W2_120x50',(2.70,-.035),(3.90,-.035),3.75,4.25)
a=np.array([4.65,0.]);b=np.array([7.60,3.90]);u=(b-a)/np.linalg.norm(b-a);normal=np.array([u[1],-u[0]])
center=a+u*.62+normal*.035;facade_rect('P1_100x210',center-u*.50,center+u*.50,2.40,4.50,2,middle=False)
linewall('P1_horizontal_transom_at_90cm',center-u*.50,center+u*.50,.16,3.27,3.33,3)
# Circular W4 disc/ring axis is perpendicular to the oblique east wall.
center=a+u*2.60-normal*.08
# A local cylinder Z-axis maps to the wall-normal horizontal axis.
def disk(rad,depth,loc,mat,name):
 m=Manifold.cylinder(depth,rad,rad,64).rotate((90,0,0)).rotate((0,0,np.rad2deg(np.arctan2(normal[1],normal[0]))+90)).translate(tuple(loc));add(name,m,mat)
disk(.50,.14,[*center,3.90],2,'W4_diameter100_backed_round_window')
ring=Manifold.cylinder(.17,.55,.55,64)-Manifold.cylinder(.20,.47,.47,64).translate((0,0,-.01));ring=ring.rotate((90,0,0)).rotate((0,0,np.rad2deg(np.arctan2(normal[1],normal[0]))+90)).translate((*center,3.90));add('W4_print_thickened_ring',ring,3)
linewall('W4_vertical_mullion',center-normal*.02,center+normal*.17,.065,3.36,4.44,3)
# Substitute-font historical name, placed at the low end and read right-to-left.
ld=np.load(R/'letter_meshes.npz');cum=np.r_[0,np.cumsum(np.linalg.norm(np.diff(path,axis=0),axis=1))]
for i,ch in enumerate('國立交通大學'):
 s=1.6+i*1.20;idx=np.searchsorted(cum,s)-1;tt=(s-cum[idx])/(cum[idx+1]-cum[idx]);pt=path[idx]*(1-tt)+path[idx+1]*tt;uu=(path[idx+1]-path[idx]);uu/=np.linalg.norm(uu);nn=np.array([-uu[1],uu[0]])
 # Front is road-side, left of ascending wall; local horizontal reversed for unmirrored lettering.
 uu=-uu;vv=ld[f'v{i}'].copy();vv3=np.c_[pt[0]+uu[0]*vv[:,0]+nn[0]*(vv[:,2]+.11),pt[1]+uu[1]*vv[:,0]+nn[1]*(vv[:,2]+.11),3.35+vv[:,1]]
 tm=trimesh.Trimesh(vv3,ld[f'f{i}'],process=True);tm.fix_normals();add('substitute_historical_letter_'+ch,Manifold(Mesh64(np.array(tm.vertices,dtype=np.float64,order='C'),np.array(tm.faces,dtype=np.uint64,order='C'))),6)
solid=P[0]
for p in P[1:]:solid=solid+p
solid=solid.translate((-12,5.5,.5)).scale((5,5,5)).simplify(.0001);m=solid.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);materials=np.zeros(len(f),dtype=int)
for i,oid in enumerate(m.run_original_id):materials[m.run_index[i]//3:m.run_index[i+1]//3]=IDS[int(oid)]
t=trimesh.Trimesh(v,f,process=False);t.merge_vertices(digits_vertex=10);assert len(t.faces)==len(f);assert t.is_watertight and t.is_winding_consistent;print('COMPONENTS',[(len(x.faces),x.bounds.tolist()) for x in t.split()]);assert len(t.split())==1,(len(t.split()),'detached geometry')
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=materials);t.export(R/'model.stl');(R/'palette.json').write_text(json.dumps(PALETTE));(R/'components.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2));(R/'WALL-PATH.json').write_text(json.dumps({'sampled_path_m':path.tolist(),'terminal_tangent_smoothing_max_shift_m':smoothing_shift,'terminal_smoothing_method':'Final Hermite interval derivative aligned56deg; sampled deviation under3cm from PCHIP, within graphical interpretation; not original CAD','arc_length_m':float(cum[-1]),'terrain_method':'Coarse interpolation, not surveyed original terrain','placement_estimate':'A1 scaled relative tower plan, not cadastral placement'},indent=2))
q={'status':'PASS_GEOMETRY_ONLY','triangles':len(t.faces),'components':len(t.split()),'watertight':bool(t.is_watertight),'winding':bool(t.is_winding_consistent),'scale':'1:200','bounds_mm':t.bounds.tolist(),'mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest()};(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(json.dumps(q))
