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
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');mesh=obj.data
verts=[tuple(v.co) for v in mesh.vertices];faces=[tuple(p.vertices) for p in mesh.polygons]
assert all(len(f)==3 for f in faces)
def digest(a,fmt):return hashlib.sha256(b''.join(struct.pack(fmt,*r) for r in a)).hexdigest()
before={'vertices':digest(verts,'<3f'),'faces':digest(faces,'<3I')}
# Approximate sRGB from the official undated entrance photograph, not calibrated finishes.
palette=[('Unknown cut / authored base','#969A95',.82),('Pale grey beige tile wall','#B8B0A0',.82),('White stone portico and columns','#D9DBCE',.83),('Pale green grey glazing proxy','#91A69D',.38),('Grey metal window frames','#9D9F8C',.55),('Dark rain canopy frame','#484B48',.7),('Pale rain canopy panels','#AAB7A7',.6),('Stone entrance steps','#BFC2B3',.82)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[];original_indices=[];changed_faces=[];change_reasons={}
def near(v,t,e=.035):return abs(v-t)<e
for p in mesh.polygons:
 x,y,z=p.center;n=p.normal;i=1
 if z<=3.01:i=0
 # Entrance step stack is a source-visible stone surface, not the whole base.
 if 2.8<z<=7.21 and -68.1<x<58.1 and y<-15:i=7
 # Existing two circular piers and projecting white stone portico.
 for cx in [-50,4]:
  if math.hypot(x-cx,y+32)<3.62 and 6.79<z<37.81:i=2
 if -62.51<x<16.51 and -37.51<y<1.51 and 36.49<z<44.31:i=2
 # Upper wall's concrete projecting beam keeps pale tile-like finish.
 if 69.79<z<81.61 and y<3.01:i=1
 # Existing window frames: only in the five source-defined groups.
 groups=[(-42,8.8,24,24),(-7,8.8,32,24),(43,8.8,36,24),(-28,50,55,20),(42,50,43,20)]
 inwin=any(cx-w/2-.61<x<cx+w/2+.61 and z0-.21<z<z0+h+.21 for cx,z0,w,h in groups)
 if inwin and 0.19<=y<4.21:i=4
 # Recess backing faces only; no new glass geometry or tint on wall reveals.
 if inwin and near(y,1.4) and n.y<-.8:i=3
 if -14.01<x<.01 and 8.79<z<27.31 and near(y,4.7) and n.y<-.8:i=3
 # Central deeper door jamb/transom remains metal.
 if -7.66<x<-6.34 and 8.59<z<27.51 and 1.54<y<6.06:i=4
 if -14.71<x<.71 and 25.99<z<27.31 and 1.54<y<6.06:i=4
 # Right lightweight canopy: original metal beams vs existing panel slab.
 if 21.49<x<64.51 and -17.51<y<1.01 and 40.79<z<44.51:i=5
 if 21.49<x<64.51 and -17.51<y<.51 and (near(z,44.5) or near(z,43)):i=6
 # All deliberately cropped outer boundary planes are neutral, not claimed elevations.
 if (near(y,20) and n.y>.8) or (near(abs(x),68) and abs(n.x)>.8) or (near(z,79) and n.z>.8):i=0
 p.material_index=i;indices.append(i);original_indices.append(i)
# V2: restore only the left ends of the already modeled entrance stairs.
# The original blanket x=-68 closure rule also neutralized genuine stair faces.
# Prove coverage of the WHOLE triangle by disjoint original step-profile bands.
# Clipping is geometric polygon clipping in the YZ plane, never a centroid test.
# y extents and tops derive from the four original build_model.py step boxes.
EPS=0.0001
step_bands=[(-44.5,-40.5,3.9),(-40.5,-36.5,5.0),(-36.5,-32.5,6.1),(-32.5,-17.5,7.2)]
def clip(poly,axis,bound,greater):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ina=a[axis]>=bound if greater else a[axis]<=bound
  inb=b[axis]>=bound if greater else b[axis]<=bound
  if ina:out.append(a)
  if ina!=inb:
   t=(bound-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
 return out
def area(poly):
 return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))*.5 if len(poly)>2 else 0
