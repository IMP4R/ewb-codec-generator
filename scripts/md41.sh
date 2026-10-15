#!/bin/bash
export DISPLAY=:99
WID=20971521
# Открыть z9.ewb БЕЗ gdb
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 45 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.6
xdotool key Return; sleep 6
xdotool key Escape; sleep 0.5
echo OPENED
# Теперь активируем gdb-инъекцию
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs37.txt
gdb -batch -x /tmp/gdbs37.txt > /tmp/gdb47.log 2>&1 &
GDBPID=$!
sleep 12
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/lab3_inv.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 45
ls -la "/root/.wine/drive_c/Program Files/EWB512/lab3_inv.ewb" | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdb47.log | head -2
echo MD41_DONE
