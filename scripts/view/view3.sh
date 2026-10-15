#!/bin/bash
export DISPLAY=:99
WID=16777217
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\$1"; sleep 0.5
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.8
# сдвинуть окно Analysis Graphs вправо, чтобы открыть холст
GW=$(xdotool search --name "Analysis" | head -1)
if [ -n "$GW" ]; then
  xdotool windowsize $GW 300 200; xdotool windowmove $GW 1090 640; sleep 1
fi
import -window root "$2"
echo V3DONE
