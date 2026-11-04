from pathlib import Path
import json,struct,hashlib,numpy as np
from csg64 import Poly,intersection,difference,halfspace
P=Path(__file__).resolve().parent;O=P/'reference-nominal'
r=json.load(open(O/'BUILD-RECORD.json'))['parts'];recs={x['id']:x for x in r};plan=json.load(open(P/'interface-design.json'))
original={}
for x in r:
 b=(O/x['file']).read_bytes();original[x['id']]=[Poly(np.array(struct.unpack_from('<12fH',b,84+i*50)[3:12]).reshape(3,3))for i in range(struct.unpack_from('<I',b,80)[0])]
current={k:[p.clone()for p in v]for k,v in original.items()}
final_gables={}
for name in ['SOURCE_NORMALIZED_A_END','SOURCE_NORMALIZED_F_GABLE']:
 b=(P/'parts'/(name+'.stl')).read_bytes();final_gables[name]=[Poly(np.array(struct.unpack_from('<12fH',b,84+i*50)[3:12]).reshape(3,3))for i in range(struct.unpack_from('<I',b,80)[0])]

def depth(name):
 rr=recs[name]
 if 'ROOF_'in name:return np.array([(1 if name.endswith('left')else-1)/np.sqrt(2),0,-1/np.sqrt(2)]),76.2/np.sqrt(2)
 if name=='SOURCE_NORMALIZED_F_GABLE':return np.array([0,-1,0]),174.91685393258427
 if name=='SOURCE_NORMALIZED_A_END':return np.array([0,1,0]),1.5147540983606558
 k='XYZ'.index(rr['plane_axis']);c=rr['plane_mm'];v=np.concatenate([p.v for p in original[name]]);sgn=1 if np.mean(v[:,k])>c else-1;n=np.zeros(3);n[k]=sgn;return n,-sgn*c
log=[]
for row in plan['interfaces']:
 a,b=row['a'],row['b'];seq=[(a,b),(b,a)]
 if row['category']=='SOURCE_SOURCE_ARTIFICIAL_BACK_INTERSECTION':continue
 if row['category']=='SOURCE_GABLE_VS_PROXY_WALL_BACK':seq=[(t,o)for t,o in seq if t.startswith('PROXY_')]
 if row['category']=='PROXY_PLATFORM_VS_PROXY_WALL':seq=[(t,o)for t,o in seq if'PLATFORM'in t]
 for t,o in seq:
  cutter=final_gables[o] if row['category']=='SOURCE_GABLE_VS_PROXY_WALL_BACK' else original[o]
  if row['category'] not in ['PROXY_PLATFORM_VS_PROXY_WALL','SOURCE_GABLE_VS_PROXY_WALL_BACK']:
   no,co=depth(o);nt,ct=depth(t);v=np.concatenate([p.v for p in cutter]);hp=halfspace(.98*no-nt,.98*co-ct,[v.min(0)-1,v.max(0)+1]);cutter=intersection(cutter,hp)
  current[t]=difference(current[t],cutter);log.append({'interface':row['interface_id'],'target':t,'owner':o,'remaining_polygons':len(current[t])});print(log[-1],flush=True)
(P/'CSG64-POLYGONS.json').write_text(json.dumps({k:[p.v.tolist()for p in ps]for k,ps in current.items()}))
(P/'CSG64-OPERATIONS.json').write_text(json.dumps(log,indent=2)+'\n')
