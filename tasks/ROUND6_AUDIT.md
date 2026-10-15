# Round 6 — current source audit

## Lab 3
Rebuilt active report `/Users/user0/АВУ/сдача/Лаб_3/Отчёт_Лаб_3.docx` using `programming/build_lab3_corrected_report.py`.
Authoritative PDF page9: minterms 0,2,3,7. Correct SDNF/SKNF, minimized SOP/POS, NAND/NOR, transistor estimates 24/11/8/8/24. Embedded five real screenshots and all40 live-case tables.
Backup preserved `programming/original_reports/Отчёт_Лаб_3.before_round6.docx`.
NOT FINAL: transistor output voltages must be measured; former numeric voltage claims excluded. Canonical wiring still needs tidying.

## Labs 4 and 5
Existing real native files discovered in submission. Captures were attempted in remote EWB; lab4 all seven files have opening captures, while lab5 RS/RS_sync/D_sync/Register/Memory opening evidence needs a clean pass because scripted captures sometimes retained the Open dialog. `FullAdder2_loaded.png` also retained the Open dialog and is not acceptance evidence. Lab4 current report explicitly says it is not accepted until individual methodic compliance is verified. Lab5 current report explicitly says live truth/state tables remain unfinished. Teacher Register.ewb and Memory.ewb have not been modified.
Lab4 methodic lines41–42: +1+4, +2−5, −3−4, +3+6, −2−7; +2−(+3), −1−(+4), −8−(−3), +7−(−6), −7−(+3). CF inverted for subtraction (line39). Seven circuit categories required: encoder, decoder, mux, demux, half adder, full adder, 4bit sum/sub.
Lab5 lines84–90: RS, syncRS, syncD truth tables; Register and Memory input/output explanations and live demonstrations. Teacher Register/Memory files must stay unchanged.

## Labs 6–8
Actual current DOCX inspected via python-docx. `tasks/reports/*.txt` are OLD exports and not current source of report truth. Lab8 txt still had obsolete piecewise formula, but actual current DOCX and ASM already correct.
Lab8 part1 PDF page1 visually inspected from references/lab8condition-1.png: (3a+5)/(b−1) if a>b;10 if equal;(a+b)/(a−b) if a<b. Matches current ASM/C++ and DOCX.
Lab7 part1 lines25–26: (2a−1)/(b−2), signedshort. Lab7 part2 lines24–28: bits1,4,7 check; set2,5,8;clear3,6,9; double inversion. Matches actual DOCX.
Lab8 part2 lines17–18 A1 positive mean; line37 B1 matrix addition; lines54–55 C1 same with dynamic2D storage. Matches current code/report.
Lab6 lines303–324 specify seven data transfer/byte tasks; native link remains unfinished.

Re-ran `programming/venv/bin/python execute_asm.py` successfully: calc2063; branch2063; avg500; static500;dynamic500;bits65536. Machine-code emulation, NOT native VisualStudio link/run. System Python lacks Unicorn; use project venv.
Current native build resources: local clang++ and nasm; remote wine; no discovered llvm-ml or i686 mingw. Need obtain a suitable native build path and verify assembled objects + C++ executables, then run under Wine.

Goal remains active. No completion claim.
