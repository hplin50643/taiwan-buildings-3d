#!/usr/bin/env python3
"""1981 drawing-based NCKU stand exterior; approximate HP shell, not as-built survey."""
from pathlib import Path
import json,math,zipfile,xml.etree.ElementTree as ET
import numpy as np,trimesh,manifold3d as mf
ROOT=Path(__file__).resolve().parent;SCALE=5
PALETTE=[{'id':a,'name':b,'hex':c,'evidence':d} for a,b,c,d in [('brick','Brick tile exterior','#A5644F','Original elevations specify terracotta tiles; official campus panorama corroborates illustrative hue'),('concrete','Concrete and washed-stone trim','#C5C1AC','Original elevations annotate exposed concrete / white washed stone; approximate material hue'),('metal','Pale railing metal','#DDDCD3','Original detail drawings; illustrative light finish'),('glass','Opaque window backing','#53615F','Opaque backing for printable exterior, not interior reconstruction'),('base','Authored support and grade block','#B3B0A0','Authored support with section-supported relative east-side raised grade')]]
items=[];ops=[];ids={}
def box(a,b):return mf.Manifold.cube(np.subtract(b,a).tolist()).translate(a)
def add(n,s,mat=1,e='Original architectural drawing, proportional simplified exterior detail'):
 s=s.translate([0,0,.5]).as_original();ids[int(s.original_id())]=mat;items.append(s);ops.append({'name':n,'material':mat,'evidence':e})
def bx(n,a,b,mat=1):add(n,box(a,b),mat)
def polyxz(pts,y,d):
 if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1]))<0:pts=list(reversed(pts))
 return mf.CrossSection([pts]).extrude(d).rotate([90,0,0]).translate([0,y+d,0])
def polyyz(pts,x,d):return polyxz(pts,-x-d,d).rotate([0,0,90])
def shell_unit(cx):
 # Four bilinear hyperbolic-paraboloid patches meet at a low central column.
 # Heights interpreted from A6/A9/S4-S6, NOT a certified exact shell equation.
 nx=32;ny=44;vs=[]
 for lower in [False,True]:
  for j in range(ny+1):
   y=-8.1+13.2*j/ny;v=abs(y)/(8.1 if y<0 else 5.1)
   for i in range(nx+1):
    x=-4+8*i/nx;u=abs(x)/4
    z=8.68+(10.78-8.68)*(u+v-u*v)-(0.14 if lower else 0)
    vs.append([x+cx,y,z])
 N=(nx+1)*(ny+1);fs=[]
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+2;d=a+nx+1
   fs.extend([[a,b,c],[a,c,d],[a+N,c+N,b+N],[a+N,d+N,c+N]])
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):fs.extend([[a,a+N,b+N],[a,b+N,b]])
 m=mf.Mesh(np.array(vs,dtype=np.float32),np.array(fs,dtype=np.uint32));s=mf.Manifold(m);assert s.status()==mf.Error.NoError,s.status();return s
bx('Authored flat plinth',[-25.5,-10,-.5],[25.5,12,0],4)
for x in [-20,-12,-4,4,12,20]:
 bx('Rectangular HP canopy column '+str(x),[x-.25,-.4,0],[x+.25,.4,8.75])
 add('Four-quadrant HP canopy '+str(x),shell_unit(x),1,'24 bilinear HP patches, approximate curvature from original plans/sections and official 2021 panorama; not surveyed shell')
 bx('Raised central column-head '+str(x),[x-.42,-.42,8.5],[x+.42,.42,9.48])
for y in [-8.1,5.1]:bx('Canopy edge upstand',[-24,y-.07,10.68],[24,y+.07,10.88])
for x in [-24,24]:bx('Canopy end edge', [x-.07,-8.1,10.68],[x+.07,5.1,10.88])
# Remaining facade and seating geometry appended below after dimension cross-check.
# Front lower rooms: retain arched facade openings, backed glazing is opaque print geometry.
def archpts(cx,w,z0,spring,top,N=24):
 return [(cx-w/2,z0),(cx+w/2,z0)]+[(cx+w/2*math.cos(t),spring+(top-spring)*math.sin(t)) for t in np.linspace(0,math.pi,N+1)]
