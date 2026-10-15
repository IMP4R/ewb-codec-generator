#!/bin/bash
export DISPLAY=:99
MAIN=$(xdotool search --name "Electronics Workbench" | head -1)
xdotool windowactivate $MAIN 2>/dev/null; sleep 0.8
xdotool key Escape; sleep 0.2
xdotool key Escape; sleep 0.5
xdotool mousemove 600 750; sleep 0.1
xdotool mousedown 1; sleep 0.15; xdotool mouseup 1; sleep 0.5
import -window root /tmp/topview.png
