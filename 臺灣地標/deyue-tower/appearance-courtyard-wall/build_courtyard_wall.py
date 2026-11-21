"""Build the supplement from an unchanged repository appearance.3mf and scene.blend.
Usage: blender -b /path/to/scene.blend -t 2 --python-exit-code 1 \
       -P build_courtyard_wall.py -- /path/to/appearance.3mf /output/directory
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json, sys, zipfile, xml.etree.ElementTree as ET
import bpy, numpy as np
from mathutils import Vector
source, out = map(Path, sys.argv[sys.argv.index('--')+1:])
out = out.resolve()
out.mkdir(parents=True, exist_ok=True)
part = '3D/3dmodel.model'
with zipfile.ZipFile(source) as archive:
    contents = {name: archive.read(name) for name in archive.namelist()}
original = contents[part]
root = ET.fromstring(original)
verts = root.findall('.//{*}vertex')
tris = root.findall('.//{*}triangle')
keys = ('v1', 'v2', 'v3')
palette = root.findall('.//{*}base')
assert sha256(source.read_bytes()).hexdigest() == '9acc549e4a1069dc85a1d1bece21e6d90e20f7a8461079468dc07aa8440d3134'
assert sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == '31e14614c443118714e8b27ae3781f01755b974339868594673caae1c758de4b'
assert [e.get('displaycolor') for e in palette] == ['#C8B3B0FF','#D9D4BDFF','#485B6BFF','#404942FF','#A7ABA5FF']
v = np.array([[float(e.get(k)) for k in 'xyz'] for e in verts])
f = np.array([[int(e.get(k)) for k in keys] for e in tris])
before = [int(e.get('p1')) for e in tris]
p = v[f]
normals = np.cross(p[:,1]-p[:,0], p[:,2]-p[:,0])
close = lambda arr, val: np.isclose(arr, val, atol=0.0001, rtol=0)
# Broad courtyard-facing rectangular shaft field below the upper belt.
# All three vertices must lie on the original +Y wall plane and the whole
# original face must be between the two molding bands. Do not classify recess
# returns, recess bottoms, pilasters, ornament, roof, or an adjacent wall.
rear_plane = close(p[:,:,1],20).all(axis=1) & (normals[:,1]>0)
lo,hi = p.min(axis=1),p.max(axis=1)
within = (lo[:,0] >= -18.4001) & (hi[:,0] <= 18.4001) & (lo[:,2] >= 17.5499) & (hi[:,2] <= 91.1001)
ids=np.flatnonzero(rear_plane & within).tolist()
assert not (rear_plane & (lo[:,2] < 91.0999) & (hi[:,2] > 91.1001)).any()
assert not (rear_plane & (lo[:,2] < 17.5499) & (hi[:,2] > 17.5501)).any()
assert len(ids)==155
area=float(normals[ids,1].sum()/2)
assert abs(area-2449.1760842433173)<.00001
assert all(before[i]==4 for i in ids)
new_name='Courtyard shaft pink gray (documented, undated finish)'
new_hex='#C3ABAA'
after = before.copy()
for i in ids: after[i] = 5
# Edit only the selected triangle tags, retain original serialization and all other members.
from re import sub
def patch(match):
    i = patch.counter
    patch.counter += 1
    tag = match[0]
    if i not in ids:
        return tag
    assert b' p1="4"' in tag
    assert b' p2=' not in tag and b' p3=' not in tag
    return tag.replace(b' p1="4"', b' p1="5"')
patch.counter = 0
modified = sub(rb'<triangle [^>]+/>', patch, original)
assert patch.counter == len(f)
assert modified.count(b'</basematerials>') == 1
modified = modified.replace(b'</basematerials>', f'<base name="{new_name}" displaycolor="{new_hex}FF" /></basematerials>'.encode())
final = out/'courtyard-wall.3mf'
with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as arc:
    for member, data in contents.items():
        arc.writestr(member, modified if member == part else data,compress_type=zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(final) as arc:
    assert arc.testzip() is None
    assert all(arc.read(name)==data for name,data in contents.items() if name!=part)
    reread=arc.read(part)
target = ET.fromstring(reread)
assert [e.attrib for e in target.findall('.//{*}base')] == [e.attrib for e in palette]+[{'name':new_name,'displaycolor':new_hex+'FF'}]
assert [e.attrib for e in target.findall('.//{*}vertex')] == [e.attrib for e in verts]
for i,(old,new) in enumerate(zip(tris,target.findall('.//{*}triangle'),strict=True)):
    expected=old.attrib.copy()
    if i in ids: expected['p1']='5'
    assert new.attrib == expected
obj = bpy.context.scene.objects['Kinmen Deyue Tower color appearance']
mesh=obj.data
def scene_state(obj):
    return (
        [tuple(vert.co) for vert in obj.data.vertices],
        [tuple(poly.vertices) for poly in obj.data.polygons],
        [poly.material_index for poly in obj.data.polygons],
        [tuple(row) for row in obj.matrix_world],
    )
scene = bpy.context.scene
assert not bpy.data.libraries and not bpy.data.texts and not bpy.data.movieclips
assert all(not im.filepath and not im.packed_file and im.type=='RENDER_RESULT' for im in bpy.data.images)
assert all(not o.hide_render for o in [obj])
notice = scene.objects['HISTORICAL_SCHEME_NOTICE_NOT_PRINT_GEOMETRY']
assert notice.hide_render and scene.objects['NOTICE_BACKDROP_NOT_PRINT_GEOMETRY'].hide_render
notice.data.body = '得月樓：正面沿用既有配色；補庭院側原有主牆面。\n庭院實景色僅為參考，不代表修後實況。'
nv, nf, nm, nt=scene_state(obj)
delta=float(np.max(np.abs(np.array(nv)-v))); print("baseline exchange vs native max mm:",delta); assert delta < 0.000005
assert np.array_equal(nf,f) and nm==before
other = [(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
palette_blend = [(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in mesh.materials]
material=mesh.materials[4].copy()
material.name=new_name
srgb=tuple(int(new_hex[i:i+2],16)/255 for i in (1,3,5))
linear=tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in srgb)
material.diffuse_color=(*linear,1)
material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*linear,1)
mesh.materials.append(material)
for i in ids: mesh.polygons[i].material_index=5
assert scene_state(obj)==(nv,nf,after,nt)
blend=out/'courtyard-wall.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
scene=bpy.context.scene
obj=scene.objects['Kinmen Deyue Tower color appearance']
assert scene_state(obj)==(nv,nf,after,nt)
assert other==[(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
assert palette_blend==[(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in list(obj.data.materials)[:5]]
assert len(obj.data.materials)==6
new_material=obj.data.materials[5]
assert new_material.name==new_name
assert np.allclose(new_material.diffuse_color,(*linear,1),atol=1e-8,rtol=0)
assert np.allclose(new_material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value,(*linear,1),atol=1e-8,rtol=0)
receipt={'added_material':{'index':5,'name':new_name,'sRGB':new_hex},'status':'PASS','vertices':len(v),'triangles':len(f),'selected_faces':ids,
 'bounds_model_mm':{'min':p[ids].reshape(-1,3).min(0).tolist(),'max':p[ids].reshape(-1,3).max(0).tolist()},
 'material_counts_before':dict(sorted(Counter(before).items())),
 'material_counts_after':dict(sorted(Counter(after).items())),
 'exact_geometry_and_original_materials_preserved':True,'3mf_other_entries_identical':True,'native_vs_exchange_baseline_max_abs_mm':delta,
 'surface_area_mm2':area,'existing_full_faces_only':True,'count_delta':0}
(out/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
# Render paired previews at identical settings. This inspection-only camera
# is not stored in the exported .blend. No text or reference texture.
cam=scene.camera
cam.location=(-62,312,147)
cam.rotation_euler=(Vector((0,0,76))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=180
scene.render.resolution_percentage=100
scene.render.resolution_x=760
scene.render.resolution_y=760
scene.cycles.samples=96
scene.cycles.use_denoising=False
scene.render.image_settings.file_format='PNG'
scene.render.use_stamp=False
qa=out/'_render_qa'
qa.mkdir(exist_ok=True)
for stem, label in (('candidate',5),('baseline',4)):
    for i in ids: obj.data.polygons[i].material_index=label
    scene.render.filepath=str(qa/(stem+'.png'))
    bpy.ops.render.render(write_still=True)
