#!/bin/sh
# usage: run.sh STEP...   STEP = derive | check | table | c1 | mut:NAME | dmut:NAME   (dmut = linear_derive.py --mutate=NAME)
# logs: runs/<step>.log with the command's output, then rc and wall time. Two lanes at most, nice 10, one thread.
cd /Users/nathan/Source/negative-mass-i232/notes/black_universe
RAW=$HOME/Source/negative-mass-raw/I232-mac
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
for st in "$@"; do
  s=$(date +%s)
  case $st in
    derive) log=derive; cmd="$PY linear_derive.py";;
    check)  log=check;  cmd="$PY linear.py check";;
    table)  log=table;  cmd="$PY linear.py table";;
    c1)     log=c1;     cmd="$PY linear.py c1";;
    mut:*)  n=${st#mut:};  log=mut_$n;  cmd="$PY linear.py check --mutate=$n";;
    dmut:*) n=${st#dmut:}; log=derive_mut_$n; cmd="$PY linear_derive.py --mutate=$n";;
  esac
  nice -n 10 $cmd > $RAW/runs/$log.log 2>&1
  rc=$?
  echo "rc=$rc wall=$(( $(date +%s) - s )) s" >> $RAW/runs/$log.log
done
