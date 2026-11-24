"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='d333eef2bd3b2deeb6493fb582ff671d1c5004bb55424ebb84ed0e689b2526f6'
PALETTE=[(p['id'],p['srgb'])for p in json.loads((A/'palette.json').read_text())['materials']]
def classify(t):
 assert hashlib.sha256((Path(__file__).parent/'baseline-face-materials.json').read_bytes()).hexdigest()=='e2af3bf051fa0a66a55af7e0ad402225f66389efab174bb54de1a023156160d7'
 assert hashlib.sha256((Path(__file__).parent/'baseline-palette.json').read_bytes()).hexdigest()=='b61455413c0cb1aa16ff9453d6cd5ddcdf78a9a39ed2a086f0b0eb122b39ff16'
 assert (A/'palette.json').read_bytes()==(Path(__file__).parent/'baseline-palette.json').read_bytes()
 b=json.loads((Path(__file__).parent/'baseline-face-materials.json').read_text());color=np.array(b['face_material_indices']);why=np.array(b['face_reasons'],dtype=object);assert np.bincount(color).tolist()==[3646,162,288]
 v=t.copy();v[:,:,2]-=2;v/=150/62;cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];eps=3e-5
 hit=(abs(v[:,:,1]-10.2)<eps).all(1)&(norm[:,1]>.99999)&(v[:,:,0]>=17.5-eps).all(1)&(v[:,:,0]<=37+eps).all(1)&(v[:,:,2]>=-eps).all(1)&(v[:,:,2]<=7.5+eps).all(1)
 ids=np.flatnonzero(hit).tolist();assert ids==[3452,3453]and(color[hit]==0).all();uv=np.unique(v[hit].reshape(-1,3),axis=0)[:,[0,2]];assert np.max(abs(np.array(sorted(uv.tolist()))-np.array([[17.5,0],[17.5,7.5],[37,0],[37,7.5]])))<eps
 area=float(np.linalg.norm(cross[hit],axis=1).sum()/2);assert abs(area-19.5*7.5*(150/62)**2)<.0002
 color[hit]=1;why[hit]='inferred_same_distinct_east_lowwing_pink_north_wall_not_photographed_blank_geometry_proxy';assert np.bincount(color).tolist()==[3644,164,288]
 (A/'qa-continuous-lowwing/selection.json').write_text(json.dumps(dict(new_face_ids=ids,new_material=1,area_mm2=area,all_whole_vertices_checked=True,existing450colors_preserved=True,north_material_samewing_inference_not_observation=True,original_blank_proxy_not_proof_no_windows=True),indent=2)+'\n');return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-continuous-lowwing').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);np.savez_compressed(A/'mesh-data.npz',vertices=v,faces=f,materials=colors);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'Tajen A Administrative Library limited original surface'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'tajen-admin-library-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
