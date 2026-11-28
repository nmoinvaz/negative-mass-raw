#!/bin/sh
# usage: run_dev.sh NAME  -> runs dev/NAME.py at nice 10, one thread, log dev/NAME_run<N>.txt (N = next free number)
cd "$(dirname "$0")" || exit 1
n=1
while [ -e "$1_run$n.txt" ]; do n=$((n+1)); done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/Source/negative-mass/.venv/bin/python "$1.py" > "$1_run$n.txt" 2>&1
echo "rc=$?" >> "$1_run$n.txt"
