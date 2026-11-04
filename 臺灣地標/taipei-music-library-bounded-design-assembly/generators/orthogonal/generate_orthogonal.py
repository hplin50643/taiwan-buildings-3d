#!/usr/bin/env python3
"""Deterministic coordinate-compressed cubical union, millimetres at assembly identity.
Requires Python 3 and NumPy. No network, external geometry engine, or source tree.
Run: python generate_orthogonal.py --output output
This is a research manufacturing model, not a print/strength/real-building certification.
"""
import argparse, collections, decimal, hashlib, json, math, pathlib, struct
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
MINIMAL_INPUTS_SHA256 = 'b8bcb8a7bbe462dfdfb24ff2403a5ec14b8796933c5c5a939f6cfdb41e4f32bf'
COALESCE_MM = 1e-10 # Numerical duplicates only, explicitly ledgered; never a fit tolerance.
AREA_ABS_MM2 = 1e-8
NAMES = {
 'contract':'THREE-MODULE-COMPLETE-REMOVABLE-ASSEMBLY-CONTRACT-V5-2124.json',
 'review':'INDEPENDENT-COMPLETE-ASSEMBLY-CONTRACT-FINAL-2125.json',
 'boxes':'THREE-MODULE-FLOOR-STOP-SWEEP-DIAGNOSTIC-2123.json',
 'slots':'THREE-MODULE-SLOT-NECK-DIAGNOSTIC-2108.json',
 'platforms':'THREE-MODULE-SWEEP-CLEARANCE-PLATFORM-CANDIDATE-2107.json',
}
def dump(p,x):
 p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bbox(v): return np.r_[v.min(axis=0),v.max(axis=0)].tolist()

def axes_normalized(lists):
 axes=[]; maps=[]; changes=[]
 for k,vals in enumerate(lists):
  vals=sorted(set(float(x) for x in vals)); out=[]; mp={}
  for x in vals:
   if out and x-out[-1] <= COALESCE_MM: y=out[-1]
   else: out.append(x);y=x
   mp[x]=y
   if x!=y:changes.append({'axis':k,'from':x,'to':y,'displacement_mm':y-x})
  axes.append(np.array(out,dtype=np.float64));maps.append(mp)
 return axes,maps,changes

def clip(poly,axis,cut,keep_greater):
 out=[]
 if not poly:return out
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=(a[axis]-cut)*(1 if keep_greater else -1);db=(b[axis]-cut)*(1 if keep_greater else -1)
  ina=da>=0;inb=db>=0
  if ina:out.append(a)
  if ina!=inb:
   t=da/(da-db);p=[a[j]+t*(b[j]-a[j]) for j in range(2)];p[axis]=cut;out.append(p)
 return out

def poly_area(p):
 if len(p)<3:return 0.
 a=np.asarray(p);a=a-a[0];return abs(float(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1))))/2

def platform_cells(skin,axes,maps):
 # Validate full triangle coverage of each retained rectangular cell, not midpoint only.
 vv=np.asarray(skin['reference_vertices_mm'],float);ff=skin['faces'];triangles=[]
 for f in ff:
  p=[[maps[0][float(vv[v,0])],maps[1][float(vv[v,1])]] for v in f]
  ar=poly_area(p)
  if ar>0: triangles.append((p,min(x[0] for x in p),min(x[1] for x in p),max(x[0] for x in p),max(x[1] for x in p),ar))
 mask=np.zeros((len(axes[0])-1,len(axes[1])-1),bool);partial=[];covered=0.;max_residual=0.
 for i,(x0,x1) in enumerate(zip(axes[0][:-1],axes[0][1:])):
  for j,(y0,y1) in enumerate(zip(axes[1][:-1],axes[1][1:])):
   area=(x1-x0)*(y1-y0);s=0.
   for p,tx0,ty0,tx1,ty1,_ in triangles:
    if tx1<=x0 or tx0>=x1 or ty1<=y0 or ty0>=y1:continue
    q=p
    for ax,cut,gr in [(0,x0,True),(0,x1,False),(1,y0,True),(1,y1,False)]:q=clip(q,ax,cut,gr)
    s+=poly_area(q)
   if s>area*.5:
    mask[i,j]=True;covered+=area;res=abs(s-area)
   else:res=abs(s)
   max_residual=max(max_residual,res)
   if res>max(AREA_ABS_MM2,area*1e-8):partial.append([i,j,float(area),float(s)])
 source_area=sum(t[-1] for t in triangles)
 return mask, {'triangle_count':len(ff),'triangle_area_sum_mm2':source_area,'rectangular_union_area_mm2':covered,'area_difference_mm2':covered-source_area,'max_cell_coverage_residual_mm2':max_residual,'partial_or_multiply_covered_cells':partial,'coverage_area_tolerance_mm2':AREA_ABS_MM2}

