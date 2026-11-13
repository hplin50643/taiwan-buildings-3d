"""Recolor exact original STL triangles without changing geometry. Python + numpy."""
from pathlib import Path
import struct,hashlib,json,zipfile,xml.etree.ElementTree as E
import numpy as np
A=Path(__file__).resolve().parents[1];R=A.parent
SOURCE_SHA='e0ea088d1f0731101ec94be59c75105435bcfb5ba3c80fc0429eec612dbc6b3e'
PALETTE=[('neutral_unverified_surfaces_and_existing_frames','#AAA79F'),('muted_gray_blue_window_backs','#5C6B6E'),('medium_gray_existing_plinth_exterior','#70706B')]
PALETTE.append(('approximate_pale_outer_crown_fascia_background','#C6C5B9'))
ids=[2603, 2604, 2605, 2607, 2610, 2613, 2614, 2616, 2618, 2619, 2620, 2623, 2625, 2627, 2631, 2637, 2647, 2648, 2651, 2652, 2654, 2657, 2659, 2660, 2661, 2668, 2669, 2671, 2672, 2675, 2676, 2678, 2681, 2693, 2694, 2697, 2699, 2702, 2704, 2707, 2709, 2717, 2718, 2719, 2721, 2723, 2725, 2727, 2729, 2737, 2751, 2753, 2754, 2756, 2759, 2761, 2764, 2765, 2767, 2768, 2779, 2781, 2782, 2787, 2789, 2797, 2799, 2802, 2808, 2809, 2813, 2814, 2818, 2820, 2823, 2825, 2828, 2830, 2833, 2834, 2842, 2845, 2846, 2848, 2849, 2857, 2859, 2861, 2866, 2869, 2870, 2871, 2878, 2881, 2883, 2886, 2887, 2895, 2896, 2899, 2900, 2907, 2908, 2911, 2912, 2918, 2923, 2925, 2926, 2930, 2931, 2936, 2940, 2943, 2944, 2948, 2949, 2956, 2960, 2961, 2964, 2967, 2971, 2972, 2975, 2980, 2981, 2982, 2989, 2990, 2993, 2997, 3002, 3004, 3008, 3011, 3013, 3017, 3020, 3023, 3025, 3028, 3030, 3033]
def classify(tri):
 t=tri;z=t[:,:,2];xy=t[:,:,:2];eps=.002
 color=np.zeros(len(t),dtype=int);why=np.full(len(t),'neutral_unverified_or_unsegmented_surface',dtype=object)
 def radial(a):
  q=np.deg2rad(a);return xy@np.array([np.cos(q),np.sin(q)]),xy@np.array([-np.sin(q),np.cos(q)])
 for a in [-150,-120,-90,-60,-30]:
  r,u=radial(a)
  for z0 in [52,76]:
   m=np.all((abs(r-51.5)<eps)&(abs(u)<=6.25+eps)&(z>=z0-eps)&(z<=z0+13.2+eps),axis=1)
   assert m.sum()==8
   color[m]=1;why[m]='whole_original_window_back_a%s_z%s'%(a,z0)
 for a in [-165,-135,-105,-75,-45,-15]:
  r,u=radial(a)
  bounds=np.all((z>=3-eps)&(z<=11.3+eps)&(abs(u)<=5.8+eps)&(r>=45.4-eps)&(r<=54.6+eps),axis=1)
  external=np.all(abs(r-54.6)<eps,axis=1)|np.all(abs(u-5.8)<eps,axis=1)|np.all(abs(u+5.8)<eps,axis=1)
  m=bounds&external;assert m.sum()==6 and np.all(color[m]==0)
  color[m]=2;why[m]='whole_existing_plinth_outer_vertical_faces_a%s'%a
 assert (color==1).sum()==80 and (color==2).sum()==36
 assert not color[ids].any()
 color[ids]=3;why[ids]="whole_original_outer_crown_fascia_facet"
 return color,why

def writezip(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def main():
 (A/'qa-rim-continuation').mkdir(exist_ok=True);(A/'previews').mkdir(exist_ok=True)
 raw=(R/'model.stl').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA
 n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 tri=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)],dtype=np.float64).reshape(n,3,3)
 v,inv=np.unique(tri.reshape(-1,3),axis=0,return_inverse=True);f=inv.reshape(-1,3)
 colors,why=classify(tri);assert set(colors)==set(range(len(PALETTE)))
 # .17g exactly roundtrips every source float32 value as float64.
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns)
 model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'resources');bm=E.SubElement(res,'basematerials',{'id':'20'})
 for name,color in PALETTE:E.SubElement(bm,'base',{'name':name,'displaycolor':color+'FF'})
 obj=E.SubElement(res,'object',{'id':'1','type':'model','pid':'20','pindex':'1','name':'NPU Library partial rotunda entrance original surface'});mesh=E.SubElement(obj,'mesh');vs=E.SubElement(mesh,'vertices');ts=E.SubElement(mesh,'triangles')
 for p in v:E.SubElement(vs,'vertex',dict(zip('xyz',[format(float(x),'.17g') for x in p])))
 for t,col in zip(f,colors):E.SubElement(ts,'triangle',{'v1':str(t[0]),'v2':str(t[1]),'v3':str(t[2]),'pid':'20','p1':str(col),'p2':str(col),'p3':str(col)})
 E.SubElement(E.SubElement(model,'build'),'item',{'objectid':'1'})
 writezip(A/'npu-library-rotunda-front-appearance.3mf',[
 ('[Content_Types].xml',b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
 ('_rels/.rels',b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
 ('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))])
 (A/'palette.json').write_text(json.dumps({'materials':[{'id':n,'srgb':c} for n,c in PALETTE],'colors':'Official NPU front and side photographs, capture dates unknown; uncalibrated display proxies, not current condition proof','scope':'Original80windowbacks/36plinthfaces retained; only144outerverticalcrownfascia new3. Remaining4662neutral. Top/bottom/inner ring/artificial rear/awning unchanged.'},ensure_ascii=False,indent=2)+'\n')
 (A/'face-materials.json').write_text(json.dumps({'source_stl_sha256':SOURCE_SHA,'vertices':len(v),'triangles':len(f),'original_triangle_order_unchanged':True,'face_material_indices':colors.tolist(),'face_reasons':why.tolist()},indent=2)+'\n')
 print(json.dumps({'faces':len(f),'vertices':len(v),'materials':dict(zip([x[0] for x in PALETTE],np.bincount(colors).tolist()))}))
if __name__=='__main__':main()
