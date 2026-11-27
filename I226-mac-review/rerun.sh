#!/bin/bash
# The review's rerun of I226-rpi5/make_output.sh on the Mac (R1, R3), then R2's two float64 jobs. Run from anywhere.
WT=$HOME/Source/negative-mass-r226/notes/wormhole_evolution
OUT=$HOME/Source/negative-mass-raw/I226-mac-review
PY=$HOME/Source/negative-mass/.venv/bin/python
cd "$WT" || exit 2
sed -e "s#^PY=.*#PY=$PY#" $HOME/Source/negative-mass-raw/I226-rpi5/make_output.sh > "$OUT/make_output_mac.sh"
NUMBA_NUM_THREADS=1 nice -n 10 bash "$OUT/make_output_mac.sh" > "$OUT/rerun_output.txt" 2> "$OUT/rerun_output.err"
echo "make_output rc=$?" > "$OUT/rerun.rc"
mkdir -p "$OUT/jobs"
for j in st_D6_k0 sm_D6_k2; do
  NUMBA_NUM_THREADS=1 nice -n 10 $PY -u constraint_plateau.py run --job=$j --table=$HOME/Source/negative-mass-raw/I226-rpi5/pstar_table.json \
    --out="$OUT/jobs" > "$OUT/jobs/$j.log" 2>&1
  echo "$j rc=$?" >> "$OUT/rerun.rc"
done
