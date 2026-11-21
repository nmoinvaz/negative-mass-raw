#!/bin/bash
# Runs cross_continue_i123.py on one log: ./run_cross.sh LOGNAME OUTNAME [flags]. nice 10, one thread, output in OUTNAME.log
HERE=$(cd "$(dirname "$0")" && pwd)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
log=$1; out=$2; shift 2
nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" -u "$HERE/cross_continue_i123.py" "$HERE/$log.log" "$@" > "$HERE/$out.log" 2>&1
echo "exit $?" >> "$HERE/$out.log"
