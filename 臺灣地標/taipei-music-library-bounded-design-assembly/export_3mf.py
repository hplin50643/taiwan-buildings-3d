from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,hashlib
ROOT=Path(__file__).resolve().parent
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',NS)
def e(tag,**a):return ET.Element('{'+NS+'}'+tag,{k:str(v)for k,v in a.items()})
def main(root=ROOT):
 d=json.loads((root/'inputs/physical-meshes.json').read_text());m=e('model',unit='millimeter');m.set('{http://www.w3.org/XML/1998/namespace}lang','en-US');res=e('resources');m.append(res);build=e('build');m.append(build)
 for i,o in enumerate(d['objects'],1):
  obj=e('object',id=i,type='model',name=o['id']);res.append(obj);mesh=e('mesh');obj.append(mesh);v=e('vertices');mesh.append(v);t=e('triangles');mesh.append(t)
  for q in o['vertices_mm']:v.append(e('vertex',x=format(q[0],'.17g'),y=format(q[1],'.17g'),z=format(q[2],'.17g')))
  for a,b,c in o['triangles']:t.append(e('triangle',v1=a,v2=b,v3=c))
  build.append(e('item',objectid=i,transform='1 0 0 0 1 0 0 0 1 0 0 0'))
 content=b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
 rel=b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
 with zipfile.ZipFile(root/'assembly.3mf','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for name,data in [('[Content_Types].xml',content),('_rels/.rels',rel),('3D/3dmodel.model',ET.tostring(m,encoding='utf-8',xml_declaration=True))]:
   zi=zipfile.ZipInfo(name,date_time=(2026,11,4,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,data)
 with zipfile.ZipFile(root/'assembly.3mf')as z:
  rt=ET.fromstring(z.read('3D/3dmodel.model'));assert rt.attrib['unit']=='millimeter'
  for expected,actual in zip(d['objects'],rt.find('{'+NS+'}resources')):
   vv=[[float(v.attrib[k])for k in ['x','y','z']]for v in actual.find('{'+NS+'}mesh/{'+NS+'}vertices')];ff=[[int(t.attrib[k])for k in ['v1','v2','v3']]for t in actual.find('{'+NS+'}mesh/{'+NS+'}triangles')];assert vv==expected['vertices_mm'];assert ff==expected['triangles']
 return {'objects':len(d['objects']),'triangles':sum(len(o['triangles'])for o in d['objects']),'millimetres':True,'all_vertices_faces_ordered_exact':True,'sha256':hashlib.sha256((root/'assembly.3mf').read_bytes()).hexdigest()}
if __name__=='__main__':(ROOT/'3MF-READBACK.json').write_text(json.dumps(main(),indent=2)+'\n')
