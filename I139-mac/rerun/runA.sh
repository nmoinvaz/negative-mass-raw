#!/bin/bash
# Mac rerun of #139: threshold_isolation.py --csv, then compare_brackets.py on the Mac's csv, its 3 controls and the planted cases.
S=/private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad
WT=$S/wt139/phase2/dg_proof; OUT=$S/r139; PY=$HOME/Source/negative-mass/.venv/bin/python
RAW=$HOME/Source/negative-mass-raw
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
run() { local name=$1; shift; local t0=$(date +%s); nice -n 10 "$PY" "$@" > "$OUT/$name.log" 2>&1; local rc=$?; echo "$name rc=$rc s=$(( $(date +%s) - t0 ))" >> "$OUT/runA.log"; }
run threshold_isolation_csv threshold_isolation.py --csv="$OUT/brackets_i2_mac.csv"
run compare compare_brackets.py --ours="$OUT/brackets_i2_mac.csv" --theirs="$RAW/I104-rpi5/sweep_brackets.csv"
for m in shift drop swap; do run mutate_$m compare_brackets.py --ours="$OUT/brackets_i2_mac.csv" --theirs="$RAW/I104-rpi5/sweep_brackets.csv" --mutate=$m; done
echo done >> "$OUT/runA.log"
