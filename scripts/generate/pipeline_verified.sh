#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
D="/root/.wine/drive_c/Program Files/EWB512"
OUT="$1"

pkill -f WEWB32; wineserver -k 2>/dev/null; sleep 5
cd "$D"; setsid wine WEWB32.EXE > /tmp/ewb_pipe.log 2>&1 < /dev/null & disown
W=""
for i in $(seq 1 40); do sleep 3; W=$(xdotool search --name "Workbench" | head -1); [ -n "$W" ] && break; done
[ -z "$W" ] && { echo "СТОП: нет окна EWB"; exit 1; }
xdotool windowsize $W 1400 860; xdotool windowmove $W 0 0; sleep 2
echo "1. EWB поднят, окно $W"

STUB="z$RANDOM.ewb"
cp /tmp/probe1_fresh.ewb "$D/$STUB"

OPEN_OK=0
for attempt in 1 2 3 4; do
  xdotool key Return; sleep 0.6
  xdotool key Escape; sleep 0.6
  xdotool windowactivate $W 2>/dev/null; sleep 0.3
  xdotool windowfocus $W 2>/dev/null; sleep 0.6
  xdotool key ctrl+o; sleep 5
  xdotool type --delay 40 "c:\\Program Files\\EWB512\\$STUB"
  sleep 1.2
  xdotool key Return; sleep 8
  xdotool key Escape; sleep 1.5
  import -window root /tmp/p_open.png
  R=$(python3 - << 'PY'
from PIL import Image
im = Image.open('/tmp/p_open.png').convert('L')
px = im.load()
# диалог ошибки: тёмная рамка+иконка в центре
n = sum(1 for y in range(440,500) for x in range(620,800) if px[x,y] < 90)
# заголовок документа: текст слева
t = sum(1 for y in range(100,116) for x in range(4,260) if px[x,y] < 90)
print('BAD' if n > 400 else ('OK' if t > 120 else 'EMPTY'))
PY
)
  echo "   попытка $attempt: $R"
  if [ "$R" = "OK" ]; then OPEN_OK=1; break; fi
done
[ "$OPEN_OK" = "0" ] && { echo "СТОП: не удалось открыть заглушку"; exit 2; }
echo "2. заглушка $STUB открыта"

PID=$(pgrep -x "WEWB32.EXE" | head -1)
python3 /tmp/mkgdb.py "$PID"
gdb -batch -x /tmp/gdb_f.txt > /tmp/gdbpipe.log 2>&1 &
GDBPID=$!
sleep 12
xdotool windowactivate $W 2>/dev/null; sleep 0.3
xdotool windowfocus $W 2>/dev/null; sleep 0.8
xdotool mousemove 600 400; xdotool click 1; sleep 0.6
xdotool key Escape; sleep 0.6
touch -d "2000-01-01" "$D/$STUB"
xdotool keydown ctrl; xdotool key s; xdotool keyup ctrl
sleep 45
N=$(grep -c INJECT /tmp/gdbpipe.log)
echo "3. блоков подмены: $N"
if [ "$N" -gt 0 ]; then
  cp "$D/$STUB" "$D/$OUT"
  echo "4. $OUT: $(stat -c %s "$D/$OUT") байт"
else
  echo "4. подмена не сработала"
fi
kill -INT $GDBPID 2>/dev/null; sleep 2; kill -9 $GDBPID 2>/dev/null
echo PIPE2_DONE
