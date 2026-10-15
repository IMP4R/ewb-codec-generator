# Laboratory completion inventory — variant1

Approved visual reference: user explicitly accepted Inverter_verified comparison (native DIN, PKWARE Python generator). Preserve it.

## Lab3
- Inverter.ewb approved appearance; MUST verify simulation Uin0.1V and2V, record actual measured voltages (not guessed).
- NAND.ewb two stacked NPN, supply5V and1kOhm, inputsU1/U2 100mV, four input combinations; reference page3.
- NOR.ewb two parallel NPN, same supply/load, four input combinations; reference page5.
- Function variant1 f(000..111)=[1,0,1,1,0,0,0,1]. Must provide original SDNF circuit, simplified ANDORNOT, NAND, NOR bases, SKNF circuit and transistor counts/truth tables.

## Lab4
- Encoder, decoder,mux,demux real digital schematics+truth tables.
- Halfadder,fulladder truth tables, power5V/toggle switches/indicators.
- Four-bit add/sub with CF/OF exposed and WordGenerator recommended. Variant1 operations:
(1+4),(2-5),(-3-4),(3+6),(-2-7),(2-3),(-1-4),(-8-(-3)),(7-(-6)),(-7-3). Subtraction CF is borrow/inverted carryout.

## Lab5
- RS latch (NAND active-low input semantics per forbidden00), synchronizedRS (AND gates before latch per assignment), syncD; truth/transition tables.
- 4-bit register: write1101 risingClock, active-low asyncSet/Clear investigate.
- 4x3 memory: addr10<-010; addr00<-111; reads; output-disable+writeenabled mode. Port labels+function.

## Labs6-8
Read full extracted source tasks. Existing source files contain unverified code and unsafe scanf loops, must audit and test. MASM+C++32 Windows is required, can't claim build/debugger success without actually doing it. Lab7.1 expression(2a-1)/(b-2), short input/output with inputsyntax/div0/overflow handling. Lab7.2 exactvariant1 masks from task. Lab8.1 piecewise from PDF (extract rendered formula to disambiguate). Lab8.2 A1 averagepositive1dstatic, B1 sum2dstatic arrays,C1 dynamic2d.

## Current defects discovered
Old Lab4/5 EWB were resistor-divider SPICE import replacements, not actual DIGITAL gates. Rebuild using native ExtComp DIGITAL models. Factory CIRCUITS/gates.ewb decoded to native_examples/gates.decoded.txt; DIGITAL And3/Nand3/Nor3/Or3/Not/Xor3/Xnor3,ProbeR/B/Probe; ExtComp fields Name/Position/ModelUnits/Common{RefID}/Data/ModelNameideal/Status. idealDigital modelPartNum99 Paramsr19 in source. Need build own 2inputgate templates by native library contract, not guessed terminal maps.

Current new Lab3 generators network.py/build_lab3_gates.py produce validated orthogonal spec but NAND v2 opens(no error, topcroppedat100; now85%) NOR90% crashes EWB reproducibly. Never publish NOR until fixed. Investigate parsed component identifiers or unsupported orientation/modelunit fields by component-only/onewire incremental probe. Last editorPID2377971 crashed while opening NORv3. Approved Inverter.ewb untouched. Scripts/source files all permanent.

All subagent delegations failed before doing work; do work directly, don't wait for nonexistent results. Goal active rev3 max40; get_goal before any updates.
