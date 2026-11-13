exec((__import__('pathlib').Path(__file__).parent/'screen.py').read_text().split('rows=[]')[0])
S=1.07;B=1.6;MPP=.13554824373866425
entry=np.array([(700-790)*MPP,(640-650)*MPP]);u=np.array([-.8,.6]);nn=np.array([.6,.8]);out=[]
for ids in groups:
 pts=nv[f[ids]].reshape(-1,3);xy=pts[:,:2]/S-entry;uu=xy@u;ww=xy@nn;zz=(pts[:,2]-B)/S
 if min(uu)>-6.001 and max(uu)<6.001 and min(ww)>-.801 and max(ww)<4.001 and min(zz)>3.999 and max(zz)<5.251:
  out.append({'faces':ids.tolist(),'count':len(ids),'u':[float(min(uu)),float(max(uu))],'n':[float(min(ww)),float(max(ww))],'z':[float(min(zz)),float(max(zz))],'normal':n[ids[0]].tolist(),'materials':np.unique(mi[ids]).tolist()})
(R/'stair-domain-screen.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
