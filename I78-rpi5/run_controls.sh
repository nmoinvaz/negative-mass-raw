#!/bin/bash
# One control at a time, nice 10, one thread. Usage: run_controls.sh NAME... ; logs ctl_<name>.log, exit in ctl_<name>.rc
RAW=/home/nathan/Source/negative-mass-raw/I78-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
SCRIPT=/home/nathan/Source/negative-mass-i78/notes/warp/same_sign_scalars.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
for m in "$@"; do
  n=1; while [ -e "$RAW/ctl_$m.log" ]; do n=$((n+1)); m2="${m}_run$n"; [ -e "$RAW/ctl_$m2.log" ] || break; done
  tag="$m"; [ "$n" -gt 1 ] && tag="${m}_run$n"
  start=$(date +%s)
  nice -n 10 $PY -u $SCRIPT --mutate=$m > $RAW/ctl_$tag.log 2>&1
  echo $? > $RAW/ctl_$tag.rc
  echo "$tag exit $(cat $RAW/ctl_$tag.rc) $(( $(date +%s) - start )) s" >> $RAW/ctl_batch.log
done
echo "batch done" >> $RAW/ctl_batch.log
