#!/bin/sh
# usage: run_mut.sh PREFIX  -- runs every control of conical_closure.py once, one log per control, from the worktree's notes/warp
PY=$HOME/Source/negative-mass/.venv/bin/python
RAW=$HOME/Source/negative-mass-raw/I172-mac
cd $HOME/Source/negative-mass-i172/notes/warp || exit 1
for m in ric-ysign fac-pivot eb-cross bes-sum bes-ode plant-pass plant-fail ser-b8 ser-a2 obs-sign trunc-b zset-sum jets-f3 coord-u mirror-f; do
  case $m in jets-f3|coord-u|mirror-f) extra="" ;; *) extra="--skip-num" ;; esac
  nice -n 10 $PY -u conical_closure.py --mutate=$m $extra > $RAW/$1_$m.log 2> $RAW/$1_$m.err
  echo $? > $RAW/$1_$m.rc
done
echo done > $RAW/$1_done
