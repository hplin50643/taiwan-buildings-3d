"""Blender 4.3.2: blender -b --python-exit-code 1 -P rebuild_brick_side.py -- BASE OUT."""
import bpy,numpy as np,sys,hashlib,json,zipfile,struct
import xml.etree.ElementTree as ET
from pathlib import Path
B,P=map(lambda p:Path(p).resolve(),sys.argv[sys.argv.index('--')+1:]);P.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
locks=json.loads(Path(__file__).with_name('baseline-locks.json').read_text())['sha256']
for n,s in locks.items():assert sha((B/n).read_bytes())==s,n
raw=(B/'model.stl').read_bytes();N=struct.unpack_from('<I',raw,80)[0];assert N==3942 and len(raw)==84+50*N
t=np.frombuffer(raw,offset=84,dtype=[('n','<f4',(3,)),('v','<f4',(3,3)),('a','<u2')])['v']
cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);assert np.all(np.linalg.norm(cross,axis=1)>0)
def bounded(axis,lo,hi):return np.all((t[:,:,axis]>=lo)&(t[:,:,axis]<=hi),axis=1)
plane=bounded(0,64.5,64.5)&(cross[:,0]>0)
mask=plane&bounded(1,-23,37)&bounded(2,17,60);ids=np.flatnonzero(mask).tolist()
assert len(ids)==92 and abs(float(cross[mask,0].sum()/2)-2055)<1e-6
assert ids==json.loads(Path(__file__).with_name('verified-face-domain.json').read_text())['ids']
def edges(f):return {tuple(sorted([tuple(t[f,i]),tuple(t[f,j])])) for i,j in ((0,1),(1,2),(2,0))}
owners={}
for i in np.flatnonzero(plane):
 for e in edges(i):owners.setdefault(e,[]).append(int(i))
seen={ids[0]};todo=list(seen)
while todo:
 i=todo.pop()
 for e in edges(i):
  for q in owners[e]:
   if q not in seen:seen.add(q);todo.append(q)
assert seen==set(ids)
assert np.unique(t[mask].reshape(-1,3),axis=0).shape[0]>4
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));ob=bpy.data.objects['Printable_CJCU'];m=ob.data
v=np.array([tuple(x.co) for x in m.vertices],dtype=np.float32);f=np.array([tuple(x.vertices) for x in m.polygons],dtype=np.int32)
assert np.array_equal(v[f],t), 'Blender and raw STL do not share original face/corner order'
assert np.array_equal(np.array(ob.matrix_world),np.eye(4))
a=np.array([p.material_index for p in m.polygons],dtype=np.uint8);assert a.tolist()==[0]*N and len(m.materials)==1
# Preserve the original zero-user startup shader datablock across save/reopen.
orph=bpy.data.materials.get("Material");assert orph is not None and orph.users==0 and orph.use_nodes;orph.use_fake_user=True
# Only this new brick slot gets a new flat display color. Existing material object/node tree is untouched.
neutral=m.materials[0];assert not neutral.use_nodes
mat=bpy.data.materials.new('Nominal red brick - verified short-wing exterior only')
srgb='985343';rgb=[int(srgb[i:i+2],16)/255 for i in (0,2,4)];lin=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
mat.diffuse_color=tuple(lin)+(1,);m.materials.append(mat)
for i in ids:m.polygons[i].material_index=1
a[ids]=1;assert np.bincount(a).tolist()==[3850,92]
q=Path(P/'color-mesh.npz');np.savez_compressed(q,vertices=v,faces=f,materials=a)
ob['side_color_scope']='92 original +X side exterior triangles only; partial color, brick-family proxy; all other surfaces unchanged'
ob['source_color_mesh_sha256']=sha(q.read_bytes())
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(P/'scene.blend'))
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
def el(parent,tag,**kw):return ET.SubElement(parent,'{'+ns+'}'+tag,{k:str(x) for k,x in kw.items()})
root=ET.Element('{'+ns+'}model',{'unit':'millimeter'});res=el(root,'resources');group=el(res,'basematerials',id=1)
def to_srgb(x):return round(255*(12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055))
neutral_hex=''.join(f'{to_srgb(float(x)):02X}' for x in neutral.diffuse_color[:3])
for name,c in ((neutral.name,neutral_hex),(mat.name,srgb.upper())):el(group,'base',name=name,displaycolor='#'+c+'FF')
o=el(res,'object',id=2,type='model',pid=1,pindex=0,name='CJCU library one solid; bounded short-wing brick color')
mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for u in v:el(vs,'vertex',**dict(zip('xyz',(format(float(x),'.17g') for x in u))))
for (i,j,k),c in zip(f,a):el(ts,'triangle',v1=i,v2=j,v3=k,pid=1,p1=c,p2=c,p3=c)
el(el(root,'build'),'item',objectid=2)
with zipfile.ZipFile(P/'appearance.3mf','w',compression=zipfile.ZIP_DEFLATED) as z:
 parts={'[Content_Types].xml':b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>','3D/3dmodel.model':ET.tostring(root,encoding='utf-8',xml_declaration=True)}
 for n,b in parts.items():
  info=zipfile.ZipInfo(n,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
(P/'palette.json').write_text(json.dumps({'partial_color_incomplete':True,'fully_colored_exterior':False,'materials':[{'id':0,'name':neutral.name,'hex':'#'+neutral_hex,'scene_linear_rgba':list(neutral.diffuse_color),'faces':3850,'meaning':'Original warm display stone, not actual color of unknown surfaces'},{'id':1,'name':mat.name,'hex':'#'+srgb.upper(),'scene_linear_rgba':list(mat.diffuse_color),'faces':92,'meaning':'Nominal visually selected reddish brick family; not measured photo RGB'}]},ensure_ascii=False,indent=2)+'\n')
(P/'model.stl').write_bytes(raw)
print('GEOMETRY_PASS',len(v),N,len(ids))
