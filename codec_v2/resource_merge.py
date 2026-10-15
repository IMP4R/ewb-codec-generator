from pathlib import Path
import struct
ROOT=Path(__file__).parent
def entries(blob):
 n,off,x,y=struct.unpack('<HIHH',blob[-10:]);out=[]
 for i in range(n):
  rec=blob[off+i*21:off+(i+1)*21]
  name=rec[:13].rstrip(b'\0');start,size=struct.unpack('<II',rec[13:]);out.append((name,blob[start:start+size]))
 return out
if __name__=='__main__':
 base=(ROOT/'WEWB.RES').read_bytes();din=(ROOT/'WEWBDIN.RES').read_bytes()
 a=entries(base);b=entries(din);print('BASE',[n for n,_ in a]);print('DIN',[n for n,_ in b][:20])
 data=bytearray(base[:38]);merged={}
 for n,v in a+b:merged[n]=v
 records=[]
 for n,v in merged.items():
  off=len(data);data.extend(v);records.append(n.ljust(13,b'\0')+struct.pack('<II',off,len(v)))
 idx=len(data)
 for r in records:data.extend(r)
 data.extend(struct.pack('<HIHH',len(records),idx,0x4802,0xaaaa))
 (ROOT/'WEWBEXACT.RES').write_bytes(data)
 print('MERGED',len(data),'entries',len(records))
