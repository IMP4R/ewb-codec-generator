#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs32.txt
gdb -batch -x /tmp/gdbs32.txt > /tmp/gdb34.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key ctrl+n; sleep 2.5
xdotool key Right; sleep 0.3; xdotool key Return; sleep 1.2
xdotool key ctrl+o; sleep 2.8
xdotool type --delay 45 "c:\\Program Files\\EWB512\\201.ewb"; sleep 0.6
xdotool key Return; sleep 6
xdotool key Escape; sleep 0.6
# Save As 201a.ewb
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 2.8
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "201a.ewb"; sleep 0.5
xdotool key Return; sleep 110
kill -INT $GDBPID 2>/dev/null; sleep 3; kill -9 $GDBPID 2>/dev/null
grep -c "^P " /tmp/gdb34.log
echo MD22_DONE
