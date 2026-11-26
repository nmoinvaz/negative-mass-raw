#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I183-rpi5
cd /home/nathan/Source/negative-mass-i183
export RAYON_NUM_THREADS=2
nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python $RAW/sys/perturb_indep.py > $RAW/dev_09_perturb.log 2>&1
echo $? > $RAW/dev_09_perturb.rc
