import bpy,zipfile,xml.etree.ElementTree as ET,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;p=P/'scene.blend';h=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(P/'model.3mf')as z:m=ET.fromstring(z.read('3D/3dmodel.model'))
colors=[b.attrib['displaycolor']for b in m.findall('m:resources/m:basematerials/m:base',ns)];rows=[]
for obj in m.findall('m:resources/m:object',ns):
 o=bpy.data.objects[obj.attrib['name']];fs=obj.findall('m:mesh/m:triangles/m:triangle',ns);assert len(fs)==len(o.data.polygons);bad=[]
 for i,(a,f)in enumerate(zip(fs,o.data.polygons)):
  c=o.data.materials[f.material_index].diffuse_color;expected='#'+''.join(f'{round(max(0,min(1,x))*255):02X}'for x in c)
  if colors[int(a.attrib['p1'])]!=expected:bad.append(i)
 rows.append({'id':obj.attrib['name'],'faces':len(fs),'exact_RGBA8_from_scene':not bad,'mismatched_faces':bad})
assert h==hashlib.sha256(p.read_bytes()).hexdigest();assert all(x['exact_RGBA8_from_scene']for x in rows)
(P/'THREEMF-MATERIAL-QA.json').write_text(json.dumps({'status':'PASS_ALL_49_FACE_PALETTE_BINDINGS','scene_sha256':h,'model_3mf_sha256':hashlib.sha256((P/'model.3mf').read_bytes()).hexdigest(),'colour_precision':'8bit RGBA quantized from scene diffuse color, not calibrated real material RGB','checks':rows,'readonly':True},indent=2)+'\n')
