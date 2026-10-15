#!/bin/bash
export DISPLAY=:99
WID=20971521
xdotool windowactivate $WID 2>/dev/null; xdotool windowfocus $WID; sleep 0.5
# Zoom Out несколько раз (клавиша 8 в EWB? нет: Zoom out = кнопка тулбара или Ctrl+Down?)
# EWB 5: Zoom In/Out кнопки на панели. Быстрее: view full? Используем горячие Ctrl+F9?
# Простейшее: перемещаем мышь и жмём клавишу ZoomOut (иконка с лупой) — не знаем координаты.
# Используем меню Circuit? Нет такого. ПРОВЕРИМ через скроллинг: скролл вправо-вниз:
xdotool key Right; xdotool key Right; xdotool key Down; sleep 0.5
import -window root /tmp/inv_zoom.png
echo ZOOM_DONE
