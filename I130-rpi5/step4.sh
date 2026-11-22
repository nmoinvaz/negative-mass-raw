#!/bin/bash
# Runs every --mutate=NAME of mutations.txt one after the other: log mutate_NAME.log, stderr mutate_NAME.err, and one line per
# mutation in step4.time with the exit code and wall seconds. One process, nice 10, one thread.
RAW=$HOME/Source/negative-mass-raw/I130-rpi5
cd $HOME/Source/negative-mass-i130 || exit 99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "commit $(git rev-parse --short HEAD)" > $RAW/step4.cmd
: > $RAW/step4.time
while read -r m; do
  t0=$(date +%s)
  nice -n 10 $HOME/Source/negative-mass-venv314/bin/python notes/warp/weitzenbock_conf.py --mutate=$m > $RAW/mutate_$m.log 2> $RAW/mutate_$m.err
  rc=$?
  echo "$m exit $rc wall $(( $(date +%s) - t0 )) s" >> $RAW/step4.time
done < $RAW/mutations.txt
echo done > $RAW/done/step4.rc
