from pathlib import Path
import numpy as np,json,hashlib,struct,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];Q=R/'qa-continuous-highwall';Q.mkdir(exist_ok=True);raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()=='353a5ce7fcd15a798f8bbf932e73d67b95ef856c60623cc3d7831f46dd609897';count=struct.unpack_from('<I',raw,80)[0];assert count==65686
tri=np.array([struct.unpack_from('<9f',raw,96+50*i)for i in range(count)],np.float64).reshape(count,3,3);vertices=[];index={};faces=[]
for t in tri:
 face=[]
 for v in t:
  k=tuple(v)
  if k not in index:index[k]=len(vertices);vertices.append(k)
  face.append(index[k])
 faces.append(face)
v=np.array(vertices);f=np.array(faces);a=np.ones(count,np.int32)
t=tri;lo=t.min(1);hi=t.max(1)
def plane(ax,v):return np.max(abs(t[:,:,ax]-v),axis=1)<.003
def span(ax,l,h):return(lo[:,ax]>=l-.003)&(hi[:,ax]<=h+.003)
fields=[]
# Original S=1.8 BASE=3; full front planes of highwall and entrylintel original add().
for x1,x2,y,z1,z2,n in [(-24.,30.2,-2.9,40.,44.4,46),(-13.,13.,-35.5,7.1,8.,2)]:
 yy=float(np.float32(y*1.8));low=np.array([x1*1.8,yy,3+z1*1.8]).astype('f4').astype(float);high=np.array([x2*1.8,yy,3+z2*1.8]).astype('f4').astype(float)
 whole=np.max(abs(t[:,:,1]-yy),1)<1e-5
 finite=whole&np.all((t>=low-1e-5)&(t<=high+1e-5),axis=(1,2))
 assert whole.sum()==n and np.array_equal(whole,finite),(yy,whole.sum(),finite.sum())
 fields.append(finite)
rail=np.logical_or.reduce(fields)
a[rail]=0
# The original entrance lintel and two piers form one light-colored frame in
# official album image 5962. Only their original finite box-boundary faces
# are colored. Side/back/soffit continuity is explicitly an inference.
entry_domains={};entry_frame=np.zeros(len(t),bool);eps=2e-5
for name,bounds in [
 ('lintel',[-13,13,-35.5,-34.4,7.1,8.0]),
 ('left_pier',[-12.95,-11.65,-35.2,-33.5,0,7.3]),
 ('right_pier',[11.65,12.95,-35.2,-33.5,0,7.3])]:
 low=np.array([bounds[0]*1.8,bounds[2]*1.8,3+bounds[4]*1.8])
 high=np.array([bounds[1]*1.8,bounds[3]*1.8,3+bounds[5]*1.8])
 within=np.all((t>=low-eps)&(t<=high+eps),axis=(1,2));mask=np.zeros(len(t),bool)
 for axis in range(3):
  for value in [low[axis],high[axis]]:
   mask|=within&(np.max(abs(t[:,:,axis]-value),axis=1)<eps)
 entry_domains[name]=int(mask.sum());entry_frame|=mask
assert entry_domains=={'lintel':34,'left_pier':27,'right_pier':32}
assert entry_frame.sum()==93 and (entry_frame&(a==1)).sum()==91
a[entry_frame]=0
assert np.bincount(a).tolist()==[139,65547]
cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];review=json.loads((Path(__file__).parent/'highwall-domain.json').read_text())['candidate'];eps=.0001;low=np.array(review['low_mm']);high=np.array(review['high_mm']);plane=(abs(t[:,:,1]-review['plane_y_mm'])<eps).all(1)&(norm[:,1]>.99999);hit=plane&(t>=low-eps).all((1,2))&(t<=high+eps).all((1,2));assert np.array_equal(plane,hit);ids=np.flatnonzero(hit).tolist();assert ids==review['faces'] and len(ids)==5 and (a[hit]==1).all();assert abs(float(np.linalg.norm(cross[hit],axis=1).sum()/2)-review['analytic_area_mm2'])<.0005;a[hit]=0;assert np.bincount(a).tolist()==[144,65542]
np.savez_compressed(R/'color-mesh.npz',vertices=v,faces=f,materials=a);pal=json.loads((R/'palette.json').read_text());ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
def el(p,t,**kw):return E.SubElement(p,'{'+ns+'}'+t,{k:str(x)for k,x in kw.items()})
m=E.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'});res=el(m,'resources');bm=el(res,'basematerials',id=1)
for name,color in pal:el(bm,'base',name=name,displaycolor=color+'FF')
o=el(res,'object',id=2,type='model',pid=1,pindex=1,name='CNU Wang Chen Library partial color');mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for p in v:el(vs,'vertex',x=repr(float(p[0])),y=repr(float(p[1])),z=repr(float(p[2])))
for face,ma in zip(f,a):el(ts,'triangle',v1=face[0],v2=face[1],v3=face[2],pid=1,p1=ma,p2=ma,p3=ma)
el(el(m,'build'),'item',objectid=2)
entries={'3D/3dmodel.model':E.tostring(m,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}
with zipfile.ZipFile(R/'appearance.3mf','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for name,data in sorted(entries.items()):
  zi=zipfile.ZipInfo(name,(2026,11,17,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16;z.writestr(zi,data)
(Q/'selection.json').write_text(json.dumps(dict(new_face_ids=sorted(ids),new_material=0,certainty='INFERRED_SAME_SOUTH_HIGHWALL_REAR_FACE',original_colored_faces=139,total_colored_faces=144,all_original_geometry_retained=True),indent=2)+'\n')
