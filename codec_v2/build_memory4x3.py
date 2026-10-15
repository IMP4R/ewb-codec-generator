"""Four words by three bits: address decoder, gated D latches, mux and tri-state output."""
from logic_builder import *
from pathlib import Path

def memory():
 n=DigitalNetwork();driver={};loads={}
 inputs=['A1','A0','D2','D1','D0','WE','OE']
 for i,s in enumerate(inputs):
  x=640;y=1360-i*160;sw=n.add(38,x,y,0,[49+i],'SW'+str(i),label=s);v=n.add(2,x-120,y+40,3,[5,0,0],'V'+str(i),unit=2);g=n.ground(x-170,y-10);lo=n.ground(x+60,y-65)
  n.connect(v,1,g,0,'0',[(x-170,y+30)]);n.connect(v,0,sw,2,'VCC'+str(i),[(x-35,y+30)]);n.connect(sw,1,lo,0,'0',[(x+60,y+10)]);driver[s]=(sw,0);loads[s]=[]
 def add(name,kind,x,y,ins):
  idx=n.addgate(kind,x,y,name,name);driver[name]=(idx,1 if kind=='Not' else 2);loads.setdefault(name,[])
  for s,p in zip(ins,[0] if kind=='Not' else [0,1] if len(ins)==2 else [0,1,3]):loads.setdefault(s,[]).append((idx,p))
  return idx
 add('NA1','Not',960,1390,['A1']);add('NA0','Not',960,1320,['A0'])
 selects=[]
 for row,bits in enumerate([(0,0),(0,1),(1,0),(1,1)]):
  y=1240-row*260;sel=f'ADDR{row}';add(sel,'And2',1170,y,['A1' if bits[0] else 'NA1','A0' if bits[1] else 'NA0']);selects.append(sel);add(f'WR{row}','And2',1380,y,[sel,'WE'])
 for bit in [2,1,0]:add(f'ND{bit}','Not',960,1090-bit*100,[f'D{bit}'])
 # twelve gated D latches made from cross-coupled NAND pairs, grouped by word and bit.
 for row in range(4):
  for bit in [2,1,0]:
   x=1660+(2-bit)*500;y=1240-row*260
   sn=f'S{row}{bit}';rn=f'R{row}{bit}';q=f'Q{row}{bit}';qn=f'NQ{row}{bit}'
   add(sn,'Nand2',x,y+55,[f'D{bit}',f'WR{row}']);add(rn,'Nand2',x,y-55,[f'ND{bit}',f'WR{row}'])
   add(q,'Nand2',x+210,y+55,[sn,qn]);add(qn,'Nand2',x+210,y-55,[rn,q])
 # Read selection and tri-state output, one independent bit-plane column.
 for bit in [2,1,0]:
  x=3400+(2-bit)*320
  for row in range(4):add(f'RD{row}{bit}','And2',x,1240-row*260,[f'Q{row}{bit}',selects[row]])
  add(f'ORa{bit}','Or2',x+160,1130,[f'RD0{bit}',f'RD1{bit}']);add(f'ORb{bit}','Or2',x+160,610,[f'RD2{bit}',f'RD3{bit}']);add(f'READ{bit}','Or2',x+320,870,[f'ORa{bit}',f'ORb{bit}'])
  tr=n.addgate('Tri',x+520,870,'TR'+str(bit),'OUTPUT'+str(bit));loads[f'READ{bit}'].append((tr,0));loads['OE'].append((tr,1));pr=n.addgate('ProbeR',x+700,870,'OUT'+str(bit),'DO'+str(bit),orientation=2);n.connect(tr,2,pr,0,'DO'+str(bit))
 # Each fanout is a separate narrow orthogonal signal channel, unique physical branch pins.
 for rank,(s,targets) in enumerate(loads.items()):
  if not targets:continue
  src=driver[s];sp=n.pin(*src);pins=[n.pin(*t) for t in targets]
  trunk=sp[0]+70+(rank%5)*12
  if s in inputs:trunk=780+inputs.index(s)*22
  ys=sorted(set([sp[1]]+[p[1] for p in pins]),reverse=True);js={y:n.junction(trunk,y,s+'_J'+str(i)) for i,y in enumerate(ys)}
  n.connect(*src,js[sp[1]],0,s)
  for a,b in zip(ys,ys[1:]):n.connect(js[a],3,js[b],1,s)
  groups={}
  for target,pin in zip(targets,pins):groups.setdefault(pin[1],[]).append(target)
  for y,group in groups.items():
   j=js[y];free=2
   for k,target in enumerate(group):
    if k<len(group)-1:
     jj=n.junction(trunk+30+k*18,y-25-k*15,s+'_T'+str(k));a=n.pin(j,free);b=n.pin(jj,0);n.connect(j,free,jj,0,s,[(a[0]+10,a[1]),(a[0]+10,b[1])]);a=n.pin(jj,2);b=n.pin(*target);lane=b[0]-20;n.connect(jj,2,*target,s,[(lane,a[1]),(lane,b[1])]);j=jj;free=3
    else:n.connect(j,free,*target,s)
 p=n.emit('Memory4x3.native.ewb',35);return p
if __name__=='__main__':print(memory())
