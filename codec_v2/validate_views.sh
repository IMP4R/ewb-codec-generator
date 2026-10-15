#!/bin/bash
set -eu
export DISPLAY=:99
mkdir -p /root/avu-views
for alias in fmin fna fno fsdn fskn enc dec mux dem ha fa ss rs rss ds; do
 xdotool key ctrl+t
 xdotool key ctrl+o
 sleep 1
 xdotool mousemove 570 360 click 1
 xdotool key Home shift+End
 xdotool type --delay 25 "$alias.ewb"
 xdotool mousemove 850 347 click 1
 sleep 1
 xdotool mousemove 850 347 click 1
 sleep 2
 import -window root "/root/avu-views/${alias}.png"
 echo "VIEW $alias"
done
