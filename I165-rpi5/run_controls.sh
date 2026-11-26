#!/bin/bash
# usage: run_controls.sh PREFIX   one run per control, one process at a time; logs ctl_<PREFIX>_<name>.log/.rc (never overwritten)
RAW=/home/nathan/Source/negative-mass-raw/I165-rpi5
REPO=/home/nathan/Source/negative-mass-i165
PY=/home/nathan/Source/negative-mass-venv314/bin/python
PREFIX=$1
cd $REPO
for NAME in Phi1-sign Psi-sign AB-sign denoms-claim Cpoints-s1 plant-s2 toy-flat cert-corrupt cert-satdrop; do
  LOG=$RAW/logs/ctl_${PREFIX}_${NAME}.log
  if [ -e "$LOG" ]; then echo "skip $NAME (log exists)"; continue; fi
  /usr/bin/time -v -o $RAW/logs/ctl_${PREFIX}_${NAME}.time nice -n 10 $PY notes/warp/one_sign_static.py --mutate=$NAME > $LOG 2>&1
  echo $? > $RAW/logs/ctl_${PREFIX}_${NAME}.rc
done
echo done > $RAW/logs/ctl_${PREFIX}.done
