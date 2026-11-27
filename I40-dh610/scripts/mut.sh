#!/bin/bash
# usage: mut.sh NAME [flags]   D = 4, family S, at the three declared h under --mutate=NAME, into runs/mut/NAME/D4_S_h<h> (never overwrites; 2 h limit each)
#        mut.sh g6 time_unit   the D = 6 growth control under --mutate=time_unit, into runs/mut/time_unit/g6
RAW=${RAW:-$HOME/Source/negative-mass-raw/I40-dh610}
TH=$HOME/Source/negative-mass-i40/notes/wormhole_evolution/threshold.py
PY=$HOME/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
run() {  # dir, command...
  local dir=$1; shift
  mkdir -p "$dir"
  if [ -e "$dir/job.rc" ]; then echo "$dir already has a result; not overwriting" >&2; return; fi
  echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) host $(hostname)" > "$dir/job.start"
  /usr/bin/time -v -o "$dir/job.time" timeout --signal=TERM --kill-after=60 7200 "$@" > "$dir/job.log" 2> "$dir/job.err"
  echo "rc=$?" > "$dir/job.rc"
}
if [ "$1" = g6 ]; then
  m=$2
  run "$RAW/runs/mut/$m/g6" $PY $TH g6 --out="$RAW/runs/mut/$m/g6" --mutate=$m
  exit
fi
m=$1; shift
for h in 0.02 0.01 0.005; do
  d="$RAW/runs/mut/$m/D4_S_h$h"
  run "$d" $PY $TH job --D=4 --family=S --h=$h --out="$d" --mutate=$m "$@"
done
