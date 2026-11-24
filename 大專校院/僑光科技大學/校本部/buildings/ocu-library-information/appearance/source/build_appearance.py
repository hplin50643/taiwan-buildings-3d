"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='c791646865a9093b141ede99f2c669587ab3a69df91b22eccd374c76eb83223c'
PALETTE=[('neutral_mixed_walls_roof_entry_and_print_backing','#AAA79F'),('source_front_muted_gold_shading_boxes','#B4A451'),('source_day_teal_cylinder_glazing_proxy','#638E8A'),('source_silver_cap_rings_and_original_mullions','#B3BCBB'),('approximate_dark_podium_front','#40494B')]
def classify(tri):
 from shapely.geometry import Polygon
 a=np.deg2rad(2.5);S=150/(88*np.cos(a)+62*np.sin(a));t=tri.copy()/S;t=t@np.array([[np.cos(a),np.sin(a),0],[-np.sin(a),np.cos(a),0],[0,0,1]]);t[:,:,2]-=1.3;eps=3e-5;out={};spec={}
 def boxmask(n,x,y,z,w,d,h):
  lo=np.array([x-w/2,y-d/2,z]);hi=lo+[w,d,h];mask=np.all((t>=lo-eps)&(t<=hi+eps),axis=(1,2));surf=np.zeros(len(t),bool)
  for ax in range(3):
   for v in [lo[ax],hi[ax]]:surf|=np.all(abs(t[:,:,ax]-v)<eps,axis=1)
  out[n]=np.flatnonzero(mask&surf).tolist();spec[n]=dict(lo=lo.tolist(),hi=hi.tolist())
 for z in [7.,12.1]:
  for x in [5.5,13.5,21.5,29.5]:
   if not(z==7 and x in [13.5,21.5]):boxmask(f'yellow_s_{x}_{z}',x,-27.9275,z+1.65,6,1.255,.55)
  for x in [-16,-8,0]:boxmask(f'yellow_s_{x}_{z}',x,-27.9275,z+1.65,6,1.255,.55)
 for z in [6.8,11.8]:boxmask(f'yellow_tower_{z}',-27,-24.45,z+1.65,8.3,1.3,.55)
 for x in [-5,6,17,28]:boxmask(f'yellow_terrace_{x}',x,-27.5625,20.35,8.5,1.225,.55)
 # curved cut backs are regular 96 segment polygon r7.35, not radial approximation.
 angles=np.linspace(np.pi-.23,2*np.pi+.23,97);xy=np.c_[7.35*np.cos(angles)-27,7.35*np.sin(angles)-1]
 glass=np.zeros(len(t),bool)
 for z in np.arange(18,49,3.2):
  zmask=np.all((t[:,:,2]>=z-eps)&(t[:,:,2]<=z+2.55+eps),axis=1)
  for v,w in zip(xy[:-1],xy[1:]):
   dv=w-v;u=(t[:,:,:2]-v)@dv/(dv@dv);normal=np.array([-dv[1],dv[0]])/np.linalg.norm(dv);dist=(t[:,:,:2]-v)@normal
   glass|=zmask&np.all((abs(dist)<eps)&(u>=-eps)&(u<=1+eps),axis=1)
 out['teal_cylinder_cut_backs']=np.flatnonzero(glass).tolist()
 # Independent tower horizontal rings, whole triangle within original polygon annular prism.
 # Silver frame surfaces: exact polygon faceting boundaries; radial interval alone is not enough.
 def ringmask(n,z,ro,ri,h):
  aa=np.linspace(0,2*np.pi,97);outer=np.c_[ro*np.cos(aa)-27,ro*np.sin(aa)-1];inner=np.c_[ri*np.cos(aa)-27,ri*np.sin(aa)-1]
  zm=np.all((t[:,:,2]>=z-eps)&(t[:,:,2]<=z+h+eps),axis=1);on=np.zeros(len(t),bool)
  for poly in [outer,inner]:
   for v,w in zip(poly[:-1],poly[1:]):
    dv=w-v;u=(t[:,:,:2]-v)@dv/(dv@dv);normal=np.array([-dv[1],dv[0]])/np.linalg.norm(dv);dist=(t[:,:,:2]-v)@normal
    on|=zm&np.all((abs(dist)<eps)&(u>=-eps)&(u<=1+eps),axis=1)
  # Entire triangle must be covered by original annular polygon, not only vertices.
  if ri<ro:
   pg=Polygon(outer[:-1], [inner[:-1]]).buffer(eps)
   for face in np.flatnonzero(zm & (np.all(abs(t[:,:,2]-z)<eps,axis=1)|np.all(abs(t[:,:,2]-z-h)<eps,axis=1))):
    if pg.covers(Polygon(t[face,:,:2])):on[face]=True
  out[n]=np.flatnonzero(on).tolist()
 for z in np.arange(17.4,50,3.2):ringmask(f'silver_ring_side_{z:.1f}',z,7.95,7.1,.64)
 # Silver cylindrical cap original outside r8.05, leave top/roof unknown.
 ringmask('silver_cap_outer',50,8.05,8.05,5.8)
 for z in np.arange(18,49,3.2):
  for j,ang in enumerate(np.linspace(np.pi+.1,2*np.pi-.1,11)):
   boxmask(f'silver_vertical_{z:.1f}_{j}',-27+7.42*np.cos(ang),-1+7.42*np.sin(ang),z-.04,.65,.65,2.63)
 for ro,ri in [(13.4,12.55),(11.95,11.10)]:ringmask(f'silver_crown_ring_{ro}',59.5,ro,ri,.85)
 
 color=np.zeros(len(t),dtype=int);why=np.full(len(t),'mainwalls_mixedwindows_lowpodium_entry_roof_printwebs_and_unknown_neutral',dtype=object)
 sets=[]
 for prefix,k,label,expected in [('yellow_',1,'source_day_front_shading_box_whole_surface_bounded_extension',328),('teal_',2,'source_day_cylinder_original_polygon_recessback_glazing_proxy',1520),('silver_',3,'source_day_original_polygon_rings_cap_outer_and_box_mullions',8806)]:
  ids=sorted(set(i for key,vals in out.items() if key.startswith(prefix) for i in vals));assert len(ids)==expected,(prefix,len(ids));assert not np.any(color[ids]);color[ids]=k;why[ids]=label;sets.append(set(ids))
 assert all(not (sets[i]&sets[j]) for i in range(3) for j in range(i))

 # Whole source-supported front podium plane only; no new geometric color boundary.
 selected=np.zeros(len(t),dtype=bool);selected[[9316, 9317, 9318, 9319, 9320, 9321, 9324, 9325, 9326, 9327, 9328, 9329, 9330, 9331, 9332, 9333, 9334, 9335, 9336, 9337, 9338, 9339, 9340, 9341, 9342, 9343, 9344, 9347, 9350, 9351, 9352, 9353, 9354, 9355, 9356, 9357, 9358, 9359, 9360, 9361, 9362, 9363, 9364, 9365, 9366, 9367, 9368, 9369, 9370, 9371, 9372, 9373, 9374, 9375, 9376, 9377, 9378, 9379, 9380, 9381, 9382, 9383, 9384, 9385, 9386, 9388, 9389, 9401, 9402, 9403, 9404, 9405, 9406, 9407, 9408, 9409, 9410, 9411, 9412, 9413, 9414, 9415, 9416, 9417, 9418, 9419, 9420, 9421, 9422, 9423, 9424, 9425, 9426, 9427, 9428, 9429, 9430, 9431, 9432, 9433, 9434, 9435, 9436, 9437, 9438, 9439, 9440, 9441, 9444, 9445, 9446, 9447, 9448, 9449, 9451, 9452, 9453, 9454, 9455, 9456, 9528, 9529, 9530, 9531, 9532, 9533, 9534, 9535, 9537, 9538, 9539, 9540, 9541, 9542, 9543, 9544, 9545, 9546, 9547, 9548, 9549, 9550, 9551, 9552, 9553, 9554, 9555, 9556, 9557, 9559, 9560, 9561, 9562, 9563, 9564, 9565, 9566, 9567, 9568, 9569, 9570, 9571, 9572, 9573, 9574, 9575, 9576, 9577, 9578, 9579, 9580, 9581, 9582, 9583, 9584, 9585, 9586, 9587, 9588, 9589, 9592, 9594, 9595, 9596, 9597, 9598, 9599, 9600, 9601, 9603, 9604, 9610, 9611, 9612, 9613, 9614, 9615, 9616, 9617, 9619, 9620, 9635, 9636, 9637, 9638, 9639, 9640, 9641, 9642, 9643, 9644, 9645, 9646, 9647]]=True
 assert np.all(abs(t[selected,:,1]+28)<1e-5);assert not color[selected].any();color[selected]=4;why[selected]='original_front_podium_dark_background_bounded_extension'
 return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-wall-continuation').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'OCU Library Bounded Cylinder And Shading Study original surface'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'oculib-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'palette.json').write_text(json.dumps({'materials':[{'id':n,'srgb':c} for n,c in PALETTE],'colors':'OCU official historicalgallery five completephotos; daytime2007/2010 primary. Mutedgold frontshadingboxes, restrainedteal cylinderrecessbacks, silver exact capouter/rings/mullions','scope':'Exact inverseplanrotation/scale and originalbox or polygonannulus surfaces only. Wholetriangle containment, nogeometrycuts. Additionally214 whole frontpodium wallfaces approximate darkgray; remaining unregistered mainwalls/windows/podiumsides/entry/roofs/northshading neutral; originalprintonly crownbackingwebs, slopingbraces andskirt neutral. Historicalmetadata notcurrentcondition; photosprivate.'},ensure_ascii=False,indent=2)+'\n')
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
