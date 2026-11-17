from pathlib import Path
import struct
R=Path(__file__).resolve().parents[1]
for name in ['preview','rear','front','back','west','east','top','entry-detail','facade-detail','roof-detail']:
 p=R/(name+'.png');b=p.read_bytes();out=b[:8];pos=8
 while pos<len(b):
  n=struct.unpack('>I',b[pos:pos+4])[0];kind=b[pos+4:pos+8]
  if kind not in [b'tEXt',b'zTXt',b'iTXt',b'eXIf']:out+=b[pos:pos+n+12]
  pos+=n+12
 p.write_bytes(out)
