#!/bin/bash
# usage: run_step.sh <step> <stdout-file-or-"-"> <args to he_type.py...>; runs in the worktree, writes <step>.log/.err/.time and done/<step>.rc
step=$1; out=$2; shift 2
RAW=$HOME/Source/negative-mass-raw/I103-rpi5
cd $HOME/Source/negative-mass-i103
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
[ "$out" = "-" ] && out=$RAW/$step.log
/usr/bin/time -v -o $RAW/$step.time nice -n 10 $HOME/Source/negative-mass-venv314/bin/python notes/warp/he_type.py "$@" > $out 2> $RAW/$step.err
echo $? > $RAW/done/$step.rc
