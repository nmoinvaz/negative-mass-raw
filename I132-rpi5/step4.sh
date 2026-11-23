#!/bin/bash
# Every control of he_tanh_bound.py, one after another, from the worktree. Run through run_step.sh as step4.
RAW=$HOME/Source/negative-mass-raw/I132-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
cd "$HOME/Source/negative-mass-i132" || exit 1
for c in shift identity-break no-tail no-small cell-gap jets-typo proof-typo factor-typo planted-eps asym-typo; do
  /usr/bin/time -f '%e s wall, %M KB peak rss' -o "$RAW/mutate_$c.time" $PY notes/warp/he_tanh_bound.py --mutate=$c > "$RAW/mutate_$c.log" 2>&1
  echo $? > "$RAW/done/mutate_$c.rc"
done
