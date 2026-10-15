#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs32.txt
gdb -batch -x /tmp/gdbs32.txt > /tmp/gdb49.log 2>&1 &
GDBPID=$!
sleep 12
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool mousemove 700 400; xdotool click 1; sleep 0.4
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 3
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "invchk.ewb"; sleep 0.5
xdotool key Return; sleep 40
kill -9 $GDBPID 2>/dev/null
grep -c "^P " /tmp/gdb49.log
echo MD44_DONE
