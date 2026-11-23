#!/bin/bash
# usage: run_step.sh <name> <args...>; stdout to <name>.log, stderr to <name>.err, exit code to <name>.rc, wall time to <name>.time
RAW=/home/nathan/Source/negative-mass-raw/I143-rpi5
D=/home/nathan/Source/negative-mass-i143/phase2/dg_proof
name=$1; shift
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
start=$(date +%s)
timeout 3600 /usr/bin/time -v -o $RAW/$name.rss /home/nathan/Source/negative-mass-venv314/bin/python $D/zerilli_derivation.py "$@" > $RAW/$name.log 2> $RAW/$name.err
echo $? > $RAW/$name.rc
echo $(( $(date +%s) - start )) > $RAW/$name.time
