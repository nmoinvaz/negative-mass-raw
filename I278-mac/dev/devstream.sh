#!/bin/bash
# usage: devstream.sh RUN NAME...   runs derive and check of family_causal.py with --mutate=NAME (none = unmutated), logs in dev/
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
SRC=$HOME/Source/negative-mass-i278/notes/black_universe
OUT=$HOME/Source/negative-mass-raw/I278-mac/dev
RUN=$1; shift
cd "$SRC" || exit 1
for m in "$@"; do
  if [ "$m" = "none" ]; then arg=""; tag=base; else arg="--mutate=$m"; tag=$m; fi
  nice -n 10 $PY family_causal.py derive $arg > "$OUT/devmut_${tag}_derive_run${RUN}.log" 2>&1
  nice -n 10 $PY family_causal.py check $arg > "$OUT/devmut_${tag}_check_run${RUN}.log" 2>&1
  cat "$OUT/devmut_${tag}_derive_run${RUN}.log" "$OUT/devmut_${tag}_check_run${RUN}.log" > "$OUT/m_${tag}_run${RUN}.log"
  echo "$tag done $(date +%T)" >> "$OUT/devstream_run${RUN}.status"
done
echo "stream done" >> "$OUT/devstream_run${RUN}.status"
