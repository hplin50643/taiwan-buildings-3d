"""Build the supplement from an unchanged repository appearance.3mf and scene.blend.
Usage: blender -b /path/to/scene.blend -t 2 --python-exit-code 1 \
       -P build_rear_lotus.py -- /path/to/appearance.3mf /output/directory
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
assert sha256(source.read_bytes()).hexdigest() == '295c7d00ae35a0847e6c286e1820e2550689a1ef9be2fcbcbdc8e49c8b6ecfe1'
assert sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == '0c5e55c42f668e5419980daf675f706aec808e784ed2f4408ccf96fc84c5a0bd'
assert [e.get('displaycolor') for e in palette] == ['#CDBFBCFF','#BEA65DFF','#55574FFF','#536A7CFF','#D5CEAFFF','#414B46FF','#A7ABA5FF']
v = np.array([[float(e.get(k)) for k in 'xyz'] for e in verts])
f = np.array([[int(e.get(k)) for k in keys] for e in tris])
before = [int(e.get('p1')) for e in tris]
p = v[f]
# Complete outward-facing planes of the existing rear lotus backing
# and ring only. The transform y -> 10-y comes from the original generator.
# Lateral return/recess surfaces and existing lattice are not touched.
normals=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0])
lo,hi=p.min(axis=1),p.max(axis=1)
def select(y):
    mask=((abs(p[:,:,1]-y)<.003).all(axis=1)&(normals[:,1]>0)&(lo[:,0]>=-11.001)&(hi[:,0]<=11.001)
            &(lo[:,2]>=46.999)&(hi[:,2]<=81.001))
    return np.flatnonzero(mask).tolist()
backing,ring=select(20.7),select(23.8)
assert len(backing)==191 and len(ring)==256 and not set(backing)&set(ring)
assert abs(normals[backing,1].sum()/2-313.53522554)<.001
assert abs(normals[ring,1].sum()/2-101.37587441)<.001
ids=sorted(backing+ring)
assert all(before[i]==6 for i in ids)
updates={i:3 for i in backing}|{i:1 for i in ring}
after=before.copy()
for i,m in updates.items(): after[i]=m
# Check the original whole coplanar domains against the old and new material
# vectors. Existing historical mixed domains must remain exactly the same.
nvect=normals/np.linalg.norm(normals,axis=1,keepdims=True)
parent=list(range(len(f)))
def root(k):
    while k!=parent[k]:
        parent[k]=parent[parent[k]]
        k=parent[k]
    return k
edges={}
for i,tri in enumerate(f):
    tri=tuple(tri)
    for a,b in zip(tri,tri[1:]+tri[:1]):
        q=tuple(sorted((a,b)))
        if q not in edges: edges[q]=i; continue
        j=edges[q]
        if np.dot(nvect[i],nvect[j])>.999999: parent[root(i)]=root(j)
groups={}
for i in range(len(f)): groups.setdefault(root(i),[]).append(i)
mix=lambda mats: [grp for grp in groups.values() if len({mats[i] for i in grp})>1]
oldmixed=mix(before)
assert mix(after)==oldmixed
assert all(len({i in updates for i in grp})==1 for grp in groups.values())
# Edit only the selected triangle tags, retain original serialization and all other members.
from re import sub
def patch(match):
    i = patch.counter
    patch.counter += 1
    tag = match[0]
    if i not in ids:
        return tag
    assert b' p1="6"' in tag
    assert b' p2=' not in tag and b' p3=' not in tag
    return tag.replace(b' p1="6"', f' p1="{updates[i]}"'.encode())
patch.counter = 0
modified = sub(rb'<triangle [^>]+/>', patch, original)
assert patch.counter == len(f)
final = out/'rear-lotus.3mf'
with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as arc:
    for member, data in contents.items():
        arc.writestr(zipfile.ZipInfo(member,date_time=(2020,1,1,0,0,0)), modified if member == part else data,compress_type=zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(final) as arc:
    assert arc.testzip() is None
    assert all(arc.read(name)==data for name,data in contents.items() if name!=part)
    reread=arc.read(part)
target = ET.fromstring(reread)
assert [e.attrib for e in target.findall('.//{*}base')]==[e.attrib for e in palette]
assert [e.attrib for e in target.findall('.//{*}vertex')] == [e.attrib for e in verts]
for i,(old,new) in enumerate(zip(tris,target.findall('.//{*}triangle'),strict=True)):
    expected=old.attrib.copy()
    if i in updates: expected['p1']=str(updates[i])
    assert new.attrib == expected
obj = bpy.context.scene.objects['Chung Tai Chan Monastery color appearance']
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
notice.data.body = '中台禪寺：依寺方日照照片補背面蓮窗底與外框；其他未證區保留。'
nv, nf, nm, nt=scene_state(obj)
delta=float(np.max(np.abs(np.array(nv)-v))); print("baseline exchange vs native max mm:",delta); assert delta < 0.00001
assert np.array_equal(nf,f) and nm==before
other = [(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
palette_blend = [(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in mesh.materials]
for i,m in updates.items(): mesh.polygons[i].material_index=m
assert scene_state(obj)==(nv,nf,after,nt)
blend=out/'rear-lotus.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
scene=bpy.context.scene
obj=scene.objects['Chung Tai Chan Monastery color appearance']
assert scene_state(obj)==(nv,nf,after,nt)
assert other==[(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
assert palette_blend==[(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in obj.data.materials]
receipt={'status':'PASS','vertices':len(v),'triangles':len(f),'changed_faces_per_material':dict(Counter(updates.values())),'selected_faces':ids,
 'bounds_model_mm':{'min':p[ids].reshape(-1,3).min(0).tolist(),'max':p[ids].reshape(-1,3).max(0).tolist()},
 'backing_faces':len(backing),'ring_faces':len(ring), 'inherited_mixed_domains_unchanged':len(oldmixed),'new_mixed_domains':0,'neutral_only':True,'palette_exactly_preserved':True,
 'material_counts_before':dict(sorted(Counter(before).items())),'material_counts_after':dict(sorted(Counter(after).items())),
 'exact_geometry_and_original_materials_preserved':True,'3mf_other_entries_identical':True,'native_vs_exchange_baseline_max_abs_mm':delta,
 'existing_full_faces_only':True,'count_delta':0}
(out/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
# Render paired previews at identical settings. This inspection-only camera
# is not stored in the exported .blend. No text or reference texture.
cam=scene.camera
cam.location=(78,305,123)
cam.rotation_euler=(Vector((0,0,63))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=213
scene.render.resolution_percentage=100
scene.render.resolution_x=900
scene.render.resolution_y=680
scene.cycles.samples=64
scene.cycles.use_denoising=False
scene.render.image_settings.file_format='PNG'
scene.render.use_stamp=False
qa=out/'_render_qa'
qa.mkdir(exist_ok=True)
for stem in ('candidate','baseline'):
    for i,m in updates.items(): obj.data.polygons[i].material_index=m if stem=='candidate' else 6
    scene.render.filepath=str(qa/(stem+'.png'))
    bpy.ops.render.render(write_still=True)