def make_domain(boxes,skin=None,base=None,courtyard=None):
 lists=[[],[],[]]
 for b in boxes:
  for k in range(3):lists[k].extend([b['bounds_mm'][k],b['bounds_mm'][k+3]])
 if skin:
  for v in skin['reference_vertices_mm']:
   for k in range(3):lists[k].append(v[k])
  lists[2].append(skin['reference_vertices_mm'][0][2]+skin['artificial_delta_mm'])
 if base:
  bx=base['base_xy_mm'];lists[0]+=bx[::2]+courtyard[::2];lists[1]+=bx[1::2]+courtyard[1::2];lists[2]+=[-2,-1.2,0]
  for g in base['groups']:
   for r in g['slot_rectangles']:lists[0]+=r[::2];lists[1]+=r[1::2]
 axes,maps,changes=axes_normalized(lists);occ=np.zeros(tuple(len(x)-1 for x in axes),bool)
 indexes=[{x:i for i,x in enumerate(a)} for a in axes]
 def idx(k,x):return indexes[k][maps[k][float(x)]]
 def apply(b,value):
  inds=[idx(k,b[k]) for k in range(3)]+[idx(k,b[k+3]) for k in range(3)]
  occ[inds[0]:inds[3],inds[1]:inds[4],inds[2]:inds[5]]=value
 for b in boxes:apply(b['bounds_mm'],True)
 skinqa=None
 if skin:
  pmask,skinqa=platform_cells(skin,axes,maps)
  z0=skin['reference_vertices_mm'][0][2];z1=z0+skin['artificial_delta_mm']
  if skinqa['partial_or_multiply_covered_cells']: raise ValueError('Platform not an exact rectangular-cell union: '+skin['id']+' '+str(skinqa))
  occ[:,:,idx(2,z0):idx(2,z1)] |= pmask[:,:,None]
 if base:
  bx=base['base_xy_mm'];apply([bx[0],bx[1],-2,bx[2],bx[3],0],True)
  for g in base['groups']:
   for r in g['slot_rectangles']:apply([r[0],r[1],-1.2,r[2],r[3],0],False)
  apply([courtyard[0],courtyard[1],-2,courtyard[2],courtyard[3],0],False)
 return axes,occ,changes,skinqa

