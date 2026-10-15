#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
OUT="$1"; REM=$(stat -c %s /tmp/inject.bin)
D="/root/.wine/drive_c/Program Files/EWB512"
WID=$(xdotool search --name "Workbench" | head -1)

xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\stub.ewb"; sleep 0.5
xdotool key Return; sleep 8
xdotool key Escape; sleep 0.6
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed "s/PIDHERE/attach $PID/; s/REMHERE/$REM/" /tmp/gdb_count.txt > /tmp/gdb_c.txt
gdb -batch -x /tmp/gdb_c.txt > /tmp/gdbcnt.log 2>&1 &
GDBPID=$!
sleep 12
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 600 400; xdotool click 1; sleep 0.4
xdotool key Escape; sleep 0.4
touch -d "2000-01-01" "$D/stub.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 50
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
cp "$D/stub.ewb" "$D/$OUT"
echo "$OUT: $(stat -c %s "$D/$OUT")"
echo "--- лог подмены:"; grep -E "INJECT|DONE" /tmp/gdbcnt.log | tail -12
echo GEN8_DONE
