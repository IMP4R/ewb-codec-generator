#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs37.txt
gdb -batch -x /tmp/gdbs37.txt > /tmp/gdb48.log 2>&1 &
GDBPID=$!
sleep 12
WID=20971521
xdotool windowactivate $WID 2>/dev/null; sleep 0.4
xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 700 400; xdotool click 1; sleep 0.5
xdotool key Escape; sleep 0.5
xdotool mousemove 700 400; xdotool click 1; sleep 0.5
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/z9.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 55
ls -la "/root/.wine/drive_c/Program Files/EWB512/z9.ewb" | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdb48.log | head -2
echo MD42_DONE
