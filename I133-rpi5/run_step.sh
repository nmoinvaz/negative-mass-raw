#!/bin/bash
# usage: run_step.sh <step> <command...>   (cwd = the worktree). One systemd user unit, nice 10, one thread, 3 h cap.
set -u
RAW=$HOME/Source/negative-mass-raw/I133-rpi5
step=$1; shift
mkdir -p "$RAW/done"
systemd-run --user --unit="nm-i133-$step" --collect --working-directory="$HOME/Source/negative-mass-i133" \
  -p RuntimeMaxSec=10800 -p Nice=10 -E OMP_NUM_THREADS=1 -E OPENBLAS_NUM_THREADS=1 -E PYTHONUNBUFFERED=1 \
  /bin/bash -c "/usr/bin/time -f '%e s wall, %M KB peak rss' -o '$RAW/$step.time' \"\$@\" > '$RAW/$step.log' 2>&1; echo \$? > '$RAW/done/$step.rc'" _ "$@"
