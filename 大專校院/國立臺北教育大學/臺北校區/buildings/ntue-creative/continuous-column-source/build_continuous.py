from pathlib import Path
import numpy as np,json,hashlib,struct,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-column';Q.mkdir(exist_ok=True);raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='426e2c3e64698c69cba3ae8221e358dc77645d6d1377e134edb196035bdc7282';count=struct.unpack_from('<I',raw,80)[0];assert count==1642
tri=np.array([struct.unpack_from('<9f',raw,96+50*i)for i in range(count)],np.float64).reshape(count,3,3);vertices=[];index={};faces=[]
for t in tri:
 face=[]
 for v in t:
  k=tuple(v)
  if k not in index:index[k]=len(vertices);vertices.append(k)
  face.append(index[k])
 faces.append(face)
v=np.array(vertices);f=np.array(faces);a=np.ones(count,np.int32)
review=json.loads((Path(__file__).parent/'column-domain.json').read_text());a[review['original_dark_ids']]=0;a[review['original_pale_ids']]=2;ids=review['selected_faces'];assert len(ids)==72 and(a[ids]==1).all()
for g in review['domains']:
 ax=g['axis'];ot=g['other_axis'];l,h=g['span'];z0,z1=g['z'];hit=(abs(tri[:,:,ax]-g['plane'])<1e-4).all(1)&(tri[:,:,ot]>=l-1e-4).all(1)&(tri[:,:,ot]<=h+1e-4).all(1)&(tri[:,:,2]>=z0-1e-4).all(1)&(tri[:,:,2]<=z1+1e-4).all(1);assert np.flatnonzero(hit).tolist()==g['faces'];area=np.linalg.norm(np.cross(tri[hit,1]-tri[hit,0],tri[hit,2]-tri[hit,0]),axis=1).sum()/2;assert abs(area-g['analytic_area_mm2'])<.00012
 # Original holed side triangulation retained exactly; missing contact faces never generated.
a[ids]=2;assert np.bincount(a).tolist()==[36,1526,80]
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);pal=json.loads((R/'palette.json').read_text());ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
def el(p,t,**kw):return E.SubElement(p,'{'+ns+'}'+t,{k:str(x)for k,x in kw.items()})
m=E.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'});res=el(m,'resources');bm=el(res,'basematerials',id=1)
for name,color in pal:el(bm,'base',name=name,displaycolor=color+'FF')
o=el(res,'object',id=2,type='model',pid=1,pindex=1,name='NTUE Creative partial color');mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for p in v:el(vs,'vertex',x=repr(float(p[0])),y=repr(float(p[1])),z=repr(float(p[2])))
for face,ma in zip(f,a):el(ts,'triangle',v1=face[0],v2=face[1],v3=face[2],pid=1,p1=ma,p2=ma,p3=ma)
el(el(m,'build'),'item',objectid=2)
entries={'3D/3dmodel.model':E.tostring(m,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for name,data in sorted(entries.items()):
  zi=zipfile.ZipInfo(name,(2026,11,17,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16;z.writestr(zi,data)
(Q/'selection.json').write_text(json.dumps(dict(new_face_ids=sorted(ids),new_material=2,certainty='INFERRED_SAME_EXPOSED_COLUMN_SHAFT',original_colored_faces=44,total_colored_faces=116,all_original_geometry_retained=True),indent=2)+'\n')