def archsolid(cx,w,z0,spring,top,y,depth):return polyxz(archpts(cx,w,z0,spring,top),y,depth)
def archtrim(name,cx,w,z0,spring,top,y,depth,trim=.14):
 out=archsolid(cx,w+2*trim,z0-.05,spring,top+trim,y,depth);cut=archsolid(cx,w,z0-.15,spring,top,y-.1,depth+.2);add(name,out-cut,1)
core=box([-22.44,-6.09,0],[22.44,.35,3.53]);front=[]
for cx in [-16,-8,0,8,16]:front.append((cx,6.8,.40,1.45,3.10))
for cx in [-21.1,21.1]:front.append((cx,1.35,.40,1.7,2.35))
for cx,w,z0,sp,tp in front:core=core-archsolid(cx,w,z0,sp,tp,-6.4,2.12)
core=core-box([-1.4,-4.5,.35],[1.4,.3,3.55])
add('Ground-floor room outer envelope with arched recesses',core,0)
for cx,w,z0,sp,tp in front:
 archtrim('Original west arched stone trim',cx,w,z0,sp,tp,-6.19,.15)
 if abs(cx)>20:
  bx('Original small end door',[cx-w/2,-4.38,.4],[cx+w/2,-4.20,2.15],3)
 else:
  back=archsolid(cx,w,z0,sp,tp,-4.30,.18)
  if cx==0:back=back-box([-1.4,-4.5,.35],[1.4,-3.9,3.55])
  add('Recessed plaster wall behind west arcade',back,1)
# Original sparse doors/windows behind arches, NOT full-width glass curtain walls.
for cx in [-14.6,-6.3,2.5,6.2,14.5]:
 bx('Recessed original door',[cx-.55,-4.40,.4],[cx+.55,-4.20,2.65],3)
 bx('Door central stile',[cx-.025,-4.43,.4],[cx+.025,-4.17,2.65],2)
for cx in [-18.0,-9.8,9.8,18.0]:
 bx('Original high window',[cx-1.15,-4.40,2.12],[cx+1.15,-4.20,2.92],3)
 for zz in [2.12,2.88]:bx('High window transom',[cx-1.15,-4.44,zz],[cx+1.15,-4.18,zz+.045],2)
for cx in [-12.9,12.9]:bx('Original narrow window',[cx-.55,-4.40,1.60],[cx+.55,-4.20,2.85],3)
for i in range(20):
 y=-4.3+i*.22;bx('Visible central internal stair',[ -1.35,y-.003,.35],[1.35,y+.223,.40+(i+1)*3.13/20])
# Ground-level underside and rear raised grade, no invented below-ground architecture.
bx('Authored raised east grade support',[-23.2,.1,0],[23.2,11.5,1.88],4)
bx('Second-level floor slab',[-22.44,-6.19,3.28],[22.44,7.53,3.53])
bx('Central rear entrance floor',[-8,7.1,2.65],[8,9.35,2.88])
# Side rooms and central rear entrance, punched original arched openings.
for sign in [-1,1]:
 a,b=(-22.44,-9.4) if sign<0 else (9.4,22.44)
 room=box([a,.05,1.85],[b,7.53,6.55])
 rearopen=[(sign*16,7.7,3.4,4.05,5.45),(sign*21,1.5,2.88,4.2,4.9),(sign*10.8,1.5,2.88,4.2,4.9)]
 for cx,w,z0,sp,tp in rearopen:room=room-archsolid(cx,w,z0,sp,tp,6.8,1.)
 add('East lower wing '+str(sign),room,0)
 for cx,w,z0,sp,tp in rearopen:
  archtrim('East wing arch trim',cx,w,z0,sp,tp,7.53,.15)
  add('East wing opaque glazing',archsolid(cx,w,z0,sp,tp,6.70,.15),3)
  for xx in np.arange(cx-w/2+.7,cx+w/2,.9):
   ztop=sp+(tp-sp)*math.sqrt(max(0,1-((xx-cx)/(w/2))**2));bx('East window frame',[xx-.035,6.82,z0],[xx+.035,7.02,ztop],2)
 # actual low concrete-tile roof slopes east, 1:4 per original detail.
 add('Low wing concrete tiled roof '+str(sign),polyyz([(3.33,7.65),(7.53,6.59),(7.53,6.75),(3.33,7.81)],a,b-a),1)
 for xx in np.arange(a,b,.28):
  add('Representative concrete tile seam',polyyz([(3.33,7.80),(7.53,6.74),(7.53,6.79),(3.33,7.85)],xx,.025),1)
