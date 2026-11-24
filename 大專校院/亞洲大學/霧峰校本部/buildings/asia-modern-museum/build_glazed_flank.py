"""Build the supplement from an unchanged repository appearance.3mf and scene.blend.
Usage: blender -b /path/to/scene.blend -t 2 --python-exit-code 1 \
       -P build_glazed_flank.py -- /path/to/appearance.3mf /output/directory
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
assert sha256(source.read_bytes()).hexdigest() == 'f2af0a8729bdc8c113b8cb92fedc9a09df9eae09d99ac50643af8738b04040c5'
assert sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == 'b05a26b2b6e3b275553e0c7d707d7576473d034eb0983139005fbf586b43b0aa'
assert [e.get('displaycolor') for e in palette] == ['#BABDB4FF','#557974FF','#364744FF','#CBCDC4FF','#B7B9B3FF']
v = np.array([[float(e.get(k)) for k in 'xyz'] for e in verts])
f = np.array([[int(e.get(k)) for k in keys] for e in tris])
before = [int(e.get('p1')) for e in tris]
p = v[f]
# Reproduce the left edge of the original 2F glazing body after the 1.05 m
# triangular inset and the independent y>=14.25 m face clip.
def panel_ids(v, f, before):
    mid=np.array([[-29.8,8.0],[1.57,61.0],[32.17,7.81]])
    local_center=mid.mean(0)
    normal=[]; offset=[]
    for i,a in enumerate(mid):
        d=mid[(i+1)%3]-a
        iv=np.array([-d[1],d[0]])/np.linalg.norm(d)
        if (local_center-a)@iv<0: iv=-iv
        normal.append(iv); offset.append(a@iv+1.05)
    normal=np.array(normal); offset=np.array(offset)
    iv=normal[0]
    assert iv[0]>.8
    p=np.array([(offset[0]-iv[1]*14.25)/iv[0],14.25])
    q=np.linalg.solve(normal[:2],offset[:2]); L=np.linalg.norm(q-p)
    tv=(q-p)/L
    # Number of bays and height come from the existing parametric source.
    n=round(L/3.4); dz=(10.70-5.15)/6
    assert n==15, n
    x=v[f][:,:,:2]/2.15; x[:,:,1]+=29
    z=(v[f][:,:,2]-3)/2.15
    d=(x-p)@iv; a=(x-p)@tv
    b=np.array(before)
    result={}
    rows=[]
    for j in range(n):
        u,w=j*L/n+.18,(j+1)*L/n-.18
        groups=[]
        for k in range(6):
            z0,z1=5.15+k*dz+.13,5.15+(k+1)*dz-.13
            bounded=(a.min(1)>=u-.003)&(a.max(1)<=w+.003)&(z.min(1)>=z0-.003)&(z.max(1)<=z1+.003)&(d.min(1)>=-.005)&(d.max(1)<=.181)
            backs=bounded&(d.min(1)>=.095)
            ret=bounded&~backs
            groups.append([Counter(b[backs]),Counter(b[ret])])
            if 2<=j<=6:
                for ids, m in [(np.flatnonzero(backs),1),(np.flatnonzero(ret),2)]:
                    for i in ids:
                        result[int(i)]=m
        rows.append(groups)
    return result,rows

updates, rows = panel_ids(v,f,before)
for j in range(2,7):
    for k in range(6):
        assert rows[j][k]==[Counter({4:2}),Counter({4:8 if k<5 else 6})]
for j in range(2):
    for k in range(6):
        assert rows[j][k]==[Counter({1:2}),Counter({2:8 if k<5 else 6})]
assert len(updates)==290 and Counter(updates.values())=={1:60,2:230}
ids=sorted(updates)
after=before.copy()
for i,m in updates.items(): after[i]=m
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
    return tag.replace(b' p1="4"', f' p1="{updates[i]}"'.encode())
patch.counter = 0
modified = sub(rb'<triangle [^>]+/>', patch, original)
assert patch.counter == len(f)
final = out/'glazed-flank.3mf'
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
obj = bpy.context.scene.objects['Asia Modern Museum color']
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
notice.data.body = '亞洲大學附屬現代美術館：2樓左側五開間補色；其他未證區保留。'
nv, nf, nm, nt=scene_state(obj)
delta=float(np.max(np.abs(np.array(nv)-v))); print("baseline exchange vs native max mm:",delta); assert delta < 0.000005
assert np.array_equal(nf,f) and nm==before
other = [(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
palette_blend = [(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in mesh.materials]
for i,m in updates.items(): mesh.polygons[i].material_index=m
assert scene_state(obj)==(nv,nf,after,nt)
blend=out/'glazed-flank.blend'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
scene=bpy.context.scene
obj=scene.objects['Asia Modern Museum color']
assert scene_state(obj)==(nv,nf,after,nt)
assert other==[(o.name, o.type, tuple(tuple(r) for r in o.matrix_world), o.hide_render) for o in scene.objects]
assert palette_blend==[(mat.name, tuple(mat.diffuse_color),tuple(mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value)) for mat in obj.data.materials]
receipt={'status':'PASS','vertices':len(v),'triangles':len(f),'changed_faces_per_material':dict(Counter(updates.values())),'selected_faces':ids,
 'bounds_model_mm':{'min':p[ids].reshape(-1,3).min(0).tolist(),'max':p[ids].reshape(-1,3).max(0).tolist()},
 'recolored_existing_panel_recesses':30,'neutral_only':True,'palette_exactly_preserved':True,
 'material_counts_before':dict(sorted(Counter(before).items())),'material_counts_after':dict(sorted(Counter(after).items())),
 'exact_geometry_and_original_materials_preserved':True,'3mf_other_entries_identical':True,'native_vs_exchange_baseline_max_abs_mm':delta,
 'existing_full_faces_only':True,'count_delta':0}
(out/'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
# Render paired previews at identical settings. This inspection-only camera
# is not stored in the exported .blend. No text or reference texture.
cam=scene.camera
cam.location=(-310,95,120)
cam.rotation_euler=(Vector((0,0,15))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=218
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
    for i,m in updates.items(): obj.data.polygons[i].material_index=m if stem=='candidate' else 4
    scene.render.filepath=str(qa/(stem+'.png'))
    bpy.ops.render.render(write_still=True)
