#!/bin/bash
# final run of record: stdout -> notes/warp/det_classify_output.txt, each control's full stdout -> final_mut/mut_<name>.log, exit code -> final.rc
RAW=/home/nathan/Source/negative-mass-raw/I80-rpi5
cd /home/nathan/Source/negative-mass-i80
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/det_classify.py --logdir=$RAW/final_mut > notes/warp/det_classify_output.txt 2> $RAW/final_stderr.txt
echo $? > $RAW/final.rc
