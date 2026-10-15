#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Workbench" | head -1)
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.8
# Save текущего пустого как probe1
xdotool mousemove 1100 500; xdotool click 1; sleep 0.5
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl; sleep 3
xdotool key ctrl+a; sleep 0.3; xdotool type --delay 35 "probe1.ewb"; sleep 0.5
xdotool key Return; sleep 5
for i in 1 2 3; do
  DID=$(xdotool search --name "Confirm" 2>/dev/null | head -1)
  [ -n "$DID" ] && { xdotool windowfocus $DID; xdotool key --window $DID Left; sleep 0.2; xdotool key --window $DID Return; sleep 1.2; }
  sleep 0.3
done
# Тащим землю: Sources flyout
xdotool mousemove 70 67; sleep 0.3; xdotool mousedown 1; sleep 0.3; xdotool mouseup 1; sleep 1.5
xdotool mousemove 72 135; sleep 0.4
xdotool mousedown 1; sleep 0.4
xdotool mousemove 400 400; sleep 0.15
xdotool mousemove 500 400; sleep 0.4
xdotool mouseup 1; sleep 1.2
xdotool mousemove 1100 250; sleep 0.3; xdotool click 1; sleep 0.8
xdotool key Escape; sleep 0.5
# Save как probe2
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl; sleep 3
xdotool key ctrl+a; sleep 0.3; xdotool type --delay 35 "probe2.ewb"; sleep 0.5
xdotool key Return; sleep 5
for i in 1 2 3; do
  DID=$(xdotool search --name "Confirm" 2>/dev/null | head -1)
  [ -n "$DID" ] && { xdotool windowfocus $DID; xdotool key --window $DID Left; sleep 0.2; xdotool key --window $DID Return; sleep 1.2; }
  sleep 0.3
done
ls -la "/root/.wine/drive_c/Program Files/EWB512/" | grep -E "probe[12]"
echo PROBE_DONE
