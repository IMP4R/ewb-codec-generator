# Verified replacement for earlier reverse-engineering hypotheses

## Independently verified
- Transport body consists of independent PKWARE DCL streams separated by `$`; first marker `/`, final `$!` followed by checksum.
- Byte encoding: first character is `(byte>>3)+48`, second is `((byte&7)<<2)+48`.
- Decoder implemented from public zlib contrib/blast semantics; every original block decompressed successfully.
- File checksum is XOR of zlib.crc32(uncompressed_block) for all blocks, not CRC of the concatenation. Verified against all readable Type2 sample files.
- Compression and decoding roundtrip exactly in codec.py. No fixed plaintext length requirement, no padding/digit hacks, no gdb injection required.
- Independent `identity_clean.ewb` opened in EWB, rendered components AND wires without load-error log (screenshots/id_clean.png). Independent arbitrary `symbol_probe.ewb` and `parts_probe.ewb` opened and rendered.
- Legacy edit controls do NOT support Ctrl+A normally. Use Home + Shift+End for filename replacement. Confirm actual dialog and title by screenshots.
- End padding bytes after a compressed block are not accepted reliably by EWB: do not add them.
- Transport newline handling is position-dependent in the legacy reader: first line 66 characters including '/', subsequent 65 characters. Current writer reproduces this.

## Geometry findings
- Component document Y increases UP (confirmed orientation probe).
- Wire `pos i:4 a pa b pb` means component index a, terminal pa, component index b, terminal pb. Not spatial coordinates.
- Wire segments are direction/length pairs. Confirmed 1=right, 2=down, 4=left, 8=up.
- NPN orientation 0: terminal0 base at (x-20,y+20), terminal1 collector at (x+10,y+50), terminal2 emitter at (x+10,y-10). Confirmed terminal1 wire in pinwire.png.
- Voltmeter orientation0: terminal1 top, terminal0 bottom; both x=center+~40 relative to stored Position (verify exact offsets next).
- Native PartNum2 is BATTERY, not circular source. Reference figure uses circular source, rectangle resistor, single-bar ground: further native-style/part investigation needed.
- Current inverter_v2*.ewb are exploratory and not accepted for submission. Incorrect terminal mapping can crash EWB. User task remains incomplete until actual reference-matching screenshot is shown.

## Current next work
1. Recover clean EWB after invalid geometry/source probe and validate terminal maps for all chosen components in isolated probes.
2. Set manual routing and correct relative segment endpoints.
3. Find circular DC source and reference symbol style via native part/service contract or resources.
4. Generate reference geometry, verify screenshot and show it; never substitute raster drawing as EWB evidence.

Primary sources: blast.c/blast.h downloaded from https://github.com/madler/zlib/tree/master/contrib/blast; codec roundtrip experiments and screenshots in permanent archive.
