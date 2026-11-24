#!/bin/bash
# step 7: the comparison with #133's files, then its two controls. Absolute paths: the unit starts in ~.
RAW=$HOME/Source/negative-mass-raw/I136-rpi5
WT=$HOME/Source/negative-mass-i136
PY=$HOME/Source/negative-mass-venv314/bin/python
CELLS=$HOME/Source/negative-mass-raw/I133-rpi5/cells.tsv
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
/usr/bin/time -f '%e %M' -o "$RAW/compare.time" nice -n 10 "$PY" notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --dump="$RAW/P_table.tsv" > notes/warp/review_he_type3_count_compare_output.txt
echo $? > "$RAW/done/compare.rc"
/usr/bin/time -f '%e %M' -o "$RAW/compare_mutate_drop-term.time" nice -n 10 "$PY" notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --mutate=compare-drop-term --only=tables > "$RAW/compare_mutate_drop-term.log" 2>&1
echo $? > "$RAW/done/compare_mutate_drop-term.rc"
/usr/bin/time -f '%e %M' -o "$RAW/compare_mutate_shift-leaf.time" nice -n 10 "$PY" notes/warp/review_he_type3_count_compare.py --cells="$CELLS" --mutate=compare-shift-leaf --only=roots --walls=le > "$RAW/compare_mutate_shift-leaf.log" 2>&1
echo $? > "$RAW/done/compare_mutate_shift-leaf.rc"
