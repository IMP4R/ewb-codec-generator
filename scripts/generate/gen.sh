#!/bin/bash
# Универсальный генератор: $1 = имя выходного файла
export DISPLAY=:99
export WINEPREFIX=/root/.wine
OUT="$1"
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs37.txt
sed -i "s/set \$rem = 5488/set \$rem = 16295/" /tmp/gdbs37.txt
gdb -batch -x /tmp/gdbs37.txt > /tmp/gdbgen.log 2>&1 &
GDBPID=$!
sleep 12
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
# открыть z9.ewb как заглушку (уже открыт в прошлый раз? переоткроем)
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.5
xdotool key Return; sleep 6
xdotool key Escape; sleep 0.5
# Save As новым именем
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 3
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 40 "$OUT"; sleep 0.5
xdotool key Return; sleep 45
ls -la "/root/.wine/drive_c/Program Files/EWB512/$OUT" 2>/dev/null | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdbgen.log | head -2
echo GEN_DONE
