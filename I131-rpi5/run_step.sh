#!/bin/bash
# usage: run_step.sh <step> <stdout-file-or-"-"> <python script, relative to the worktree or absolute> <args...>
# Runs in the worktree. Writes <step>.log (stdout), <step>.err, <step>.time (/usr/bin/time -v) and done/<step>.rc.
step=$1; out=$2; script=$3; shift 3
RAW=$HOME/Source/negative-mass-raw/I131-rpi5
cd $HOME/Source/negative-mass-i131
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
[ "$out" = "-" ] && out=$RAW/$step.log
/usr/bin/time -v -o $RAW/$step.time nice -n 10 $HOME/Source/negative-mass-venv314/bin/python "$script" "$@" > "$out" 2> $RAW/$step.err
echo $? > $RAW/done/$step.rc
