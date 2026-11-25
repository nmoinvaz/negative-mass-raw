#!/bin/bash
# third batch (README section 7): cpath rerun (run3) and the background control's first run
R=/home/nathan/Source/negative-mass-raw/I151-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
SCRIPT=/home/nathan/Source/negative-mass-i151/notes/ellis_efold.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd /home/nathan/Source/negative-mass-i151/notes
for spec in cpath:_run3 background:; do
  m=${spec%%:*}; sfx=${spec##*:}
  if [ -f $R/mut_${m}${sfx}.rc ]; then echo "skip $m"; continue; fi
  echo "$(date +%T) start $m ($sfx)" >> $R/mutations.log
  /usr/bin/time -v -o $R/mut_${m}${sfx}.time $PY -I $SCRIPT --mutate=$m > $R/mut_${m}${sfx}.log 2>&1
  echo $? > $R/mut_${m}${sfx}.rc
  echo "$(date +%T) end $m ($sfx) rc $(cat $R/mut_${m}${sfx}.rc)" >> $R/mutations.log
done
echo "$(date +%T) all done (batch 3)" >> $R/mutations.log
