"""Capture running EWB at observed 111, traverse Gray code, verify PNG probes.
Run only after inspecting the current running schematic and its probe positions.
"""
import subprocess,json,sys
from pathlib import Path
from PIL import Image
host='root@205.196.80.53';key='/Users/user0/.ssh/winmcp'
name=sys.argv[1];local=Path('/Users/user0/ewb_rev/screenshots')/(name+'_verified')
remote='/root/avu-views/'+name+'_verified'
states=['111','110','100','101','001','000','010','011'];keys=['3','2','3','1','3','2','3']
cmd=['export DISPLAY=:99',f'mkdir -p {remote}',f'import -window root {remote}/111.png']
for k,s in zip(keys,states[1:]):cmd += [f'xdotool key {k}','sleep 0.6',f'import -window root {remote}/{s}.png']
subprocess.run(['ssh','-i',key,host,'; '.join(cmd)],check=True)
subprocess.run(['scp','-r','-i',key,host+':'+remote,str(local.parent)],check=True)
results=[]
for p in sorted(local.glob('*.png')):
 im=Image.open(p).convert('RGB')
 def on(x,y):
  return int(any(r>150 and r>g+45 and r>b+45 for r,g,b in [im.getpixel((xx,yy)) for xx in range(x-4,x+5) for yy in range(y-4,y+5)]))
 inputs=[on(623,y) for y in [557,417,277]];output=on(1267,403);expected=[1,0,1,1,0,0,0,1][int(p.stem,2)]
 assert inputs==list(map(int,p.stem)),(p,inputs)
 assert output==expected,(p,output,expected)
 results.append({'inputs':p.stem,'observed_inputs':inputs,'observed_output':output,'expected':expected,'screenshot':str(p)})
(local/'results.json').write_text(json.dumps(results,indent=2));print(name,'8/8 LIVE PASS')
