"""Publication metadata hygiene, no geometry modification."""
from pathlib import Path
import struct,re,json,argparse,math
path=Path(__file__).resolve().parent/'scene.blend'
b=path.read_bytes();assert b[:7]==b'BLENDER' and b[7:9]==b'-v','Expected uncompressed 64-bit little-endian Blend'
o=12;blocks=[]
while o+24<=len(b):
 code,n,ptr,idx,count=struct.unpack_from('<4sIQII',b,o);blocks.append((code,n,ptr,idx,count,o+24));o+=24+n
 if code==b'ENDB':break
blk=next(x for x in blocks if x[0]==b'DNA1');data=b[blk[5]:blk[5]+blk[1]];assert data[:8]==b'SDNANAME';o=8
n=struct.unpack_from('<I',data,o)[0];o+=4;names=[]
for _ in range(n):z=data.index(0,o);names.append(data[o:z].decode());o=z+1
o=(o+3)&~3;assert data[o:o+4]==b'TYPE';o+=4;n=struct.unpack_from('<I',data,o)[0];o+=4;types=[]
for _ in range(n):z=data.index(0,o);types.append(data[o:z].decode());o=z+1
o=(o+3)&~3;assert data[o:o+4]==b'TLEN';o+=4;lens=struct.unpack_from('<'+str(n)+'H',data,o);o+=2*n;o=(o+3)&~3;assert data[o:o+4]==b'STRC';o+=4;n=struct.unpack_from('<I',data,o)[0];o+=4;structs=[];byname={}
for _ in range(n):
 t,nf=struct.unpack_from('<HH',data,o);o+=4;fields=[];offset=0
 for _ in range(nf):
  ft,fn=struct.unpack_from('<HH',data,o);o+=4;name=names[fn];size=(8 if '*' in name else lens[ft])*math.prod(int(x)for x in re.findall(r'\[(\d+)\]',name));fields.append({'type':types[ft],'name':name,'offset':offset,'size':size});offset+=size
 rec={'name':types[t],'size':lens[t],'fields':fields,'computed_size':offset};structs.append(rec);byname[types[t]]=rec
for name in ('FileSelectParams','RenderData','Scene'):assert byname[name]['computed_size']==byname[name]['size'],name

changed=bytearray(b);ranges=[]
fp=next(f for f in byname['FileSelectParams']['fields'] if f['name']=='dir[1090]')
rp=next(f for f in byname['RenderData']['fields'] if f['name']=='pic[1024]')
sr=next(f for f in byname['Scene']['fields'] if f['type']=='RenderData' and f['name']=='r')
for code,n,ptr,idx,count,start in blocks:
 if code in (b'DNA1',b'ENDB'):continue
 st=structs[idx]
 for j in range(count):
  if st['name']=='FileSelectParams':off=start+j*st['size']+fp['offset'];size=fp['size'];val=b'//';field='FileSelectParams.dir'
  elif st['name']=='Scene':off=start+j*st['size']+sr['offset']+rp['offset'];size=rp['size'];val=b'//court-oblique.png';field='Scene.r.pic'
  else:continue
  new=val+b'\0'*(size-len(val));changed[off:off+size]=new;ranges.append({'field':field,'offset':off,'size':size,'value':val.decode(),'entire_tail_zero':True})
assert ranges
cursor=0
for item in sorted(ranges,key=lambda x:x['offset']):
 off=item['offset'];assert b[cursor:off]==changed[cursor:off];cursor=off+item['size']
assert b[cursor:]==changed[cursor:]
path.write_bytes(changed)
import hashlib,zlib
pngs=[]
for png in path.parent.glob('*.png'):
 raw=png.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';out=raw[:8];pos=8;before=[];after=[];removed=[]
 while pos<len(raw):
  size=struct.unpack_from('>I',raw,pos)[0];kind=raw[pos+4:pos+8];data=raw[pos+8:pos+8+size];chunk=raw[pos:pos+size+12]
  assert zlib.crc32(kind+data)&0xffffffff==struct.unpack('>I',chunk[-4:])[0]
  if kind==b'IDAT':before.append(data)
  if kind in (b'tEXt',b'zTXt',b'iTXt'):removed.append(kind.decode())
  else:
   out+=chunk
   if kind==b'IDAT':after.append(data)
  pos+=size+12
 assert pos==len(raw) and before==after;png.write_bytes(out);pngs.append({'path':png.name,'removed_text_chunks':removed,'IDAT_exact':True,'sha256':hashlib.sha256(out).hexdigest()})
report={'method':'Embedded SDNA declared offsets; entire fixed buffers zeroed after relative value, every byte outside declared fields unchanged. PNG textual chunks removed, IDAT identical.','fields':ranges,'scene_sha256':hashlib.sha256(changed).hexdigest(),'outside_declared_fields_exact':True,'png':pngs}
(path.parent/'metadata-hygiene.json').write_text(json.dumps(report,indent=2)+'\n')
