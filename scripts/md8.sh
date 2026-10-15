#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
rm -f /tmp/core5*
gdb -batch -x /tmp/gdbs19.txt > /tmp/gdb19.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 1100 500; xdotool click 1; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 25
ls -la /tmp/core5* 2>/dev/null
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -cE "BIG len" /tmp/gdb19.log
echo MD8_DONE
