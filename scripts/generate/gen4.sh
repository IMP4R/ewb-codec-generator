#!/bin/bash
# $1 = итоговое имя файла
export DISPLAY=:99
export WINEPREFIX=/root/.wine
OUT="$1"
REM=$(stat -c %s /tmp/inject.bin)
WID=$(xdotool search --name "Workbench" | head -1)
# 1) заглушка: открыть z9.ewb БЕЗ подмены
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.5
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.6
# 2) подключить подмену
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/^attach .*/attach $PID/" /tmp/gdbs40.txt
sed -i "s/^set \$rem = .*/set \$rem = $REM/" /tmp/gdbs40.txt
grep -m1 "^set \$rem" /tmp/gdbs40.txt
gdb -batch -x /tmp/gdbs40.txt > /tmp/gdbgen.log 2>&1 &
GDBPID=$!
sleep 12
# 3) тихое сохранение
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 600 400; xdotool click 1; sleep 0.4
xdotool key Escape; sleep 0.4
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/z9.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 55
cp "/root/.wine/drive_c/Program Files/EWB512/z9.ewb" "/root/.wine/drive_c/Program Files/EWB512/$OUT"
ls -la "/root/.wine/drive_c/Program Files/EWB512/$OUT" | awk '{print $5,$6,$7,$8}'
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdbgen.log | head -2
echo GEN4_DONE
