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
# Undated official accessibility-map photograph; not calibrated or a current-date claim.
palette=[('Unknown sides roof and display base','#A5A7A3',.85),('Pale grey beige sunshade webs','#C4C3B5',.85),('Grey beige canopy piers and steps','#B4B4A9',.85),('Dark green grey recess proxy','#3F5148',.7),('Dark blue grey large glazing proxy','#434E53',.45),('Dark grey brown upper fascia','#68675E',.82),('Unlettered dark existing header','#41403A',.8)]
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))
def lin(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
mesh.materials.clear()
for name,col,rough in palette:
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=tuple(lin(v) for v in rgb(col))+(1,);bs.inputs['Roughness'].default_value=rough;m.diffuse_color=tuple(rgb(col))+(1,);mesh.materials.append(m)
indices=[]
original_indices=[]
changed_faces=[]
change_reasons={}
def near(v,t,e=.035):return abs(v-t)<e
def plane(axis,value):return all(abs(mesh.vertices[j].co[axis]-value)<.001 for j in p.vertices)
def bounds(lo,hi):return all(all(lo[a]-.001<=mesh.vertices[j].co[a]<=hi[a]+.001 for a in range(3)) for j in p.vertices)
for p in mesh.polygons:
 x,y,z=p.center;n=p.normal;i=0
 # Only the source-visible front envelope and original reveals receive tile-like finish.
 if -65.01<x<65.01 and y<=-20.29 and 3.01<z<45.81:i=1
 if near(y,-20.3,.015) and n.y<-.8 and 4.99<z<43.61:i=3
 if near(y,-20.1,.015) and n.y<-.8:i=4
 if near(y,-18,.015) and n.y<-.8 and 3<z<12.01:i=4
 # Existing entrance porch and two piers only, no new signage or framing.
 if -9.51<x<25.51 and -40.01<y<-19.99 and 11.99<z<14.71:i=2
 for cx in [-7,23]:
  if abs(x-cx)<1.41 and -38.91<y<-35.09 and 2.99<z<13.01:i=2
 if -12.01<x<28.01 and y<-37 and 3.0<z<4.91:i=2
 if -5.51<x<21.51 and -38.11<y<-35.89 and 14.49<z<17.51:i=6
 # Observed dark top frontage; unseen roof horizontal surface remains neutral.
 if near(y,-22.5,.015) and n.y<-.8 and 43.61<z<45.51:i=5
 if near(y,-23.5,.015) and n.y<-.8 and 45.49<z<47.11:i=5
 if z<=3.0 or (z>=45.49 and n.z>.8):i=0
 if near(abs(x),65,.015) and abs(n.x)>.8:i=0
 original_indices.append(i);reason=None
 # v2: only existing neutral faces on identifiable continuous exterior elements.
 # Main solid body was modelled as a complete approximate envelope, not a cut cap.
 if i==0:
  if abs(n.z)<.001 and bounds((-65,-22.5,3),(65,32.5,45.5)) and ((plane(0,-65) and n.x<-.999) or (plane(0,65) and n.x>.999) or (plane(1,32.5) and n.y>.999)):
   i=1;reason='inferred_existing_side_rear_exterior_pale_wall'
  # Extend the same dark vertical fascia around the original continuous roof slab.
  elif abs(n.z)<.001 and bounds((-66,-23.5,45.5),(66,33.5,47.1)) and ((plane(0,-66) and n.x<-.999) or (plane(0,66) and n.x>.999) or (plane(1,33.5) and n.y>.999)):
   i=5;reason='inferred_existing_vertical_fascia_continuity'
  # Three original shallow left bands: pale structural reveals only. The broad
  # back planes remain neutral: the photographs do not establish pure glazing.
  for z0 in [13,25,37]:
   if i==0 and bounds((-65,-16,z0),(-63.25,24,z0+3)) and not plane(0,-63.25):
    if (plane(1,-16) and n.y>.999) or (plane(1,24) and n.y<-.999) or (plane(2,z0) and n.z>.999) or (plane(2,z0+3) and n.z<-.999):
     i=1;reason='inferred_pale_left_band_structural_reveals_only'
 if i!=original_indices[-1]:changed_faces.append(p.index);change_reasons[str(p.index)]=reason
 p.material_index=i;indices.append(i)
# Entire connected portico/entry-lintel underside domain, including inner half.
entry_soffit_domain=[5307, 5308, 5310, 5316, 5317, 5329, 5330, 5332, 5335, 5336, 5344, 5349, 5351, 5356, 5359, 5362, 5363, 5366]
assert sum(indices[i]==0 for i in entry_soffit_domain)==1
assert indices[5308]==0
for i in entry_soffit_domain:
 p=mesh.polygons[i]
 assert indices[i] in (0,2) and p.normal.z < -.999
 for vi in p.vertices:
  a=mesh.vertices[vi].co
  assert abs(a.z-12)<.001 and -9.501<=a.x<=25.501 and -40.001<=a.y<=-17.999
 p.material_index=2;indices[i]=2
assert before=={'vertices':digest([tuple(v.co) for v in mesh.vertices],'<3f'),'faces':digest([tuple(p.vertices) for p in mesh.polygons],'<3I')}
obj['appearance_policy']='Source-guided approximate sRGB; same exact vertices/triangles as original; side/rear wall and fascia continuity inferred; uncertain band backs, roof and base neutral'
scene=bpy.context.scene;scene['appearance_revision']='color-v3-entry-soffit'
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
(R/'appearance-materials.json').write_text(json.dumps({'revision':'color-v3-entry-soffit','geometry':before,'palette':[{'name':n,'srgb':c,'roughness':r} for n,c,r in palette],'prior_v2_changed_faces':changed_faces,'entry_soffit_domain':entry_soffit_domain,'entry_soffit_changed_faces':[5308],'change_reasons':change_reasons,'original_face_material_indices':original_indices,'face_counts':dict(Counter(indices)),'face_material_indices':indices,'limits':['Photographic approximation, not calibrated real finish values','Opaque glazing proxies, no real transparency or physical material certification','Side/rear pale exterior walls, narrow vertical roof fascia and existing left-band structural reveals are material-family continuity inferences, not rear photographic verification. All original colored faces and exact material RGBA/roughness preserved. Three uncertain left-band backs, roofs, base and unresolved faces remain neutral. No new windows or geometry; lattice recess proxy does not prove every opening is glazing.','No actual trial print; original partial-model QA caveats remain']},indent=2))
# New images only; locked previews/front.png and original scene are never overwritten.
views={'front':((-195,-220,155),(0,0,23.55),180),'rear':((195,230,160),(0,0,23.55),180),'elevation':((0,-260,23.55),(0,0,23.55),180),'source-angle':((-120,-260,65),(0,0,23.55),180),'left':((-300,0,145),(0,0,23.55),180),'right':((300,0,145),(0,0,23.55),180),'top':((0,0,260),(0,0,0),180)}
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
