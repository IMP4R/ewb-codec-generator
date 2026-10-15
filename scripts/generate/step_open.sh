#!/bin/bash
export DISPLAY=:99
D="/root/.wine/drive_c/Program Files/EWB512"
W=$(xdotool search --name "Workbench" | head -1)
STUB="o$RANDOM.ewb"
cp /tmp/probe1_fresh.ewb "$D/$STUB"
echo "$STUB" > /tmp/current_stub.txt
# гасим диалог, если есть
xdotool key Return; sleep 0.8
xdotool key Return; sleep 0.8
xdotool key Escape; sleep 0.8
xdotool windowactivate $W 2>/dev/null; sleep 0.5
xdotool windowfocus $W 2>/dev/null; sleep 0.6
xdotool key Escape; sleep 0.6
xdotool key ctrl+o; sleep 4
xdotool type --delay 40 "c:\\Program Files\\EWB512\\$STUB"
sleep 1
xdotool key Return; sleep 8
xdotool key Escape; sleep 1
import -window root /tmp/opened.png
echo "заглушка: $STUB"
echo STEPOPEN_DONE
