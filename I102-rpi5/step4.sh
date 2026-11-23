#!/bin/bash
# Step 4: every control of he_type3.py, one at a time, nice 10, one thread. Each exit code goes to done/mutate_<name>.rc.
cd ~/Source/negative-mass-i102 || exit 2
PY=~/Source/negative-mass-venv314/bin/python
RAW=~/Source/negative-mass-raw/I102-rpi5
mkdir -p "$RAW/done"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
while read -r name; do
  [ -z "$name" ] && continue
  [ -f "$RAW/done/mutate_$name.rc" ] && continue
  /usr/bin/time -f "%e s wall, %M KB max rss" -o "$RAW/mutate_$name.time" nice -n 10 "$PY" notes/warp/he_type3.py --mutate="$name" > "$RAW/mutate_$name.log" 2>&1
  echo $? > "$RAW/done/mutate_$name.rc"
done < "$RAW/step4.list"
echo finished > "$RAW/done/step4.rc"
