#!/bin/bash
cd /home/nathan/Source/negative-mass-i78 || exit 2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
RAW=/home/nathan/Source/negative-mass-raw/I78-rpi5
start=$(date +%s)
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python -u notes/warp/same_sign_scalars.py > notes/warp/same_sign_scalars_output.txt 2> $RAW/final.err
echo $? > $RAW/final.rc
echo "wall $(( $(date +%s) - start )) s" > $RAW/final.time
cp notes/warp/same_sign_scalars_output.txt $RAW/final.log
