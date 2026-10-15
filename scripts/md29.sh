#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs37.txt
gdb -batch -x /tmp/gdbs37.txt > /tmp/gdb41.log 2>&1 &
GDBPID=$!
sleep 12
WID=16777217
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/201c.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 4
# Save As диалог
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "201c.ewb"; sleep 0.5
xdotool key Return; sleep 60
ls -la "/root/.wine/drive_c/Program Files/EWB512/201c.ewb" 2>/dev/null | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdb41.log | head -2
echo MD29_DONE
