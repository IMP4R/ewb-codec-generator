"""Assemble MASM instruction bodies via lossless operand-syntax translation to NASM;
execute machine code in Unicorn x86-32. Not a claim of native Visual Studio linkage."""
from pathlib import Path
import re,subprocess,struct,json,random
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import *
ROOT=Path('/Users/user0/АВУ/сдача');OUT=Path(__file__).parent
REGS={s.upper() for s in 'eax ebx ecx edx esi edi ebp esp ax bx cx dx si di al ah bl bh cl ch dl dh'.split()}
class Program:
 def __init__(self,path):
  self.path=path;t=path.read_text();self.variables={};offset=0
  for line in t.split('DATA ENDS')[0].splitlines():
   m=re.match(r'\s*(\w+)\s+(DB|DW|DD|DQ)\s+(.+)',line,re.I)
   if not m:continue
   name,typ,val=m.groups();width={'DB':1,'DW':2,'DD':4,'DQ':8}[typ.upper()];count=1
   if ',' in val.split(';')[0]:count=len(val.split(';')[0].split(','))
   dm=re.match(r'(\d+)\s+DUP',val,re.I)
   if dm:count=int(dm.group(1))
   self.variables[name]=(0x200000+offset,width,count);offset+=width*count
  body=t.split(' PROC',1)[1].split(' ENDP',1)[0];body=body.rsplit('\n',1)[0]
  result=[]
  for line in body.splitlines():
   line=line.split(';',1)[0].strip()
   if not line:continue
   line=re.sub(r'\b([0-9][0-9A-F]*)h\b',r'0x\1',line,flags=re.I)
   line=re.sub(r'\b(?:WORD|DWORD|BYTE) PTR\b',lambda m:m.group(0).split()[0].lower(),line,flags=re.I)
   for name,(addr,width,count) in sorted(self.variables.items(),key=lambda x:-len(x[0])):
    line=re.sub(r'\b'+re.escape(name)+r'\[([^\]]+)\]',lambda m:f'[{addr}+{m.group(1)}]',line)
    # Bare symbols are memory, not immediate labels.
    line=re.sub(r'\b'+re.escape(name)+r'(?:\s*\+\s*(\d+))?\b',lambda m:f'[{addr+int(m.group(1) or 0)}]',line)
   # MASM typed-symbol MOVSX/MOVZX needs explicit source width in NASM.
   if re.match(r'(MOVSX|MOVZX)\b',line,re.I):
    line=re.sub(r'(,\s*)(\[\d+\])',lambda m:m.group(1)+('word ' if next(v[1] for v in self.variables.values() if v[0]==int(m.group(2)[1:-1]))==2 else 'dword ')+m.group(2),line)
   # NASM needs destination size for immediate-to-memory operations.
   m=re.match(r'(MOV|CMP|ADD|SUB)\s+(\[\d+\]),\s*([^,]+)$',line,re.I)
   if m and m.group(3).upper() not in REGS and not '[' in m.group(3):
    addr=int(m.group(2)[1:-1]);w=next(v[1] for v in self.variables.values() if v[0]==addr);line=f'{m.group(1)} '+('word' if w==2 else 'dword')+' '+m.group(2)+','+m.group(3)
   result.append(line)
  src='BITS 32\nORG 0x100000\n'+ '\n'.join(result)+'\n';self.asm=OUT/(path.stem+'.nasm');self.asm.write_text(src);self.bin=OUT/(path.stem+'.bin')
  subprocess.run(['nasm','-f','bin',str(self.asm),'-o',str(self.bin)],check=True)
  self.code=self.bin.read_bytes()
 def run(self,inputs,extra_memory=None):
  u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x100000,0x10000);u.mem_map(0x200000,0x10000);u.mem_map(0x300000,0x10000);u.mem_write(0x100000,self.code)
  for k,value in inputs.items():
   addr,width,count=self.variables[k];values=value if isinstance(value,list) else [value]
   u.mem_write(addr,b''.join(int(v&((1<<(width*8))-1)).to_bytes(width,'little') for v in values))
  for addr,data in (extra_memory or {}).items():u.mem_write(addr,data)
  sent=0x10ffff;sp=0x30ff00;u.mem_write(sp,struct.pack('<I',sent));u.reg_write(UC_X86_REG_ESP,sp)
  saved={UC_X86_REG_EBX:0x12345678,UC_X86_REG_ESI:0x24681357,UC_X86_REG_EDI:0x76543210,UC_X86_REG_EBP:0x34567812}
  for r,v in saved.items():u.reg_write(r,v)
  u.emu_start(0x100000,sent,count=100000)
  assert all(u.reg_read(r)==v for r,v in saved.items()),('ABI preservation',self.path)
  result={k:[int.from_bytes(u.mem_read(addr+i*width,width),'little',signed=True) for i in range(count)] for k,(addr,width,count) in self.variables.items()}
  result['_extra']={addr:bytes(u.mem_read(addr,len(data))) for addr,data in (extra_memory or {}).items()}
  return result
