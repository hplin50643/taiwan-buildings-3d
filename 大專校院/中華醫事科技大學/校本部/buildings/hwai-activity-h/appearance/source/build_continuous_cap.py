"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='6e1960bf13afe0f05ead516f8994e5fc83d220cd010d304b524a4a9231d020ee'
PALETTE=[('neutral_unresolved_envelope_and_base','#AAA79F'),('muted_blue_green_stair_tower_front_frames','#638A8B')]
import build_appearance as old
def classify(t):
 color,why=old.classify(t);assert np.bincount(color).tolist()==[3180,128];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];review=json.loads((Path(__file__).parent/'cap-domain.json').read_text())['candidate'];ids=[];eps=.0001
 for g in review['groups']:
  ax=g['axis'];lo=np.array(g['low_mm']);hi=np.array(g['high_mm']);hit=(abs(t[:,:,ax]-g['plane'])<eps).all(1)&(norm[:,ax]*g['normal_sign']>.99999)&(t>=lo-eps).all((1,2))&(t<=hi+eps).all((1,2));got=np.flatnonzero(hit).tolist();assert got==g['faces'] and len(got)==2 and(color[hit]==0).all();uv=np.unique(t[hit].reshape(-1,3),axis=0)[:,g['rectangle_axes']];other=g['rectangle_axes'][0];expected=np.array([[lo[other],56],[lo[other],57.8],[hi[other],56],[hi[other],57.8]]);assert np.max(abs(np.array(sorted(uv.tolist()))-np.array(sorted(expected.tolist()))))<eps;assert abs(float(np.linalg.norm(cross[hit],axis=1).sum()/2)-g['analytic_area_mm2'])<.00002;color[hit]=1;why[hit]='inferred_same_original_cap_vertical_returns_no_sidecheeks';ids+=got
 assert sorted(ids)==review['faces'] and np.bincount(color).tolist()==[3168,140]
 (A/'qa-continuous-cap/selection.json').write_text(json.dumps(dict(new_face_ids=sorted(ids),new_material=1,original128preserved=True,baseline_mixed_coplanar_groups_retained=2,no_new_mixed_coplanar_groups=True),indent=2)+'\n');return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-continuous-cap').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);np.savez_compressed(A/'mesh-data.npz',vertices=v,faces=f,materials=colors);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'HWAI H Student Activities Center limited original surface'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'hwai-activity-h-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
