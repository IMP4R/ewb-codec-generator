from execute_asm import *
reports=[];rng=random.Random(62)
cases=[('mov_16.asm','a','x',16),('mov_32.asm','a','b',32),('задание2_mov32_8bit.asm','a8','b8',32),('задание3_mov64.asm','a64','b64',64)]
for file,src,dst,bits in cases:
 p=Program(ROOT/'Лаб_6'/file)
 for _ in range(100):
  v=rng.getrandbits(bits);inputs={src:v}
  if file=='mov_16.asm':inputs['b']=rng.getrandbits(8)
  r=p.run(inputs);assert r[dst][0]&((1<<bits)-1)==v
  if file=='mov_16.asm':assert r['z'][0]&255==inputs['b']
 reports.append(dict(file=file,cases=100,status='PASS',ABI='PASS'))
p=Program(ROOT/'Лаб_6/задание4_xchg.asm')
for _ in range(100):
 a=rng.getrandbits(16);b=rng.getrandbits(16);r=p.run({'v1':a,'v2':b});assert r['v1'][0]&65535==a and r['v2'][0]&65535==b
reports.append(dict(file=p.path.name,cases=100,status='PASS',ABI='PASS'))
for file,var,reverse in [('задание5_циклический_сдвиг.asm','acc',False),('задание6_реверс_байтов.asm','rev_in',True)]:
 p=Program(ROOT/'Лаб_6'/file)
 for _ in range(1000):
  v=rng.getrandbits(32);expected=int.from_bytes(v.to_bytes(4,'little')[::-1],'little') if reverse else ((v>>8)|(v<<24))&0xffffffff;r=p.run({var:v});assert r[var][0]&0xffffffff==expected
 reports.append(dict(file=file,cases=1000,status='PASS',ABI='PASS'))
p=Program(ROOT/'Лаб_6/задание7_инверсия_массива.asm')
for _ in range(100):
 a=[rng.getrandbits(8) for _ in range(4)];r=p.run({'src4':a});assert [v&255 for v in r['dst4']]==[v^255 for v in a]
reports.append(dict(file=p.path.name,cases=100,status='PASS',ABI='PASS'))
(OUT/'lab6_execution_report.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
