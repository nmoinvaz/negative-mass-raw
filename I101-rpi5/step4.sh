#!/bin/bash
# Step 4 of I101-rpi5: every --mutate=NAME of the three review scripts, one process at a time, nice 10, one thread.
# Each log is mutate_<script>_<name>.log; step4.summary has "script control exit seconds max_rss_kB".
NR=$HOME/Source/negative-mass-i101
RAW=$HOME/Source/negative-mass-raw/I101-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1
cd $NR
: > $RAW/step4.summary
while IFS=' ' read -r script ctl; do
  log=$RAW/mutate_${script}_${ctl}.log
  /usr/bin/time -f "%e %M" -o $RAW/.t nice -n 10 $PY notes/warp/review_he_surface_${script}.py --mutate=$ctl > $log 2>&1
  rc=$?
  echo "exit $rc" >> $log
  echo "$script $ctl $rc $(cat $RAW/.t)" >> $RAW/step4.summary
done < $RAW/step4.list
echo 0 > $RAW/done/step4.rc
