"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='6a529f825d294ee1066af11a9202e2f55214a43a5c91959407cbfc0f9c24b290'
PALETTE=[('neutral_unresolved_envelope_and_base','#AAA79F'),('muted_red_brown_visible_low_wing_roof','#8C4847'),('muted_green_single_recess_glazing','#3D8D72'),('approximate_entry_front_brick_fascia','#A16457')]
import build_appearance as old
def classify(t):
 color,why=old.classify(t);assert np.bincount(color).tolist()==[4476,16,22,2]
 r=json.loads((Path(__file__).parent/'lowhiprear-domain.json').read_text());cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);eps=.00015
 mask=(abs(t[:,:,2]-71-(-5-t[:,:,1])*3.2/13.58)<eps).all(1)&(cross[:,1]>0)&(cross[:,2]>0)
 ids=np.flatnonzero(mask);assert ids.tolist()==r['changed_original_face_ids'];assert (color[ids]==0).all()
 # Source SHA fixes exact historical Boolean cuts; these are the entire original plane's two bounded islands.
 assert (t[ids,:,0]>=-67-eps).all() and(t[ids,:,0]<=-42+eps).all();assert(t[ids,:,1]>=-18.58-eps).all() and(t[ids,:,1]<=-5+eps).all();assert(t[ids,:,2]>=71-eps).all() and(t[ids,:,2]<=74.2+eps).all()
 assert abs(np.linalg.norm(cross[ids],axis=1).sum()/2-r['domain']['analytic_surface_area_mm2'])<.0001
 color[ids]=1;why[ids]='inferred_same_low_front_left_hip_rear_slope_two_bounded_exposed_islands'
 assert np.bincount(color).tolist()==[4468,24,22,2]
 (A/'qa-continuous-lowhiprear/selection.json').write_text(json.dumps(dict(new_face_ids=ids.tolist(),new_material=1,original40colored_preserved=True,whole_oriented_plane=True,two_complete_coplanar_islands=True,same_cap_hidden_inference=True),indent=2)+'\n')
 return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-continuous-lowhiprear').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);np.savez_compressed(A/'mesh-data.npz',vertices=v,faces=f,materials=colors);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'HWAI J Nursing Building limited original surface'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'hwai-nursing-j-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
