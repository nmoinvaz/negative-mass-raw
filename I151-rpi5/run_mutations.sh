#!/bin/bash
# one mutated run at a time (README section 5); logs mut_<name>.log, exit codes mut_<name>.rc, /usr/bin/time in mut_<name>.time
R=/home/nathan/Source/negative-mass-raw/I151-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
SCRIPT=/home/nathan/Source/negative-mass-i151/notes/ellis_efold.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd /home/nathan/Source/negative-mass-i151/notes
for m in potential printedW matrix planted xmap units tfactor count domain deltaphi cpath background; do
  if [ -f $R/mut_$m.rc ]; then echo "skip $m"; continue; fi
  echo "$(date +%T) start $m" >> $R/mutations.log
  /usr/bin/time -v -o $R/mut_$m.time $PY -I $SCRIPT --mutate=$m > $R/mut_$m.log 2>&1
  echo $? > $R/mut_$m.rc
  echo "$(date +%T) end $m rc $(cat $R/mut_$m.rc)" >> $R/mutations.log
done
echo "$(date +%T) all done" >> $R/mutations.log
