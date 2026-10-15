# Собирает вариант текста: рабочий plain201 с изменённым набором компонентов.
import re, pickle, sys, os
t, blocks, info = pickle.load(open('/tmp/parsed.pkl','rb'))
NL='\r\n'
def block(k): return t[blocks[k][0]:blocks[k][1]]

def edit(blk, pos=None, ref=None, val=None):
    s=blk
    if pos: s=re.sub(r'Position i:3 \d+ \d+ \d+','Position i:3 %d %d %d'%pos,s,count=1)
    if ref: s=re.sub(r'RefID A "[^"]*"','RefID A "%s"'%ref,s,count=1)
    if val: s=re.sub(r'Value r:\d+ [^\r\n]*','Value r:%d %s '%(val[0],val[1]),s,count=1)
    return s

def build(spec, out_path, keep_wires=3):
    """spec: список (шаблон, pos, ref, val)"""
    i_el=t.find('    Elements '+NL)
    i_wr=t.find('    Wires '+NL)
    head=t[:i_el]
    els=''.join(edit(block(src),pos=p,ref=r,val=v) for src,p,r,v in spec)
    # берём первые keep_wires блоков wire
    i_inst=t.find('    InstSettings '+NL)
    tail_txt=t[i_inst:]
    out = head + '    Elements '+NL+'    { '+NL + els + '    }'+NL + t[i_wr:i_inst] + tail_txt
    data=out.encode('cp1251')
    open(out_path,'wb').write(data)
    return len(data), len(spec)

if __name__=='__main__':
    mode=sys.argv[1]; out=sys.argv[2]
    R={6:(0,967,859,'RC',(5,'1000 0 0 0 0'))}
    if mode=='full':
        spec=[(0,(0,1118,785),'M1',(2,'1 0')),(1,(0,943,856),'3',(1,'0')),
              (2,(0,1168,811),'2',(1,'0')),(3,(0,1141,894),'1',(1,'0')),
              (4,(3,873,829),'VCC',(3,'5 0 0')),(5,(1,1178,749),'VIN',(3,'0.1 0 0')),
              (6,(0,967,859),'RC',(5,'1000 0 0 0 0')),(7,(2,1098,809),'Q1',None),
              (8,(0,1138,869),'0',(1,'0')),(9,(1,1237,749),'0',(1,'0')),
              (10,(3,812,829),'0',(1,'0'))]
    elif mode=='drop_meter':
        spec=[x for x in [ (0,(0,1118,785),'M1',(2,'1 0')),(1,(0,943,856),'3',(1,'0')),
              (2,(0,1168,811),'2',(1,'0')),(3,(0,1141,894),'1',(1,'0')),
              (4,(3,873,829),'VCC',(3,'5 0 0')),(5,(1,1178,749),'VIN',(3,'0.1 0 0')),
              (6,(0,967,859),'RC',(5,'1000 0 0 0 0')),(7,(2,1098,809),'Q1',None),
              (8,(0,1138,869),'0',(1,'0')),(9,(1,1237,749),'0',(1,'0')),
              (10,(3,812,829),'0',(1,'0'))] if x[2]!='M1']
    n,c=build(spec,out)
    print(f'{mode}: {n} байт, {c} компонентов')
