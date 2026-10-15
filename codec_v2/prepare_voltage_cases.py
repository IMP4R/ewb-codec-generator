from pathlib import Path
import re
from codec import unpack,explode,encode_ewb
root=Path('/Users/user0/АВУ/сдача/Лаб_3/ewb');out=Path('/Users/user0/ewb_rev/codec_v2/voltage_cases');out.mkdir(exist_ok=True)
for name in ['NAND','NOR','Inverter']:
 raw=b''.join(explode(s) for s in unpack((root/(name+'.ewb')).read_bytes())).decode('cp1251')
 sources=[]
 for m in re.finditer(r'      Comp\s*\{.*?\n      \}',raw,re.S):
  b=m.group();v=re.search(r'Value r:3 ([\d.]+) 0 0',b)
  if 'PartNum i 2' in b and v and float(v[1])==100:sources.append((m.start(),m.end(),b))
 assert len(sources)==(1 if name=='Inverter' else 2),(name,len(sources))
 for j in range(2**len(sources)):
  bits=f'{j:0{len(sources)}b}';t=raw
  for bit,(start,end,b) in reversed(list(zip(bits,sources))):
   replacement=re.sub(r'Value r:3 100 0 0',f'Value r:3 {2000 if bit=="1" else 100} 0 0',b)
   t=t[:start]+replacement+t[end:]
  p=out/f'{name}_{bits}.ewb';p.write_bytes(encode_ewb(t.encode('cp1251')));print(p)
