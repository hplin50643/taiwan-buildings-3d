from pathlib import Path
import numpy as np,json,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parent;d=np.load(R/'color-mesh.npz');pal=json.loads((R/'palette.json').read_text());N='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',N)
def el(parent,tag,**attrs):return E.SubElement(parent,'{'+N+'}'+tag,{k:str(v) for k,v in attrs.items()})
m=E.Element('{'+N+'}model',{'unit':'millimeter','xml:lang':'en-US'});r=el(m,'resources');bas=el(r,'basematerials',id=1)
for name,col in pal:el(bas,'base',name=name,displaycolor=col+'FF')
o=el(r,'object',id=2,type='model',name='HKU P Comprehensive Teaching partial color');mesh=el(o,'mesh');vs=el(mesh,'vertices')
for x,y,z in d['vertices']:el(vs,'vertex',x=f'{x:.8f}',y=f'{y:.8f}',z=f'{z:.8f}')
ts=el(mesh,'triangles')
for f,ma in zip(d['faces'],d['materials']):el(ts,'triangle',v1=int(f[0]),v2=int(f[1]),v3=int(f[2]),pid=1,p1=int(ma))
b=el(m,'build');el(b,'item',objectid=2)
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('3D/3dmodel.model',E.tostring(m,encoding='utf-8',xml_declaration=True));z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>');z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
print('3MF exported')
