#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
D="/root/.wine/drive_c/Program Files/EWB512"
OUT="$1"
STUB=$(cat /tmp/current_stub.txt)
W=$(xdotool search --name "Workbench" | head -1)

PID=$(pgrep -x "WEWB32.EXE" | head -1)
python3 /tmp/mkgdb.py "$PID"
gdb -batch -x /tmp/gdb_f.txt > /tmp/gdbf.log 2>&1 &
GDBPID=$!
sleep 12
xdotool key Return; sleep 0.8
xdotool key Escape; sleep 0.8
xdotool windowactivate $W 2>/dev/null; sleep 0.4
xdotool windowfocus $W 2>/dev/null; sleep 0.8
xdotool mousemove 600 400; xdotool click 1; sleep 0.6
xdotool key Escape; sleep 0.6
touch -d "2000-01-01" "$D/$STUB"
echo "ДО : $(stat -c '%s %y' "$D/$STUB" | cut -d. -f1)"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 40
echo "ПОСЛЕ: $(stat -c '%s %y' "$D/$STUB" | cut -d. -f1)"
cp "$D/$STUB" "$D/$OUT"
echo "БЛОКОВ ПОДМЕНЫ: $(grep -c INJECT /tmp/gdbf.log)"
grep INJECT /tmp/gdbf.log | tail -3
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2->/dev/null
echo "РЕЗУЛЬТАТ $OUT: $(stat -c %s "$D/$OUT") байт"
echo STEP_SAVE_DONE
