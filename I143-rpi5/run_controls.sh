#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I143-rpi5
D=/home/nathan/Source/negative-mass-i143/phase2/dg_proof
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 CTRL_LOGDIR=$RAW/controls_logs
start=$(date +%s)
timeout 3600 /usr/bin/time -v -o $RAW/controls.rss /home/nathan/Source/negative-mass-venv314/bin/python $D/zerilli_derivation_controls.py > $RAW/controls.log 2> $RAW/controls.err
echo $? > $RAW/controls.rc
echo $(( $(date +%s) - start )) > $RAW/controls.time
