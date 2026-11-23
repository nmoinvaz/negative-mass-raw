#!/bin/bash
# Step 4: every control, all checks, one run at a time, 3 h cap each. cwd = the worktree.
set -u
RAW=$HOME/Source/negative-mass-raw/I133-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
cd $HOME/Source/negative-mass-i133
for c in sigma-1e-3 drop-P-term no-tail-large no-tail-small cell-gap eps-typo T-off w-range krawczyk-nocorr double-root skip-y drop-P-term-low; do
  /usr/bin/time -f '%e s wall, %M KB peak rss' -o "$RAW/mutate_$c.time" timeout 10800 $PY notes/warp/he_type3_count.py --mutate=$c > "$RAW/mutate_$c.log" 2>&1
  echo $? > "$RAW/done/mutate_$c.rc"
done
echo finished > "$RAW/done/step4.rc"
