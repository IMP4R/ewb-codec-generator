#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
D="/root/.wine/drive_c/Program Files/EWB512"
OUT="$1"
W=$(xdotool search --name "Workbench" | head -1)
[ -z "$W" ] && { echo "нет окна"; exit 1; }
cp /tmp/probe1_fresh.ewb "$D/stub.ewb"
xdotool windowactivate $W 2>/dev/null; xdotool windowfocus $W 2>/dev/null; sleep 1
xdotool key Escape; sleep 0.5
xdotool key ctrl+o; sleep 4
xdotool type --delay 40 "c:\\Program Files\\EWB512\\stub.ewb"; sleep 1
xdotool key Return; sleep 9
xdotool key Escape; sleep 1
PID=$(pgrep -x "WEWB32.EXE" | head -1)
python3 /tmp/mkgdb.py "$PID"
gdb -batch -x /tmp/gdb_f.txt > /tmp/gdbf.log 2>&1 &
GDBPID=$!
sleep 12
xdotool windowactivate $W 2>/dev/null; xdotool windowfocus $W 2>/dev/null; sleep 1
xdotool mousemove 600 400; xdotool click 1; sleep 0.5
xdotool key Escape; sleep 0.5
touch -d "2000-01-01" "$D/stub.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 45
cp "$D/stub.ewb" "$D/$OUT"
echo "$OUT: $(stat -c %s "$D/$OUT") байт, блоков подмены: $(grep -c INJECT /tmp/gdbf.log)"
grep -E "INJECT" /tmp/gdbf.log | tail -3
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
echo FINAL2_DONE
