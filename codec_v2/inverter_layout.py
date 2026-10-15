from schematic import *
import re
# Coordinate convention empirically verified: x increases right, y increases UP.
# Native symbol probe: Q orientation 0 has B=(-20,+20), C=(+10,+50), E=(+10,-10).
# Resistor orientation 1: top=(0,+30), bottom=(0,-30).
# Ground orientation 0: terminal=(0,+20).
def wire(a,pa,b,pb,segments,node):
 vals=[v for d,n in segments for v in (d,n)]
 return f'      wire \r\n      {{ \r\n        pos i:4 {a} {pa} {b} {pb} \r\n        segs i:{len(vals)} '+' '.join(map(str,vals))+f' \r\n        colour i 0 \r\n        wire_id i 0 \r\n        node_p A "{node}" \r\n        x_factor r 1 \r\n        y_factor r 1 \r\n      }}\r\n'
if __name__=='__main__':
 # Goal canvas locations near reference: C=(750,420), E=(750,560), B=(720,465).
 c=[comp(5,1130,840,0,None,'Q1'), #0 transistor C~1140,890 E~1140,830 B~1110,860
    comp(1,1140,980,1,[1000,0,0,0,0],'R1'), #1 resistor top1010 bottom950
    comp(2,1250,1060,3,[5,0,0],'V1'), #2 supply horizontal
    comp(2,1000,790,0,[0.1,0,0],'U1'), #3 input vertical
    comp(8,1000,680,0,[0],''), #4 input ground terminal700
    comp(8,1140,680,0,[0],''), #5 emitter ground terminal700
    comp(8,1340,990,0,[0],''), #6 supply ground terminal1010
    comp(13,1270,840,0,[1,0],'M1')] #7 meter
 w=''
 # Verified: 1=right, 2=up, 4=left, 8=down; Q0 B0 C1 E2; V top1 bottom0.
 # R1 terminal0 bottom / terminal1 top; center is stored x-10.
 w+=wire(1,0,2,1,[(2,50),(1,80)],'3')
 w+=wire(2,0,6,0,[(1,60),(8,50)],'0')
 w+=wire(1,0,0,1,[(8,80),(1,10)],'1')
 w+=wire(3,0,0,0,[(2,20),(1,110)],'2')
 w+=wire(3,1,4,0,[(8,60)],'0')
 w+=wire(0,2,5,0,[(8,110)],'0')
 w+=wire(7,1,0,1,[(2,10),(4,170)],'1')
 w+=wire(7,0,0,2,[(8,10),(4,170)],'0')
 print(emit('inverter_v2.ewb',c,w))
