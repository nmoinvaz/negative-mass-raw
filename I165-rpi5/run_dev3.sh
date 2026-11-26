#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I165-rpi5
REPO=/home/nathan/Source/negative-mass-i165
PY=/home/nathan/Source/negative-mass-venv314/bin/python
cd $REPO
for NAME in Phi1-sign Psi-sign sconst-kappa; do
  LOG=$RAW/logs/ctl_dev2_${NAME}.log
  [ -e "$LOG" ] && continue
  /usr/bin/time -v -o $RAW/logs/ctl_dev2_${NAME}.time nice -n 10 $PY notes/warp/one_sign_static.py --mutate=$NAME > $LOG 2>&1
  echo $? > $RAW/logs/ctl_dev2_${NAME}.rc
done
echo done > $RAW/logs/ctl_dev2.done
