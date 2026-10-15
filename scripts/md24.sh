#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs33.txt
gdb -batch -x /tmp/gdbs33.txt > /tmp/gdb36.log 2>&1 &
GDBPID=$!
sleep 12
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.5
xdotool key ctrl+o; sleep 3
xdotool type --delay 45 "c:\\Program Files\\EWB512\\201.ewb"; sleep 0.6
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.5
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 3
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "201b.ewb"; sleep 0.5
xdotool key Return; sleep 25
kill -9 $GDBPID 2>/dev/null
grep -c "^P " /tmp/gdb36.log
echo MD24_DONE
