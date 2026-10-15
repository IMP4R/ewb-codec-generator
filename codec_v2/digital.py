from schematic import *
import re
NATIVE=Path('/Users/user0/ewb_rev/native_examples/gates.decoded.txt')
def digital_model_section():
 t=NATIVE.read_bytes().decode('cp1251');_,_,models=section(t,'Models');return models

def gate(name,x,y,ref='G1',label='',orientation=0):
 return f'      ExtComp \r\n      {{ \r\n        Name R "DIGITAL:{name}" \r\n        Position i:3 {orientation} {x} {y} \r\n        ModelUnits i:1 0 \r\n        Common \r\n        {{ \r\n          RefID A "{ref}" \r\n        }}\r\n        Data R "" \r\n        ModelName R "ideal" \r\n        Status i 0 \r\n        Label R "{label}" \r\n      }}\r\n'
def emit_digital(name,components,wires='',zoom=100):
 t=base();a,b,_=section(t,'Models');t=t[:a]+digital_model_section()+t[b:]
 t=replace_section(t,'Elements',''.join(components));t=replace_section(t,'Wires',wires)
 if '    AnalysisValues \r\n' in t:
  a,b,_=section(t,'AnalysisValues');t=t[:a]+t[b:]
 t=t.replace('Info i:10 1 0 100 1','Info i:10 1 0 100 0').replace('Manual i 0','Manual i 1').replace('Auto i 1','Auto i 0').replace('Reroute i 1','Reroute i 0');t=re.sub(r'ZoomFactor i \d+',f'ZoomFactor i {zoom}',t)
 raw=t.encode('cp1251');p=Path(__file__).with_name(name);p.with_suffix('.txt').write_bytes(raw);p.write_bytes(encode_ewb(raw));assert b''.join(map(explode,unpack(p.read_bytes())))==raw;return p
if __name__=='__main__':
 names=['Not','And','And2','And3','And4','Nand','Nand2','Nand3','Or','Or2','Or3','Or4','Nor','Nor2','Nor3','Xor','Xor2']
 c=[gate(s,800+(i%4)*180,700+(i//4)*150,f'G{i}',s) for i,s in enumerate(names)]
 print(emit_digital('digital_probe.ewb',c))
