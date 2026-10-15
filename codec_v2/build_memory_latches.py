from digital_network import *
def latch(kind):
 n=DigitalNetwork();rs=kind=='RS'
 # NAND latch uses active-low S/R; synchronized versions use input inversion/gating.
 labels=['S_n','R_n'] if rs else ['S','R','C'] if kind=='RS_sync' else ['D','C']
 switches=[];branches=[]
 for i,label in enumerate(labels):
  x=740;y=1080-i*210;sw=n.add(38,x,y,0,[49+i],f'SW{i}',label=label);v=n.add(2,620,y+40,3,[5,0,0],f'V{i}',unit=2);g=n.ground(570,y-10);low=n.ground(800,y-65)
  n.connect(v,1,g,0,'0',[(570,y+30)]);n.connect(v,0,sw,2,f'VCC{i}',[(705,y+30)]);n.connect(sw,1,low,0,'0',[(800,y+10)])
  j=n.junction(900+i*35,y+20,label+'_BUS');n.connect(sw,0,j,0,label);switches.append(sw);branches.append(j)
 q=n.addgate('Nand2',1450,1010,'L1','Q');qn=n.addgate('Nand2',1450,770,'L2','/Q')
 jq=n.junction(1600,1010,'Q_BUS');jqn=n.junction(1660,770,'QN_BUS');pq=n.addgate('ProbeR',1820,1010,'OUTQ','Q',orientation=2);pn=n.addgate('ProbeR',1820,770,'OUTQN','/Q',orientation=2)
 n.connect(q,2,jq,0,'Q');n.connect(qn,2,jqn,0,'QN');n.connect(jq,2,pq,0,'Q');n.connect(jqn,2,pn,0,'QN')
 n.connect(jq,3,qn,1,'Q',[(1600,720),(1370,720),(1370,760)])
 n.connect(jqn,1,q,1,'QN',[(1660,1070),(1390,1070),(1390,1000)])
 if rs:
  n.connect(branches[0],2,q,0,'SN',[(1170,1100),(1170,1020)])
  n.connect(branches[1],2,qn,0,'RN',[(1190,890),(1190,780)])
 elif kind=='RS_sync':
  a=n.addgate('Nand2',1200,1010,'GS','/SC');b=n.addgate('Nand2',1200,770,'GR','/RC')
  n.connect(branches[0],2,a,0,'S',[(1100,1100),(1100,1020)]);n.connect(branches[1],2,b,0,'R',[(1120,890),(1120,780)])
  n.connect(branches[2],2,a,1,'C',[(1010,680),(1010,1000)]);n.connect(branches[2],1,b,1,'C',[(970,760)])
  n.connect(a,2,q,0,'SN',[(1350,1010),(1350,1020)]);n.connect(b,2,qn,0,'RN',[(1350,770),(1350,780)])
 else:
  inv=n.addgate('Not',1100,870,'ND','/D');a=n.addgate('Nand2',1240,1010,'GD','/DC');b=n.addgate('Nand2',1240,770,'GND','/D C')
  n.connect(branches[0],2,a,0,'D',[(1020,1100),(1020,1020)]);n.connect(branches[0],3,inv,0,'D',[(900,870)])
  n.connect(inv,1,b,0,'ND',[(1190,870),(1190,780)])
  n.connect(branches[1],2,a,1,'C',[(970,890),(970,1000)]);n.connect(branches[1],3,b,1,'C',[(935,760)])
  n.connect(a,2,q,0,'SN',[(1380,1010),(1380,1020)]);n.connect(b,2,qn,0,'RN',[(1380,770),(1380,780)])
 return n.emit(kind+'.native.ewb',65)
if __name__=='__main__':
 for kind in ['RS','RS_sync','D_sync']:print(latch(kind))
