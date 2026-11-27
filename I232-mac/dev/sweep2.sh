#!/bin/sh
# usage: sweep2.sh NAME...   (NAME = none runs the unmutated check); logs dev_92_mut_<name>.log in this folder, rc and wall time at the end
cd /Users/nathan/Source/negative-mass-i232
RAW=$HOME/Source/negative-mass-raw/I232-mac
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
for m in "$@"; do
  s=$(date +%s)
  if [ "$m" = none ]; then
    nice -n 10 $PY notes/black_universe/linear.py check > $RAW/dev/dev_92_mut_none.log 2>&1
  else
    nice -n 10 $PY notes/black_universe/linear.py check --mutate=$m > $RAW/dev/dev_92_mut_$m.log 2>&1
  fi
  rc=$?
  echo "rc=$rc wall=$(( $(date +%s) - s )) s" >> $RAW/dev/dev_92_mut_$m.log
done
