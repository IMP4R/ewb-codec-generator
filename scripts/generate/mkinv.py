import re, pickle, sys
t, blocks, info = pickle.load(open('/tmp/parsed.pkl','rb'))
NL='\r\n'
def block(k): return t[blocks[k][0]:blocks[k][1]]
B={k:block(k) for k in range(len(blocks))}

def edit(blk, pos=None, ref=None, val=None, partnum=None):
    s=blk
    if pos:
        s=re.sub(r'Position i:3 \d+ \d+ \d+',
                 'Position i:3 %d %d %d'%pos, s, count=1)
    if ref:
        s=re.sub(r'RefID A "[^"]*"', 'RefID A "%s"'%ref, s, count=1)
    if val:
        s=re.sub(r'Value r:\d+ [^\r\n]*', 'Value r:%d %s'%(val[0], val[1]), s, count=1)
    if partnum:
        s=re.sub(r'PartNum i \d+', 'PartNum i %d'%partnum, s, count=1)
    return s

# шаблоны
T_VSRC = B[5]     # PN2 dc source (VIN 0.1V) — используем как источник входа
T_R    = B[6]     # PN1 резистор
T_Q    = B[7]     # PN5 транзистор
T_GND  = B[8]     # PN8 земля
T_RAIL = B[1]     # PN39 линия питания
T_M    = B[0]     # PN13 мультиметр (вольтметр)

els=[]
els.append(edit(T_VSRC, pos=(1, 620, 860), ref='VIN',  val=(3,'0.1 0 0')))
els.append(edit(T_R,     pos=(0, 820, 860), ref='Rb',  val=(5,'10000 0 0 0 0')))
els.append(edit(T_Q,     pos=(2, 1000, 860), ref='Q1'))
els.append(edit(T_R,     pos=(0, 1000, 660), ref='Rc', val=(5,'1000 0 0 0 0')))
els.append(edit(T_RAIL,  pos=(0, 1000, 560), ref='3'))
els.append(edit(T_GND,   pos=(0, 1000, 1010), ref='0'))
els.append(edit(T_M,     pos=(0, 1160, 760), ref='M1', val=(2,'1 0')))

new_elems = '    Elements '+NL+'    { '+NL+''.join(els)+'    }'+NL

i_el=t.find('    Elements '+NL)
i_wr=t.find('    Wires '+NL)
out = t[:i_el] + new_elems + t[i_wr:]
data = out.encode('cp1251')
open('/tmp/inject_inv.bin','wb').write(data)
print('инвертор собран:', len(data), 'байт; компонентов:', len(els))
