import bpy,bmesh,json,hashlib,struct,itertools
from pathlib import Path
P=Path(__file__).resolve().parent;p=P/'scene.blend';h=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));records=json.loads((P/'BUILD-RECORD.json').read_text())['parts'];checks=[];obs=[]
for r in records:
 o=bpy.data.objects[r['id']];b=(P/r['file']).read_bytes();ex=[]
 for i in range(struct.unpack_from('<I',b,80)[0]):
  f=struct.unpack_from('<12fH',b,84+50*i);ex.extend([f[k:k+3]for k in[3,6,9]])
 ac=[tuple(o.data.vertices[k].co)for f in o.data.polygons for k in f.vertices];err=max(abs(x-y)for a,e in zip(ac,ex)for x,y in zip(a,e));assert len(ac)==len(ex)and err<1e-6
 counts={str(i):sum(f.material_index==i for f in o.data.polygons)for i in range(len(o.data.materials))};checks.append({'id':r['id'],'ordered_STL_error_mm':err,'assigned_faces':counts});obs.append((o,r['bbox']))
candidates=[];overlaps=[];failures=[];raw=[]
for (a,ba),(b,bb)in itertools.combinations(obs,2):
 overlap=[min(ba[1][k],bb[1][k])-max(ba[0][k],bb[0][k])for k in range(3)]
 if min(overlap)<=0:continue
 candidates.append([a.name,b.name]);x=a.copy();x.data=a.data.copy();bpy.context.collection.objects.link(x);bpy.context.view_layer.objects.active=x
 try:
  m=x.modifiers.new('readonly intersection check','BOOLEAN');m.operation='INTERSECT';m.solver='EXACT';m.object=b;bpy.ops.object.modifier_apply(modifier=m.name)
  bm=bmesh.new();bm.from_mesh(x.data);vol=abs(bm.calc_volume());bm.free()
  raw.append({'a':a.name,'b':b.name,'volume_mm3':vol})
  if vol>1e-5:overlaps.append({'a':a.name,'b':b.name,'volume_mm3':vol})
 except Exception as e:failures.append({'a':a.name,'b':b.name,'error':str(e)})
 finally:bpy.data.objects.remove(x,do_unlink=True)
assert hashlib.sha256(p.read_bytes()).hexdigest()==h
(P/'ACTUAL-READONLY.json').write_text(json.dumps({'status':'PASS_ORDERED_STL_AND_MATERIAL_READBACK','scene_sha256':h,'checks':checks,'scene_unchanged':True},indent=2)+'\n')
(P/'ASSEMBLY-COLLISION-QA.json').write_text(json.dumps({'status':'ASSEMBLY_NOT_FIT_APPROVED'if overlaps or failures else'NO_POSITIVE_INTERSECTION_AT_THIS_NOMINAL_PLACEMENT','method':'AABB broadphase then exact Blender Boolean INTERSECT in temporary copies; no original scene save','all_pairs':len(obs)*(len(obs)-1)//2,'broadphase_reject_only_nonpositive_axis_extent':True,'positive_volume_detection_threshold_mm3':1e-5,'broadphase_candidates':len(candidates),'all_candidate_volumes':raw,'positive_intersections':overlaps,'errors':failures,'source_and_proxy_seams_not_solved':True,'not_physical_test':True},indent=2)+'\n');print('candidates',len(candidates),'positive',len(overlaps),'failures',len(failures))
