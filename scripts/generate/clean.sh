#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
D="/root/.wine/drive_c/Program Files/EWB512"
pkill -f WEWB32; wineserver -k 2>/dev/null; sleep 6
cd "$D"; setsid wine WEWB32.EXE > /tmp/ewb_c.log 2>&1 < /dev/null & disown
W=""
for i in $(seq 1 40); do sleep 3; W=$(xdotool search --name "Workbench" | head -1); [ -n "$W" ] && break; done
[ -z "$W" ] && { echo "нет окна"; exit 1; }
xdotool windowsize $W 1400 860; xdotool windowmove $W 0 0; sleep 2
echo "окно $W"
xdotool windowactivate $W 2>/dev/null; sleep 0.5
xdotool windowfocus $W 2>/dev/null; sleep 0.8
xdotool mousemove 700 450; xdotool click 1; sleep 0.8
xdotool key Escape; sleep 0.8
import -window root /tmp/clean_state.png
echo CLEAN_DONE
