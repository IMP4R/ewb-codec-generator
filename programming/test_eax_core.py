from execute_asm import *
p=Program(ROOT/'Лаб_6/reverse_eax_core.asm');rng=random.Random(16)
for _ in range(1000):
 v=rng.getrandbits(32);u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x100000,0x10000);u.mem_map(0x300000,0x10000);u.mem_write(0x100000,p.code);u.mem_write(0x30ff00,struct.pack('<I',0x10ffff));u.reg_write(UC_X86_REG_ESP,0x30ff00);u.reg_write(UC_X86_REG_EAX,v);u.reg_write(UC_X86_REG_EBP,0x12345678);u.emu_start(0x100000,0x10ffff,count=10000)
 assert u.reg_read(UC_X86_REG_EAX)==int.from_bytes(v.to_bytes(4,'little')[::-1],'little');assert u.reg_read(UC_X86_REG_EBP)==0x12345678
print('Exact EAX input/output reversal: 1000 machine-code cases PASS')
(OUT/'eax_core_report.json').write_text(json.dumps(dict(cases=1000,status='PASS',actual_x86_instructions=True)))
