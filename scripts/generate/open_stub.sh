#!/bin/bash
export DISPLAY=:99
D="/root/.wine/drive_c/Program Files/EWB512"
W=$(xdotool search --name "Workbench" | head -1)
STUB="inv$RANDOM.ewb"
cp "$D/201.ewb" "$D/$STUB"          # заглушка — реальная схема на 16 КБ текста
echo "$STUB" > /tmp/cur_stub.txt
xdotool windowactivate $W 2>/dev/null; sleep 0.4
xdotool windowfocus $W 2>/dev/null; sleep 0.8
xdotool key ctrl+o; sleep 5
xdotool type --delay 40 "c:\\Program Files\\EWB512\\$STUB"; sleep 1.2
xdotool key Return; sleep 10
xdotool key Escape; sleep 1
import -window root /tmp/stub_open.png
echo "заглушка: $STUB ($(stat -c %s "$D/$STUB") байт)"
echo OPENSTUB_DONE
