# Handoff — true state (latest)

## Shipped, independently re-verified
23 `.ewb` files under /Users/user0/АВУ/сдача, 18 of them native DIGITAL, all decode and re-encode byte-exactly with our own codec. Inventory: tasks/shipped_ewb_inventory.json.

Removed from submission (kept in /Users/user0/ewb_rev/legacy_superseded):
- lab3_2_nand.ewb / lab3_3_nor.ewb — actually EWB 4.83 format, not EWB5.
- 7 lab4 + 3 lab5 old "generated" files — SPICE imports using resistors as stand-ins, not real logic gates.
- Memory4x3.native.ewb — custom rebuild rendered an empty canvas; experiment only.

Real EWB measurements complete for lab3 (measurements/actual_voltages.json, 10 screenshots): Inverter 0.1V→4.995V and 2V→0.01793V; NAND low only at 11 (0.04168V); NOR low for any high input (0.01793V); other cases 4.995V.

Native LAB4 digital set (encoder, decoder, mux, demux, half adder, full adder, 4-bit add/sub) and five lab3 function variants: all exhaustively checked by an independent pin-connectivity oracle — 641 cases including all 512 add/sub combinations with CF/OF. This is topology verification, explicitly not live EWB simulation. FullAdder, Mux2to1, HalfAdder, Register, D_sync and the teacher Memory were additionally opened in real EWB without errors.

Assembly labs: 71 162 machine-code cases (lab7/8) + 2 600 (lab6) executed in Unicorn x86-32 after MASM→NASM operand translation — all PASS with callee-saved ABI checks; 1 000 more for the exact EAX→EAX byte-reversal core. Not native Visual Studio/MASM link proof, and the reports say so.

Reports regenerated and re-openable: lab3, lab4 (real EWB figures), lab5, lab6, lab7, lab8. Originals in programming/original_reports.

## Still open — do not claim finished
1. Individual EWB load confirmation (screenshot) is missing for several generated native files; batch job was killed after 14/15.
2. Lab5 scenarios not yet executed with logged states: memory 10←010, 00←111, reads, OE off; register 1101 + async Set/Clear.
3. Register.native left-side layout still crowded; overall aesthetics pass pending.
4. Lab6 report lists the earlier verified routine set; reconcile with reverse_eax_core.asm.
5. No native MASM/VS build performed.

## Environment facts
root@205.196.80.53 (key /Users/user0/.ssh/winmcp), DISPLAY=:99, EWB512 with native DIN mode: EWB.INI [Options] Resfile=wewb.res+wewbmsg.res, Din=on, Ansi=off, VectorGraphics=on (only on/off parse as true).
Simulate: Alt+A then click Activate at (140,30) — verify elapsed time/indicator. Open: Ctrl+O, field (570,360), Home+Shift+End replaces the name, Open (850,347) often needs two clicks; error OK and save-confirm No both at (700,483). Use short unique file names. Do not disturb non-wine services.
Format rules: coincident-terminal wire must carry minimal segments [(1,0)] (`segs i:0` crashes legacy EWB); checksum footer `$!xxxxxxxx` must remain contiguous; strip transport newlines before locating the marker.
