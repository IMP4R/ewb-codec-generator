#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
gdb -batch -x /tmp/gdbs17.txt > /tmp/gdb17.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 1100 500; xdotool click 1; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 6
ls -la "/root/.wine/drive_c/Program Files/EWB512/md3.ewb" | awk "{print \$5, \$6, \$7, \$8}"
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "^W " /tmp/gdb17.log | head -20
echo MD6_DONE
