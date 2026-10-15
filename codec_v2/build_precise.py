"""Reproducible exact-reference DIN inverter build, independent of live EWB."""
from pathlib import Path
import re
from schematic import section,replace_section
from inverter_layout import wire
from codec import encode_ewb,explode,unpack
ROOT=Path(__file__).parent

def build():
 t=(ROOT/'match115g.txt').read_bytes().decode('cp1251')
 t=t.replace('Info i:10 1 0 100 1','Info i:10 1 0 100 0')
 _,_,elements=section(t,'Elements')
 blocks=re.findall(r'      Comp \r\n      \{ .*?\r\n      \}\r\n',elements,re.S)
 positions=[(0,1130,880),(1,1150,977),(1,1208,1060),(0,1020,817),(0,1020,751),(0,1140,751),(0,1300,1009),(0,1209,860),(0,1155,940),(0,1155,820)]
 for i,(o,x,y) in enumerate(positions):
  blocks[i]=re.sub(r'Position i:3 \d+ -?\d+ -?\d+',f'Position i:3 {o} {x} {y}',blocks[i])
 t=replace_section(t,'Elements',''.join(blocks))
 w=''
 w+=wire(1,1,2,0,[(2,53),(1,58)],'3')
 w+=wire(2,1,6,0,[(1,44),(8,26)],'0')
 w+=wire(1,0,8,1,[(8,22)],'1')
 w+=wire(8,3,0,1,[(8,5)],'1')
 w+=wire(3,0,0,0,[(2,29),(1,90)],'2')
 w+=wire(3,1,4,0,[(8,35)],'0')
 w+=wire(0,2,9,1,[(8,45)],'0')
 w+=wire(9,3,5,0,[(8,29)],'0')
 w+=wire(8,2,7,1,[(1,104),(8,25)],'1')
 w+=wire(9,2,7,0,[(1,104),(2,32)],'0')
 t=replace_section(t,'Wires',w)
 raw=t.encode('cp1251');encoded=encode_ewb(raw)
 assert b''.join(explode(block) for block in unpack(encoded))==raw
 return raw,encoded
if __name__=='__main__':
 raw,encoded=build();(ROOT/'Inverter.ewb').write_bytes(encoded);(ROOT/'Inverter.txt').write_bytes(raw)
 print('Built real DIN Inverter.ewb:',len(encoded),'bytes; plaintext',len(raw),'bytes')
