import re, pickle
t, blocks, info = pickle.load(open('/tmp/parsed.pkl','rb'))
NL='\r\n'
def block(k): return t[blocks[k][0]:blocks[k][1]]
def edit(blk, pos=None, ref=None, val=None):
    s=blk
    if pos:  s=re.sub(r'Position i:3 \d+ \d+ \d+','Position i:3 %d %d %d'%pos,s,count=1)
    if ref:  s=re.sub(r'RefID A "[^"]*"','RefID A "%s"'%ref,s,count=1)
    if val:  s=re.sub(r'Value r:\d+ [^\r\n]*','Value r:%d %s'%(val[0],val[1]),s,count=1)
    return s

i_el=t.find('    Elements '+NL)
head=t[:i_el]                     # всё до Elements: CircuitHeader + Circuit { Models Preferences

els=[]
els.append(edit(block(5), pos=(1, 560, 820), ref='VIN', val=(3,'0.1 0 0')))   # источник входа
els.append(edit(block(6), pos=(0, 760, 820), ref='Rb',  val=(5,'10000 0 0 0 0')))
els.append(edit(block(7), pos=(2, 980, 860), ref='Q1'))                          # транзистор
els.append(edit(block(6), pos=(0, 980, 640), ref='Rc',  val=(5,'1000 0 0 0 0')))
els.append(edit(block(1), pos=(0, 980, 540), ref='3'))                           # линия VCC
els.append(edit(block(8), pos=(0, 980, 1010), ref='0'))                          # земля
els.append(edit(block(0), pos=(0, 1140, 720), ref='M1', val=(2,'1 0')))          # вольтметр

out = head + '    Elements '+NL+'    { '+NL + ''.join(els) + '    }'+NL + '  }'+NL+'}'+NL
data=out.encode('cp1251')
open('/tmp/inject_inv2.bin','wb').write(data)
print('компактный инвертор:', len(data),'байт; компонентов:', len(els))
