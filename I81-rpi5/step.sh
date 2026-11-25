#!/bin/bash
# usage: step.sh <log> <rc> <args to sheared.py...>; runs inside a systemd user unit (see launch.sh)
LOG=$1; RC=$2; shift 2
cd /home/nathan/Source/negative-mass-i81 || exit 99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
START=$(date +%s)
timeout 3600 /home/nathan/Source/negative-mass-venv314/bin/python notes/warp/sheared.py "$@" > "$LOG" 2> "$LOG.err"
RCV=$?
echo "$RCV" > "$RC"
echo "wall $(( $(date +%s) - START )) s, exit $RCV" >> "$LOG.err"
