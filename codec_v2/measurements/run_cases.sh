#!/bin/bash
set -eu
export DISPLAY=:99
mkdir -p /root/avu-measurements
for alias in in1 na00 na01 na10 na11 no00 no01 no10 no11; do
 xdotool key ctrl+t
 xdotool key ctrl+o
 sleep 1
 xdotool mousemove 570 360 click 1
 xdotool key Home shift+End
 xdotool type --delay 30 "$alias.ewb"
 xdotool mousemove 850 347 click 1
 sleep 1
 xdotool mousemove 850 347 click 1
 sleep 2
 import -window root "/root/avu-measurements/${alias}_open.png"
 xdotool key alt+a
 sleep 0.5
 xdotool mousemove 140 30 click 1
 sleep 2
 import -window root "/root/avu-measurements/${alias}_run.png"
 echo "CAPTURED $alias"
done
