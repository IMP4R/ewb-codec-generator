"""Verify generated native EWB bytes, not truth files or topology sidecars."""
from pathlib import Path
from codec import unpack,explode
from schematic import section
from verify_logic import DSU
import re,itertools,json
EXPECTED=(1,0,1,1,0,0,0,1)
def verify(path):
    text=b''.join(map(explode,unpack(path.read_bytes()))).decode('cp1251')
    _,_,elements=section(text,'Elements');_,_,wires=section(text,'Wires')
    blocks=re.split(r'\n\s{6}(?:ExtComp|Comp)\s*\n',elements)[1:]
    cs=[]
    for b in blocks:
        name=re.search(r'Name R "DIGITAL:([^"]+)"',b)
        pn=re.search(r'PartNum i (\d+)',b)
        cs.append(name[1] if name else int(pn[1]))
    ds=DSU()
    for a,pa,b,pb in re.findall(r'pos i:4 (\d+) (\d+) (\d+) (\d+)',wires):ds.union((int(a),int(pa)),(int(b),int(pb)))
    for i,c in enumerate(cs):
        if c==9:
            for p in range(1,4):ds.union((i,0),(i,p))
    switches=[i for i,c in enumerate(cs) if c==38]
    outputs=[i for i,b in enumerate(blocks) if 'RefID A "F"' in b]
    assert len(switches)==3 and len(outputs)==1
    actual=[]
    for bits in itertools.product([0,1],repeat=3):
        net={ds.find((i,0)):v for i,v in zip(switches,bits)}
        for _ in cs:
            for i,c in enumerate(cs):
                if not isinstance(c,str) or c.startswith('Probe'):continue
                pins=[0] if c=='Not' else list(range(int(c[-1])))
                values=[net.get(ds.find((i,p))) for p in pins]
                if None in values:continue
                if c=='Not':v=1-values[0];op=1
                else:
                    op=int(c[-1])
                    if c.startswith('Nand'):v=int(not all(values))
                    elif c.startswith('Nor'):v=int(not any(values))
                    elif c.startswith('And'):v=int(all(values))
                    elif c.startswith('Or'):v=int(any(values))
                    else:raise ValueError(c)
                k=ds.find((i,op))
                assert k not in net or net[k]==v,('multiple drivers',path,k)
                net[k]=v
        actual.append(net.get(ds.find((outputs[0],0))))
    assert tuple(actual)==EXPECTED,(path,actual,EXPECTED)
    return {'file':str(path),'actual':actual,'expected':EXPECTED,'status':'PASS','method':'native EWB byte decode + pin connectivity; not live simulation'}
if __name__=='__main__':
    results=[verify(p) for p in Path(__file__).parent.glob('F1_*_exact.ewb')]
    Path(__file__).with_name('lab3_native_verification.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
