#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 45 "c:\\Program Files\\EWB512\\invchk.ewb"; sleep 0.6
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.5
# Zoom Out: в EWB 5 это кнопка тулбара или Ctrl+'-'? Пробуем несколько:
for i in 1 2 3; do xdotool key ctrl+minus; sleep 0.4; done
import -window root /tmp/invchk_open.png
echo OK45