def truncdiv(a,b):return abs(a)//abs(b)*(1 if a*b>=0 else -1)
def main():
 reports=[];rng=random.Random(421)
 calc=Program(ROOT/'Лаб_7/lab7_1_calc.asm');branch=Program(ROOT/'Лаб_8/lab8_1_branch.asm')
 for p,kind in [(calc,'calc'),(branch,'branch')]:
  cases=[(a,b) for a in [-32768,-32767,-1,0,1,2,3,16384,32767] for b in [-32768,-1,0,1,2,3,32767]]+[(rng.randint(-32768,32767),rng.randint(-32768,32767)) for _ in range(2000)]
  for a,b in cases:
   if kind=='calc':num=2*a-1;den=b-2;statuskey='calc_status';reskey='res';y=None if den==0 else truncdiv(num,den)
   else:statuskey='branch_status';reskey='y';num=3*a+5 if a>b else a+b;den=b-1 if a>b else a-b;y=10 if a==b else None if den==0 else truncdiv(num,den)
   status=1 if y is None else 2 if not -32768<=y<=32767 else 0;r=p.run({'a':a,'b':b});assert r[statuskey][0]==status,(kind,a,b,r,y)
   if not status:assert r[reskey][0]==y,(kind,a,b,r,y)
  reports.append(dict(source=str(p.path),cases=len(cases),machine_code=True,status='PASS',ABI='PASS'))
 avg=Program(ROOT/'Лаб_8/lab8_2_A1_avg.asm')
 for _ in range(500):
  a=[rng.randint(-32768,32767) for _ in range(10)];positive=[v for v in a if v>0];r=avg.run({'arr':a,'n':10});assert r['avg'][0]==(sum(positive)//len(positive) if positive else 0)
  assert r['positive_sum'][0]==sum(positive) and r['positive_count'][0]==len(positive)
 reports.append(dict(source=str(avg.path),cases=500,machine_code=True,status='PASS',ABI='PASS'))
 static=Program(ROOT/'Лаб_8/lab8_2_B1_sum2d.asm')
 for _ in range(500):
  a=[rng.randint(-32768,32767) for _ in range(9)];b=[rng.randint(-32768,32767) for _ in range(9)];ref=[x+y for x,y in zip(a,b)];ok=all(-32768<=v<=32767 for v in ref);r=static.run({'A2':a,'B2':b});assert r['static_error'][0]==int(not ok)
  if ok:assert r['C2']==ref
 reports.append(dict(source=str(static.path),cases=500,machine_code=True,status='PASS',ABI='PASS'))
 dynamic=Program(ROOT/'Лаб_8/lab8_2_C1_sum2d_dyn.asm')
 for _ in range(500):
  a=[rng.randint(-32768,32767) for _ in range(9)];b=[rng.randint(-32768,32767) for _ in range(9)];ref=[x+y for x,y in zip(a,b)];ok=all(-32768<=v<=32767 for v in ref)
  mem={0x204000:struct.pack('<9h',*a),0x205000:struct.pack('<9h',*b),0x206000:struct.pack('<9h',*([123]*9))}
  r=dynamic.run({'pa':0x204000,'pb':0x205000,'pc':0x206000,'m':9},mem);assert r['dyn_error'][0]==int(not ok)
  actual=struct.unpack('<9h',r['_extra'][0x206000]);assert actual==tuple(ref if ok else [123]*9)
 reports.append(dict(source=str(dynamic.path),cases=500,machine_code=True,status='PASS',ABI='PASS'))
 bits=Program(ROOT/'Лаб_7/lab7_2_bits.asm')
 for x in range(65536):
  r=bits.run({'x':x});assert r['x'][0]&65535==(x|0x124)&(~0x248&65535)
  assert r['m1_set'][0]==x&0x92 and r['m3_set'][0]==x&0x248
 reports.append(dict(source=str(bits.path),cases=65536,machine_code=True,status='PASS',ABI='PASS'))
 (OUT/'machine_execution_report.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