central=box([-8,.25,1.85],[8,9.28,8.68]);rearopen=[(0,8.8,2.88,5.45,7.45),(-6.45,1.6,2.88,5.2,5.95),(6.45,1.6,2.88,5.2,5.95)]
for cx,w,z0,sp,tp in rearopen:central=central-archsolid(cx,w,z0,sp,tp,8.5,.9)
# Central hall must not fill the spectator-platform volume. It begins behind the seating.
central=central-box([-8.1,-.1,3.53],[8.1,3.33,9.0])
add('Central east entry hall exterior',central,0)
for cx,w,z0,sp,tp in rearopen:
 archtrim('Central entry arch trim',cx,w,z0,sp,tp,9.28,.18)
 if cx==0:
  add('Recessed plaster entry arch backing',archsolid(cx,w,z0,sp,tp,8.40,.20),1)
  bx('Original recessed double entry door',[-2.3,8.36,2.88],[2.3,8.63,6.35],3)
  bx('Entry door centre stile',[-.04,8.32,2.88],[.04,8.66,6.35],2)
 else:bx('Rear secondary door',[cx-.72,8.4,2.88],[cx+.72,8.65,5.3],3)
# Entry stairs are relative surveyed levels; no asserted surrounding terrain.
for i in range(6):bx('East entrance step',[-3.9,9+i*.3,1.88],[3.9,9+(i+1)*.3,2.88-i/6])


# Ten dimensioned seating tiers: 72cm tread, 36cm riser, EL353 to EL713.
for side,(a,b) in enumerate([(-22.44,-6.6),(6.6,22.44)]):
 for i in range(10):
  y=-4.72+i*.72;z=3.53+(i+1)*.36
  seat=box([a,y-.003,3.45],[b,y+.723,z])
  for cx in ([-18,-7.2] if side==0 else [7.2,18]):seat=seat-box([cx-.42,y-.01,3.44],[cx+.42,y+.74,8.0])
  add('Tier %d wing %d'%(i+1,side),seat)
 # Rear high walkway at +713, not a flat slab across the seating.
 bx('Rear high walkway '+str(side),[a,2.48,3.45],[b,3.37,7.13])
 # Narrow intermediate stair aisles, double cadence per seat tier.
 for cx in ([-18,-7.2] if side==0 else [7.2,18]):
  for j in range(20):
   y=-4.72+j*.36;z=3.53+(j+1)*.18
   # aisle cuts are subtracted from tier mass below after assembly using explicit step fill
   # At this scale represent each additional half-riser proud of the seat tread.
   bx('Aisle half-step',[cx-.423,y-.003,3.45],[cx+.423,y+.363,z])
# Central projecting low platform and smaller raised dais; no modern filled rooms.
bx('Central west projecting platform',[-5.0,-7.45,3.28],[5.0,-.75,3.53])
bx('Central raised dais',[-4.0,-1.20,3.45],[4.0,.55,5.38])
# Side passages climb beside dais to rear high walkway.
for side in [-1,1]:
 a,b=(-6.6,-4.05)if side<0 else(4.05,6.6)
 for j in range(10):
  y=-3.2+j*.55;z=3.53+(j+1)*.36
  bx('Central side passage step',[a,y,3.45],[b,y+.55,z])
