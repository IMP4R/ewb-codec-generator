from pathlib import Path
import re
from codec import *
BASEFILE=Path(__file__).with_name('server201.ewb')
def section(text,name,indent=4):
 pat=' '*indent+name+' \r\n';start=text.index(pat);op=text.index('{',start);depth=1;end=op+1
 while depth:
  if text[end]=='{':depth+=1
  elif text[end]=='}':depth-=1
  end+=1
 if text[end:end+2]=='\r\n':end+=2
 return start,end,text[start:end]
def replace_section(text,name,body):
 a,b,_=section(text,name);return text[:a]+'    '+name+' \r\n    { \r\n'+body+'    }\r\n'+text[b:]
def comp(pn,x,y,orient=0,value=None,ref=''):
 valuefield='' if value is None else f'        Value r:{len(value)} '+' '.join(map(str,value))+' \r\n'
 modelunits='2 2 0' if pn==13 else ('3 2 0 0' if pn==2 else '1 0')
 model='        ModelName R "spice:QN" \r\n' if pn==5 else '        ModelName R "" \r\n'
 return f'      Comp \r\n      {{ \r\n        PartNum i {pn} \r\n        Position i:3 {orient} {x} {y} \r\n'+valuefield+f'        ModelUnits i:{modelunits} \r\n        Common \r\n        {{ \r\n          RefID A "{ref}" \r\n        }}\r\n'+model+'        Status i 0 \r\n      }\r\n'
def base():return b''.join(map(explode,unpack(BASEFILE.read_bytes()))).decode('cp1251')
def emit(name,comps,wires=''):
 t=base();t=replace_section(t,'Elements',''.join(comps));t=replace_section(t,'Wires',wires)
 if '    AnalysisValues \r\n' in t:
  a,b,_=section(t,'AnalysisValues');t=t[:a]+t[b:]
 t=re.sub(r'ZoomFactor i \d+', 'ZoomFactor i 100',t)
 p=Path(__file__).with_name(name);p.with_suffix('.txt').write_bytes(t.encode('cp1251'));p.write_bytes(encode_ewb(t.encode('cp1251')));return p
if __name__=='__main__':
 c=[]
 for o in range(4):c.append(comp(2,800+o*160,650,o,[5,0,1],f'S{o}'))
 for o in range(4):c.append(comp(1,800+o*160,800,o,[1000,0,0,0,0],f'R{o}'))
 for o in range(4):c.append(comp(5,800+o*160,950,o,None,f'Q{o}'))
 for o in range(4):c.append(comp(8,800+o*160,1080,o,[0],''))
 print(emit('symbol_probe.ewb',c))
