#!/bin/bash
# Step 5 of I101-rpi5: each script's full run (checks, then every control), stdout to its output file in the worktree.
NR=$HOME/Source/negative-mass-i101
RAW=$HOME/Source/negative-mass-raw/I101-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1
cd $NR
for sc in ricci typeI points; do
  /usr/bin/time -f "%e s wall, %M kB max rss" -o $RAW/final_$sc.time nice -n 10 $PY notes/warp/review_he_surface_$sc.py > notes/warp/review_he_surface_${sc}_output.txt 2> $RAW/final_$sc.err
  echo $? > $RAW/done/final_$sc.rc
done
echo 0 > $RAW/done/final.rc
