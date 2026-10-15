#!/bin/bash
# Серия замеров: чистая схема -> +1 резистор -> +1 батарея -> +1 транзистор
export DISPLAY=:99
D='/root/.wine/drive_c/Program Files/EWB512'

pick() { # $1 = корзина, $2 = элемент в палитре, $3 = куда поставить
  xdotool mousemove 700 700; sleep 0.1
  xdotool mousemove $1 67; sleep 0.25
  xdotool mousedown 1; sleep 0.2; xdotool mouseup 1; sleep 1.4
  for pt in "390 105" "420 120" "432 133" "450 140" "405 136" "380 136"; do xdotool mousemove $pt; sleep 0.1; done
  sleep 0.3
  xdotool mousedown 1; sleep 0.3
  xdotool mousemove 600 350; sleep 0.2
  xdotool mousemove $3; sleep 0.35
  xdotool mouseup 1; sleep 1.0
  xdotool mousemove 300 700; sleep 0.15
  xdotool mousedown 1; sleep 0.2; xdotool mouseup 1; sleep 0.4
  xdotool key Escape; sleep 0.4
}
snap() { /tmp/ee_snapshot.sh "$1"; }

# 1) Чистая схема
xdotool key Escape; sleep 0.4
xdotool mousemove 700 700; sleep 0.1
xdotool mousemove 15 10; sleep 0.25
xdotool mousedown 1; sleep 0.2; xdotool mouseup 1; sleep 1.3
xdotool mousemove 450 46; sleep 0.2; xdotool mousemove 40 46; sleep 0.25
xdotool mousedown 1; sleep 0.2; xdotool mouseup 1; sleep 2.5
xdotool type --delay 30 "c:\\Program Files\\EWB512\\201.ewb"; sleep 0.6
xdotool key --clearmodifiers Return; sleep 4
xdotool key --clearmodifiers Return; sleep 0.8
snap "S0_clean.ewb"

# 2) + резистор (корзина Basic = x=100)
pick 100 "res" "500 620"
snap "S1_resistor.ewb"
import -window root /tmp/ser1.png
