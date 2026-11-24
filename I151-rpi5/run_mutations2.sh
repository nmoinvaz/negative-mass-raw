#!/bin/bash
# reruns of the four mutated runs whose first run crashed or hung (README section 7); logs mut_<name>_run2.*
R=/home/nathan/Source/negative-mass-raw/I151-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
SCRIPT=/home/nathan/Source/negative-mass-i151/notes/ellis_efold.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd /home/nathan/Source/negative-mass-i151/notes
for m in xmap domain cpath background; do
  if [ -f $R/mut_${m}_run2.rc ]; then echo "skip $m"; continue; fi
  echo "$(date +%T) start $m (run2)" >> $R/mutations.log
  /usr/bin/time -v -o $R/mut_${m}_run2.time $PY -I $SCRIPT --mutate=$m > $R/mut_${m}_run2.log 2>&1
  echo $? > $R/mut_${m}_run2.rc
  echo "$(date +%T) end $m (run2) rc $(cat $R/mut_${m}_run2.rc)" >> $R/mutations.log
done
echo "$(date +%T) all done (run2)" >> $R/mutations.log
