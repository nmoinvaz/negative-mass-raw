#!/bin/bash
# usage: run_final.sh N   (run of record number N: stdout to run_final.runN.log, exit code to run_final.runN.rc)
N=$1
RAW=/home/nathan/Source/negative-mass-raw/I161-rpi5
cd /home/nathan/Source/negative-mass-i161 || exit 99
mkdir -p "$RAW/final_mut$N"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /home/nathan/Source/negative-mass-venv314/bin/python -u notes/warp/planar_closure.py --logdir="$RAW/final_mut$N" > "$RAW/run_final.run$N.log" 2>&1
echo $? > "$RAW/run_final.run$N.rc"
