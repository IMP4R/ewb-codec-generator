#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs37.txt
sed -i "s/set \$rem = 16295/set \$rem = 5488/" /tmp/gdbs37.txt
gdb -batch -x /tmp/gdbs37.txt > /tmp/gdb45.log 2>&1 &
GDBPID=$!
sleep 12
WID=16777217
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
# открыть z9.ewb (валидная заглушка), потом Save As lab3_inv.ewb
xdotool key ctrl+o; sleep 3
xdotool type --delay 45 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.6
xdotool key Return; sleep 6
xdotool key Escape; sleep 0.5
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 3
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "lab3_inv.ewb"; sleep 0.5
xdotool key Return; sleep 50
ls -la "/root/.wine/drive_c/Program Files/EWB512/lab3_inv.ewb" 2>/dev/null | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdb45.log | head -2
echo MD37_DONE