bx('Central rear high walkway',[-6.6,2.3,3.45],[6.6,3.37,7.13])
# Vertical end walls follow seating slope, not arbitrary box closures.
for xx in [-22.48,22.13]:
 add('Sloping exterior end wall',polyyz([(-6.09,0),(7.53,0),(7.53,6.6),(3.37,7.8),(2.48,7.8),(-4.72,4.2),(-6.09,4.2)],xx,.35),1)
# Front balustrades anchored to the walkway; simplified section, source A19.
def rail_x(name,a,b,y,z):
 for zz in [z+.35,z+.68]:bx(name+' horizontal',[a,y-.035,zz],[b,y+.035,zz+.06],2)
 for x in np.arange(a,b+.001,1.25):bx(name+' upright',[x-.035,y-.035,z],[x+.035,y+.035,z+.74],2)
for a,b in [(-22.44,-5.0),(5.0,22.44)]:
 bx('Front low parapet',[a,-6.15,3.5],[b,-5.96,3.7],1);rail_x('West walkway rail',a,b,-6.13,3.7)
rail_x('Central low platform rail',-5,5,-7.43,3.53)
rail_x('Raised central dais rail',-4,4,-1.18,5.38)
for a,b in [(-22.44,-6.6),(6.6,22.44)]:rail_x('High rear seating rail',a,b,3.32,7.13)
# Two visible west stair flights, each from original lower floor to central deck.
for sign in [-1,1]:
 pts=[]
 for i in range(20):
  x=11.2-i*.31;z=.40+(i+1)*3.13/20
  pts.extend([(sign*x,z),(sign*(x-.31),z)])
 pts.extend([(sign*5,3.15),(sign*11.2,.10)])
 add('West open-underneath stair slab',polyxz(pts,-7.28,1.24))
 bx('West stair foot',[sign*11.2-.16,-7.28,0],[sign*11.2+.16,-6.04,.58])
 # Sloped brick parapet and white coping along the two flights.
 pts=[(sign*11.2,.4),(sign*5,3.53),(sign*5,4.23),(sign*11.2,1.10)]
 add('West stair brick cheek',polyxz(pts,-7.4,.18),0)
 pts=[(sign*11.2,1.10),(sign*5,4.23),(sign*5,4.31),(sign*11.2,1.18)]
 add('West stair coping',polyxz(pts,-7.44,.26),1)

for a,b in [(-22.44,-9.4),(9.4,22.44)]:
 add('Low-wing sloping roof bearing volume',polyyz([(3.33,6.5),(7.53,6.5),(7.53,6.75),(3.33,7.80)],a,b-a),0)
