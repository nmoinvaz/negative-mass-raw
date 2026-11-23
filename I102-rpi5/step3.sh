#!/bin/bash
# Step 3: the checks type2_failures ... lab_ricci, no controls. Exit code in done/step3.rc.
cd ~/Source/negative-mass-i102 || exit 2
RAW=~/Source/negative-mass-raw/I102-rpi5
mkdir -p "$RAW/done"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
/usr/bin/time -f "%e s wall, %M KB max rss" -o "$RAW/step3.time" nice -n 10 ~/Source/negative-mass-venv314/bin/python notes/warp/he_type3.py --checks=type2_failures,description,tanh_jets,tanh_planted,tanh_points,tanh_curve,tanh_enclosure,lab_ricci > "$RAW/step3.log" 2>&1
echo $? > "$RAW/done/step3.rc"
