#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
PID=$(pgrep -f "WEWB32.EXE" | head -1)
sed -i "s/attach 2062406/attach $PID/" /tmp/gdbs32.txt
gdb -batch -x /tmp/gdbs32.txt > /tmp/gdb33.log 2>&1 &
GDBPID=$!
sleep 10
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
# добавить землю: Sources flyout @70,67 -> gnd @72,135; drag to canvas
xdotool mousemove 70 67; sleep 0.3; xdotool mousedown 1; sleep 0.3; xdotool mouseup 1; sleep 1.5
xdotool mousemove 72 135; sleep 0.4
xdotool mousedown 1; sleep 0.4
xdotool mousemove 400 400; sleep 0.15
xdotool mousemove 500 400; sleep 0.4
xdotool mouseup 1; sleep 1.5
xdotool mousemove 1100 250; sleep 0.3; xdotool click 1; sleep 0.8
xdotool key Escape; sleep 0.5
# сохранить
touch -d "2000-01-01" "/root/.wine/drive_c/Program Files/EWB512/md3.ewb"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 110
kill -INT $GDBPID 2>/dev/null; sleep 3; kill -9 $GDBPID 2>/dev/null
grep -c "^P " /tmp/gdb33.log
echo MD21_DONE
