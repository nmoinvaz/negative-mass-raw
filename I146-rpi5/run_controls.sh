#!/bin/bash
RAW=/home/nathan/Source/negative-mass-raw/I146-rpi5
D=/home/nathan/Source/negative-mass-i146/phase2/dg_proof
name=${1:-controls}
mkdir -p $RAW/${name}_logs
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 CTRL_LOGDIR=$RAW/${name}_logs
start=$(date +%s)
timeout 3600 nice -n 10 /usr/bin/time -v -o $RAW/$name.rss /home/nathan/Source/negative-mass-venv314/bin/python $D/zerilli_gauge_rs_controls.py > $RAW/$name.log 2> $RAW/$name.err
echo $? > $RAW/$name.rc
echo $(( $(date +%s) - start )) > $RAW/$name.time
