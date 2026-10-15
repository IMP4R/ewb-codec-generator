#!/bin/bash
# $1 = итоговое имя
export DISPLAY=:99
export WINEPREFIX=/root/.wine
OUT="$1"
REM=$(stat -c %s /tmp/inject.bin)
WID=16777217
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.5
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.5
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs40.txt
sed -i "s/set \$rem = 1/set \$rem = $REM/" /tmp/gdbs40.txt
gdb -batch -x /tmp/gdbs40.txt > /tmp/gdbgen.log 2>&1 &
GDBPID=$!
sleep 12
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 700 400; xdotool click 1; sleep 0.4
xdotool key Escape; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/z9.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 55
cp "/root/.wine/drive_c/Program Files/EWB512/z9.ewb" "/root/.wine/drive_c/Program Files/EWB512/$OUT"
ls -la "/root/.wine/drive_c/Program Files/EWB512/$OUT" | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdbgen.log | head -2
echo GEN3_DONE
