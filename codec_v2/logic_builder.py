"""Native DIGITAL DAG compiler: aligned layers, dedicated fanout lanes, exact topology."""
from digital_network import *
from pathlib import Path
import json,itertools
class LogicCircuit:
 def __init__(self,name,inputs,gates,outputs):
  self.name=name;self.inputs=inputs;self.gates=gates;self.outputs=outputs
 def evaluate(self,values):
  v=dict(zip(self.inputs,values))
  for name,kind,ins in self.gates:
   a=[v[s] for s in ins]
   if kind=='Not':z=not a[0]
   elif kind.startswith('And'):z=all(a)
   elif kind.startswith('Nand'):z=not all(a)
   elif kind.startswith('Or'):z=any(a)
   elif kind.startswith('Nor'):z=not any(a)
   elif kind.startswith('Xor'):z=sum(a)%2
   elif kind.startswith('Xnor'):z=not(sum(a)%2)
   else:raise ValueError(kind)
   v[name]=int(z)
  return tuple(v[o] for o in self.outputs)
 def build(self):
  n=DigitalNetwork();drivers={};loads={};levels={s:0 for s in self.inputs};placements={};gate_specs=[]
  for name,kind,ins in self.gates:levels[name]=1+max(levels[i] for i in ins)
  layers={}
  for name,kind,ins in self.gates:layers.setdefault(levels[name],[]).append((name,kind,ins))
  maxrows=max([len(self.inputs)]+[len(v) for v in layers.values()]);height=max(480,maxrows*160);top=1080;bottom=top-height
  for i,s in enumerate(self.inputs):
   y=top-70-i*(height//max(1,len(self.inputs)-1));x=700
   sw=n.add(38,x,y,0,[49+i],f'S{i}',label=s)
   src=n.add(2,x-120,y+40,3,[5,0,0],f'V{i}',unit=2);g=n.ground(x-170,y-10);low=n.ground(x+60,y-65)
   n.connect(src,1,g,0,'0',[(x-170,y+30)])
   n.connect(src,0,sw,2,f'VCC{i}',[(x-35,y+30)])
   n.connect(sw,1,low,0,'0',[(x+60,y+10)])
   drivers[s]=(sw,0);loads[s]=[]
  for lev,items in sorted(layers.items()):
   x=1050+(lev-1)*300
   for i,(name,kind,ins) in enumerate(items):
    y=top-70-(height//2 if len(items)==1 else round(i*height/(len(items)-1)));g=n.addgate(kind,x,y,name,name);placements[name]=(x,y);drivers[name]=(g,1 if kind=='Not' else 2);loads.setdefault(name,[])
    pins=[0] if kind=='Not' else ([0,1] if len(ins)==2 else [0,1,3] if len(ins)==3 else None)
    if pins is None:raise ValueError('only1..3 inputs supported')
    for s,pin in zip(ins,pins):loads.setdefault(s,[]).append((g,pin))
  outx=1050+max(levels.values())*300
  for i,s in enumerate(self.outputs):
   y=top-70-round(i*height/max(1,len(self.outputs)-1));p=n.addgate('ProbeR',outx,y,'OUT'+str(i),s,orientation=2);loads[s].append((p,0))
  # Branch nodes form an ordered vertical backbone to each net's distinct receivers.
  for rank,(s,targets) in enumerate(loads.items()):
   if not targets:continue
   source=drivers[s];start=n.pin(*source);targetpins=[n.pin(*t) for t in targets]
   trunkx=start[0]+70+(rank%4)*12
   if self.inputs.count(s):trunkx=820+rank*26
   # Each receiver gets its own native junction, preserving no duplicate terminals.
   nodes=[]
   ys=sorted(set([p[1] for p in targetpins]+[start[1]]),reverse=True)
   ymap={}
   for j,y in enumerate(ys):ymap[y]=n.junction(trunkx,y,f'{s}_J{j}')
   sourcej=ymap[start[1]];n.connect(*source,sourcej,0,s)
   for u,v in zip(ys,ys[1:]):n.connect(ymap[u],3,ymap[v],1,s)
   per_y={}
   for target,(tx,ty) in zip(targets,targetpins):per_y.setdefault(ty,[]).append(target)
   for y,group in per_y.items():
    j=ymap[y];free=2
    if len(group)>1:
     for k,target in enumerate(group):
      jj=n.junction(trunkx+30+(k*25),y-20-k*12,f'{s}_T{k}');n.connect(j,free,jj,0,s,[(n.pin(j,free)[0]+15,n.pin(j,free)[1]),(n.pin(j,free)[0]+15,n.pin(jj,0)[1])]);n.connect(jj,2,*target,s,[(n.pin(*target)[0]-30,n.pin(jj,2)[1]),(n.pin(*target)[0]-30,n.pin(*target)[1])]);j=jj;free=3
    else:n.connect(j,free,*group[0],s)
  zoom=max(10,min(90,round(1100/(outx-520)*100),round(620/(height+240)*100)))
  p=n.emit(self.name+'.ewb',zoom)
  table=[dict(inputs=dict(zip(self.inputs,v)),outputs=dict(zip(self.outputs,self.evaluate(v)))) for v in itertools.product([0,1],repeat=len(self.inputs))]
  p.with_suffix('.truth.json').write_text(json.dumps(table,indent=2));p.with_suffix('.logic.json').write_text(json.dumps(dict(inputs=self.inputs,gates=self.gates,outputs=self.outputs),indent=2));return p

def halfadder():return LogicCircuit('HA_layout',['A','B'],[('S','Xor2',['A','B']),('C','And2',['A','B'])],['S','C'])
def fulladder():return LogicCircuit('FullAdder',['A','B','Cin'],[('P','Xor2',['A','B']),('G','And2',['A','B']),('S','Xor2',['P','Cin']),('H','And2',['P','Cin']),('Cout','Or2',['G','H'])],['S','Cout'])
if __name__=='__main__':print(fulladder().build())
