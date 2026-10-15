"""Lab 3 variant 1: PDF page 9, f vector [1,0,1,1,0,0,0,1].
Page 6 is an EXAMPLE, not the variant. Four canonical terms require
AND3/OR4 for SDNF, OR3/AND4 for SKNF. Reduced gates follow task 5.4.
Current EWB live calibration: multi-input gate output pin N, inputs 0..N-1.
Older example files use different numbering and are not valid contracts here.
"""
from digital_network import DigitalNetwork
from pathlib import Path
import json

TRUTH=[1,0,1,1,0,0,0,1]
GATE_INPUTS={2:[0,1],3:[0,1,2],4:[0,1,2,3]}

class Lab3Network(DigitalNetwork):
    # LIVE EWB calibration calpin2_live.png: inputs 0..N-1, output N.
    def pin(self,i,p):
        c=self.spec[i];kind=c.get('name','')
        if kind in ('And2','Or2','Nand2','Nor2','And3','Or3','And4','Or4'):
            count=int(kind[-1])
            if p==count:return (c['x']+50,c['y'])
            return (c['x']-10,c['y']+10*(count-1)-20*p)
        return super().pin(i,p)

def split_net(n,source,targets,x,y,label):
    if not targets:return
    if len(targets)==1:n.connect(*source,*targets[0],label);return
    j=n.junction(x,y,label+'_BUS');n.connect(*source,j,0,label)
    if len(targets)<=3:
        for pin,t in enumerate(targets,1):n.connect(j,pin,*t,label)
    else:
        for pin,t in enumerate(targets[:2],1):n.connect(j,pin,*t,label)
        split_net(n,(j,3),targets[2:],x+30,y-35,label+'_NEXT')

def build(name, specs, output):
    n=Lab3Network()
    src=n.source(560,900,'VCC',horizontal=True);n.connect(src,1,n.ground(630,840),0,'0')
    # Orientation 1: pin 0 is the positive terminal (native screenshot + left).
    v=n.junction(680,890,'VCC_BUS');n.connect(src,0,v,0,'VCC',[(500,890),(500,850),(675,850)])
    drivers={};loads={k:[] for k in ['x','y','z']}
    for i,(k,y) in enumerate(zip(['x','y','z'],[700,900,1100])):
        sw=n.add(38,760,y,0,[49+i],f'S{i}',label=k)
        n.connect(sw,1,n.ground(900,y+65),0,'0');n.connect(v,i+1,sw,2,'VCC')
        drivers[k]=(sw,0)
        pr=n.addgate('ProbeR',980,y,'P'+k,k,orientation=2);loads[k].append((pr,0))
    coords={k:(940,y) for k,y in zip(['x','y','z'],[700,900,1100])}
    for k,kind,signals,x,y in specs:
        g=n.addgate(kind,x,y,k,k);drivers[k]=(g,1 if kind=='Not' else int(kind[-1]))
        loads.setdefault(k,[]);coords[k]=(x+85,y)
        pins=[0] if kind=='Not' else GATE_INPUTS[int(kind[-1])]
        assert len(pins)==len(signals)
        for signal,pin in zip(signals,pins):loads.setdefault(signal,[]).append((g,pin))
    out=n.addgate('ProbeR',1900,920,'F','f',orientation=2);loads[output].append((out,0))
    for k,ts in loads.items():split_net(n,drivers[k],ts,*coords[k],k)
    p=n.emit(name+'.ewb',zoom=70)
    p.with_suffix('.assignment.json').write_text(json.dumps({'source':'Lab3 PDF page9 variant1','truth':TRUTH,'specs':specs},indent=2))
    return p

def canonical(sknf=False):
    rows=[1,4,5,6] if sknf else [0,2,3,7]
    specs=[('n'+k,'Not',[k],1050,y) for k,y in zip(['x','y','z'],[700,900,1100])]
    names=[]
    for row,y in zip(rows,[620,820,1020,1220]):
        name=('M' if sknf else 'm')+str(row);names.append(name)
        bits=[row>>2&1,row>>1&1,row&1]
        signals=[('n'+k if b==int(sknf) else k) for k,b in zip(['x','y','z'],bits)]
        specs.append((name,'Or3' if sknf else 'And3',signals,1320,y))
    specs.append(('f','And4' if sknf else 'Or4',names,1650,920))
    return build('F1_SKNF_exact' if sknf else 'F1_SDNF_exact',specs,'f')

def main():
    results=[canonical(),canonical(True)]
    # f = ~x~z + yz = (~x+y)(~z+z) is NOT equivalent.
    # Correct POS by grouping zeros: (~x+z)(y+~z).
    for name,specs in [
      ('ANDORNOT',[('nx','Not',['x'],1050,700),('nz','Not',['z'],1050,1100),('a','And2',['nx','nz'],1350,780),('b','And2',['y','z'],1350,1060),('f','Or2',['a','b'],1650,920)]),
      ('NAND',[('nx','Not',['x'],1050,700),('nz','Not',['z'],1050,1100),('a','Nand2',['nx','nz'],1350,780),('b','Nand2',['y','z'],1350,1060),('f','Nand2',['a','b'],1650,920)]),
      ('NOR',[('nx','Not',['x'],1050,700),('nz','Not',['z'],1050,1100),('a','Nor2',['nx','z'],1350,780),('b','Nor2',['y','nz'],1350,1060),('f','Nor2',['a','b'],1650,920)])]:
        results.append(build('F1_min_'+name+'_exact',specs,'f'))
    for p in results:print(p)
if __name__=='__main__':main()
