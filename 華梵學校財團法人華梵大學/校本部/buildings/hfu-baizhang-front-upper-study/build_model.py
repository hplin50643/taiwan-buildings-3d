import bpy,bmesh,math,json,struct,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
(R/'previews').mkdir(exist_ok=True)
import os
os.chdir(R)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
materials=[]
for name,color in [('Artificial cut backing - NOT original building',(0.52,0.55,0.57,1)),('Visible roof nominal brown',(0.22,0.155,0.13,1)),('Visible ridge nominal red brown',(0.42,0.12,0.115,1)),('Visible upper wood nominal dark brown',(0.24,0.16,0.10,1)),('Opaque neutral glazing proxy - NOT glass colour',(0.44,0.48,0.49,1)),('Visible frame nominal muted beige',(0.57,0.53,0.40,1))]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;materials.append(m)
objects=[]
def prism(name,poly,yfront,yback,mat):
 poly=[(x,max(z,10)-10) for x,z in poly] # explicit higher artificial bottom cut, old z10
 n=len(poly);verts=[(x,yfront,z) for x,z in poly]+[(x,yback,z) for x,z in poly]
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
 for m in materials:mesh.materials.append(m)
 for p in mesh.polygons:p.material_index=mat if p.index==0 else 0
 # Recalculate consistent outside normals.
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free();objects.append(obj);return obj
def rect(name,x0,x1,z0,z1,y0,y1,mat):return prism(name,[(x0,z0),(x1,z0),(x1,z1),(x0,z1)],y0,y1,mat)
# Perspective-preserving shallow relief. Coordinates are graphic-study millimetres, not measured building geometry.
base=prism('Baizhang historical front UPPER STUDY only',[(-51,0),(65,0),(65,26),(-51,22)],0,6,0)
roof=prism('Visible forward roof projected silhouette',[(-75,23),(75,28),(72,56),(-59,49)],-2,6,1)
# Roof grooves/ribs omitted: photograph supports texture, not measured profile/depth.
prism('Visible ridge strip',[(-59,48),(72,55),(72,56.5),(-59,50)],-2.7,0,2)
prism('Visible eave upper timber',[(-52,21),(65,25),(65,29),(-52,25)],-2.8,1,3)
# Upper portions only, bounded by intentionally artificial bottom cut; no feet/steps.
rect('Left visible upper post',-49,-44,0,23,-3.3,1,3)
rect('Right visible upper post',60,65,0,26,-3.3,1,3)
prism('Visible upper glazing opaque proxy',[(-44,0),(60,0),(60,23),(-44,20)],-1.1,1,4)
# Visible three upper glazing fields, using approximate image positions, no inferred door bottoms.
for i,x in enumerate([-43,-18,31,59]):rect('Observed upper vertical frame %d'%i,x,x+1.5,0,21.6+(x+43)*.025,-2.4,1,5)
prism('Visible glazing header',[(-44,18.8),(61,21.9),(61,23.4),(-44,20.3)],-2.4,1,5)
# Union solids retains visible front material slots and makes a printable study relief; no scene-only architecture.
bpy.context.view_layer.objects.active=base;base.select_set(True)
for obj in list(objects)[1:]:
 mod=base.modifiers.new('Study union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=obj
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(obj,do_unlink=True)
bm=bmesh.new();bm.from_mesh(base.data);bmesh.ops.triangulate(bm,faces=bm.faces);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(base.data);bm.free()
base.name='HFU Baizhang Historical Front Upper Study - artificial shallow cut'
verts=[v.co.copy() for v in base.data.vertices];records=[]
for p in base.data.polygons:
 a,b,c=[verts[i] for i in p.vertices];n=(b-a).cross(c-a).normalized();records.append(struct.pack('<12fH',*n,*a,*b,*c,0))
stl=b'Baizhang FRONT UPPER STUDY; mm; artificial shallow backing'.ljust(80,b'\0')+struct.pack('<I',len(records))+b''.join(records);(R/'model.stl').write_bytes(stl)
bm=bmesh.new();bm.from_mesh(base.data); nonman=sum(not e.is_manifold for e in bm.edges); remaining=set(bm.verts); components=0
while remaining:
 components+=1; stack=[remaining.pop()]
 while stack:
  for edge in stack.pop().link_edges:
   for v in edge.verts:
    if v in remaining:remaining.remove(v);stack.append(v)
vol=bm.calc_volume(signed=True);bm.free()
report={'status':'DIGITAL_BUILD_CHECK_ONLY_NOT_PUBLICATION_STATUS','triangles':len(records),'nonmanifold_edges':nonman,'connected_components':components,'signed_volume_mm3':vol,'dimensions_mm':list(base.dimensions),'stl_sha256':hashlib.sha256(stl).hexdigest(),'scope':'Perspective-preserving FRONT UPPER relief only. Artificial shallow extrusion, back closure and bottom cut, NOT inferred true building depth or roof pitch.','roof_texture':'No invented corrugation counts or profile.','limitations':['Not complete building, no rear roof slope, side walls, steps or post feet.','Neutral opaque glazing proxy is not observed glass material.','No print or slicer test, no comprehensive self-intersection or minimum feature proof.','Source EXIF suggests 2006-12-07, independently unverified; not 2024/current.']};(R/'TRIAL-QA.json').write_text(json.dumps(report,indent=2))
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.background_type='WORLD';scene.world.color=(0.85,0.85,0.85);scene.render.resolution_x=1400;scene.render.resolution_y=900;scene.render.resolution_percentage=100
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=174;scene.camera=cam
for name,loc in [('front',(0,-280,23)),('oblique',(180,-280,160)),('artificial-back',(160,280,160))]:
 cam.location=loc;cam.rotation_euler=(Vector((0,0,23))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath='previews/'+name+'.png';bpy.ops.render.render(write_still=True)
# Standard 3MF: explicit millimetres and display-only material grouping.
import xml.etree.ElementTree as ET,zipfile
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
m=ET.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'})
ET.SubElement(m,'{'+ns+'}metadata',{'name':'Title'}).text='HFU Baizhang Historical Front Upper Study - NOT whole building'
res=ET.SubElement(m,'{'+ns+'}resources');palette=ET.SubElement(res,'{'+ns+'}basematerials',{'id':'1'})
for material in materials:
 colour=material.diffuse_color
 ET.SubElement(palette,'{'+ns+'}base',{'name':material.name,'displaycolor':'#'+''.join('%02X'%round(max(0,min(1,c))*255) for c in colour[:3])+'FF'})
obj=ET.SubElement(res,'{'+ns+'}object',{'id':'2','type':'model','name':base.name});mesh=ET.SubElement(obj,'{'+ns+'}mesh');vv=ET.SubElement(mesh,'{'+ns+'}vertices');tt=ET.SubElement(mesh,'{'+ns+'}triangles')
for v in base.data.vertices:ET.SubElement(vv,'{'+ns+'}vertex',dict(zip(('x','y','z'),(format(float(a),'.9g') for a in v.co))))
for poly in base.data.polygons:ET.SubElement(tt,'{'+ns+'}triangle',{'v1':str(poly.vertices[0]),'v2':str(poly.vertices[1]),'v3':str(poly.vertices[2]),'pid':'1','p1':str(poly.material_index),'p2':str(poly.material_index),'p3':str(poly.material_index)})
ET.SubElement(ET.SubElement(m,'{'+ns+'}build'),'{'+ns+'}item',{'objectid':'2'})
with zipfile.ZipFile(R/'model.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(m,encoding='utf-8',xml_declaration=True))
cam.location=(0,-280,23);cam.rotation_euler=(Vector((0,0,23))-cam.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath='//previews/front.png'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'scene.blend'))
exec(compile((R/'sanitize_metadata.py').read_text(),str(R/'sanitize_metadata.py'),'exec'),{'__file__':str(R/'sanitize_metadata.py')})
print(json.dumps(report))
