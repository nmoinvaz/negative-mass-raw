#!/bin/bash
# usage: launch_mut.sh RAWDIR OUTDIR NAME...   one mutated analysis per name; the log ends with "mutation NAME: fired [...] declared [...]" and "rc N"
RAW=$1; OUT=$2; shift 2
WD=~/Source/negative-mass-i41/notes/wormhole_evolution
PY=~/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
cd "$WD" || exit 1
mkdir -p "$OUT"
for M in "$@"; do
  nice -n 10 "$PY" settled_mass.py analyze --raw="$RAW" --mutate="$M" > "$OUT/mut_$M.log" 2>&1
  echo "rc $?" >> "$OUT/mut_$M.log"
done
