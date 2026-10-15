#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs22.txt
gdb -batch -x /tmp/gdbs22.txt > /tmp/gdb22.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 1100 500; xdotool click 1; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 20
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -cE "FILEWRITE" /tmp/gdb22.log
grep -E "STACK" /tmp/gdb22.log | head -24
echo MD11_DONE
