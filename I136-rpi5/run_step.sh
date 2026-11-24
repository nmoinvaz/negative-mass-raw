#!/bin/bash
# usage: run_step.sh STEP [script args...]
# Runs notes/warp/review_he_type3_count.py of the i136 worktree as a systemd user unit nm-i136-STEP (nice 10, one thread,
# 2 h stop). stdout and stderr go to STEP.log, wall seconds and peak rss (KB) to STEP.time, the exit code to done/STEP.rc.
STEP=$1; shift
RAW=$HOME/Source/negative-mass-raw/I136-rpi5
WT=$HOME/Source/negative-mass-i136
PY=$HOME/Source/negative-mass-venv314/bin/python
mkdir -p "$RAW/done"
systemd-run --user --unit="nm-i136-$STEP" --collect -p RuntimeMaxSec=7200 \
  bash -c "cd $WT && export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1; /usr/bin/time -f '%e %M' -o $RAW/$STEP.time nice -n 10 $PY notes/warp/review_he_type3_count.py $* > $RAW/$STEP.log 2>&1; echo \$? > $RAW/done/$STEP.rc"
