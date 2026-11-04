import bpy,json,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
P=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(P/'scene.blend'));rows=json.load(open(P/'BUILD-RECORD.json'))['parts'];NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',NS)
def E(tag,**a):return ET.Element('{'+NS+'}'+tag,a)
m=E('model',unit='millimeter');res=E('resources');m.append(res);base=E('basematerials',id='1');res.append(base);palette=[]
for r in rows:
 o=bpy.data.objects[r['id']]
 for mat in o.data.materials:
  c=tuple(mat.diffuse_color)
  if c not in palette:palette.append(c)
for i,c in enumerate(palette):base.append(E('base',name='Research source family or neutral proxy '+str(i),displaycolor='#'+''.join(f'{round(max(0,min(1,x))*255):02X}'for x in c)))
build=E('build');m.append(build)
for oid,r in enumerate(rows,2):
 o=bpy.data.objects[r['id']];obj=E('object',id=str(oid),type='model',name=r['id']);mesh=E('mesh');vs=E('vertices');ts=E('triangles');mesh.extend([vs,ts]);obj.append(mesh);res.append(obj)
 for v in o.data.vertices:vs.append(E('vertex',x=format(v.co.x,'.9g'),y=format(v.co.y,'.9g'),z=format(v.co.z,'.9g')))
 for f in o.data.polygons:ts.append(E('triangle',v1=str(f.vertices[0]),v2=str(f.vertices[1]),v3=str(f.vertices[2]),pid='1',p1=str(palette.index(tuple(o.data.materials[f.material_index].diffuse_color)))))
 build.append(E('item',objectid=str(oid)))
meta=E('metadata',name='Description');meta.text='Bounded nominal design research. 49 separate parts. Not physical fit or print approval. Unknown roof domains unbuilt.';m.insert(0,meta)
with zipfile.ZipFile(P/'model.3mf','w',zipfile.ZIP_DEFLATED)as z:
 def put(n,b):
  i=zipfile.ZipInfo(n,(2026,11,4,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
 put('[Content_Types].xml',b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 put('_rels/.rels',b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 put('3D/3dmodel.model',ET.tostring(m,encoding='utf-8',xml_declaration=True))
