#!/bin/bash
# usage: run_step.sh <log-name> [ellis_efold.py args...]   (one process, one thread, nice 10; log, rc and time next to this script)
name=$1; shift
RAW=$(cd "$(dirname "$0")" && pwd)
cd /home/nathan/Source/negative-mass-i163/notes || exit 2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/usr/bin/time -v -o "$RAW/$name.time" nice -n 10 ~/Source/negative-mass-venv314/bin/python ellis_efold.py "$@" > "$RAW/$name.log" 2> "$RAW/$name.err"
echo $? > "$RAW/$name.rc"
