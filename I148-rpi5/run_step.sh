#!/bin/bash
# usage: run_step.sh <name> [zerilli_certificate.py args...]; stdout -> RAW/<name>.log, stderr -> .err, rss -> .rss, exit code -> .rc, seconds -> .time
RAW=/home/nathan/Source/negative-mass-raw/I148-rpi5
D=/home/nathan/Source/negative-mass-i148/phase2/dg_proof
name=$1; shift
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
start=$(date +%s)
timeout 3600 /usr/bin/time -v -o $RAW/$name.rss /home/nathan/Source/negative-mass-venv314/bin/python -I $D/zerilli_certificate.py "$@" > $RAW/$name.log 2> $RAW/$name.err
echo $? > $RAW/$name.rc
echo $(( $(date +%s) - start )) > $RAW/$name.time
