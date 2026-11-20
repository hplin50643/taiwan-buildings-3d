"""Apply the fixed right-end return to the frozen roof-cap package. No mesh edits."""
from pathlib import Path
import collections, hashlib, json, struct, sys, zipfile, xml.etree.ElementTree as E
import numpy as np

NAME='VNU Renai RHB right wall muted terracotta'
HEX='#A77C6C'
OBJECT='VNU Renai RHB partial color'
IDS=[502, 503, 534, 535, 536, 641, 642, 643, 668, 669, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698]
STL='e907ae0be17200fc2391d9f17f942db0847b0e1ff6c6622eaec143ebee6390fe'
NPZ='de7488362e5060bb292d96e6fc171797f863ea80774cf49504191b6c237f5a30'
OLD_PALETTE=[['VNU Renai RHB front right cap muted gray brown','#8F857B'],['VNU Renai RHB unverified walls windows neutral','#B8BAB5']]
N='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
NS={'m':N}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def build(src,dst):
    assert sha(src/'model.stl')==STL and sha(src/'color-mesh.npz')==NPZ
    raw=(src/'model.stl').read_bytes()
    st=np.frombuffer(raw[84:],dtype=np.dtype([('normal','<f4',(3,)),('pos','<f4',(3,3)),('a','<u2')]))['pos']
    assert len(st)==struct.unpack_from('<I',raw,80)[0]==2940
    def mask(t):
        eps=1e-5
        return (abs(t[:,:,0]-68).max(1)<eps)&(t[:,:,1].min(1)>=-17-eps)&(t[:,:,1].max(1)<=27+eps)&(t[:,:,2].min(1)>=2.8-eps)&(t[:,:,2].max(1)<=71+eps)
    sel=mask(st)
    assert np.flatnonzero(sel).tolist()==IDS and len(IDS)==34
    st64=st.astype(float); n=np.cross(st64[:,1]-st64[:,0],st64[:,2]-st64[:,0])
    assert np.all(n[sel,0]>0) and np.array_equal(n[sel,1:],np.zeros((34,2))) and np.isclose(n[sel,0].sum()/2,2855)
    d=np.load(src/'color-mesh.npz')
    v,f,old=(d[k] for k in ('vertices','faces','materials'))
    assert np.array_equal(v[f],st64) and collections.Counter(old.tolist())=={0:4,1:2936} and np.all(old[sel]==1)
    new=old.copy();new[sel]=2
    assert json.loads((src/'palette.json').read_text())==OLD_PALETTE
    dst.mkdir(exist_ok=True,parents=True)
    np.savez_compressed(dst/'color-mesh.npz',vertices=v,faces=f,materials=new)
    (dst/'palette.json').write_text(json.dumps(OLD_PALETTE+[[NAME,HEX]],indent=2)+'\n')
    E.register_namespace('',N)
    with zipfile.ZipFile(src/'appearance.3mf') as oldzip:
        root=E.fromstring(oldzip.read('3D/3dmodel.model'))
        mat=root.find('m:resources/m:basematerials',NS)
        assert [tuple(x.attrib[k] for k in ('name','displaycolor')) for x in mat]==[(n,h+'FF') for n,h in OLD_PALETTE]
        E.SubElement(mat,'{'+N+'}base',name=NAME,displaycolor=HEX+'FF')
        obj=root.find('m:resources/m:object',NS)
        obj.set('pid','1');obj.set('pindex','1') # Strict SDK requires explicit object-level default.
        vx=obj.findall('m:mesh/m:vertices/m:vertex',NS); ts=obj.findall('m:mesh/m:triangles/m:triangle',NS)
        old_v=np.array([[float(x.get(k)) for k in ['x','y','z']] for x in vx])
        assert np.array_equal(old_v.astype('float32'),v.astype('float32'))
        assert np.array_equal(np.array([[int(x.get(k)) for k in ['v1','v2','v3']] for x in ts]),f)
        assert [int(x.get('p1')) for x in ts]==old.tolist() and all(x.get('pid')=='1' for x in ts)
        for i in IDS:ts[i].set('p1','2')
        with zipfile.ZipFile(dst/'appearance.3mf','w',zipfile.ZIP_DEFLATED) as zout:
            for name in oldzip.namelist():
                info=zipfile.ZipInfo(name,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                data=E.tostring(root,encoding='utf-8',xml_declaration=True) if name=='3D/3dmodel.model' else oldzip.read(name)
                zout.writestr(info,data)
if __name__=='__main__':build(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve())
