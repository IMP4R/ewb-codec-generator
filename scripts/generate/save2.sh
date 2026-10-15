#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
D="/root/.wine/drive_c/Program Files/EWB512"
OUT="$1"
STUB=$(cat /tmp/cur_stub.txt)
W=$(xdotool search --name "Workbench" | head -1)
PID=$(pgrep -x "WEWB32.EXE" | head -1)
python3 /tmp/mkgdb.py "$PID"
gdb -batch -x /tmp/gdb_f.txt > /tmp/gdb_s2.log 2>&1 &
GP=$!
sleep 12
# фокус на окно БЕЗ клика по холсту
xdotool windowactivate $W 2>/dev/null; sleep 0.5
xdotool windowfocus $W 2>/dev/null; sleep 1
xdotool key Escape; sleep 0.5
touch -d "2000-01-01" "$D/$STUB"
echo "ДО: $(stat -c '%s %y' "$D/$STUB" | cut -d. -f1)"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 45
echo "ПОСЛЕ: $(stat -c '%s %y' "$D/$STUB" | cut -d. -f1)"
N=$(grep -c INJECT /tmp/gdb_s2.log)
echo "блоков: $N"
grep INJECT /tmp/gdb_s2.log | tail -8
if [ "$N" -gt 0 ]; then cp "$D/$STUB" "$D/$OUT"; echo "$OUT: $(stat -c %s "$D/$OUT") байт"; fi
kill -9 $GP 2>/dev/null
echo SAVE2_DONE
