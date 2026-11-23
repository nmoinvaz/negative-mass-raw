#!/bin/bash
# Mac rerun of #136: the full run, then the comparison with #133 and its two controls. One process, nice 10.
S=/private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad
WT=$S/wt136; OUT=$S/r136; PY=$HOME/Source/negative-mass/.venv/bin/python
CELLS=$HOME/Source/negative-mass-raw/I133-rpi5/cells.tsv
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
run() { local name=$1; shift; local t0=$(date +%s); nice -n 10 "$PY" "$@" > "$OUT/$name.log" 2>&1; local rc=$?; echo "$name rc=$rc s=$(( $(date +%s) - t0 ))" >> "$OUT/runA.log"; }
run full notes/warp/review_he_type3_count.py
run compare notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --dump="$OUT/P_table.tsv"
run compare_mutate_drop-term notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --mutate=compare-drop-term --only=tables
run compare_mutate_shift-leaf notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --mutate=compare-shift-leaf --only=roots --walls=le
echo done >> "$OUT/runA.log"
