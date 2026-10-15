"""Independent pin-graph truth evaluator for serialized topology, not generator equations."""
import json,itertools
from pathlib import Path
class DSU:
 def __init__(self):self.p={}
 def find(self,x):
  self.p.setdefault(x,x)
  if self.p[x]!=x:self.p[x]=self.find(self.p[x])
  return self.p[x]
 def union(self,a,b):self.p[self.find(a)]=self.find(b)
def evaluate(top,inputs):
 d=DSU();cs=top['components']
 for e in top['connections']:d.union((e['a'],e['pa']),(e['b'],e['pb']))
 for i,c in enumerate(cs):
  if c['pn']==9:
   for p in range(1,4):d.union((i,0),(i,p))
  if c['pn']==8:d.union((i,0),('GROUND',0))
 net={d.find(('GROUND',0)):0};switches=[i for i,c in enumerate(cs) if c['pn']==38]
 # Inputs assigned at actual switch common terminal0; independent from gate list.
 for i,v in zip(switches,inputs):net[d.find((i,0))]=v
 def get(i,p):return net.get(d.find((i,p)))
 for _ in range(len(cs)+1):
  changed=False
  for i,c in enumerate(cs):
   if c['pn']!=99 or c['name'].startswith('Probe'):continue
   name=c['name'];pins=[0] if name=='Not' else ([0,1] if name.endswith('2') else [0,1,3]);a=[get(i,p) for p in pins]
   if None in a:continue
   if name=='Not':v=1-a[0];out=1
   elif name.startswith('And'):v=int(all(a));out=2
   elif name.startswith('Nand'):v=int(not all(a));out=2
   elif name.startswith('Or'):v=int(any(a));out=2
   elif name.startswith('Nor'):v=int(not any(a));out=2
   elif name.startswith('Xnor'):v=1-(sum(a)%2);out=2
   elif name.startswith('Xor'):v=sum(a)%2;out=2
   else:raise ValueError(name)
   k=d.find((i,out))
   if k not in net:net[k]=v;changed=True
   elif net[k]!=v:raise AssertionError(('conflictingdrivers',k,v,net[k]))
  if not changed:break
 return [get(i,0) for i,c in enumerate(cs) if c['pn']==99 and c['name'].startswith('Probe')]
def verify(root):
 reports=[]
 for p in root.glob('*.logic.json'):
  circuit=json.loads(p.read_text());tp=p.with_name(p.name.replace('.logic.json','.topology.json'))
  if not tp.exists():continue
  top=json.loads(tp.read_text());truth=json.loads(p.with_name(p.name.replace('.logic.json','.truth.json')).read_text());count=0
  for row in truth:
   values=list(row['inputs'].values());actual=evaluate(top,values);expected=list(row['outputs'].values());assert actual==expected,(p.name,values,actual,expected);count+=1
  reports.append(dict(circuit=p.stem,cases=count,status='PASS',method='independent serialized component-pin connectivity evaluator',not_ewb_simulation=True))
 return reports
if __name__=='__main__':
 root=Path(__file__).parent;r=verify(root);(root/'connectivity_verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
