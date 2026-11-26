#!/bin/bash
# dev_03: noise amplification on exploration cases
cd "$(dirname "$0")/explore" || exit 1
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I191-rpi5
$PY explore5.py > $RAW/dev_03_noise.log 2>&1; echo $? > $RAW/dev_03_noise.rc
