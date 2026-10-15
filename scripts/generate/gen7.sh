#!/bin/bash
# Генератор с ВОССТАНОВИМОЙ заглушкой и проверкой, что подмена реально сработала.
export DISPLAY=:99
export WINEPREFIX=/root/.wine
OUT="$1"
REM=$(stat -c %s /tmp/inject.bin)
D="/root/.wine/drive_c/Program Files/EWB512"
WID=$(xdotool search --name "Workbench" | head -1)

# свежая заглушка каждый раз
cp "$D/201.ewb" "$D/stub.ewb" 2>/dev/null || cp "/tmp/ewb_save/201.ewb" "$D/stub.ewb"
STUB_BEFORE=$(stat -c %s "$D/stub.ewb")

xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\stub.ewb"; sleep 0.5
xdotool key Return; sleep 8
xdotool key Escape; sleep 0.6

PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed "s/PIDHERE/attach $PID/; s/REMHERE/$REM/" /tmp/gdb_fixed.txt > /tmp/gdb_run.txt
gdb -batch -x /tmp/gdb_run.txt > /tmp/gdbgen.log 2>&1 &
GDBPID=$!
sleep 12

xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool mousemove 600 400; xdotool click 1; sleep 0.4
xdotool key Escape; sleep 0.4
touch -d "2000-01-01" "$D/stub.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 55
STUB_AFTER=$(stat -c %s "$D/stub.ewb")
cp "$D/stub.ewb" "$D/$OUT"
echo "заглушка до=$STUB_BEFORE после=$STUB_AFTER (разница: $((STUB_AFTER-STUB_BEFORE)))"
echo "результат $OUT: $(stat -c %s "$D/$OUT") байт"
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
grep -E "MMAP|SIGSEGV" /tmp/gdbgen.log | head -2
echo GEN7_DONE
