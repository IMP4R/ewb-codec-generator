from pathlib import Path
import subprocess,time,json
from PIL import Image
P=Path('/Users/user0/ewb_rev/screenshots/sumsub_verified');P.mkdir(exist_ok=True)
SSH=['ssh','-i','/Users/user0/.ssh/winmcp','root@205.196.80.53']
cases=[(1,4,0),(2,-5,0),(-3,-4,0),(3,6,0),(-2,-7,0),(2,3,1),(-1,4,1),(-8,-3,1),(7,-6,1),(-7,3,1)]
current=[1,0,0,0,0,0,1,0,0];rows=[]
for i,(a,b,sub) in enumerate(cases):
 bits=[((a&15)>>j)&1 for j in range(4)]+[((b&15)>>j)&1 for j in range(4)]+[sub]
 keys=[str(j+1) for j in range(9) if current[j]!=bits[j]]
 command='export DISPLAY=:99; '+('xdotool key '+ ' '.join(keys)+'; ' if keys else '')+f'sleep 1; import -window root /root/avu-views/sumcase{i}.png'
 subprocess.run(SSH+[command],check=True);current=bits
 f=P/f'case{i+1:02}.png';subprocess.run(['scp','-q','-i','/Users/user0/.ssh/winmcp',f'root@205.196.80.53:/root/avu-views/sumcase{i}.png',str(f)],check=True)
 im=Image.open(f).convert('RGB')
 actual=[int(any(r>150 and r>g+45 and r>b+45 for r,g,b in [im.getpixel((x,yy)) for x in range(679,685) for yy in range(y-3,y+4)])) for y in [200,283,367,450,533,617]]
 exact=a-b if sub else a+b;r=exact&15;cf=int((a&15)<(b&15) if sub else (a&15)+(b&15)>15);of=int(not -8<=exact<=7);expected=[(r>>j)&1 for j in [3,2,1,0]]+[cf,of]
 assert actual==expected,(i,a,b,sub,actual,expected)
 rows.append({'A':a,'B':b,'SUB':sub,'exact':exact,'signed4':r if r<8 else r-16,'outputs_S3_S2_S1_S0_CF_OF':actual,'screenshot':str(f)})
(P/'results.json').write_text(json.dumps({'status':'PASS','cases':rows,'input_evidence':'known initial all switches HIGH; keys1..9 tracked; screenshots focus output pane'},indent=2));print('SumSub variant1 live10/10 PASS')
