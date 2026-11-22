#!/bin/bash
# usage: run_any.sh <step> <script in RAW> <args>; stdout to <step>.log, stderr <step>.err, exit code to done/<step>.rc
step=$1; script=$2; shift 2
RAW=$HOME/Source/negative-mass-raw/I103-rpi5
cd $HOME/Source/negative-mass-i103
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
/usr/bin/time -v -o $RAW/$step.time nice -n 10 $HOME/Source/negative-mass-venv314/bin/python $RAW/$script "$@" > $RAW/$step.log 2> $RAW/$step.err
echo $? > $RAW/done/$step.rc
