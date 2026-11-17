from pathlib import Path
import numpy as np,json,hashlib,struct,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-caprim';Q.mkdir(exist_ok=True);raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='167ad46cb6da38ceb84ef62dfedabc8aac461d8581357f96f51047168e833a94';count=struct.unpack_from('<I',raw,80)[0];assert count==9662
tri=np.array([struct.unpack_from('<9f',raw,96+50*i)for i in range(count)],np.float64).reshape(count,3,3);vertices=[];index={};faces=[]
for t in tri:
 face=[]
 for v in t:
  k=tuple(v)
  if k not in index:index[k]=len(vertices);vertices.append(k)
  face.append(index[k])
 faces.append(face)
v=np.array(vertices);f=np.array(faces);a=np.ones(count,np.int32)
# Reconstruct previous two roofs and tower exactly from their original finite rules.
t=tri;e=.0001;xs=np.linspace(-18,18,49);zs=23.2+4.4*np.cos(xs/18*np.pi/2)
for side in [-1,1]:
 theta=np.radians(side*18);dx=t[:,:,0]-side*39;dy=t[:,:,1]-26;x=np.cos(theta)*dx+np.sin(theta)*dy;y=-np.sin(theta)*dx+np.cos(theta)*dy;allids=[]
 for j in range(48):
  k=(zs[j+1]-zs[j])/(xs[j+1]-xs[j]);b=zs[j]-k*xs[j];hit=(abs(t[:,:,2]-(k*x+b)).max(1)<=e)&(x.min(1)>=xs[j]-e)&(x.max(1)<=xs[j+1]+e)&(y.min(1)>=-47.5-e)&(y.max(1)<=47.5+e);allids.extend(np.flatnonzero(hit).tolist())
 assert len(allids)==len(set(allids))==130;a[allids]=0
xy=t[:,:,:2]-[0,51];r=10.5;eps=2e-5;bound=np.all(np.linalg.norm(xy,axis=2)<=r+eps,axis=1)&np.all((t[:,:,2]>=2.8-eps)&(t[:,:,2]<=36+eps),axis=1);mask=np.zeros(len(t),bool)
for k in range(80):
 theta=(k+.5)*2*np.pi/80;normal=np.array([np.cos(theta),np.sin(theta)]);mask|=bound&np.all(abs(xy@normal-r*np.cos(np.pi/80))<eps,axis=1)
assert mask.sum()==276 and not np.any(mask&(a==0));a[mask]=2;assert np.bincount(a).tolist()==[260,9126,276]
cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];review=json.loads((Path(__file__).parent/'caprim-domain.json').read_text())['candidate'];ids=[];eps=.0001
for g in review['groups']:
 normal=np.array(g['normal_xy']);tangent=np.array(g['tangent_xy']);half=g['tangent_halfwidth'];z0,z1=g['z'];plane=(abs(xy@normal-g['plane_offset'])<eps).all(1)&(norm[:,:2]@normal>.99999);hit=plane&(abs(xy@tangent)<=half+eps).all(1)&(t[:,:,2]>=z0-eps).all(1)&(t[:,:,2]<=z1+eps).all(1)
 got=np.flatnonzero(hit).tolist();assert got==g['faces'] and len(got)==2 and (a[hit]==1).all();uv=np.column_stack(((v[np.unique(f[hit])][:,:2]-[0,51])@tangent,v[np.unique(f[hit])][:,2]));expected=np.array([[-half,z0],[-half,z1],[half,z0],[half,z1]]);assert np.max(abs(np.array(sorted(uv.tolist()))-np.array(sorted(expected.tolist()))))<eps;assert abs(float(np.linalg.norm(cross[hit],axis=1).sum()/2)-g['analytic_area_mm2'])<.00002;a[hit]=2;ids+=got
assert sorted(ids)==review['faces'] and len(ids)==160 and np.bincount(a).tolist()==[260,8966,436]
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);pal=json.loads((R/'palette.json').read_text());ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
def el(p,t,**kw):return E.SubElement(p,'{'+ns+'}'+t,{k:str(x)for k,x in kw.items()})
m=E.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'});res=el(m,'resources');bm=el(res,'basematerials',id=1)
for name,color in pal:el(bm,'base',name=name,displaycolor=color+'FF')
o=el(res,'object',id=2,type='model',pid=1,pindex=1,name='NCUT Machine Tool Complex partial color');mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for p in v:el(vs,'vertex',x=repr(float(p[0])),y=repr(float(p[1])),z=repr(float(p[2])))
for face,ma in zip(f,a):el(ts,'triangle',v1=face[0],v2=face[1],v3=face[2],pid=1,p1=ma,p2=ma,p3=ma)
el(el(m,'build'),'item',objectid=2)
entries={'3D/3dmodel.model':E.tostring(m,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for name,data in sorted(entries.items()):
  zi=zipfile.ZipInfo(name,(2026,11,17,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16;z.writestr(zi,data)
(Q/'selection.json').write_text(json.dumps(dict(new_face_ids=sorted(ids),new_material=2,certainty='INFERRED_SAME_TOWER_CAP_OUTER_RIM',original_colored_faces=536,total_colored_faces=696,all_original_geometry_retained=True),indent=2)+'\n')
