from digital_network import *
from inverter_layout import wire
if __name__=='__main__':
 n=DigitalNetwork()
 for o in [0,2,6]:
  x=900+o*100;y=900
  i=n.add(38,x,y,o,[49],'SW'+str(o),label='KEY 1')
  n.components[i]=n.components[i].replace('Status i 0','Status i 1')
  for p in range(3):n.ground(x-90+p*90,700)
 w=''
 for k,o in enumerate([0,2,6]):
  base=k*4
  for p in range(3):w+=wire(base,p,base+p+1,0,[(8,100)],'0')
 print(emit_digital('switch_pins.ewb',n.components,w))
