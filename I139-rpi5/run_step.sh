#!/bin/bash
# usage: run_step.sh STEP STDOUT_FILE CMD [args...]
# Runs CMD from phase2/dg_proof of the i139 worktree as a systemd user unit nm-i139-STEP (nice 10, one thread, 1 h stop).
# stdout goes to STDOUT_FILE, stderr to STEP.err, wall seconds and peak rss (KB) to STEP.time, the exit code to done/STEP.rc.
STEP=$1; OUT=$2; shift 2
RAW=$HOME/Source/negative-mass-raw/I139-rpi5
WT=$HOME/Source/negative-mass-i139
mkdir -p "$RAW/done"
systemd-run --user --unit="nm-i139-$STEP" --collect -p RuntimeMaxSec=3600 \
  bash -c "cd $WT/phase2/dg_proof && export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1; /usr/bin/time -f '%e %M' -o $RAW/$STEP.time nice -n 10 $* > $OUT 2> $RAW/$STEP.err; echo \$? > $RAW/done/$STEP.rc"
