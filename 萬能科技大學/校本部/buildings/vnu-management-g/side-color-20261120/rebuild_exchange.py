"""Deterministic output from untouched original binary STL and verified wall domain."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as E
import numpy as np
import sys
D=Path(__file__).resolve().parent; input_path=Path(sys.argv[1]) if len(sys.argv)>1 else D.parent/'model.stl'
raw=input_path.read_bytes(); domain=json.loads((D/'domain.json').read_text()); assert hashlib.sha256(raw).hexdigest()==domain['original_stl_sha256']
t=np.frombuffer(raw,dtype=np.dtype([('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')]),offset=84)['v']; assert len(t)==1714
v,ix=np.unique(t.reshape(-1,3),axis=0,return_inverse=True); f=ix.reshape(-1,3); assert np.array_equal(v[f],t)
ids=[i for i,row in enumerate(t) if all(x==66 for x in row[:,0])];assert ids==domain['ids']
mi=np.zeros(len(t),dtype=int);mi[ids]=1
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
def el(n,**a):return E.Element('{'+ns+'}'+n,{k:str(x) for k,x in a.items()})
# Neutral original diffuse linear (.69,.64,.54) retained; equivalent8-bit sRGB for3MF display.
conv=lambda x:round(255*(1.055*x**(1/2.4)-.055))
neutral='#'+''.join(f'{conv(x):02X}' for x in [.69,.64,.54]);pal=[{'name':'Warm stone preview only','color':neutral},{'name':'VNU G right wall sand beige; uncalibrated','color':'#B5A075'}]
r=el('model',unit='millimeter');res=el('resources');r.append(res);bg=el('basematerials',id=1);res.append(bg)
for x in pal:bg.append(el('base',name=x['name'],displaycolor=x['color']+'FF'))
o=el('object',id=2,type='model',name='VNU Management Building G partial color');res.append(o);mesh=el('mesh');o.append(mesh);vs=el('vertices');ts=el('triangles');mesh.extend([vs,ts])
for x in v:vs.append(el('vertex',**dict(zip('xyz',map(repr,map(float,x))))))
for ff,mm in zip(f,mi):ts.append(el('triangle',v1=ff[0],v2=ff[1],v3=ff[2],pid=1,p1=mm,p2=mm,p3=mm))
b=el('build');b.append(el('item',objectid=2));r.append(b)
ct='<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
rels='<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
with zipfile.ZipFile(D/'model-colored.3mf','w',zipfile.ZIP_DEFLATED) as z:
 for name,data in [('[Content_Types].xml',ct),('_rels/.rels',rels),('3D/3dmodel.model',E.tostring(r,encoding='utf-8',xml_declaration=True))]:
  info=zipfile.ZipInfo(name,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
(D/'palette.json').write_text(json.dumps(pal,indent=2)+'\n')
print(pal)
