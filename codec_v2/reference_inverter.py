from inverter_layout import *
import re

def junction(x,y,ref):return comp(9,x,y,0,[0],ref)
if __name__=='__main__':
 # Native DIN source/resistor. Stored positions calibrated by isolated probes.
 # Effective vertical collector line x1140. Q B0=(1120,860), C1=(1140,880), E2=(1140,840).
 c=[comp(5,1130,873,0,None,'Q1'),
 comp(1,1150,985,1,[1000,0,0,0,0],'R1'),
 comp(2,1220,1076,1,[5,0,0],'V1'),
 comp(2,1000,800,0,[0.1,0,0],'U1'),
 comp(8,1000,726,0,[0],''),
 comp(8,1140,726,0,[0],''),
 comp(8,1320,1008,0,[0],''),
 comp(13,1225,850,0,[1,0],'M1'),
 junction(1140,900,'N1'),junction(1140,770,'N0')]
 # Connector center has x-10,y-20; terminal0 = x-18,y-20. Compensate to x1140.
 c[8]=junction(1150,936,'N1');c[9]=junction(1150,798,'N0')
 # Real per-component labels / units, not screenshot editing.
 c[1]=c[1].replace('Value r:5 1000 0 0 0 0','Value r:5 1 0 0 0 0').replace('ModelUnits i:1 0','ModelUnits i:1 1')
 c[3]=c[3].replace('Value r:3 0.1 0 0','Value r:3 100 0 0').replace('ModelUnits i:3 2 0 0','ModelUnits i:3 1 0 0')
 for index in [0,1,2,3,7]:
  label='U1' if index==3 else ''
  opts=f'          Label R "{label}" \r\n          useGlobalSchematicOpts i 0 \r\n          showLabel i 1 \r\n          showValue i {0 if index==0 else 1} \r\n          showRefID i 0 \r\n          showModel i 0 \r\n'
  c[index]=c[index].replace('        Status i 0 \r\n','        Status i 0 \r\n'+opts.replace('          ','        '))
 w=''
 w+=wire(1,1,2,0,[(2,51),(1,70)],'3')
 w+=wire(2,1,6,0,[(1,70),(8,63)],'0')
 w+=wire(1,0,8,1,[(8,39)],'1')
 w+=wire(8,3,0,1,[(8,8)],'1')
 w+=wire(3,0,0,0,[(2,48),(1,110)],'2')
 w+=wire(3,1,4,0,[(8,59)],'0')
 w+=wire(0,2,9,1,[(8,65)],'0')
 w+=wire(9,3,5,0,[(8,37)],'0')
 w+=wire(8,2,7,1,[(1,115),(8,36)],'1')
 w+=wire(9,2,7,0,[(1,115),(2,42)],'0')
 p=emit('reference_inverter.ewb',c,w)
 t=p.with_suffix('.txt').read_bytes().decode('cp1251')
 t=t.replace('Manual i 0','Manual i 1').replace('Auto i 1','Auto i 0').replace('Reroute i 1','Reroute i 0')
 p.with_suffix('.txt').write_bytes(t.encode('cp1251'));p.write_bytes(encode_ewb(t.encode('cp1251')))
 print(p)
