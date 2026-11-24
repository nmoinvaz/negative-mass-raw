#!/bin/bash
# the final full run (stdout to the repository's output file), then the controls queue. Absolute paths: the unit starts in ~.
RAW=$HOME/Source/negative-mass-raw/I136-rpi5
WT=$HOME/Source/negative-mass-i136
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
/usr/bin/time -f '%e %M' -o "$RAW/step6.time" nice -n 10 timeout 7200 "$PY" notes/warp/review_he_type3_count.py > notes/warp/review_he_type3_count_output.txt
echo $? > "$RAW/done/step6.rc"
"$RAW/controls.sh" "$RAW/controls.txt"
