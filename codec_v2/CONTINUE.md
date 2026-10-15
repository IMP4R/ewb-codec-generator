# Continuation checkpoint — authoritative live progress

The user's task is NOT complete. User explicitly rejects previous horizontal layout and wants matching methodology figure screenshots, shown via show_image. Do not claim current probes are deliverables. Active goal goal-6ff43c86-3f2d-4cae-88a9-21f875f1293d.

## Major breakthrough this turn
Fully independent decoder AND encoder implemented in codec.py. EWB body is independent PKWARE DCL blocks with `$` delimiters, not a state-dependent cipher. Byte transport uses two symbols (high5 and low3-shifted). checksum = XOR crc32 per decoded block. All 26 Type2 sample checksums pass. Roundtrip server201 (16295B plaintext) exact. Compression uses greedy LZ + fixed inverted canonical tables (blast.c reference). EWB loaded identity_clean.ewb with all symbols/wires and arbitrary generated probes without parse errors. Encoder doesn't require EXE, gdb, fixed text size, padding or digit-count hacks.

## Legacy file dialog quirks
Ctrl+A doesn't select filename; Home + Shift+End does. Dialog text field (570,360), Open button (850,347), save/discard question No (700,483), error OK same. Sometimes first click just focuses: inspect screenshot, click again only if dialog still open. Screenshots in /Users/user0/ewb_rev/screenshots/.

## Geometry experimentally verified
Document x right, y UP; native render approximately screen x = stored x-389 and screen y=1287-stored y (symbol-specific offset).
wire pos = component-index, terminal-index, component-index, terminal-index.
Direction 1 RIGHT, 2 UP, 4 LEFT, 8 DOWN. Verified isolated direction_probe.
Q NPN PartNum5 orient0: B pin0 at (x-20,y+20), C pin1 at (x+10,y+50), E pin2 at (x+10,y-10). pinwire probe verified C pin1.
Voltmeter PartNum13 orient0: pin1 top, pin0 bottom, terminal x=stored x+40; top y=stored y+30, bottom y=stored y-30; body size ~110x30px.
Resistor PN1 orient1: pin0 TOP, pin1 BOTTOM; terminal x=stored x-10; top y=stored y+30, bottom y=stored y-30 (respin probe shows pin1 weird routed loop when segment2/down assumption wrong; see screenshots).
Battery PN2 orient3: pin0 RIGHT, pin1 LEFT (inverter_v2d top supply reversed loop); should use pin1 for left resistor feed, pin0 for right ground.
Ground PN8 orient0 terminal=(x,y+20).

## Critical lesson
Don't change component terminal indexes on guesses: incorrect pin mapping caused EWB crash when opening next file. Isolate probes first. Programmatic files regenerate instantly; GUI only used to open/inspect, not author.

## Current generator/probes
schematic.py emits arbitrary components/text + checksum/PKWARE file. inverter_layout.py latest inverter_v2d has a close vertical arrangement but source/resistor/grounds are ANSI symbols, not reference, some wire offsets still wrong (emitter-to-ground missing and upper supply reversed). NOT ACCEPTED.
Reference /tmp/fig_inv.png and /tmp/pdf3/page0_bottom.png; target circular DC sources, rectangular resistor, single-bar grounds, U1 100mV, V1 5V, NPN upright center and two junction dots.
Native PN0 = AC circular source (has sine and composite label); PN2 = battery, no native circular DC yet. Styles may exist in WEWBDIN.RES (downloaded), but configuration experiments Resfile=wewb.res+wewbdin.res+wewbmsg.res didn't change symbols; DIN-only and DIN-first made symbols invisible. Original EWB.INI RESTORED at end. Need investigate resource format / mode switch (VectorGraphics flag alone didn't change).

## Live server
SSH root@205.196.80.53 with /Users/user0/.ssh/winmcp. DISPLAY=:99, wine prefix /root/.wine. EWB512 dir. Last live process 2296706 (check before using). Original ini restored but running process still may have DIN-first cached config, must restart exact WEWB32 process for original rendering. Do not kill production services. Restart exact PID with kill -TERM (avoid pkill -f commands matching own SSH command, prior restarts killed launch shell). Start setsid bash -c 'cd ...; exec wine WEWB32.EXE' redirected /root/log, no EXE arguments (program interprets whole command line as filename and fails).

## Next useful actions
1. Correct topology/geometry in inverter_layout based on verified pin maps and actual screenshot; source pin0/right, pin1/left; ground wire length110 from emitter y830 to ground terminal700. This should render reference-like layout.
2. Find correct DIN symbol overrides via inspecting WEWBDIN.RES binary (maybe loader vector graphics vs bitmap resource mapping). Need circular DC native source/resource and 1kOhm units label.
3. Use real screenshot comparison, preserve unmodified screenshots and crops; do not raster-forge output.
4. Keep task active; no claiming finished while unmatched.

## Latest verified corrections
Native wire directions were corrected again by isolated direction_probe.png: 1 right, 2 UP, 4 left, 8 DOWN. Resistor orient1 pin1 connects from TOP (respin shows wire starting top), pin0 bottom. Q0 collector pin1 (pinwire), emitter pin2; voltmeter pin1 top/pin0 bottom. Current inverter_layout.py top supply recently fixed to R pin0->battery pin1 (left) and battery pin0->ground; not rendered after this last edit. Last live EWB PID2304869 using custom archive. Original ini restored on disk; restart exact PID to restore cached standard resources.
DIN RES isn't PE resource: proprietary archive footer <HIHH>, last 10 bytes: count, index_offset, marker, AAAA. Each directory record 21 bytes: name[13],offset u32,size u32. resource_merge.py parses and merges, but merge still renders shapes INVISIBLE. Need resolve resource names/loading for WMF — extracted DIN has dc.wmf (circle DC), res.wmf(rectangle), gnd.wmf(single bar), so true shapes exist. WEWB.RES downloaded and archived. DIN-first/DIN-only and custom merged tested, all invisible. Standard original configuration restored after experiments. Actual screenshots retained. Do not claim this resource switch worked.
New files generated entirely by codec: symbol_probe, parts probes, pinprobe/pinwire, direction_probe, respin, inverter_v2*. No edits to submission files this turn. Goal remains active for next autonomous round.
