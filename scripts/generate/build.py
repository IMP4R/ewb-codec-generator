import re
b=open('/tmp/plain201.bin','rb').read()
t=b.decode('cp1251')
NL='\r\n'
PAT='      Comp '+NL+'      { '+NL
CLOSE=NL+'      }'+NL
blocks=[]; idx=0
while True:
    i=t.find(PAT, idx)
    if i<0: break
    j=t.find(CLOSE, i)
    j+=len(CLOSE)
    blocks.append((i,j))
    idx=j
print('блоков:', len(blocks))
info=[]
for k,(a,e) in enumerate(blocks):
    blk=t[a:e]
    pn=re.search(r'PartNum i (\d+)', blk).group(1)
    ref=re.search(r'RefID A "([^"]*)"', blk)
    pos=re.search(r'Position i:3 (\d+) (\d+) (\d+)', blk)
    val=re.search(r'Value r:(\d+) ([^\r\n]*)', blk)
    info.append((k,pn,ref.group(1) if ref else '-',pos.groups() if pos else None,
                 val.group(2).strip() if val else '-',a,e))
    print(k,'PN=',pn,'ref=',info[-1][2],'pos=',info[-1][3],'val=',info[-1][4])
import pickle
pickle.dump((t,blocks,info), open('/tmp/parsed.pkl','wb'))
