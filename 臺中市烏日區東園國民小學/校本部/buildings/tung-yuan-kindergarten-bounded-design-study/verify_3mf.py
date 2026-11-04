import json,zipfile,struct,hashlib,xml.etree.ElementTree as ET,numpy as np
from pathlib import Path
P=Path(__file__).resolve().parent;ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
with zipfile.ZipFile(P/'model.3mf')as z:
 assert z.testzip()is None;m=ET.fromstring(z.read('3D/3dmodel.model'));assert m.attrib['unit']=='millimeter'
 rows=[]
 for o in m.findall('m:resources/m:object',ns):
  v=np.array([[float(x.attrib[k])for k in ['x','y','z']]for x in o.findall('m:mesh/m:vertices/m:vertex',ns)],dtype=np.float32);fs=np.array([[int(x.attrib[k])for k in ['v1','v2','v3']]for x in o.findall('m:mesh/m:triangles/m:triangle',ns)]);b=(P/'parts'/(o.attrib['name']+'.stl')).read_bytes();t=np.array([struct.unpack_from('<12fH',b,84+i*50)[3:12]for i in range(struct.unpack_from('<I',b,80)[0])],dtype=np.float32).reshape(-1,3,3);assert np.array_equal(v[fs],t);rows.append({'part':o.attrib['name'],'triangles':len(t),'ordered_float32_STL_exact':True})
 assert len(rows)==49
(P/'THREEMF-QA.json').write_text(json.dumps({'status':'PASS_49_SEPARATE_OBJECTS_ORDERED_STL','unit':'millimeter','sha256':hashlib.sha256((P/'model.3mf').read_bytes()).hexdigest(),'parts':rows,'not_print_or_physical_assembly_approval':True},indent=2)+'\n')
