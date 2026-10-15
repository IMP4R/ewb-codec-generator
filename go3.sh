#!/bin/bash
export DISPLAY=:99
export WINEPREFIX=/root/.wine
export WINEDEBUG=-all
cd "/root/.wine/drive_c/Program Files/EWB512"
wine WEWB32.EXE
