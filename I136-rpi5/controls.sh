#!/bin/bash
# usage: controls.sh LISTFILE  (lines NAME|CHECKS). Runs notes/warp/review_he_type3_count.py --mutate=NAME --checks=CHECKS one after
# the other (nice 10, one thread, 2 h per run), log mutate_NAME.log, wall s and peak rss KB in mutate_NAME.time, exit code in
# done/mutate_NAME.rc. A control whose rc file exists is skipped. Do not edit the script while this runs.
RAW=$HOME/Source/negative-mass-raw/I136-rpi5
WT=$HOME/Source/negative-mass-i136
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
while IFS='|' read -r NAME CHECKS; do
  [ -z "$NAME" ] && continue
  [ -f "$RAW/done/mutate_$NAME.rc" ] && continue
  /usr/bin/time -f '%e %M' -o "$RAW/mutate_$NAME.time" nice -n 10 timeout 7200 "$PY" notes/warp/review_he_type3_count.py "--mutate=$NAME" "--checks=$CHECKS" > "$RAW/mutate_$NAME.log" 2>&1
  echo $? > "$RAW/done/mutate_$NAME.rc"
done < "$1"
