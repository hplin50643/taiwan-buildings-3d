from pathlib import Path
import numpy as np,json,hashlib,struct,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-column';Q.mkdir(exist_ok=True);raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='86fd4f37381c68e567d5c836d44dafa5bc2378bb05664480fee790693edd003f';count=struct.unpack_from('<I',raw,80)[0];assert count==11418
tri=np.array([struct.unpack_from('<9f',raw,96+50*i)for i in range(count)],np.float64).reshape(count,3,3);vertices=[];index={};faces=[]
for t in tri:
 face=[]
 for v in t:
  k=tuple(v)
  if k not in index:index[k]=len(vertices);vertices.append(k)
  face.append(index[k])
 faces.append(face)
v=np.array(vertices);f=np.array(faces);a=np.ones(count,np.int32)
# Exact prior front quarter domains, then only complete exposed shaft continuation.
t=tri;cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];review=json.loads((Path(__file__).parent/'column-domain.json').read_text())['candidate'];ids=[];eps=.0001
for g in review['existing_front_groups']+review['groups']:
 normal=np.array(g['normal_xy']);tangent=np.array(g['tangent_xy']);origin=np.array(g['origin_xy']);u0,u1=g['u_bounds_mm'];z0,z1=g['z_bounds_mm'];delta=t[:,:,:2]-origin;u=delta@tangent;hit=(abs(delta@normal)<eps).all(1)&(norm[:,:2]@normal>.99999)&(u>=u0-eps).all(1)&(u<=u1+eps).all(1)&(t[:,:,2]>=z0-eps).all(1)&(t[:,:,2]<=z1+eps).all(1)
 got=np.flatnonzero(hit).tolist();assert got==g['faces'] and len(got)==2 and (a[hit]==1).all();uv=np.column_stack(((v[np.unique(f[hit])][:,:2]-origin)@tangent,v[np.unique(f[hit])][:,2]));expected=np.array([[u0,z0],[u0,z1],[u1,z0],[u1,z1]]);assert np.max(abs(np.array(sorted(uv.tolist()))-np.array(sorted(expected.tolist()))))<eps;assert abs(float(np.linalg.norm(cross[hit],axis=1).sum()/2)-g['analytic_area_mm2'])<.00004;a[hit]=0
 if not g['already_colored']:ids+=got
assert sorted(ids)==review['faces'] and len(ids)==144 and np.bincount(a).tolist()==[240,11178]
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);pal=json.loads((R/'palette.json').read_text());ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
def el(p,t,**kw):return E.SubElement(p,'{'+ns+'}'+t,{k:str(x)for k,x in kw.items()})
m=E.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'});res=el(m,'resources');bm=el(res,'basematerials',id=1)
for name,color in pal:el(bm,'base',name=name,displaycolor=color+'FF')
o=el(res,'object',id=2,type='model',pid=1,pindex=1,name='CTU Library Humanities 2002 partial color');mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for p in v:el(vs,'vertex',x=repr(float(p[0])),y=repr(float(p[1])),z=repr(float(p[2])))
for face,ma in zip(f,a):el(ts,'triangle',v1=face[0],v2=face[1],v3=face[2],pid=1,p1=ma,p2=ma,p3=ma)
el(el(m,'build'),'item',objectid=2)
entries={'3D/3dmodel.model':E.tostring(m,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for name,data in sorted(entries.items()):
  zi=zipfile.ZipInfo(name,(2026,11,17,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16;z.writestr(zi,data)
(Q/'selection.json').write_text(json.dumps(dict(new_face_ids=sorted(ids),new_material=0,certainty='INFERRED_SAME_EXPOSED_COLUMN_SHAFT',original_colored_faces=96,total_colored_faces=240,all_original_geometry_retained=True),indent=2)+'\n')
