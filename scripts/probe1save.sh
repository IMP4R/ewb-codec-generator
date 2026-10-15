#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Workbench" | head -1)
act(){ xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6; }
act
xdotool mousemove 1100 250; xdotool click 1; sleep 0.5
xdotool keydown ctrl; xdotool key a; xdotool keyup ctrl; sleep 1
xdotool key Delete; sleep 1.5
xdotool mousemove 1100 600; xdotool click 1; sleep 0.5
act
xdotool key alt+f; sleep 1
xdotool key a; sleep 2.5
xdotool mousemove 350 335; xdotool click 1; xdotool click 1; sleep 0.4
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 40 "probe1.ewb"; sleep 0.5
xdotool key Return; sleep 6
for i in 1 2 3; do
  DID=$(xdotool search --name "Confirm" 2>/dev/null | head -1)
  [ -n "$DID" ] && { xdotool windowfocus $DID; xdotool key --window $DID Left; sleep 0.2; xdotool key --window $DID Return; sleep 1.2; }
  sleep 0.3
done
ls -la "/root/.wine/drive_c/Program Files/EWB512/" | grep probe1 && echo P1_OK
echo STEP_B_DONE
