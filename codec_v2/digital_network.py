from network import Network
from digital import gate,emit_digital
class DigitalNetwork(Network):
 def addgate(self,name,x,y,ref,label='',orientation=0):
  self.components.append(gate(name,x,y,ref,label,orientation));self.spec.append(dict(pn=99,name=name,x=x,y=y,o=orientation,ref=ref));return len(self.spec)-1
 def pin(self,i,p):
  c=self.spec[i]
  if c['pn']!=99:return super().pin(i,p)
  x,y,name=c['x'],c['y'],c['name']
  if name.startswith('Probe'):return (x+(-20 if c['o']==2 else 20),y)
  if name=='Not':return [(x-10,y),(x+50,y)][p]
  if name.endswith('2'):return [(x-10,y+10),(x-10,y-10),(x+50,y)][p]
  if name in ('And3','Or3','Nand3','Nor3','Xor3','Xnor3'):return [(x-10,y+10),(x-10,y),(x+50,y),(x-10,y-10)][p]
  if name in ('And4','Or4','Nand4','Nor4','Xor4','Xnor4'):return [(x-10,y+20),(x-10,y+10),(x+50,y),(x-10,y-10),(x-10,y-20)][p]
  if name=='Tri':return [(x-10,y+10),(x-10,y-10),(x+50,y)][p]
  if name=='D':return [(x-10,y+20),(x-10,y),(x+50,y+20),(x+50,y)][p]
  if name=='DN':return [(x-10,y+10),(x-10,y),(x-10,y+20),(x-10,y-10),(x+50,y+20),(x+50,y-10)][p]
  raise ValueError(('unverified digitalpin',c,p))
 def emit(self,name,zoom=100):
  wires=''.join(__import__('inverter_layout').wire(e['a'],e['pa'],e['b'],e['pb'],e['segments'],e['node']) for e in self.connections)
  p=emit_digital(name,self.components,wires,zoom)
  import json
  p.with_suffix('.topology.json').write_text(json.dumps(dict(components=self.spec,connections=self.connections),indent=2))
  return p
if __name__=='__main__':
 n=DigitalNetwork();a=n.addgate('And2',1000,850,'G1','AND');b=n.addgate('ProbeR',1200,850,'OUT','Q');g=n.ground(900,780);s=n.source(900,900,'V1',horizontal=True)
 # Probe accepts pin0? probe factoryuses0/2; test0 directly.
 n.connect(a,1,b,0,'Q');n.connect(a,0,g,0,'0');n.connect(a,2,s,0,'A');print(n.emit('digital_pins.ewb'))
