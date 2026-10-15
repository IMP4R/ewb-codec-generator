#!/bin/bash
export DISPLAY=:99
WID=16777217
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key alt+f; sleep 1.2; xdotool key a; sleep 3
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "z9b.ewb"; sleep 0.5
xdotool key Return; sleep 8
ls -la "/root/.wine/drive_c/Program Files/EWB512/z9b.ewb" 2>/dev/null | awk '{print $5}'
echo MD35_DONE
