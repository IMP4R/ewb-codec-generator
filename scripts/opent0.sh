#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+n; sleep 2.5
xdotool key Right; sleep 0.3; xdotool key Return; sleep 1.2
xdotool key ctrl+o; sleep 2.8
xdotool type --delay 45 "c:\\Program Files\\EWB512\\t0test.ewb"; sleep 0.6
xdotool key Return; sleep 5
import -window root /tmp/t0open.png
echo OPEN_ATTEMPT_DONE
