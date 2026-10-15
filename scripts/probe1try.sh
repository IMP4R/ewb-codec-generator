#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Workbench" | head -1)
act(){ xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.5; }
act
xdotool key Escape; sleep 0.4
# Удаляем всё выделением
xdotool mousemove 1100 250; xdotool click 1; sleep 0.4
xdotool keydown ctrl; xdotool key a; xdotool keyup ctrl; sleep 0.8
xdotool key Delete; sleep 1.2
import -window root /tmp/after_del.png
act
# Save As
xdotool key alt+f; sleep 1.2
xdotool key a; sleep 2.8
import -window root /tmp/sas_open.png
# Печатаем имя
xdotool mousemove 350 335; xdotool click 1; sleep 0.3
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 45 "probe1.ewb"; sleep 0.5
import -window root /tmp/typed.png
xdotool key Return; sleep 6
import -window root /tmp/after_ret.png
ls -la "/root/.wine/drive_c/Program Files/EWB512/" | grep probe1 && echo P1_OK || echo P1_FAIL
