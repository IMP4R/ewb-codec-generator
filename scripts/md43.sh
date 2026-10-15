#!/bin/bash
export DISPLAY=:99
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 45 "c:\\Program Files\\EWB512\\z9.ewb"; sleep 0.6
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.5
import -window root /tmp/inv2_open.png
echo DONE2
