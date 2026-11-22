#!/bin/bash
# Usage: run_step.sh <step> <weitzenbock_conf.py args...>. One process, nice 10, one thread, from the worktree.
# stdout to <step>.log, stderr to <step>.err, /usr/bin/time -v to <step>.time, the exit code to done/<step>.rc.
step=$1; shift
RAW=$HOME/Source/negative-mass-raw/I130-rpi5
cd $HOME/Source/negative-mass-i130 || exit 99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
echo "commit $(git rev-parse --short HEAD), args: $*" > $RAW/$step.cmd
nice -n 10 /usr/bin/time -v -o $RAW/$step.time $HOME/Source/negative-mass-venv314/bin/python notes/warp/weitzenbock_conf.py "$@" > $RAW/$step.log 2> $RAW/$step.err
echo $? > $RAW/done/$step.rc
