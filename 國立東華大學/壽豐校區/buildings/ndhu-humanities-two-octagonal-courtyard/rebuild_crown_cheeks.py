"""SHA-locked surface-only patch. Blender 4.3.2: blender -b -P this.py -- BASELINE OUTPUT"""
import bpy,sys,json,hashlib,zipfile,shutil,struct
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
B,O=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:]);O.mkdir(parents=True,exist_ok=True)
LOCKS={'model.stl':'1c7ce3f56c3ccbcd7fd7b49e15ce081ece18e6743336db81e19c0fd62d3f0c48','scene.blend':'6c1430e60e6ea603b1d992f24104df0fb1428d089492250b76177d3beb96340d'}
IDS=[3714,3715,3718,3719,3720,3721,3722,3723,3724,3725,3726,3727]
for n,h in LOCKS.items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h
bpy.ops.wm.open_mainfile(filepath=str(B/'scene.blend'));ob=bpy.data.objects['Printable_NDHU'];me=ob.data
v=np.array([tuple(x.co) for x in me.vertices],dtype=np.float64);f=np.array([tuple(x.vertices) for x in me.polygons],dtype=np.int32);mi=np.array([x.material_index for x in me.polygons],dtype=np.int32)
assert v.shape==(4849,3) and f.shape==(9934,3) and len(me.materials)==5
raw=(B/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];t=np.frombuffer(raw,dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('att','<u2')]),offset=84,count=n)['v'];assert np.array_equal(v[f],t) and np.all(mi[IDS]==0)
old=mi.copy();oldpalette=[{'index':i,'name':m.name,'linear_rgba':list(m.diffuse_color),'use_nodes':m.use_nodes,'status':'original preview material, not fully calibrated real facade'} for i,m in enumerate(me.materials)]
retained=[]
for col in ['materials']:
 for m in getattr(bpy.data,col):
  if m.users==0 and not m.use_fake_user:m.use_fake_user=True;retained.append(m.name)
name='Crown redbrown — nominal historical family';srgb=[166/255,83/255,60/255]
linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in srgb]
m=bpy.data.materials.new(name);m.diffuse_color=(*linear,1);m.use_nodes=False;me.materials.append(m)
for i in IDS:me.polygons[i].material_index=5
mi[IDS]=5
scope='Only 315-degree crown post +X/-Y complete original cheeks, 12 faces; historical 2006/2007 material-family inference, uncalibrated nominal redbrown. Other 9922 faces and five original preview slots unchanged; not comprehensive true-material calibration.'
ob['side_color_scope']=scope;ob['source_original_stl_sha256']=LOCKS['model.stl']
bpy.ops.wm.save_as_mainfile(filepath=str(O/'scene.blend'),check_existing=False)
shutil.copyfile(B/'model.stl',O/'model.stl')
np.savez_compressed(O/'surface-colors.npz',vertices=v,faces=f,materials=mi)
palette=oldpalette+[{'index':5,'name':name,'linear_rgba':list(m.diffuse_color),'nominal_srgb':'#A6533C','use_nodes':False,'status':'new uncalibrated historical redbrown family, not measured photographic color'}]
(O/'surface-palette.json').write_text(json.dumps({'new_exchange_format':True,'materials':palette},ensure_ascii=False,indent=2)+'\n')
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
def el(p,n,**a):return ET.SubElement(p,'{'+ns+'}'+n,{k:str(v) for k,v in a.items()})
r=ET.Element('{'+ns+'}model',{'unit':'millimeter','xml:lang':'en-US'});res=el(r,'resources');bm=el(res,'basematerials',id=1)
def rgbhex(c):
 s=[12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055 for x in c[:3]];return '#'+''.join(f'{round(max(0,min(1,x))*255):02X}' for x in s)+'FF'
for p in palette:el(bm,'base',name=p['name'],displaycolor=rgbhex(p['linear_rgba']))
o=el(res,'object',id=2,type='model',pid=1,pindex=0,name='NDHU humanities II limited historical surface colors');mesh=el(o,'mesh');vs=el(mesh,'vertices');ts=el(mesh,'triangles')
for row in v:el(vs,'vertex',**dict(zip('xyz',map(repr,map(float,row)))))
for tri,c in zip(f,mi):el(ts,'triangle',v1=tri[0],v2=tri[1],v3=tri[2],pid=1,p1=c,p2=c,p3=c)
el(el(r,'build'),'item',objectid=2)
entries={'3D/3dmodel.model':ET.tostring(r,encoding='utf-8',xml_declaration=True),'[Content_Types].xml':b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>','_rels/.rels':b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'}
# Correct OPC namespace (new exchange, not rewriting an original 3MF).
entries['[Content_Types].xml']=entries['[Content_Types].xml'].replace(b'openxmlformats-package.org',b'openxmlformats.org')
with zipfile.ZipFile(O/'surface-colors.3mf','w',zipfile.ZIP_DEFLATED) as z:
 for k,b in entries.items():
  zi=zipfile.ZipInfo(k,(2026,11,18,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,b)
change={'fixed_ref':'8f90ae2478f00cce6832a07de537f7d333f6dbc0','original_locks':LOCKS,'faces':IDS,'old':0,'new':5,'counts':np.bincount(mi,minlength=6).tolist(),'non_target_faces_unchanged':9922,'new_exchange_files':['surface-colors.npz','surface-colors.3mf'],'geometry':'exact saved Blender vertex/order and original STL triangle sequence; no remesh','new_material':palette[-1],'retained_orphan_fake_user':retained,'new_custom_properties':['side_color_scope','source_original_stl_sha256'],'scope':scope}
(O/'crown-cheeks-change.json').write_text(json.dumps(change,ensure_ascii=False,indent=2)+'\n');print(json.dumps(change,ensure_ascii=False))
