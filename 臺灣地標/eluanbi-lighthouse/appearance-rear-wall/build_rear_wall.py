"""Build the supplement from an unchanged repository appearance.3mf and scene.blend.
Usage: blender -b /path/to/scene.blend -t 2 --python-exit-code 1 \
       -P build_rear_wall.py -- /path/to/appearance.3mf /output/directory
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
assert [e.get('displaycolor') for e in palette] == ['#D8DBD5FF', '#454945FF', '#303837FF', '#B8BAB6FF']
v = np.array([[float(e.get(k)) for k in 'xyz'] for e in verts])
f = np.array([[int(e.get(k)) for k in keys] for e in tris])
before = [int(e.get('p1')) for e in tris]
p = v[f]
normals = np.cross(p[:,1]-p[:,0], p[:,2]-p[:,0])
close = lambda arr, val: np.isclose(arr, val, atol=0.0001, rtol=0)
# Whole existing courtyard-facing rear side; exclude outer wall and the
# separate x=-68..-67.8 disconnected return beyond the western corner.
ids = np.flatnonzero(close(p[:,:,1], 42.7).all(axis=1) & (normals[:,1] < 0) &
   (p[:,:,0].min(axis=1) >= -66.2001) & (p[:,:,0].max(axis=1) <= 56.0001) &
   (p[:,:,2].min(axis=1) >= 3.7999) & (p[:,:,2].max(axis=1) <= 9.0001)).tolist()
assert ids == [9543, 9544] and all(before[i] == 3 for i in ids)
assert len(set(f[ids[0]]) & set(f[ids[1]])) == 2
assert np.allclose(p[ids].reshape(-1,3).min(0), [-66.2,42.7,3.8],atol=0.0001,rtol=0)
assert np.allclose(p[ids].reshape(-1,3).max(0), [56,42.7,9],atol=0.0001,rtol=0)
assert abs(np.linalg.norm(normals[ids],axis=1).sum()/2 - (56+66.2)*(9-3.8)) < .001
after = before.copy()
for i in ids:
    after[i] = 0
# Edit only the selected triangle tags, retain original serialization and all other members.
from re import sub
def patch(match):
    i = patch.counter
    patch.counter += 1
    tag = match[0]
    if i not in ids:
        return tag
    assert b' p1="3"' in tag
    assert b' p2=' not in tag and b' p3=' not in tag
    return tag.replace(b' p1="3"', b' p1="0"')
patch.counter = 0
modified = sub(rb'<triangle [^>]+/>', patch, original)
assert patch.counter == len(f)
final = out/'rear-wall.3mf'
with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as arc:
    for member, data in contents.items():
        arc.writestr(member, modified if member == part else data)
with zipfile.ZipFile(final) as arc:
    assert arc.testzip() is None
    assert all(arc.read(name)==data for name,data in contents.items() if name!=part)
    reread=arc.read(part)
target = ET.fromstring(reread)
assert [e.attrib for e in target.findall('.//{*}base')] == [e.attrib for e in palette]
assert [e.attrib for e in target.findall('.//{*}vertex')] == [e.attrib for e in verts]
for i,(old,new) in enumerate(zip(tris,target.findall('.//{*}triangle'),strict=True)):
    expected=old.attrib.copy()
    if i in ids: expected['p1']='0'
    assert new.attrib == expected
obj = bpy.context.scene.objects['Eluanbi Lighthouse color appearance']
mesh=obj.data
def scene_state(obj):
    return (
        [tuple(vert.co) for vert in obj.data.vertices],
        [tuple(poly.vertices) for poly in obj.data.polygons],
        [poly.material_index for poly in obj.data.polygons],
        [tuple(row) for row in obj.matrix_world],
    )
scene = bpy.context.scene
nv, nf, nm, nt=scene_state(obj)
delta=float(np.max(np.abs(np.array(nv)-v))); print("baseline exchange vs native max mm:",delta); assert delta < 0.000001
assert np.array_equal(nf,f) and nm==before
other = [(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
palette_blend = [(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in mesh.materials]
for i in ids: mesh.polygons[i].material_index=0
assert scene_state(obj)==(nv,nf,after,nt)
blend=out/'rear-wall.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
scene=bpy.context.scene
obj=scene.objects['Eluanbi Lighthouse color appearance']
assert scene_state(obj)==(nv,nf,after,nt)
assert other==[(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
assert palette_blend==[(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in obj.data.materials]
receipt={'status':'PASS','vertices':len(v),'triangles':len(f),'selected_faces':ids,
 'bounds_model_mm':{'min':p[ids].reshape(-1,3).min(0).tolist(),'max':p[ids].reshape(-1,3).max(0).tolist()},
 'material_counts_before':dict(sorted(Counter(before).items())),
 'material_counts_after':dict(sorted(Counter(after).items())),
 'exact_geometry_and_palette_preserved':True,'3mf_other_entries_identical':True,'native_vs_exchange_baseline_max_abs_mm':delta,
 'existing_full_faces_only':True,'count_delta':0}
(out/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
# Render paired previews at identical settings. This inspection-only camera
# is not stored in the exported .blend. No text or reference texture.
cam=scene.camera
cam.location=(103,-209,148)
cam.rotation_euler=(Vector((-14,4,38))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=218
scene.render.resolution_x=960
scene.render.resolution_y=720
scene.cycles.samples=32
scene.render.image_settings.file_format='PNG'
scene.render.use_stamp=False
qa=out.parent/'qa'
qa.mkdir(exist_ok=True)
for stem, label in (('candidate',0),('baseline',3)):
    for i in ids: obj.data.polygons[i].material_index=label
    scene.render.filepath=str(qa/(stem+'.png'))
    bpy.ops.render.render(write_still=True)
