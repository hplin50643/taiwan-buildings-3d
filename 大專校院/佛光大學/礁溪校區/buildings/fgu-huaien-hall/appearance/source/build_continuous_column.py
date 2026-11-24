from pathlib import Path
import json,numpy as np,argparse,tempfile
import build_appearance as old
D=Path(__file__).resolve().parents[1]
def build(stl,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);q=out/'qa-continuous-column';q.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  old.build(stl,td);base=Path(td);d=np.load(base/'mesh-data.npz');v=d['vertices'];f=d['faces'];mi=d['materials'].copy();info=json.loads((base/'face-materials.json').read_text())
 t=v[f].astype(float);xyz=(t-[0,0,3])/2;review=json.loads((Path(__file__).parent/'column-domain.json').read_text())['candidate'];a=np.array(review['local_origin_design_m']);basis=np.array(review['local_basis']).T;l=(xyz-a)@basis;c=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=c/np.linalg.norm(c,axis=1)[:,None];changed=[]
 for g in review['groups']:
  axis=g['axis'];sign=g['sign'];s=(np.abs(l[:,:,axis]-sign*.45).max(1)<1e-5)&(np.abs(l[:,:,1-axis]).max(1)<=.45001)&(l[:,:,2].min(1)>=-1e-5)&(l[:,:,2].max(1)<=review['local_box_design_m']['axis_max']+1e-5)&(norm@(sign*basis[:,axis])>.99999)
  ids=np.flatnonzero(s).tolist();assert ids==g['faces'] and not mi[s].any();area=float(np.linalg.norm(c[s],axis=1).sum()/2);assert abs(area-g['analytic_area_mm2'])<.0001;changed.extend(ids);mi[s]=4
 assert sorted(changed)==review['faces']
 for i,g in enumerate(info['face_groups']):
  if i not in [0,4]:continue
  s=mi==i;g['original_face_ids']=np.flatnonzero(s).tolist();g['face_count']=int(s.sum());g['surface_area_mm2']=float(np.linalg.norm(c[s],axis=1).sum()/2)
 info['unknown_policy']+=' Six original faces of the same90degreecolumn sideandreverse extend material4 by explicit samecomponent inference. Othercolumns,all walls,glazing andcontacts unchanged.'
 info['continuation']={'face_ids':sorted(changed),'material_index':4,'certainty':'INFERRED_SAME_COMPONENT','no2026conditionclaim':True}
 np.savez_compressed(out/'mesh-data.npz',vertices=v,faces=f,materials=mi);(out/'face-materials.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n');(q/'selection.json').write_text(json.dumps(info['continuation'],indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stl',type=Path,default=D.parent/'model.stl');ap.add_argument('--out',type=Path,default=D);a=ap.parse_args();build(a.stl,a.out)
