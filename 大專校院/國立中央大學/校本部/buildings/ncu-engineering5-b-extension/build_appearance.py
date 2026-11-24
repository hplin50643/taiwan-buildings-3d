"""Add source-guided approximate materials; never modify original mesh or locked previews.
Run Blender 4.3.2: blender -b -t 1 --python-exit-code 1 -P build_appearance.py
Requires original scene.blend and model.stl alongside this script. No source photos embedded.
"""
from pathlib import Path
import sys
import bpy,hashlib,json,math,struct,zipfile,xml.etree.ElementTree as ET
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'scene.blend'))
bpy.context.preferences.filepaths.save_version=0
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');mesh=obj.data
verts=[tuple(v.co) for v in mesh.vertices];faces=[tuple(p.vertices) for p in mesh.polygons]
assert all(len(f)==3 for f in faces)
def digest(a,fmt):return hashlib.sha256(b''.join(struct.pack(fmt,*r) for r in a)).hexdigest()
before={'vertices':digest(verts,'<3f'),'faces':digest(faces,'<3I')}
# Two actual project23 photos, B extension only; original build mirrors x. No geometry changes.
palette=[('Unknown flat roof cut ends old connection base','#A7A9A5',.86),('Pale grey beige original deep facade frames','#B9B9AF',.84),('Grey taupe recessed front wall','#96968C',.85),('Dark grey green original glazing proxy','#465954',.48),('Pale grey opposite wall and original core front','#BEC1B7',.84),('Darker grey original louvers and core fins','#777D75',.8),('Pale grey blue simplified sloping cover proxy','#A1AAAB',.85)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[];original_indices=[];changed_faces=[];change_reasons={}
def near(v,t,e=.035):return abs(v-t)<e
def boxed(p,x0,x1,y0,y1,z0,z1):
 return all(x0-.015<=-mesh.vertices[v].co.x<=x1+.015 and y0-.015<=mesh.vertices[v].co.y<=y1+.015 and z0-.015<=mesh.vertices[v].co.z<=z1+.015 for v in p.vertices)
for p in mesh.polygons:
 # Undo coordinate reflection only for material classification, not actual mesh coordinates.
 x=-p.center.x;y=p.center.y;z=p.center.z;nx=-p.normal.x;ny=p.normal.y;nz=p.normal.z;i=0
 if near(y,-10,.015) and ny<-.8 and -66.51<x<58.51 and 3<z<63.81:i=2
 # Front structural frame component bounds, whole triangles only, no centroid cross-wall spill.
 if boxed(p,-64,52,-17,-13,3,63):i=1
 for lo in [3,17,30,43,61]:
  if boxed(p,-64,52,-17,-7,lo,lo+1.8):i=1
 if near(y,-8.5,.015) and ny<-.8 and any(abs(x-cx)<4.26 for cx in range(-56,45,13)) and any(lo-.01<z<lo+7.01 for lo in [7,20,33,47]):i=3
 # Photographed opposite long elevation; not the bright oldB block beyond the cut-off.
 if near(y,18,.015) and ny>.8 and -66.51<x<58.51 and 3<z<63.81:i=4
 if near(y,16.5,.015) and ny>.8 and any(abs(x-cx)<4.26 for cx in range(-56,45,13)) and any(lo-.01<z<lo+6.01 for lo in [8,20,32,44,56]):i=3
 if near(y,19,.015) and ny>.8 and 45.99<x<68.01 and 3<z<67.81:i=4
 if near(y,-11,.015) and ny<-.8 and 45.99<x<68.01 and 3<z<67.81:i=2
 if near(y,17.5,.015) and ny>.8 and 47.49<x<56.51 and 7.99<z<60.01:i=3
 for xx in [49,52,55]:
  if boxed(p,xx-.55,xx+.55,17.25,20.75,8,60):i=5
 for lo in [15,27,39,51]:
  for dz in [0,1.4]:
   if boxed(p,-63.5,51.5,17.95,19.05,lo+dz,lo+dz+.9):i=5
 # Source-visible simple sloping canopy surface only; does not certify photovoltaic panels.
 if boxed(p,-66,47,-6.5,18.5,63,66) and nz>.5:i=6
 if z<=3:i=0
 # Broad unknown narrow ends/cut-off remain neutral, not copied from adjacent old building.
 if abs(nx)>.8 and any(near(x,xx,.015) for xx in [-66.5,68]):i=0
 p.material_index=i;indices.append(i);original_indices.append(i)
# Revision 2: complete ORIGINAL window-recess wall surfaces only.
# Whole-triangle tests in the ORIGINAL generator coordinates (-mesh x, y, z).
# Existing colored fronts/glazing/fins remain unchanged. These original recess
# returns continue the adjacent wall material; this is a same-component inference,
# not a direct photographic measurement of every jamb/soffit/sill.
def plane(p,axis,value):
 return all(abs(((-mesh.vertices[v].co.x) if axis==0 else mesh.vertices[v].co[axis])-value)<.003 for v in p.vertices)
for p in mesh.polygons:
 if original_indices[p.index]!=0:continue
 i=0;reason=None;support=None
 for cx in range(-56,45,13):
  for z in [7,20,33,47]:
   if boxed(p,cx-4.25,cx+4.25,-10,-8.5,z,z+7) and ((abs(p.normal.x)>.999 and any(plane(p,0,q) for q in [cx-4.25,cx+4.25])) or (abs(p.normal.z)>.999 and any(plane(p,2,q) for q in [z,z+7]))):
    i=2;reason='front_recess_wall_returns';support=[cx-4.25,cx+4.25,-10,-8.5,z,z+7]
  for z in [8,20,32,44,56]:
   if boxed(p,cx-4.25,cx+4.25,16.5,18,z,z+6) and ((abs(p.normal.x)>.999 and any(plane(p,0,q) for q in [cx-4.25,cx+4.25])) or (abs(p.normal.z)>.999 and any(plane(p,2,q) for q in [z,z+6]))):
    i=4;reason='opposite_recess_wall_returns';support=[cx-4.25,cx+4.25,16.5,18,z,z+6]
 if boxed(p,47.5,56.5,17.5,19,8,60) and ((abs(p.normal.x)>.999 and any(plane(p,0,q) for q in [47.5,56.5])) or (abs(p.normal.z)>.999 and any(plane(p,2,q) for q in [8,60]))):
  i=4;reason='core_glazed_strip_wall_returns';support=[47.5,56.5,17.5,19,8,60]
 if reason:
  p.material_index=i;indices[p.index]=i;changed_faces.append(p.index);change_reasons[str(p.index)]={'family':reason,'support_bounds_unmirrored_generator_coordinates':support,'basis':'Every vertex is on a complete original window-recess jamb, head or sill support. Adjacent original wall finish continuity is inferred; no artificial building cut end is colored.'}

assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Original geometry and colors preserved; whole original window-recess wall returns colored by continuity. Cut ends, flat roofs, uncertain core step side, sloping cover edges and base remain neutral.'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-complete-window-returns'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=96;scene.cycles.seed=0;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=1
scene.render.resolution_x=900;scene.render.resolution_y=800
for attr in dir(scene.render):
 if attr.startswith('use_stamp'):
  try:setattr(scene.render,attr,False)
  except (TypeError,AttributeError):pass
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.82,.85,.89,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
for name,energy,ang,rot in [('Key',2.1,.16,(28,-26,-32)),('Fill',.55,.35,(-20,32,140))]:
 light=bpy.data.lights.new(name,'SUN');light.energy=energy;light.angle=ang;o=bpy.data.objects.new(name,light);bpy.context.collection.objects.link(o);o.rotation_euler=tuple(math.radians(a) for a in rot)

scene.render.filepath='//appearance/front.png'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'appearance.blend'))
# Core 3MF base materials per original triangle: no geometry splitting/resampling.
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
e=lambda tag,attrs={}:ET.Element('{'+ns+'}'+tag,attrs)
root=e('model',{'unit':'millimeter','xml:lang':'en-US'});res=ET.SubElement(root,'{'+ns+'}resources');bm=ET.SubElement(res,'{'+ns+'}basematerials',{'id':'1'})
for name,col,_ in palette:ET.SubElement(bm,'{'+ns+'}base',{'name':name,'displaycolor':col+'FF'})
o=ET.SubElement(res,'{'+ns+'}object',{'id':'2','type':'model'});m=ET.SubElement(o,'{'+ns+'}mesh');vs=ET.SubElement(m,'{'+ns+'}vertices')
for v in verts:ET.SubElement(vs,'{'+ns+'}vertex',dict(zip(['x','y','z'],[format(c,'.17g') for c in v])))
ts=ET.SubElement(m,'{'+ns+'}triangles')
for f,i in zip(faces,indices):ET.SubElement(ts,'{'+ns+'}triangle',{'v1':str(f[0]),'v2':str(f[1]),'v3':str(f[2]),'pid':'1','p1':str(i),'p2':str(i),'p3':str(i)})
build=ET.SubElement(root,'{'+ns+'}build');ET.SubElement(build,'{'+ns+'}item',{'objectid':'2'})
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED) as out:
 for n,b in {'3D/3dmodel.model':ET.tostring(root,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}.items():
  info=zipfile.ZipInfo(n,date_time=(2026,10,29,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;out.writestr(info,b)
from collections import Counter
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-complete-window-returns','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'original_face_material_indices':original_indices,'changed_faces':changed_faces,'change_reasons':change_reasons,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','72 original window recesses and core glazed-strip wall returns continue adjacent taupe/pale-gray wall colors by whole-face component continuity. Artificial cut ends, exposed core step side, roof cover edges, flat roofs and base remain neutral. Existing estimated geometry and every originally colored face remain unchanged. Photo dates are unknown and no current-condition or measured-finish claim is made','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-195,-260,145),(0,0,33.9),200),'rear':((195,260,145),(0,0,33.9),200),'elevation':((0,-300,33.9),(0,0,33.9),200),'source-angle':((-150,300,60),(0,0,33.9),200),'left':((-330,0,125),(0,0,33.9),200),'right':((330,0,125),(0,0,33.9),200),'top':((0,0,330),(0,0,0),200)}
out=R/'appearance';out.mkdir(exist_ok=True);camera_records=[]
for name,(pos,target,scale) in ([] if '--skip-render' in sys.argv else views.items()):
 c=scene.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 inv=c.rotation_euler.to_matrix().transposed();projected=[inv@(obj.matrix_world@Vector(corner)-c.location) for corner in obj.bound_box]
 width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected)
 c.data.ortho_scale=max(width,height*scene.render.resolution_x/scene.render.resolution_y)*1.18
 camera_records.append({'view':name,'location':list(c.location),'rotation_euler':list(c.rotation_euler),'ortho_scale':c.data.ortho_scale,'target':list(target)})
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 data=(out/(name+'.png')).read_bytes(); cleaned=data[:8]; off=8
 while off<len(data):
  length=struct.unpack_from('>I',data,off)[0];typ=data[off+4:off+8];body=data[off+8:off+8+length];key=body.split(b'\0',1)[0]
  variable=typ in (b'tEXt',b'zTXt',b'iTXt') # no private path/date/timing metadata
  if not variable:cleaned+=data[off:off+length+12]
  off+=length+12
 (out/(name+'.png')).write_bytes(cleaned)
if camera_records:(R/'render-cameras.json').write_text(json.dumps(camera_records,indent=2))
print('APPEARANCE_DONE',before,dict(Counter(indices)))
