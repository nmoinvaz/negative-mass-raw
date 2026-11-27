#!/bin/sh
# usage: sweep.sh LANE NAME...   one mutation after the other; logs dev_9x_<name>.log in this folder; rc and wall time recorded
cd /Users/nathan/Source/negative-mass-i232
RAW=$HOME/Source/negative-mass-raw/I232-mac
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
for m in "$@"; do
  s=$(date +%s)
  nice -n 10 $PY notes/black_universe/linear.py check --mutate=$m > $RAW/dev/dev_90_mut_$m.log 2>&1
  rc=$?
  echo "rc=$rc wall=$(( $(date +%s) - s )) s" >> $RAW/dev/dev_90_mut_$m.log
done
