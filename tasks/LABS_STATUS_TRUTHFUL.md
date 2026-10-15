# Truthful completion status at this point (highest priority; newer than prior checkpoints)

User asked finish all labs3–8, approved Inverter style. Goal active (rev4, armed, 40). Do not present work as fully finished; several items below remain open. No background jobs pending (bash5 completed/collected, bash11 killed after partial). Subagents repeatedly failed before producing work — do the work directly.

## FULLY verified now
Lab3 analog measurements COMPLETE and from real EWB: measurements/actual_voltages.json, 10 screenshots (in0_run, in1_run, na00..na11_run, no00..no11_run). Inverter 0.1V→4.995V, 2V→0.01793V; NAND low only for 11 (0.04168V); NOR low for any high input (0.01793V); all other outputs 4.995V. Report validated with these, variant1 truth table, SDNF/SKNF, both bases, transistor estimate marked as estimate.
Native digital circuits: 11 combinational + SumSub4, all exhaustively checked by independent DSU pin-connectivity oracle (641 cases incl. 512 add/sub with CF/OF). This is topology/logic verification, explicitly NOT faked live EWB simulation.
Assembly: 71162 Lab7/8 machine-code cases + 2600 Lab6 cases PASS in Unicorn x86-32 after MASM→NASM operand-syntax translation; ABI callee-saved checks PASS. Separate exact EAX→EAX byte-reversal core: 1000 cases PASS. All fronts syntax-checked with clang++11.
Reports regenerated and valid (python-docx reopen verified): Lab3, Lab4 (with real EWB figures attached), Lab5, Lab6, Lab7, Lab8. Originals backed up in programming/original_reports; the earlier Lab4 DOCX was malformed XML and is not silently reused.

## Written but NOT yet live-proven
Lab4/5 EWB files exist and some open cleanly (fa_native.png, mux_new.png, reg_new.png, dsync_new.png, teacher_mem.png). Not all generated files have confirmed error-free load screenshots: the batch job bash-11 was killed mid-run after 14 of 15 aliases. Re-verify each before calling it done; do not assume.
Lab5: teacher-provided Memory.ewb/Register.ewb are the authoritative files; the specified write/read scenarios (10←010, 00←111, reads, OE disable) and register 1101/set/clear are NOT yet executed with logged state.
Custom Memory4x3.native.ewb renders an empty canvas at 35% and 60%; it is NOT a valid deliverable and must not be shipped as the memory lab.
Register.native.ewb has 7 switch sources crowded on the left; layout needs cleanup for the "beautiful cable management" request.
Lab6 MOV/XCHG report states files tested; the report's table maps to procedures actually executed; the new reverse_eax_core.asm is verified but the docx lists the older routines — reconcile names.

## EWB operational facts (keep)
Native DIN mode: EWB.INI [Options] Resfile=wewb.res+wewbmsg.res, Din=on, Ansi=off, VectorGraphics=on (on/off only; 1/0 parse false).
Activate simulation: Alt+A then click the Activate menu item (140,30); verify by elapsed time/indicator change. Ctrl+G and toolbar clicks often only focus.
Open dialog: custom edit box; Ctrl+A does nothing, use Home+Shift+End; field (570,360), Open (850,347) sometimes needs two clicks; check the title bar screenshot. Long filenames can lose a trailing char — use short unique aliases. Error OK and save-question No both at (700,483).
Fixed switch states: Status 0 = high side (measured 4.995V), Status 1 = low. Do not infer logical input bits from filenames; read the displayed source labels and probe colours.
Live editor: root@205.196.80.53, DISPLAY=:99, last PID 2383234 / window 16777217. Do NOT touch non-wine services.
File format rules: coincident-terminal wire needs minimal segments [(1,0)] — `segs i:0` crashes legacy EWB; checksum footer `$!xxxxxxxx` must stay contiguous (never split by newline); unpack must strip newlines before locating the marker.

## Next concrete steps
1. Re-open the remaining generated .ewb files one at a time with screenshot proof; fix or drop each that errors. Improve routing aesthetics (shared power bus, single source per rail, aligned output lanes) for the "beautiful" requirement, then re-capture.
2. Execute the Lab5 Memory/Register scenarios in real EWB with logged probe states and attach those screenshots; update the Lab5 report with the actual results.
3. Fix Register.native layout or rely on the teacher-provided Register.ewb per the assignment wording.
4. Reconcile Lab6 report procedure names with the newly verified reverse_eax_core.asm; consider native MASM/VS build if available, otherwise keep the emulation boundary explicit.
5. Only after all of the above, present the final gallery via show_image (absolute paths) with an honest PASS/PARTIAL list.
