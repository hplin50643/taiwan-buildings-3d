from pathlib import Path
import tempfile,json,numpy as np,shutil
import build_appearance as old
A=old.A;R=old.R;base=old.classify;REVIEW=json.loads((Path(__file__).parent/'rear-roof-domain.json').read_text())['candidate']
def classify(tri):
 color,why=base(tri);q=tri.copy();q[:,:,:2]/=1.75;q[:,:,2]=(q[:,:,2]-1.6)/1.75;cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=cross/np.linalg.norm(cross,axis=1)[:,None];eps=.0001
 mask=(norm[:,1]>.4)&(norm[:,2]>.8)&(abs(q[:,:,2]-(29+(17.25-q[:,:,1])*1.8/3.45))<=eps).all(1)&(q[:,:,0]>=-30-eps).all(1)&(q[:,:,0]<=30+eps).all(1)&(q[:,:,1]>=13.8-eps).all(1)&(q[:,:,1]<=17.25+eps).all(1)
 ids=np.flatnonzero(mask).tolist();assert ids==REVIEW['faces'] and not color[mask].any();area=float(np.linalg.norm(cross[mask],axis=1).sum()/2);assert abs(area-REVIEW['analytic_area_mm2'])<.001;color[mask]=2;why[mask]='same_paired_roof_family_north_sloping_strip_explicit_material_inference'
 (A/'qa-continuous-walls').mkdir(exist_ok=True);(A/'qa-continuous-walls/selection.json').write_text(json.dumps(dict(face_ids=ids,changed_faces=len(ids),area_mm2=area,analytic_area_mm2=REVIEW['analytic_area_mm2'],no_geometry_change=True),indent=2)+'\n');return color,why
def main():
 with tempfile.TemporaryDirectory() as td:
  temp=Path(td);(temp/'source').mkdir();shutil.copyfile(Path(__file__).parent/'source-selection.json',temp/'source/source-selection.json');old.A=temp;old.R=R;old.classify=classify;old.main()
  for n in ['chu-administration-library-appearance.3mf','face-materials.json','palette.json']:shutil.copyfile(temp/n,A/n)
 p=A/'palette.json';d=json.loads(p.read_text());d['scope']='Preserve230existingcoloredfacesand4materials;add18originalnorthslopingstripfaceswithmaterial2bypairedroof-familyinference,notrearphotographicproof.No2026conditionclaim.19432neutralfaces.';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
