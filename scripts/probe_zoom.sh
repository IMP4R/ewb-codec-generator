#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Electronics Workbench" | head -1)
xdotool windowfocus $WID 2>/dev/null; sleep 0.6
xdotool mousemove 670 482; sleep 0.25
xdotool mousedown 1; sleep 0.25; xdotool mouseup 1; sleep 1.2
xdotool key Escape; sleep 0.4
xdotool mousemove 700 480; sleep 0.2
xdotool keydown ctrl; for i in 1 2 3 4 5 6; do xdotool click 4; sleep 0.2; done; xdotool keyup ctrl
sleep 1.2
import -window root /tmp/pz.png
