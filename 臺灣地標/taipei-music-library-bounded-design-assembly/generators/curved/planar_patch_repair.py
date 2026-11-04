"""Retessellate two strictly coplanar artificial side patches, preserving boundary exactly.
No tolerance, vertex welding, point movement, or source-plane shift.
"""
from fractions import Fraction as F
from collections import Counter

def boundary(fs):
 c=Counter((a,b) for t in fs for a,b in zip(t,t[1:]+t[:1]));return sorted((a,b) for (a,b),n in c.items() for _ in range(max(0,n-c[(b,a)])))
def repair_patch(name,v,f):
 if name=='A_NOMINAL_ROOF_SUPPORT_0':indices=[161,165,258,273];expected=[[137,82,138],[136,81,137],[137,81,82],[136,137,138]];new=[[136,81,82],[136,82,138]];inside=137;ring=[136,81,82,138]
 elif name=='A_NOMINAL_ROOF_SUPPORT_1':indices=[71,76,95];expected=[[6,51,52],[6,52,53],[53,52,51]];new=[[6,51,53]];inside=52;ring=[6,51,53]
 else:return v,f,{'applied':False}
 old=[f[i] for i in indices];assert old==expected
 assert [i for i,t in enumerate(f) if inside in t]==indices
 assert len({F(v[i][0]) for t in old for i in t})==1
 assert boundary(old)==boundary(new)
 def ar(ff):return sum((F(v[b][1])-F(v[a][1]))*(F(v[c][2])-F(v[a][2]))-(F(v[b][2])-F(v[a][2]))*(F(v[c][1])-F(v[a][1])) for a,b,c in ff)
 assert ar(old)==ar(new)
 turns=[]
 for a,b,c in zip(ring,ring[1:]+ring[:1],ring[2:]+ring[:2]):turns.append((F(v[b][1])-F(v[a][1]))*(F(v[c][2])-F(v[b][2]))-(F(v[b][2])-F(v[a][2]))*(F(v[c][1])-F(v[b][1])))
 assert all(x>0 for x in turns) or all(x<0 for x in turns)
 ff=[t for i,t in enumerate(f) if i not in indices]+new
 used=sorted(set(i for t in ff for i in t));remap={a:i for i,a in enumerate(used)}
 proof={'applied':True,'old_face_indices':indices,'old_faces':old,'new_faces':new,'removed_interior_vertex':inside,'removed_coordinate_mm':v[inside],'all_patch_vertices':{str(i):v[i] for t in old for i in t},'unchanged_directed_boundary':boundary(old),'exact_signed_twice_area':str(ar(new)),'exact_convex_turns':[str(x) for x in turns],'other_incident_faces':0,'role':'artificial support-side / hypothetical roof-back intersection only; not conditional top surface','all_retained_coordinates_unchanged':True}
 return [v[i] for i in used],[[remap[i] for i in t] for t in ff],proof
