#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
rm -f /tmp/core3*
gdb -batch -x /tmp/gdbs16.txt > /tmp/gdb16.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
# Save As
xdotool key alt+f; sleep 1.2
xdotool key a; sleep 2.8
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "md3.ewb"; sleep 0.5
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb" 2>/dev/null
xdotool key Return; sleep 12
ls -la /tmp/core3* 2>/dev/null
ls -la "/root/.wine/drive_c/Program Files/EWB512/" | grep md3
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "BIGWRITE" /tmp/gdb16.log | head -3
echo MD4_DONE
