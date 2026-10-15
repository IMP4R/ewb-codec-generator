#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
rm -f /tmp/core3*
gdb -batch -x /tmp/gdbs15.txt > /tmp/gdb15.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 1100 500; xdotool click 1; sleep 0.5
# Открываем nodbg.ewb чтобы сохранить существующий документ:
xdotool key ctrl+o; sleep 2.8
xdotool type --delay 45 "c:\\Program Files\\EWB512\\nodbg.ewb"; sleep 0.6
xdotool key Return; sleep 5
xdotool key Escape; sleep 0.5
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/nodbg.ewb"
# Тихое сохранение
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 12
ls -la /tmp/core3* 2>/dev/null
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "BIG WRITE" /tmp/gdb15.log | head -3
echo MD3_DONE