support_records=[]
for p in mesh.polygons:
 if original_indices[p.index]!=0:continue
 q=[verts[j] for j in p.vertices]
 if not all(abs(v[0]+68)<EPS for v in q) or p.normal.x>-.999:continue
 if min(v[2] for v in q)<3-EPS or max(v[2] for v in q)>7.2+EPS:continue
 yz=[(v[1],v[2]) for v in q];whole=area(yz);covered=0
 for y0,y1,z1 in step_bands:
  part=yz
  for axis,bound,greater in [(0,y0,True),(0,y1,False),(1,3.0,True),(1,z1,False)]:
   part=clip(part,axis,bound,greater)
  covered+=area(part)
 if whole<1e-10 or abs(covered-whole)>max(1e-7,whole*1e-6):continue
 p.material_index=7;indices[p.index]=7;changed_faces.append(p.index)
 change_reasons[str(p.index)]='Whole original triangle inside the genuine left staircase-end profile; existing stone-step material continued. The left end is inferred, not directly established by the photograph.'
 support_records.append({'face':p.index,'triangle_area_mm2':whole,'covered_by_original_step_bands_mm2':covered})
assert len(changed_faces)==49

assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='49 original left step-end triangles restored to the existing stone-step material; all artificial wall, rear and top closures neutral; geometry and original material values unchanged'
scene=bpy.context.scene;scene['appearance_revision']='color-v2-stair-end-continuity'
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
for text in list(bpy.data.texts):bpy.data.texts.remove(text)
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v2-stair-end-continuity','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'original_face_material_indices':original_indices,'changed_faces':changed_faces,'change_reasons':change_reasons,'step_profile_bands_y0_y1_ztop':step_bands,'whole_triangle_support':support_records,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','Official entrance photograph freshly downloaded and personally viewed; capture date unknown, no current-condition claim. Only the existing left step end is newly colored, as inferred same-component continuity. All original colored faces and material values unchanged. Genuine artificial wall side x=+/-68 above the steps, rear y=20, top z=79, and authored base remain neutral. This is a cropped entrance segment, not a full building. Other historical plans and renovation sources not freshly reread.','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((145,-260,110),(0,-12,40.8),180),'rear':((-195,230,160),(0,-12,40.8),180),'elevation':((0,-260,40.8),(0,-12,40.8),180),'source-angle':((110,-260,18),(0,-12,47),180),'top':((0,0,260),(0,-12,0),180)}
out=R/'appearance';out.mkdir(exist_ok=True)
for name,(pos,target,scale) in ([] if '--skip-render' in sys.argv else views.items()):
 c=scene.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 inv=c.rotation_euler.to_matrix().transposed();projected=[inv@(obj.matrix_world@Vector(corner)-c.location) for corner in obj.bound_box]
 width=max(v.x for v in projected)-min(v.x for v in projected);height=max(v.y for v in projected)-min(v.y for v in projected)
 c.data.ortho_scale=max(width,height*scene.render.resolution_x/scene.render.resolution_y)*1.18
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 data=(out/(name+'.png')).read_bytes(); cleaned=data[:8]; off=8
 while off<len(data):
  length=struct.unpack_from('>I',data,off)[0];typ=data[off+4:off+8];body=data[off+8:off+8+length];key=body.split(b'\0',1)[0]
  variable=typ in (b'tEXt',b'zTXt',b'iTXt') # no private path/date/timing metadata
  if not variable:cleaned+=data[off:off+length+12]
  off+=length+12
 (out/(name+'.png')).write_bytes(cleaned)
print('APPEARANCE_DONE',before,dict(Counter(indices)))
