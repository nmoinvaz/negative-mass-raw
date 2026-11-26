#!/bin/bash
# run of record NN: checks, then every control; stdout to run_NN.log, exit code to rcNN, /usr/bin/time to run_NN.time
NN=${1:-01}
RAW=$HOME/Source/negative-mass-raw/I168-rpi5
cd "$HOME/Source/negative-mass-i168"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /usr/bin/time -v -o $RAW/run_$NN.time nice -n 10 \
  $HOME/Source/negative-mass-venv314/bin/python notes/warp/conical_attraction.py --logdir=$RAW > $RAW/run_$NN.log 2>&1
echo $? > $RAW/rc$NN
