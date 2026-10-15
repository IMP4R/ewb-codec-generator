from logic_builder import *

def build_all():
 c=[]
 c.append(halfadder());c.append(fulladder())
 c.append(LogicCircuit('Encoder4to2',['D0','D1','D2','D3'],[('Y0','Or2',['D1','D3']),('Y1','Or2',['D2','D3'])],['Y1','Y0']))
 c.append(LogicCircuit('Decoder2to4',['A1','A0'],[('nA1','Not',['A1']),('nA0','Not',['A0']),('Y0','And2',['nA1','nA0']),('Y1','And2',['nA1','A0']),('Y2','And2',['A1','nA0']),('Y3','And2',['A1','A0'])],['Y0','Y1','Y2','Y3']))
 c.append(LogicCircuit('Mux2to1',['D0','D1','SEL'],[('nSEL','Not',['SEL']),('P0','And2',['D0','nSEL']),('P1','And2',['D1','SEL']),('Y','Or2',['P0','P1'])],['Y']))
 c.append(LogicCircuit('Demux1to2',['D','SEL'],[('nSEL','Not',['SEL']),('Y0','And2',['D','nSEL']),('Y1','And2',['D','SEL'])],['Y0','Y1']))
 # Lab3 variant1: f=minterms0,2,3,7; simplified f=(~x&~z)|(y&z).
 c.append(LogicCircuit('F1_min_ANDORNOT',['x','y','z'],[('nx','Not',['x']),('nz','Not',['z']),('P','And2',['nx','nz']),('Q','And2',['y','z']),('f','Or2',['P','Q'])],['f']))
 c.append(LogicCircuit('F1_min_NAND',['x','y','z'],[('nx','Not',['x']),('nz','Not',['z']),('nP','Nand2',['nx','nz']),('nQ','Nand2',['y','z']),('f','Nand2',['nP','nQ'])],['f']))
 c.append(LogicCircuit('F1_min_NOR',['x','y','z'],[('nx','Not',['x']),('nz','Not',['z']),('nP','Nor2',['nx','z']),('nQ','Nor2',['y','nz']),('f','Nor2',['nP','nQ'])],['f']))
 c.append(LogicCircuit('F1_SDNF',['x','y','z'],[('nx','Not',['x']),('ny','Not',['y']),('nz','Not',['z']),('m0','And3',['nx','ny','nz']),('m2','And3',['nx','y','nz']),('m3','And3',['nx','y','z']),('m7','And3',['x','y','z']),('o0','Or2',['m0','m2']),('o1','Or2',['m3','m7']),('f','Or2',['o0','o1'])],['f']))
 c.append(LogicCircuit('F1_SKNF',['x','y','z'],[('nx','Not',['x']),('ny','Not',['y']),('nz','Not',['z']),('M1','Or3',['x','y','nz']),('M4','Or3',['nx','y','z']),('M5','Or3',['nx','y','nz']),('M6','Or3',['nx','ny','z']),('a0','And2',['M1','M4']),('a1','And2',['M5','M6']),('f','And2',['a0','a1'])],['f']))
 for circuit in c:
  if circuit.name.startswith('F1'):
   expected=[1,0,1,1,0,0,0,1];actual=[circuit.evaluate(bits)[0] for bits in itertools.product([0,1],repeat=3)];assert actual==expected,(circuit.name,actual)
  print(circuit.build())
 return c
if __name__=='__main__':build_all()
