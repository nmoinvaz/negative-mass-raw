#!/bin/bash
# Step 5: the full run, stdout to notes/warp/he_type3_output.txt (copied here as final.log). Exit code in done/final.rc.
cd ~/Source/negative-mass-i102 || exit 2
RAW=~/Source/negative-mass-raw/I102-rpi5
mkdir -p "$RAW/done"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
/usr/bin/time -f "%e s wall, %M KB max rss" -o "$RAW/final.time" nice -n 10 ~/Source/negative-mass-venv314/bin/python notes/warp/he_type3.py > notes/warp/he_type3_output.txt 2> "$RAW/final.err"
echo $? > "$RAW/done/final.rc"
cp notes/warp/he_type3_output.txt "$RAW/final.log"
