from digital_network import *
def register():
 n=DigitalNetwork();sources=[]
 for i,label in enumerate(['D3','D2','D1','D0','CLOCK','SET_n','CLEAR_n']):
  x=700;y=1140-i*100;sw=n.add(38,x,y,0,[49+i],'SW'+str(i),label=label);v=n.add(2,580,y+40,3,[5,0,0],'V'+str(i),unit=2);g=n.ground(530,y-10);lo=n.ground(760,y-55)
  n.connect(v,1,g,0,'0',[(530,y+30)]);n.connect(v,0,sw,2,'VCC'+str(i),[(665,y+30)]);n.connect(sw,1,lo,0,'0',[(760,y+10)]);sources.append((sw,0))
 ff=[];outs=[]
 for i in range(4):
  y=1120-i*170;f=n.addgate('DN',1350,y,'FF'+str(3-i),'BIT '+str(3-i));p=n.addgate('ProbeR',1640,y+20,'Q'+str(3-i),'Q'+str(3-i),orientation=2);ff.append(f);n.connect(f,4,p,0,'Q'+str(3-i));n.connect(*sources[i],f,0,'D'+str(3-i),[(1100-i*25,n.pin(*sources[i])[1]),(1100-i*25,y+10)])
 for net,source,pin,x in [('CLOCK',sources[4],1,1160),('SET_n',sources[5],2,1200),('CLEAR_n',sources[6],3,1240)]:
  start=n.pin(*source);ys=sorted(set([start[1]]+[n.pin(f,pin)[1] for f in ff]),reverse=True);js={y:n.junction(x,y,net+str(j)) for j,y in enumerate(ys)};n.connect(*source,js[start[1]],0,net)
  for a,b in zip(ys,ys[1:]):n.connect(js[a],3,js[b],1,net)
  for f in ff:n.connect(js[n.pin(f,pin)[1]],2,f,pin,net)
 return n.emit('Register.native.ewb',75)
if __name__=='__main__':print(register())
