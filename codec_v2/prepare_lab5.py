"""Prepare required lab5 assets; preserve teacher circuits byte-for-byte.
Viewer copy changes WindowInfo/grid only, never Elements or Wires.
"""
from pathlib import Path
import shutil, hashlib, json, re
from schematic import section, base
from codec import unpack, explode, encode_ewb
ROOT=Path('/Users/user0/АВУ')
REV=Path('/Users/user0/ewb_rev')
def decoded(p): return b''.join(map(explode,unpack(p.read_bytes()))).decode('cp1251')
def main():
 out=ROOT/'сдача/Лаб_5/ewb'; out.mkdir(parents=True,exist_ok=True)
 archive=REV/'additional_examples/lab5'; archive.mkdir(parents=True,exist_ok=True)
 custom=out/'native/Register.native.ewb'
 if custom.exists(): shutil.move(str(custom),str(archive/custom.name))
 manifest=[]
 for name in ['Register','Memory']:
  src=ROOT/f'лабы/lab05/{name}.ewb';dst=out/(name+'.ewb')
  shutil.copy2(src,dst); assert src.read_bytes()==dst.read_bytes()
  manifest.append(dict(file=str(dst),source=str(src),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),byte_identical=True))
  t=decoded(src);a,b,_=section(t,'WindowInfo');_,_,window=section(base(),'WindowInfo');view=t[:a]+window+t[b:]
  view=view.replace('Info i:10 1 0 100 1','Info i:10 1 0 100 0')
  for sec in ['Elements','Wires']:assert section(t,sec)[2]==section(view,sec)[2]
  (REV/'codec_v2'/f'{name}.teacher_view.ewb').write_bytes(encode_ewb(view.encode('cp1251')))
 for name in ['RS','RS_sync','D_sync']:
  src=REV/'codec_v2'/(name+'.native.ewb');dst=out/'native'/src.name
  shutil.copy2(src,dst)
  t=decoded(dst);assert not re.search(r'Name R "DIGITAL:(?:D|DN|RS)"',t)
  manifest.append(dict(file=str(dst),built_from_basic_gates=True))
 (REV/'tasks/lab5_required_assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
