#!/bin/bash
# usage: joblane.sh LANE OUTDIR "job args 1" "job args 2" ...
# Runs throat_scaling.py job once per quoted argument string, one after the other, nice 10, one thread, at most 3 h of wall time per job.
# Logs: OUTDIR/logs/LANE_<k>.log (never overwritten; an existing log is skipped). A job stopped by the 3 h limit exits 124 and is reported, not rerun.
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
LANE=$1; OUT=$2; shift 2
cd "$HOME/Source/negative-mass-i230/notes/wormhole_evolution" || exit 2
mkdir -p "$OUT/logs"
k=0
for spec in "$@"; do
  k=$((k+1))
  log="$OUT/logs/${LANE}_${k}.log"
  [ -e "$log" ] && { echo "$log exists, skipped"; continue; }
  echo "$(date '+%F %T') start: $spec" > "$log"
  timeout 10800 nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" throat_scaling.py job $spec --out="$OUT" >> "$log" 2>&1
  echo "$(date '+%F %T') exit $?" >> "$log"
done