QUADS=[ # axis, direction, outward CCW corners, shared global grid vertices.
 (0,-1,[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),
 (0, 1,[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),
 (1,-1,[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
 (1, 1,[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
 (2,-1,[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
 (2, 1,[(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
]
def extract(axes,occ):
 vert=[];faces=[];mapping={}
 def vertex(g):
  if g not in mapping:mapping[g]=len(vert);vert.append([axes[k][g[k]] for k in range(3)])
  return mapping[g]
 for t in np.argwhere(occ):
  c=tuple(int(x) for x in t)
  for ax,d,corners in QUADS:
   nb=list(c);nb[ax]+=d
   if 0<=nb[ax]<occ.shape[ax] and occ[tuple(nb)]:continue
   ids=[vertex(tuple(c[k]+r[k] for k in range(3))) for r in corners]
   faces.extend([(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])])
 return np.array(vert,dtype=np.float64),np.array(faces,dtype=np.int64)

def quantize_domain(axes,occ):
 qa=[];newaxes=[];maps=[]
 for k,a in enumerate(axes):
  aq=a.astype(np.float32).astype(np.float64);uniq,inds=np.unique(aq,return_inverse=True)
  newaxes.append(uniq);maps.append(inds)
  qa.append({'axis':k,'original_coordinate_count':len(a),'serialized_coordinate_count':len(uniq),'collapsed_intervals':int(np.sum(np.diff(aq)==0)),'max_abs_coordinate_movement_mm':float(np.max(np.abs(aq-a))),'coordinate_changes':[{'from':float(x),'to':float(y),'delta_mm':float(y-x)} for x,y in zip(a,aq) if x!=y]})
 newocc=np.zeros(tuple(len(a)-1 for a in newaxes),bool);collapsed=0
 for t in np.argwhere(occ):
  lo=[maps[k][t[k]] for k in range(3)];hi=[maps[k][t[k]+1] for k in range(3)]
  if any(a==b for a,b in zip(lo,hi)):collapsed+=1;continue
  newocc[lo[0]:hi[0],lo[1]:hi[1],lo[2]:hi[2]]=True
 return newaxes,newocc,{'axes':qa,'occupied_cells_collapsed_by_float32':collapsed}

def exact_volume(axes,occ):
 # Integer arithmetic over exact IEEE754 dyadic coordinates. Decimal output is exact.
 exponents=[];ds=[]
 for axis in axes:
  ratios=[float(x).as_integer_ratio() for x in axis]
  exponent=max(d.bit_length()-1 for n,d in ratios)
  ints=[n*(2**exponent//d) for n,d in ratios]
  exponents.append(exponent);ds.append([b-a for a,b in zip(ints[:-1],ints[1:])])
 numerator=0
 for i,j in np.argwhere(np.any(occ,axis=2)):
  height=sum(ds[2][k] for k in np.flatnonzero(occ[i,j]));numerator+=ds[0][i]*ds[1][j]*height
 exponent=sum(exponents)
 decimal.getcontext().prec=max(100, len(str(abs(numerator)))+exponent+10)
 result=decimal.Decimal(numerator)/decimal.Decimal(2**exponent)
 return str(result),float(result)

def symmetric_difference(axes_a,occ_a,axes_b,occ_b):
 merged=[np.unique(np.r_[a,b]) for a,b in zip(axes_a,axes_b)]
 def sample(axes,occ):
  inds=[];valid=[]
  for old,new in zip(axes,merged):
   # Search by left endpoint instead of midpoint to avoid rounding tiny intervals.
   ii=np.searchsorted(old,new[:-1],side='right')-1
   ok=(new[:-1]>=old[0])&(new[1:]<=old[-1]);inds.append(np.clip(ii,0,len(old)-2));valid.append(ok)
  mask=occ[np.ix_(*inds)].copy();mask &= valid[0][:,None,None]&valid[1][None,:,None]&valid[2][None,None,:]
  return mask
 aa=sample(axes_a,occ_a);bb=sample(axes_b,occ_b)
 added_s,added=exact_volume(merged,bb&~aa);removed_s,removed=exact_volume(merged,aa&~bb)
 return {'added_volume_mm3_exact_decimal':added_s,'removed_volume_mm3_exact_decimal':removed_s,'symmetric_difference_volume_mm3':added+removed,'net_volume_difference_mm3':added-removed,'method':'Exact common coordinate arrangement, exact integer dyadic cell integration. No sampling tolerance.'}

def connected_cells(occ):
 pending=set(tuple(int(x) for x in a) for a in np.argwhere(occ));sizes=[]
 while pending:
  queue=[pending.pop()];n=0
  while queue:
   a=queue.pop();n+=1
   for k in range(3):
    for d in [-1,1]:
     b=list(a);b[k]+=d;b=tuple(b)
     if b in pending:pending.remove(b);queue.append(b)
  sizes.append(n)
 return sorted(sizes,reverse=True)

def topology(v,f):
 edges=collections.defaultdict(list);links=[[] for _ in v];adj=[set() for _ in v];badfaces=[]
 area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)/2
 for i,tri in enumerate(f):
  a,b,c=map(int,tri)
  if len(set((a,b,c)))!=3 or area[i]<=0:badfaces.append(i)
  for x,y in [(a,b),(b,c),(c,a)]:edges[tuple(sorted((x,y)))].append((i,1 if x<y else -1));adj[x].add(y);adj[y].add(x)
  links[a].append((b,c));links[b].append((c,a));links[c].append((a,b))
 badedges=[{'edge':list(e),'count':len(h)} for e,h in edges.items() if len(h)!=2]
 badorientation=[list(e) for e,h in edges.items() if len(h)==2 and h[0][1]+h[1][1]!=0]
 badlinks=[]
 for vid,ee in enumerate(links):
  graph=collections.defaultdict(list)
  for a,b in ee:graph[a].append(b);graph[b].append(a)
  seen=set();q=[next(iter(graph))] if graph else []
  while q:
   x=q.pop()
   if x in seen:continue
   seen.add(x);q.extend(graph[x])
  if len(seen)!=len(graph) or any(len(ns)!=2 for ns in graph.values()):badlinks.append(vid)
 unseen=set(range(len(v)));components=[]
 while unseen:
  q=[unseen.pop()];n=0
  while q:
   a=q.pop();n+=1
   for b in adj[a]:
    if b in unseen:unseen.remove(b);q.append(b)
  components.append(n)
 vv=v-(v.min(0)+v.max(0))/2
 volume=float(np.sum(np.einsum('ij,ij->i',vv[f[:,0]],np.cross(vv[f[:,1]],vv[f[:,2]])))/6)
 return {'vertices':len(v),'triangles':len(f),'undirected_edges':len(edges),'euler_characteristic':len(v)-len(edges)+len(f),'edge_incidence_failures':badedges,'orientation_edge_failures':badorientation,'vertex_link_cycle_failures':badlinks,'nondegenerate_triangle_failures':badfaces,'min_triangle_area_mm2':float(area.min()),'surface_area_mm2':float(area.sum()),'signed_volume_mm3':volume,'surface_components':len(components),'surface_component_vertices':sorted(components,reverse=True),'bounds_mm':bbox(v),'topology_pass':not(badedges or badorientation or badlinks or badfaces) and len(components)==1 and volume>0}

def axis_chord_risks(axes,occ,threshold=0.8,tolerance=2e-5):
 # Exhaustive exact runs on all orthogonal arrangement columns. This is a directional
 # boundary-normal chord screen, NOT an orientation-free minimum-neck certificate.
 report=[]
 for axis in range(3):
  dims=[k for k in range(3) if k!=axis];a=np.moveaxis(occ,axis,0);minimum=float('inf');short=[];count=0;surface=0.;near=0
  for i,j in np.argwhere(np.any(a,axis=0)):
   col=a[:,i,j];padded=np.r_[False,col,False];starts=np.flatnonzero(~padded[:-1]&padded[1:]);stops=np.flatnonzero(padded[:-1]&~padded[1:])
   area=float((axes[dims[0]][i+1]-axes[dims[0]][i])*(axes[dims[1]][j+1]-axes[dims[1]][j]))
   for lo,hi in zip(starts,stops):
    length=float(axes[axis][hi]-axes[axis][lo]);minimum=min(minimum,length)
    if abs(length-threshold)<=tolerance:near+=1
    if length<threshold-tolerance:
     count+=1;surface+=2*area
     bounds=[0.]*6;bounds[axis]=float(axes[axis][lo]);bounds[axis+3]=float(axes[axis][hi])
     for k,ind in zip(dims,[i,j]):bounds[k]=float(axes[k][ind]);bounds[k+3]=float(axes[k][ind+1])
     short.append({'chord_length_mm':length,'column_bounds_mm':bounds,'two_opposing_boundary_patch_area_mm2':2*area})
  short.sort(key=lambda x:(x['chord_length_mm'],x['column_bounds_mm']))
  report.append({'axis':'XYZ'[axis],'minimum_contiguous_inward_axis_chord_mm':minimum,'sub_0p8_beyond_numeric_tolerance_column_count':count,'sum_affected_two_opposing_surface_patch_area_mm2':surface,'within_numeric_tolerance_of_0p8_column_count':near,'shortest_40_columns':short[:40]})
 return {'method':'Exhaustive occupied-column contiguous runs along X/Y/Z of actual float32 grid. Distances are to the first opposite occupied-domain boundary on the same axis. This detects local thin terminal or step regions, but does not classify structural load paths or certify an orientation-free minimum neck. Counts are arrangement columns, not independent defects.','nominal_threshold_mm':threshold,'numeric_comparison_tolerance_mm':tolerance,'axes':report,'physical_or_minimum_neck_certification':False}

def stl_write(path,v,f):
 with path.open('wb') as out:
  out.write(b'Research artificial orthogonal union; mm; assembly identity'.ljust(80,b' '));out.write(struct.pack('<I',len(f)))
  for tri in f:
   pts=v[tri];n=np.cross(pts[1]-pts[0],pts[2]-pts[0]);n/=np.linalg.norm(n)
   out.write(struct.pack('<12fH',*n,*pts.ravel(),0))
def stl_read(path):
 raw=path.read_bytes();n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+50*n
 verts=[];faces=[];seen={};normals=[]
 for i in range(n):
  q=struct.unpack_from('<12fH',raw,84+i*50);ff=[];normals.append(q[:3])
  for j in (3,6,9):
   key=q[j:j+3]
   if key not in seen:seen[key]=len(verts);verts.append(key)
   ff.append(seen[key])
  faces.append(ff)
 return np.asarray(verts),np.asarray(faces),np.asarray(normals)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,default=ROOT/'output');args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
 minimal=ROOT/'inputs'/'MINIMAL_BUILD_INPUTS.json'
 assert sha(minimal)==MINIMAL_INPUTS_SHA256,'Minimal input binding mismatch'
 snapshot=json.loads(minimal.read_text());bindings=snapshot['sourcebindings'];inputs=snapshot['inputs']
 # Optional full provenance snapshots are checked whenever present, but not required to rebuild.
 for name,digest in bindings.items():
  full=ROOT/'inputs'/name
  if full.exists():assert sha(full)==digest,name
 c=inputs['contract'];review=inputs['review'];assert review['contract']['sha256']==bindings[NAMES['contract']]
 boxes=inputs['boxes']['boxes'];skins={s['id']:s for s in inputs['platforms']['skins']}
 result={'scope':'Limited mesh construction and topology checks for three proxy frames, two manufactured platform units, and artificial shared display base; not source architecture, print, fit, minimum-neck, stability or strength certification.','units':'mm','assembly_transform':'identity','input_sha256':bindings,'numerical_duplicate_tolerance_mm':COALESCE_MM,'manufacturing_revision':snapshot.get('manufacturing_revision'),'parts':{},'unverified':['global minimum wall/neck and thin tips','all-nine-unit mesh collision and continuous sweeps','visual source-only/hypothesis removal','physical fit/strength/printing']}
 partnames=['A','B','CENTRAL','C8_NOMINAL_PLATFORM','L5_NOMINAL_PLATFORM','ARTIFICIAL_SHARED_BASE']
 bounds={u['id']:u['parameter_bounds_mm'] for u in c['units']}
 for name in partnames:
  bs=[b for b in boxes if b['unit']==name];skin=skins.get(name);base=c['base'] if name=='ARTIFICIAL_SHARED_BASE' else None
  if skin and name not in ['C8_NOMINAL_PLATFORM','L5_NOMINAL_PLATFORM']:skin=None
  ax,occ,changes,skinqa=make_domain(bs,skin,base,inputs['slots']['courtyard_hole_xy_mm'] if base else None)
  terminal_trims=json.loads((ROOT/'inputs/manufacturing-terminal-trims.json').read_text())
  trim=terminal_trims['parts'].get(name);removed_exact=0.
  if trim:
   # Endpoints already occur in the original domain grid; no silent snapping.
   inds=[]
   for k in range(3):
    ids=[]
    for q in [trim[k],trim[k+3]]:
     j=int(np.argmin(abs(ax[k]-q)));assert abs(ax[k][j]-q)<1e-10;(ids.append(j))
    inds.append(ids)
   region=tuple(slice(a,b) for a,b in inds)
   before=exact_volume(ax,occ)[1];occ[region]=False;removed_exact=before-exact_volume(ax,occ)[1]
  sourcev,sourcef=extract(ax,occ);referenceqa=topology(sourcev,sourcef);exacts,exact=exact_volume(ax,occ)
  ax32,occ32,qledger=quantize_domain(ax,occ);v,f=extract(ax32,occ32);q=topology(v,f);exact32s,exact32=exact_volume(ax32,occ32)
  stl=out/(name+'.stl');stl_write(stl,v,f);vr,fr,nr=stl_read(stl);stlqa=topology(vr,fr)
  normals=np.cross(vr[fr[:,1]]-vr[fr[:,0]],vr[fr[:,2]]-vr[fr[:,0]]);normalmatch=bool(np.all(np.einsum('ij,ij->i',nr,normals)>0))
  expected=bounds[name] if not base else [base['base_xy_mm'][0],base['base_xy_mm'][1],-2,base['base_xy_mm'][2],base['base_xy_mm'][3],0]
  qa={'input_boxes_count':len(bs),'source_box_ids':[b['id'] for b in bs],'source_coordinate_grid_dimensions':[len(a) for a in ax],'occupied_cell_count':int(occ.sum()),'occupied_cell_components':connected_cells(occ),'float32_occupied_cell_components':connected_cells(occ32),'numerical_coordinate_coalescing':{'tolerance_mm':COALESCE_MM,'max_abs_movement_mm':max([abs(x['displacement_mm']) for x in changes] or [0]),'changes':changes},'float32_coordinate_conversion':qledger,'platform_projection':skinqa,'parameter_bounds_mm':expected,'source_bounds_residual_mm':(np.array(referenceqa['bounds_mm'])-expected).tolist(),'float32_bounds_residual_mm':(np.array(q['bounds_mm'])-expected).tolist(),'coordinate_grid_union_exact_volume_mm3_decimal':exacts,'float32_grid_union_exact_volume_mm3_decimal':exact32s,'float32_volume_difference_mm3':exact32-exact,'float32_symmetric_difference_vs_reference64':symmetric_difference(ax,occ,ax32,occ32),'source_parameter_box_bounds_comparison':[{'id':bb['id'],'source_bounds_mm':bb['bounds_mm'],'float32_parameter_bounds_mm':np.asarray(bb['bounds_mm'],np.float32).astype(float).tolist(),'max_abs_quantization_mm':float(np.max(np.abs(np.asarray(bb['bounds_mm'],np.float32).astype(float)-bb['bounds_mm'])))} for bb in bs],'float64_mesh_minus_union_volume_mm3':referenceqa['signed_volume_mm3']-exact,'float32_mesh_minus_union_volume_mm3':q['signed_volume_mm3']-exact32,'reference_float64_mesh_qa':referenceqa,'actual_float32_mesh_qa':q,'serialized_binary_stl_qa':stlqa,'binary_stl_normal_direction_agrees':normalmatch,'self_intersection_basis':'Each emitted face is an exposed face of a nonoverlapping cell in one global orthogonal coordinate grid. Faces therefore have disjoint interiors, or meet along shared subdivided grid edges; no Boolean triangulation or T-junctions. Vertex-link and edge-incidence checks independently reject nonmanifold contacts.','pass':bool(q['topology_pass'] and stlqa['topology_pass'] and normalmatch and len(connected_cells(occ32))==1 and abs(q['signed_volume_mm3']-exact32)<1e-6)}
  original_bs=[bb for bb in snapshot.get('original_boxes',boxes) if bb['unit']==name]
  if original_bs and name in ['A','B','CENTRAL']:
   oa,oo,_,_=make_domain(original_bs)
   qa['manufacturing_revision_symmetric_difference_vs_original_bound_boxes']=symmetric_difference(oa,oo,ax,occ)
  qa['additional_manufacturing_terminal_trim']={'bounds_mm':trim,'removed_volume_mm3':removed_exact,'reference_unchanged':True}
  qa['axis_aligned_chord_risk_scan']=axis_chord_risks(ax32,occ32)
  dump(out/(name+'.mesh.json'),{'id':name,'units':'mm','coordinate_space':'assembly identity','role':'artificial_shared_display_base_not_original_floor' if base else 'manufacturing_proxy_with_all_dedicated_supports','vertices':v.tolist(),'triangles':f.tolist(),'serialization':'coordinates are exactly representable float32, JSON numbers retain full values'})
  dump(out/(name+'.reference64.mesh.json'),{'id':name,'units':'mm','vertices':sourcev.tolist(),'triangles':sourcef.tolist(),'note':'Numerical reference to exact coordinate-grid union before float32 serialization; only explicitly ledgered near-duplicate coalescing.'})
  dump(out/(name+'.qa.json'),qa);result['parts'][name]=qa
  print(name,'PASS' if qa['pass'] else 'FAIL','verts',len(v),'triangles',len(f),'volume',q['signed_volume_mm3'],'links',len(q['vertex_link_cycle_failures']),flush=True)
 result['limited_geometry_pass']=all(x['pass'] for x in result['parts'].values());dump(out/'ORTHOGONAL-BUILD-QA.json',result)
 manifest={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.iterdir()) if p.is_file() and p.name!='MANIFEST.json'};dump(out/'MANIFEST.json',manifest)
 if not result['limited_geometry_pass']:raise SystemExit(2)
if __name__=='__main__':main()
