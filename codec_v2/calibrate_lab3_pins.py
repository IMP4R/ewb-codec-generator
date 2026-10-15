"""Diagnostic outside submission: calibrate NOT and multi-input native gates."""
from digital_network import DigitalNetwork
from build_lab3_variant1_forms import split_net
class CalibrationNetwork(DigitalNetwork):
 def pin(self,i,p):
  c=self.spec[i]
  if c.get('name','') in ('And2','And3','Or3','And4','Or4'):
   arity=int(c['name'][-1]);return (c['x']+50,c['y']) if p==arity else (c['x']-10,c['y']+10*(arity-1)-20*p)
  return super().pin(i,p)
n=CalibrationNetwork()
s=n.source(650,1100,'V',horizontal=True);n.connect(s,1,n.ground(750,1070),0,'0')
cases=[('Not',0,1),('And2',None,2),('And3',None,3),('Or3',None,3),('And4',None,4),('Or4',None,4)]
loads=[]
for i,(kind,ip,op) in enumerate(cases):
 x=1000+(i%3)*260;y=1000-(i//3)*300
 g=n.addgate(kind,x,y,'T'+str(i),kind+'-'+str(ip))
 pr=n.addgate('ProbeR',x+140,y,'P'+str(i),str(i),orientation=2)
 n.connect(g,op,pr,0,str(i))
 pins=[ip] if ip is not None else list(range(int(kind[-1])))
 loads.extend((g,p) for p in pins)
split_net(n,(s,0),loads,850,1090,'HIGH')
print(n.emit('calibrate_lab3_pins.ewb',zoom=80))
