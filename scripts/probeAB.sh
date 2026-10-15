#!/bin/bash
export DISPLAY=:99
WID=$(xdotool search --name "Workbench" | head -1)
act(){ xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.6; }
# Текущая схема = пустой+земля. Сохраняем как probe2.ewb (File>Save As через клаву НЕ выйдет,
# поэтому: Ctrl+S -> он молча сохранит nodbg.ewb. Нам нужен Save As: меню File(8,10)->Save As.
act
xdotool mousemove 8 10; xdotool click 1; sleep 1.2
# меню File открыто: Save As пункт ~ (8+..., y=48)? По прежним скриптам Save As = пункт под Save.
# Пробуем клавишный путь: Alt+F затем A (стандарт Windows):
xdotool key Escape; sleep 0.3
act
xdotool key alt+f; sleep 1
xdotool key a; sleep 2.5
# Диалог Save As: поле имени
xdotool mousemove 350 335; xdotool click 1; xdotool click 1; sleep 0.4
xdotool key ctrl+a; sleep 0.2
xdotool type --delay 40 "probe2.ewb"; sleep 0.5
xdotool key Return; sleep 6
for i in 1 2 3; do
  DID=$(xdotool search --name "Confirm" 2>/dev/null | head -1)
  [ -n "$DID" ] && { xdotool windowfocus $DID; xdotool key --window $DID Left; sleep 0.2; xdotool key --window $DID Return; sleep 1.2; }
  sleep 0.3
done
ls -la "/root/.wine/drive_c/Program Files/EWB512/" | grep probe2 && echo P2_OK
echo STEP_A_DONE