# Original raised central sign/plaque, lettering intentionally omitted rather than invented.
bx('Central rear ceremonial screen',[-4.05,2.95,7.05],[4.05,3.45,9.15],0)
bx('Original blank central inscription panel',[-2.05,2.82,7.55],[2.05,3.02,9.04],1)
for o,i in zip(ops,items):assert i.status()==mf.Error.NoError,(o,i.status())
s=mf.Manifold.batch_boolean(items,mf.OpType.Add)
assert s.status()==mf.Error.NoError,s.status()
s=s.set_tolerance(.001).simplify(.001)
m=s.to_mesh64()
# Quantize into STL's actual float32-mm precision before final topology simplification.
# This removes sub-precision CSG seam slivers rather than shipping a broken float32 STL.
qv=np.ascontiguousarray((np.asarray(m.vert_properties)*SCALE).astype(np.float32).astype(np.float64))
qm=mf.Mesh64(qv,np.array(m.tri_verts,dtype=np.uint64,order="C",copy=True),merge_from_vert=np.array(m.merge_from_vert,dtype=np.uint64,copy=True),merge_to_vert=np.array(m.merge_to_vert,dtype=np.uint64,copy=True),run_index=np.array(m.run_index,dtype=np.uint64,copy=True),run_original_id=np.array(m.run_original_id,dtype=np.uint32,copy=True),tolerance=.002)
qs=mf.Manifold(qm).simplify(.01);assert qs.status()==mf.Error.NoError,qs.status()
# Remove only sub-0.001 mm3 numerical CSG crumbs, never meaningful geometry.
comps=qs.decompose();crumbs=[q for q in comps if abs(q.volume())<.001];assert sum(abs(q.volume()) for q in crumbs)<.01
qs=mf.Manifold.batch_boolean([q for q in comps if abs(q.volume())>=.001],mf.OpType.Add)
m=qs.to_mesh64();v=np.asarray(m.vert_properties)[:,:3];f=np.asarray(m.tri_verts);mi=np.zeros(len(f),np.int32)
for i,oid in enumerate(m.run_original_id):mi[m.run_index[i]//3:m.run_index[i+1]//3]=ids[int(oid)]
# Weld duplicate material-boundary positions, retaining each surface triangle's real original material.
v,inv=np.unique(np.round(v,9),axis=0,return_inverse=True);f=inv[f]
t=trimesh.Trimesh(v,f,process=False);t.export(ROOT/'model.stl');np.savez_compressed(ROOT/'mesh-data.npz',vertices=v,faces=f,materials=mi)
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns);E=lambda s:'{'+ns+'}'+s
root=ET.Element(E('model'),unit='millimeter');res=ET.SubElement(root,E('resources'));bm=ET.SubElement(res,E('basematerials'),id='1')
for p in PALETTE:ET.SubElement(bm,E('base'),name=p['name'],displaycolor=p['hex']+'FF')
o=ET.SubElement(res,E('object'),id='2',type='model',name='NCKU Guangfu Grandstand 1981 drawing reconstruction');mesh=ET.SubElement(o,E('mesh'));vs=ET.SubElement(mesh,E('vertices'));ts=ET.SubElement(mesh,E('triangles'))
for row in v:ET.SubElement(vs,E('vertex'),**{k:f'{float(a):.7f}' for k,a in zip('xyz',row)})
for row,c in zip(f,mi):ET.SubElement(ts,E('triangle'),v1=str(row[0]),v2=str(row[1]),v3=str(row[2]),pid='1',p1=str(c),p2=str(c),p3=str(c))
b=ET.SubElement(root,E('build'));ET.SubElement(b,E('item'),objectid='2')
with zipfile.ZipFile(ROOT/'model.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats-package.relationships/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'.replace('http://schemas.openxmlformats-package.relationships/2006/relationships','http://schemas.openxmlformats.org/package/2006/relationships'))
 z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
parts=[]
for op,item in zip(ops,items):
 q=item.to_mesh();parts.append({**op,'vertices':(np.asarray(q.vert_properties)[:,:3]*SCALE).tolist(),'faces':np.asarray(q.tri_verts).tolist()})
(ROOT/'construction-parts.json').write_text(json.dumps(parts,separators=(',',':')));(ROOT/'editable-parts.json').write_text(json.dumps({'palette':PALETTE,'features':ops},indent=2))
r={'vertices':len(v),'triangles':len(f),'watertight':bool(t.is_watertight),'winding_consistent':bool(t.is_winding_consistent),'components':len(qs.decompose()),'volume_mm3':float(t.volume),'dimensions_mm':t.extents.tolist(),'min_triangle_area_mm2':float(t.area_faces.min()),'material_counts':{p['id']:int((mi==i).sum()) for i,p in enumerate(PALETTE)},'scope':'1981 drawing-based grandstand exterior reconstruction; approximate HP curvature, original windows, authored support, no current-state or as-built claim'}
(ROOT/'build-summary.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

