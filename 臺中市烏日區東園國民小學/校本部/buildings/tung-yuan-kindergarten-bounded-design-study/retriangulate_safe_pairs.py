from pathlib import Path
import numpy as np,struct,json,hashlib
P=Path(__file__).resolve().parent
work=[('SOURCE_NORMALIZED_A_END.stl',71,72,[8,11]),('SOURCE_NORMALIZED_ROOF_left.stl',77,43,[22,26])];rows=[]
for filename,i,j,edge in work:
 p=P/'parts'/filename;b=p.read_bytes();t=np.array([struct.unpack_from('<12fH',b,84+50*k)[3:12]for k in range(struct.unpack_from('<I',b,80)[0])]).reshape(-1,3,3);v,idx=np.unique(t.reshape(-1,3),axis=0,return_inverse=True);fs=idx.reshape(-1,3);f=fs[i];a,bb=edge
 for k in range(3):
  if set(map(int,[f[k],f[(k+1)%3]]))==set(edge):a,bb,c=[int(f[(k+l)%3])for l in range(3)];break
 d=next(int(x)for x in fs[j]if x not in[a,bb]);A,B,C,D=v[[a,bb,c,d]];normal=np.cross(B-A,C-A);plane=abs((D-A)@normal)/np.linalg.norm(normal);new=[np.array([C,A,D]),np.array([C,D,B])];areas=lambda q:np.linalg.norm(np.cross(q[1]-q[0],q[2]-q[0]))/2
 assert plane<=1e-12 and all(np.cross(q[1]-q[0],q[2]-q[0])@normal>0 for q in new)
 assert abs(sum(areas(q)for q in new)-areas(t[i])-areas(t[j]))<1e-10
 before=hashlib.sha256(b).hexdigest();oldfaces=t[[i,j]].copy();t[i],t[j]=new
 data=bytearray(b'SAFE COPLANAR DIAGONAL FLIP; VERTICES AND SURFACE UNCHANGED'.ljust(80,b' '));data+=struct.pack('<I',len(t))
 for q in t:
  n=np.cross(q[1]-q[0],q[2]-q[0]);n/=np.linalg.norm(n);data+=struct.pack('<12fH',*n,*q.reshape(-1),0)
 p.write_bytes(data);rows.append({'file':'parts/'+filename,'old_sha256':before,'new_sha256':hashlib.sha256(data).hexdigest(),'triangle_indices':[i,j],'old_triangles':oldfaces.tolist(),'new_triangles':np.array(new).tolist(),'all_vertices_identical_set':True,'fourth_vertex_plane_distance_mm':float(plane),'area_change_mm2':float(sum(areas(q)for q in new)-sum(areas(q)for q in oldfaces))})
(P/'SAFE-RETRIANGULATION-RECORD.json').write_text(json.dumps({'status':'TWO_COPLANAR_DIAGONAL_FLIPS_ONLY','triangle_count_unchanged':True,'checks':rows,'other_five_micro_triangles_retained':True},indent=2)+'\n')
