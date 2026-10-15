#!/bin/bash
# $1 = файл для просмотра, $2 = png на сервере
export DISPLAY=:99
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6
xdotool key Escape; sleep 0.4
xdotool key ctrl+o; sleep 3
xdotool type --delay 40 "c:\\Program Files\\EWB512\\$1"; sleep 0.5
xdotool key Return; sleep 7
xdotool key Escape; sleep 0.5
# закрыть Analysis Graphs если мешает: окно графика можно закрыть (правый верхний крестик)
import -window root "$2"
echo VIEW_DONE
