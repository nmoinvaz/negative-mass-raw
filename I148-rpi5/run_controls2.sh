#!/bin/bash
# usage: run_controls2.sh <name> [controls runner args...]: stdout -> RAW/<name>.log, per-run logs -> RAW/<name>_logs/, rc -> <name>.rc
RAW=/home/nathan/Source/negative-mass-raw/I148-rpi5
D=/home/nathan/Source/negative-mass-i148/phase2/dg_proof
name=$1; shift
mkdir -p $RAW/${name}_logs
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 CTRL_LOGDIR=$RAW/${name}_logs
start=$(date +%s)
timeout 7200 /usr/bin/time -v -o $RAW/$name.rss /home/nathan/Source/negative-mass-venv314/bin/python $D/zerilli_certificate_controls.py "$@" > $RAW/$name.log 2> $RAW/$name.err
echo $? > $RAW/$name.rc
echo $(( $(date +%s) - start )) > $RAW/$name.time
