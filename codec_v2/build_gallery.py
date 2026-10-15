"""Assemble a single evidence gallery from real screenshots only (no synthetic drawing)."""
from PIL import Image,ImageDraw
from pathlib import Path
R=Path('/Users/user0/ewb_rev/screenshots');OUT=R/'gallery_labs.png'
items=[('Рис.1 Инвертор (измерено 4.995 В)','in0_run.png'),('Рис.2 NAND 00 (4.995 В)','na00_run.png'),('Рис.3 NAND 11 (41.68 мВ)','na11_run.png'),('Рис.4 NOR 00 (4.995 В)','no00_run.png'),('Рис.5 NOR 01 (17.93 мВ)','no01_run.png'),('Полусумматор','ha_clean.png'),('Полный сумматор','fa_native.png'),('Мультиплексор','mux_new.png'),('Регистр (native)','reg_new.png'),('D-триггер (native)','dsync_new.png'),('Память по методичке','teacher_mem.png'),('Инвертор: методичка vs EWB','Inverter_verified_comparison.png')]
thumb=(420,270);cols=3;rows=(len(items)+cols-1)//cols;W=cols*(thumb[0]+16)+16;H=rows*(thumb[1]+34)+16
g=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(g)
for i,(cap,fn) in enumerate(items):
 p=R/fn
 if not p.exists():continue
 im=Image.open(p).convert('RGB');crop=im.crop((0,60,im.width,min(im.height,60+int(im.width*thumb[1]/thumb[0])))) if im.height>im.width else im
 crop.thumbnail(thumb);x=16+(i%cols)*(thumb[0]+16);y=16+(i//cols)*(thumb[1]+34);g.paste(crop,(x,y));d.text((x,y+thumb[1]+6),cap,fill='black')
g.save(OUT);print(OUT,g.size)
