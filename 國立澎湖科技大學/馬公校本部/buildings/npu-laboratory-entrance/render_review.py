from pathlib import Path
import bpy,json,struct,sys
from mathutils import Vector
D=Path(__file__).resolve().parent;V=D/'appearance-review-v3';V.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(D/'appearance.blend'));s=bpy.context.scene;o=next(o for o in s.objects if o.type=='MESH')
meta=json.loads((D/'appearance-materials.json').read_text())
views={'front':((145,-260,110),(0,-12,40.8),180),'rear':((-195,230,160),(0,-12,40.8),180),'elevation':((0,-260,40.8),(0,-12,40.8),180),'source-angle':((110,-260,18),(0,-12,47),180),'left':((-300,-12,95),(0,-12,40.8),180),'right':((300,-12,95),(0,-12,40.8),180),'top':((0,0,260),(0,-12,0),180)}
records=[];byname={}
def render(name,pos,target,path):
 c=s.camera;c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();inv=c.rotation_euler.to_matrix().transposed();v=[inv@(o.matrix_world@Vector(x)-c.location) for x in o.bound_box];c.data.ortho_scale=max(max(x.x for x in v)-min(x.x for x in v),(max(x.y for x in v)-min(x.y for x in v))*s.render.resolution_x/s.render.resolution_y)*1.18
 r={'view':name,'location':list(c.location),'rotation_euler':list(c.rotation_euler),'ortho_scale':c.data.ortho_scale,'target':list(target)}
 s.render.filepath=str(path);bpy.ops.render.render(write_still=True);d=path.read_bytes();out=d[:8];off=8
 while off<len(d):
  n=struct.unpack_from('>I',d,off)[0];typ=d[off+4:off+8]
  if typ not in (b'tEXt',b'zTXt',b'iTXt'):out+=d[off:off+n+12]
  off+=n+12
 path.write_bytes(out);return r
for name,(pos,target,_) in views.items():
 r=render(name,pos,target,D/'appearance'/(name+'.png'));records.append(r);byname[name]=r
(D/'render-cameras.json').write_text(json.dumps(records,indent=2))
for p,i in zip(o.data.polygons,meta['continuation_baseline_face_material_indices']):p.material_index=i
comps=[]
for name in ['front','rear']:
 pos,target,_=views[name];r=render(name,pos,target,V/('original-'+name+'.png'));assert r==byname[name];r['view']='original-'+name;r['same_camera_as']=name;comps.append(r)
(V/'comparison-camera-records.json').write_text(json.dumps(comps,indent=2));(V/'camera-consistency.json').write_text(json.dumps({'both_original_comparisons_match_repaired_camera_formulas_exactly':True,'render_settings_match':True,'method':'Exact location, Euler rotation and orthographic scale equality; same lighting and material values, only original face assignments restored.'},indent=2))
print('NINE_RENDER_DONE')
