"""EWB v5 transport and PKWARE DCL decoder; no EWB process required."""
from pathlib import Path
import re,zlib
LITREP=[11,124,8,7,28,7,188,13,76,4,10,8,12,10,12,10,8,23,8,9,7,6,7,8,7,6,55,8,23,24,12,11,7,9,11,12,6,7,22,5,7,24,6,11,9,6,7,22,7,11,38,7,9,8,25,11,8,11,9,12,8,12,5,38,5,38,5,11,7,5,6,21,6,10,53,8,7,24,10,27,44,253,253,253,252,252,252,13,12,45,12,45,12,61,12,45,44,173]
LENREP=[2,35,36,53,38,23]
DISTREP=[2,20,53,230,247,151,248]
BASE=[3,2,4,5,6,7,8,9,10,12,16,24,40,72,136,264]
EXTRA=[0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8]
def lengths(rep):
 return [v&15 for v in rep for _ in range((v>>4)+1)]
def table(rep):
 ls=lengths(rep); count=[ls.count(n) for n in range(14)]; syms=sorted(range(len(ls)),key=lambda i:(ls[i],i));return count,syms
class Bits:
 def __init__(self,data):self.data=data;self.pos=0
 def read(self,n):
  if self.pos+n>len(self.data)*8:raise EOFError(self.pos)
  v=sum(((self.data[(self.pos+k)//8]>>((self.pos+k)%8))&1)<<k for k in range(n));self.pos+=n;return v
 def decode(self,t):
  count,syms=t;code=first=index=0
  for ln in range(1,14):
   code|=self.read(1)^1;c=count[ln]
   if code<first+c:return syms[index+code-first]
   index+=c;first=(first+c)<<1;code<<=1
  raise ValueError('invalid Huffman code')
def unpack(data):
 start=data.index(b'\n',data.index(b'UsingVectorGraphics:'))+1
 tail=data[start:].replace(b'\r',b'').replace(b'\n',b'');end=tail.rfind(b'$!');body=tail[:end]
 assert body.startswith(b'/')
 chunks=body[1:].split(b'$');streams=[]
 for s in chunks:
  assert len(s)%2==0,(len(s),s[-8:])
  streams.append(bytes(((s[i]-48)<<3)|((s[i+1]-48)>>2) for i in range(0,len(s),2)))
 return streams
def explode(data):
 b=Bits(data);lit=b.read(8);dictbits=b.read(8)
 assert lit in (0,1) and dictbits in (4,5,6),(lit,dictbits)
 out=bytearray();lt=table(LITREP);nt=table(LENREP);dt=table(DISTREP)
 while True:
  if b.read(1):
   sym=b.decode(nt);ln=BASE[sym]+b.read(EXTRA[sym])
   if ln==519:break
   n=2 if ln==2 else dictbits;dist=(b.decode(dt)<<n)+b.read(n)+1
   if dist>len(out):raise ValueError(('distance',dist,len(out)))
   for _ in range(ln):out.append(out[-dist])
  else:out.append(b.decode(lt) if lit else b.read(8))
 return bytes(out)
def implode_literals(data):
 # Valid PKWARE DCL binary-mode stream. Literal-only avoids any heuristic LZ parser.
 nt=table(LENREP);codes={};count,syms=nt;first=index=0
 for ln in range(1,14):
  for k in range(count[ln]):
   canonical=first+k
   codes[syms[index+k]]=[1-((canonical>>(ln-1-j))&1) for j in range(ln)]
  index+=count[ln];first=(first+count[ln])<<1
 bits=[]
 def put(value,n):bits.extend((value>>j)&1 for j in range(n))
 put(0,8);put(4,8)
 dt=table(DISTREP);dcodes={};cnt,syms=dt;first=index=0
 for ln in range(1,14):
  for k in range(cnt[ln]):
   c=first+k;dcodes[syms[index+k]]=[1-((c>>(ln-1-j))&1) for j in range(ln)]
  index+=cnt[ln];first=(first+cnt[ln])<<1
 pos=0
 while pos<len(data):
  best=0;distance=0
  for dist in range(1,min(pos,1024)+1):
   if data[pos]!=data[pos-dist]:continue
   ln=0
   while ln<min(518,len(data)-pos) and data[pos+ln]==data[pos+ln-dist]:ln+=1
   if ln>best:best=ln;distance=dist
  if best>=3:
   sym=next(i for i in range(16) if BASE[i]<=best<=BASE[i]+(1<<EXTRA[i])-1)
   put(1,1);bits.extend(codes[sym]);put(best-BASE[sym],EXTRA[sym])
   db=4;bits.extend(dcodes[(distance-1)>>db]);put((distance-1)&15,db);pos+=best
  else:put(0,1);put(data[pos],8);pos+=1
 put(1,1);bits.extend(codes[15]);put(255,8)
 bits.extend([0]*((-len(bits))%8))
 return bytes(sum(bits[i+j]<<j for j in range(8)) for i in range(0,len(bits),8))
def encode_ewb(text,header=None):
 if header is None:header=b'Electronics Workbench Circuit File\r\nVersion: 5\r\nCharset: ANSI\r\nDescription: \r\n"" \r\n\r\nEncryptionType: 2\r\nUsingVectorGraphics: 0\r\n'
 rawchunks=[text[i:i+1024] for i in range(0,len(text),1024)]
 bodies=[];crc=0
 for raw in rawchunks:
  packed=implode_literals(raw);assert explode(packed)==raw
  bodies.append(bytes(v for ch in packed for v in ((ch>>3)+48,((ch&7)<<2)+48)))
  crc^=zlib.crc32(raw)
 body=b'/'+b'$'.join(bodies)+b'$!'+f'{crc:08x}'.encode()
 main=body[:-10];checksum=body[-10:]
 return header+main[:66]+b'\n'+b'\n'.join(main[i:i+65] for i in range(66,len(main),65))+checksum

if __name__=='__main__':
 import sys
 p=Path(sys.argv[1]);out=b''.join(explode(chunk) for chunk in unpack(p.read_bytes()));dest=p.with_suffix('.decoded.txt');dest.write_bytes(out)
 print(p,len(out),out[:80],hex(zlib.crc32(out)),dest)
