"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='e0ea088d1f0731101ec94be59c75105435bcfb5ba3c80fc0429eec612dbc6b3e'
PALETTE=[(p['id'],p['srgb'])for p in json.loads((A/'palette.json').read_text())['materials']]
def classify(t):
 assert hashlib.sha256((Path(__file__).parent/'baseline-face-materials.json').read_bytes()).hexdigest()=='cca02a346666007939b2d0f03b965d12a1609239858a4937d78a3bf01d9fb3ac'
 assert hashlib.sha256((Path(__file__).parent/'baseline-palette.json').read_bytes()).hexdigest()=='41b317988ff969822603ae2d5d26b37a9a548ec9e2ed455f8cfdc8303c5bd97c'
 assert (A/'palette.json').read_bytes()==(Path(__file__).parent/'baseline-palette.json').read_bytes()
 b=json.loads((Path(__file__).parent/'baseline-face-materials.json').read_text());color=np.array(b['face_material_indices']);why=np.array(b['face_reasons'],dtype=object);assert np.bincount(color).tolist()==[4662,80,36,144]
 cr=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cr/np.linalg.norm(cr,axis=1)[:,None];groups=[];allids=[];eps=.0001
 for angle in [-165,-135,-105,-75,-45,-15]:
  a=np.deg2rad(angle);rad=np.array([np.cos(a),np.sin(a),0]);tan=np.array([-np.sin(a),np.cos(a),0]);rr=t@rad;u=t@tan;z=t[:,:,2];hit=(abs(rr-45.4)<eps).all(1)&(abs(u)<=5.8+eps).all(1)&(z>=3-eps).all(1)&(z<=11.3+eps).all(1)&(norm@rad<-.99999);ids=np.flatnonzero(hit).tolist();assert len(ids)==2 and(color[hit]==0).all();pts=np.unique(t[hit].reshape(-1,3),axis=0);uv=np.c_[pts@tan,pts[:,2]];assert len(uv)==4 and np.max(abs(np.array(sorted(uv.tolist()))-np.array([[-5.8,3],[-5.8,11.3],[5.8,3],[5.8,11.3]])))<eps
  area=float(np.linalg.norm(cr[hit],axis=1).sum()/2);assert abs(area-96.28)<.0001;color[hit]=2;why[hit]='inferred_same_original_gray_plinth_inward_vertical_face_not_toplip_or_pale_pier';allids+=ids;groups.append(dict(angle=angle,faces=ids,area_mm2=area,analytic_area_mm2=96.28))
 assert sorted(allids)==[1858,1861,1892,1893,1925,1927,1958,1959,1988,1989,2022,2023];assert np.bincount(color).tolist()==[4650,80,48,144]
 (A/'qa-continuous-plinth/selection.json').write_text(json.dumps(dict(new_face_ids=sorted(allids),new_material=2,groups=groups,original260colors_preserved=True,same_plinth_inward_face_inference=True,toplip_and_pale_upper_pier_unchanged=True),indent=2)+'\n');return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-continuous-plinth').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);np.savez_compressed(A/'mesh-data.npz',vertices=v,faces=f,materials=colors);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'NPU Library rotunda bounded original plinth continuation'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'npu-library-rotunda-front-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
