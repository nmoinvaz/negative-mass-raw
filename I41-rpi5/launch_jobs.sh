#!/bin/bash
# usage: launch_jobs.sh RAWDIR DELTA_TAG DELTA   (RAWDIR holds runs/pstar_h*.json; writes runs/h<h>_d<TAG>/ with series.npz, summary.json, job.log)
# the folder name uses Python's {:g} format of the numbers: 1e-06 and 1e-08, 0.02, 0.01, 0.005, 0.0025
RAW=$1; TAG=$2; DELTA=$3
WD=~/Source/negative-mass-i41/notes/wormhole_evolution
PY=~/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
cd "$WD" || exit 1
for H in 0.02 0.01 0.005 0.0025; do
  D="$RAW/runs/h${H}_d${TAG}"
  mkdir -p "$D"
  if [ -f "$D/job.rc" ]; then continue; fi
  date +%FT%T > "$D/job.start"
  nice -n 10 "$PY" settled_mass.py job --h=$H --delta=$DELTA --out="$D" --pstar="$RAW/runs" > "$D/job.log" 2>&1
  echo $? > "$D/job.rc"
  date +%FT%T > "$D/job.end"
done
