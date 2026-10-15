from logic_builder import *
def sumsub():
 inputs=[f'A{i}' for i in range(4)]+[f'B{i}' for i in range(4)]+['SUB'];g=[];carry='SUB'
 for i in range(4):
  b=f'Bx{i}';p=f'P{i}';q=f'G{i}';h=f'H{i}';s=f'S{i}';c=f'C{i+1}'
  g.extend([(b,'Xor2',[f'B{i}','SUB']),(p,'Xor2',[f'A{i}',b]),(q,'And2',[f'A{i}',b]),(s,'Xor2',[p,carry]),(h,'And2',[p,carry]),(c,'Or2',[q,h])]);carry=c
 g.extend([('CF','Xor2',['C4','SUB']),('OF','Xor2',['C3','C4'])])
 return LogicCircuit('SumSub4',inputs,g,['S3','S2','S1','S0','CF','OF'])
if __name__=='__main__':
 c=sumsub()
 for a in range(16):
  for b in range(16):
   for sub in [0,1]:
    v=[(a>>i)&1 for i in range(4)]+[(b>>i)&1 for i in range(4)]+[sub];out=c.evaluate(v);r=(a-b if sub else a+b)&15
    assert out[:4]==tuple((r>>i)&1 for i in [3,2,1,0])
    assert out[4]==int(a<b if sub else a+b>15)
    sa=a if a<8 else a-16;sb=b if b<8 else b-16;expected=sa-sb if sub else sa+sb;assert out[5]==int(not -8<=expected<=7)
 print(c.build())
