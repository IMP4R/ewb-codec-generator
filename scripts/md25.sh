#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs34.txt
gdb -batch -x /tmp/gdbs34.txt > /tmp/gdb37.log 2>&1 &
GDBPID=$!
sleep 12
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 40
ls -la "/root/.wine/drive_c/Program Files/EWB512/md3.ewb" | awk '{print $5}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -c "inj" /tmp/gdb37.log | head -1
echo MD25_DONE
