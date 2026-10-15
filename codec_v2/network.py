"""Native analog schematic builder with calibrated DIN terminal contracts."""
from pathlib import Path
import re,json
from schematic import *
from inverter_layout import wire
class Network:
 def __init__(self):self.components=[];self.spec=[];self.connections=[];self.used=set()
 def add(self,pn,x,y,orientation=0,value=None,ref='',label=None,unit=None):
  s=comp(pn,x,y,orientation,value,ref)
  if unit is not None:
   if pn==1:s=s.replace('ModelUnits i:1 0',f'ModelUnits i:1 {unit}')
   elif pn==2:s=s.replace('ModelUnits i:3 2 0 0',f'ModelUnits i:3 {unit} 0 0')
  opt=f'        Label R "{label or ""}" \r\n        useGlobalSchematicOpts i 0 \r\n        showLabel i 1 \r\n        showValue i {0 if pn in (5,8,9) else 1} \r\n        showRefID i 0 \r\n        showModel i 0 \r\n'
  s=s.replace('        Status i 0 \r\n','        Status i 0 \r\n'+opt)
  self.components.append(s);self.spec.append(dict(pn=pn,x=x,y=y,o=orientation,value=value,ref=ref));return len(self.spec)-1
 def q(self,x,y,ref):return self.add(5,x,y,0,None,ref)
 def resistor(self,x,y,ref='R',kilohms=1):return self.add(1,x,y,1,[kilohms,0,0,0,0],ref,unit=1)
 def source(self,x,y,ref='U1',mv=100,horizontal=False):return self.add(2,x,y,1 if horizontal else 0,[5 if horizontal else mv,0,0],ref,label='' if horizontal else ref,unit=2 if horizontal else 1)
 def ground(self,x,y):return self.add(8,x,y,0,[0],'')
 def meter(self,x,y,ref='M1'):return self.add(13,x,y,0,[1,0],ref)
 def junction(self,cx,cy,ref='N'):return self.add(9,cx+15,cy+20,0,[0],ref)
 def pin(self,i,p):
  c=self.spec[i];x,y,o=c['x'],c['y'],c['o'];pn=c['pn']
  if pn==5:return [(x-20,y+20),(x+10,y+50),(x+10,y-10)][p]
  if pn==9:return [(x-20,y-20),(x-15,y-15),(x-10,y-20),(x-15,y-25)][p]
  if pn==8:return (x,y+11)
  if pn==13:return (x+40,y+(-30 if p==0 else 30))
  if pn==1 and o==1:return (x-10,y+(-30 if p==0 else 20))
  if pn==2 and o==0:return (x,y+(25 if p==0 else -31))
  if pn==2 and o==1:return (x+(-10 if p==0 else 50),y-10)
  if pn==2 and o==3:return (x+(50 if p==0 else -10),y-10)
  if pn==38 and o==0:return [(x-10,y+20),(x+20,y+10),(x+20,y+30)][p]
  raise ValueError(('unknown terminal contract',c,p))
 def connect(self,a,pa,b,pb,node,points=None):
  assert (a,pa) not in self.used and (b,pb) not in self.used,('duplicate terminal',a,pa,b,pb)
  self.used|={(a,pa),(b,pb)};start=self.pin(a,pa);end=self.pin(b,pb)
  if points is None:points=[(start[0],end[1])] if start[0]!=end[0] and start[1]!=end[1] else []
  path=[start]+points+[end];segments=[]
  for (x,y),(xx,yy) in zip(path,path[1:]):
   if x==xx and y==yy:continue
   assert x==xx or y==yy,('nonorthogonal path',path)
   if xx>x:d=1;n=xx-x
   elif xx<x:d=4;n=x-xx
   elif yy>y:d=2;n=yy-y
   else:d=8;n=y-yy
   segments.append((d,n))
  if not segments:
   # Legacy EWB dereferences an absent segment array for segs i:0.
   # Coincident endpoints still require a native minimal segment record.
   segments=[(1,0)]
  self.connections.append(dict(a=a,pa=pa,b=b,pb=pb,node=node,path=path,segments=segments))
 def emit(self,name,zoom=100):
  wires=''.join(wire(e['a'],e['pa'],e['b'],e['pb'],e['segments'],e['node']) for e in self.connections)
  p=emit(name,self.components,wires);t=p.with_suffix('.txt').read_bytes().decode('cp1251')
  t=t.replace('Info i:10 1 0 100 1','Info i:10 1 0 100 0').replace('Manual i 0','Manual i 1').replace('Auto i 1','Auto i 0').replace('Reroute i 1','Reroute i 0');t=re.sub(r'ZoomFactor i \d+',f'ZoomFactor i {zoom}',t)
  raw=t.encode('cp1251');encoded=encode_ewb(raw);assert b''.join(map(explode,unpack(encoded)))==raw
  p.with_suffix('.txt').write_bytes(raw);p.write_bytes(encoded);p.with_suffix('.topology.json').write_text(json.dumps(dict(components=self.spec,connections=self.connections),indent=2));return p
