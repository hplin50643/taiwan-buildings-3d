"""Independent all-three-vertices checks against original radial planes, not centroids."""
from pathlib import Path
import numpy as np,struct,json,hashlib
A=Path(__file__).resolve().parents[1];raw=(A.parent/'model.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0]
t=np.array([struct.unpack_from('<9f',raw,96+50*i) for i in range(n)]).reshape(n,3,3);c=np.array(json.loads((A/'face-materials.json').read_text())['face_material_indices']);eps=.002
expected=np.zeros(n,int);counts={}
for a in [-150,-120,-90,-60,-30]:
 q=np.deg2rad(a);r=t[:,:,0]*np.cos(q)+t[:,:,1]*np.sin(q);s=-t[:,:,0]*np.sin(q)+t[:,:,1]*np.cos(q)
 for z in [52,76]:
  m=(np.abs(r-51.5).max(1)<eps)&(np.abs(s).max(1)<=6.25+eps)&(t[:,:,2].min(1)>=z-eps)&(t[:,:,2].max(1)<=z+13.2+eps)
  assert m.sum()==8;expected[m]=1;counts[f'glass_{a}_{z}']=int(m.sum())
for a in [-165,-135,-105,-75,-45,-15]:
 q=np.deg2rad(a);r=t[:,:,0]*np.cos(q)+t[:,:,1]*np.sin(q);s=-t[:,:,0]*np.sin(q)+t[:,:,1]*np.cos(q)
 m=(r.min(1)>=45.4-eps)&(r.max(1)<=54.6+eps)&(abs(s).max(1)<=5.8+eps)&(t[:,:,2].min(1)>=3-eps)&(t[:,:,2].max(1)<=11.3+eps)&((abs(r-54.6).max(1)<eps)|(abs(s-5.8).max(1)<eps)|(abs(s+5.8).max(1)<eps))
 assert m.sum()==6 and np.all(expected[m]==0);expected[m]=2;counts[f'plinth_{a}']=int(m.sum())
rim=[]
cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None]
for deg in np.arange(-178.75,0,2.5):
 q=np.deg2rad(deg);normal=np.array([np.cos(q),np.sin(q),0]);u=np.array([-np.sin(q),np.cos(q),0]);half=np.deg2rad(1.25)
 m=np.all(abs(t@normal-55.4*np.cos(half))<1e-5,axis=1)&(norm@normal>1-1e-7)&np.all(t[:,:,2]>=119-1e-5,axis=1)&np.all(t[:,:,2]<=122+1e-5,axis=1)&np.all(abs(t@u)<=55.4*np.sin(half)+1e-5,axis=1)
 assert m.sum()==2 and np.all(expected[m]==0);expected[m]=3;rim.extend(np.flatnonzero(m).tolist())
assert sorted(rim)==[2603, 2604, 2605, 2607, 2610, 2613, 2614, 2616, 2618, 2619, 2620, 2623, 2625, 2627, 2631, 2637, 2647, 2648, 2651, 2652, 2654, 2657, 2659, 2660, 2661, 2668, 2669, 2671, 2672, 2675, 2676, 2678, 2681, 2693, 2694, 2697, 2699, 2702, 2704, 2707, 2709, 2717, 2718, 2719, 2721, 2723, 2725, 2727, 2729, 2737, 2751, 2753, 2754, 2756, 2759, 2761, 2764, 2765, 2767, 2768, 2779, 2781, 2782, 2787, 2789, 2797, 2799, 2802, 2808, 2809, 2813, 2814, 2818, 2820, 2823, 2825, 2828, 2830, 2833, 2834, 2842, 2845, 2846, 2848, 2849, 2857, 2859, 2861, 2866, 2869, 2870, 2871, 2878, 2881, 2883, 2886, 2887, 2895, 2896, 2899, 2900, 2907, 2908, 2911, 2912, 2918, 2923, 2925, 2926, 2930, 2931, 2936, 2940, 2943, 2944, 2948, 2949, 2956, 2960, 2961, 2964, 2967, 2971, 2972, 2975, 2980, 2981, 2982, 2989, 2990, 2993, 2997, 3002, 3004, 3008, 3011, 3013, 3017, 3020, 3023, 3025, 3028, 3030, 3033]
assert np.array_equal(c,expected) and np.bincount(c).tolist()==[4662,80,36,144]
for m in [np.all(abs(t[:,:,1])<eps,axis=1),t[:,:,2].max(1)<=3+eps,(t[:,:,2].min(1)>=45-eps)&(t[:,:,2].max(1)<=47.4+eps)]:assert np.all(c[m]==0)
# Crown other than designated outer fascia stays neutral, including open bay returns, top and bottom.
m=(t[:,:,2].min(1)>=99.5-eps);m[rim]=False;assert np.all(c[m]==0)
d={'triangles':n,'all_vertices_full_existing_faces':True,'no_centroid_or_subdivision':True,'expected_face_map_exact':True,'counts':counts,'material_counts':[4662,80,36,144],'outer_crown_fascia_count':144,'scope':'Only72wholeouterverticalfacets; awning/crownremaining/base/rear neutral','source_sha256':hashlib.sha256(raw).hexdigest()}
(A/'qa-rim-continuation/boundary-validation.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
