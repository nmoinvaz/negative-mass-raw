#!/bin/bash
# usage: mutlane.sh TAG OUTDIR m1 m2 ...   one reduced-suite mutation run per name; each log is OUTDIR/TAG_<mutation>.log (never overwritten)
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
TAG=$1; OUT=$2; shift 2
cd "$HOME/Source/negative-mass-i230/notes/wormhole_evolution" || exit 2
mkdir -p "$OUT"
for m in "$@"; do
  log="$OUT/${TAG}_${m}.log"
  [ -e "$log" ] && { echo "$log exists, skipped"; continue; }
  nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" throat_scaling.py mutate --mutate="$m" > "$log" 2>&1
  echo "$m: exit $? $(grep -E '^mutation' "$log" | cut -c1-300)"
done
