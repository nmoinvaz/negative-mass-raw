#!/bin/bash
# usage: run_step.sh <name> [script args...]   runs zerilli_derivation.py with the args; stdout -> RAW/<name>.log, rc -> <name>.rc
RAW=/home/nathan/Source/negative-mass-raw/I147-rpi5
D=/home/nathan/Source/negative-mass-i147/phase2/dg_proof
name=$1; shift
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
start=$(date +%s)
timeout 3600 /usr/bin/time -v -o $RAW/$name.rss /home/nathan/Source/negative-mass-venv314/bin/python -I $D/zerilli_derivation.py "$@" > $RAW/$name.log 2> $RAW/$name.err
echo $? > $RAW/$name.rc
echo $(( $(date +%s) - start )) > $RAW/$name.time
