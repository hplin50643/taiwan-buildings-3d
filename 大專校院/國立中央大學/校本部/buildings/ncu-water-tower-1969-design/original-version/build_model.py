"""NCU 1969 design water tower. T1 controls 366 cm inner diameter; T2 says 360.
Metres -> millimetres at 1:100. Not an as-built/current-site model.
"""
from pathlib import Path
import json,hashlib,numpy as np,trimesh
from manifold3d import Manifold
R=Path(__file__).resolve().parent
P=[];LOG=[]
PALETTE=[('neutral concrete interpretation','#C7C5BB'),('authored display base','#96988F'),('neutral access cover','#666D6C')]
def box(a,b,c,d,e,f):return Manifold.cube((b-a,d-c,f-e)).translate((a,c,e))
def cyl(r,z0,z1):return Manifold.cylinder(z1-z0,r,r,128).translate((0,0,z0))
def ring(r0,r1,z0,z1):return cyl(r1,z0,z1)-cyl(r0,z0-.01,z1+.01)
def add(n,m,mat=0):
 assert not m.is_empty(),n
 P.append(m);LOG.append({'name':n,'material':mat,'bounds_m':list(m.bounding_box())})
add('authored_display_base_not_terrain',cyl(3.2,-.25,0),1)
# T1 clear inside radius1.83; shell10cm, upper ribs35cm to2.18.
for i in range(16):
 a=22.5*i
 add('C1_20x50_radial_support_%02d'%i,box(1.68,2.18,-.10,.10,-.02,11.22).rotate((0,0,a)))
 add('C2_20x35_tank_rib_%02d'%i,box(1.83,2.18,-.10,.10,11.0,17.20).rotate((0,0,a)))
 # Top15cm setback before B1 ring; axis lies20cm outside tank inside face.
 add('C2_upper_neck_%02d'%i,box(1.83,2.03,-.10,.10,17.19,17.37).rotate((0,0,a)))
# B4 rings use straight chords between radial supports, not invented circular beams.
for z in [2.75,5.50,8.25]:
 for i in range(16):
  a=np.deg2rad((i+.5)*22.5);rr=1.93*np.cos(np.deg2rad(11.25));half=1.93*np.sin(np.deg2rad(11.25))+.04
  add('B4_40x20_chord_ring',box(rr-.20,rr+.20,-half,half,z-.20,z).rotate((0,0,np.rad2deg(a))))
add('tank_bottom_20cm',cyl(1.94,11.00,11.20))
add('tank_10cm_wall',ring(1.83,1.93,11.19,17.75))
add('B2_25x50_bottom_ring',ring(1.68,1.93,11.00,11.50))
add('B1_35x50_top_ring',ring(1.83,2.18,17.35,17.85))
# Roof10cm slab, opening70cm with10cm curb. Closed display lid, not functional hatch.
hole=cyl(.35,17.6,18.1).translate((1.23,0,0))
add('roof_slab_with_70cm_access',cyl(2.18,17.75,17.85)-hole)
add('outer_roof_10cm_raised_rim',ring(2.08,2.18,17.84,17.95))
add('access_10cm_raised_curb',ring(.35,.45,17.84,17.95).translate((1.23,0,0)))
add('closed_access_cover_print_thickness_25mm',cyl(.45,17.95,17.975).translate((1.23,0,0)),2)
# Access rungs are depicted in T1; display simplified as rung array on inside tower.
# Omit hidden tank ladder and reinforcing steel; do not invent external services.
for z in np.arange(2.90,10.9,.40):
 add('lower_access_rung_simplified',box(1.62,1.69,-.40,.40,z,z+.025).rotate((0,0,11.25)),2)
# Each rung touches C1 at angle0; rung projection is source-derived10cm embed/80cm bar,
# 80cm bar span; rectangularized cross-section for printable contact. No fictitious continuous ladder rails.
# T1 1/A1 return pipe: 20cm outside roof edge /30cm inside, +/-90cm.
# Nominal1inch -> explicit 0.8mm printed diameter at1:100 (80mm design equivalent).
def rod(a,b,r=.04):
 a=np.array(a);b=np.array(b);d=b-a;L=np.linalg.norm(d);theta=np.degrees(np.arccos(d[2]/L));phi=np.degrees(np.arctan2(d[1],d[0]));return Manifold.cylinder(L,r,r,24).rotate((0,theta,phi)).translate(tuple(a))
path=[(0,1.88,17.74),(0,1.88,18.65)]
for a in np.linspace(0,np.pi/2,9)[1:]:path.append((0,1.98-.10*np.cos(a),18.65+.10*np.sin(a)))
path.append((0,2.28,18.75))
for a in np.linspace(np.pi/2,0,9)[1:]:path.append((0,2.28+.10*np.cos(a),18.65+.10*np.sin(a)))
path.append((0,2.38,17.05))
for a in np.linspace(0,-np.pi/2,9)[1:]:path.append((0,2.28+.10*np.cos(a),17.05+.10*np.sin(a)))
path.append((0,2.02,16.95))
pipe=rod(path[0],path[1])
for a,b in zip(path[1:-1],path[2:]):pipe=pipe+rod(a,b)
for q in path[1:-1]:pipe=pipe+Manifold.sphere(.04,16).translate(q)
add('T1_return_pipe_explicit_print_diameter_0p8mm',pipe,2)
add('nonarchitectural_solid_print_core_inside_closed_tank',cyl(1.835,11.19,17.85)+cyl(.36,17.84,17.96).translate((1.23,0,0)))
solid=Manifold.batch_boolean(P, __import__('manifold3d').OpType.Add)
solid=solid.simplify(1e-7).translate((0,0,.25)).scale((10,10,10))
m=solid.to_mesh64();verts=np.array(m.vert_properties[:,:3]);faces=np.array(m.tri_verts)
t=trimesh.Trimesh(verts,faces,process=True)
assert t.is_watertight and t.is_winding_consistent and (t.area_faces>0).all()
assert len(t.split(only_watertight=False))==1
mat=np.zeros(len(t.faces),dtype=int);cent=t.triangles_center/10-np.array([0,0,.25])
mat[cent[:,2]<0]=1;mat[cent[:,2]>17.95]=2
np.savez_compressed(R/'mesh.npz',vertices=t.vertices,faces=t.faces,materials=mat)
t.export(R/'model.stl');(R/'components.json').write_text(json.dumps(LOG,indent=2));(R/'palette.json').write_text(json.dumps(PALETTE))
q={'status':'PASS_GEOMETRY','triangles':len(t.faces),'watertight':True,'winding':True,'components':1,'scale':'1:100','mesh_sha256':hashlib.sha256((R/'mesh.npz').read_bytes()).hexdigest(),'bounds_mm':t.bounds.tolist()}
(R/'BUILD-QA.json').write_text(json.dumps(q,indent=2));print(q)
