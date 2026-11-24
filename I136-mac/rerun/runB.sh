#!/bin/bash
# Mac rerun of #136's 13 controls, one after the other, nice 10.
S=/private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad
WT=$S/wt136; OUT=$S/r136; PY=$HOME/Source/negative-mass/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
while IFS='|' read -r NAME CHECKS; do
  [ -z "$NAME" ] && continue
  t0=$(date +%s)
  nice -n 10 "$PY" notes/warp/review_he_type3_count.py "--mutate=$NAME" "--checks=$CHECKS" > "$OUT/mutate_$NAME.log" 2>&1
  echo "$NAME rc=$? s=$(( $(date +%s) - t0 ))" >> "$OUT/runB.log"
done < "$HOME/Source/negative-mass-raw/I136-rpi5/controls.txt"
echo done >> "$OUT/runB.log"
