#!/bin/bash
# development sweep of the controls: which checks does each mutation make fail (not of record)
PY=$HOME/Source/negative-mass-venv314/bin/python
SCRIPT=$HOME/Source/negative-mass-i168/notes/warp/conical_attraction.py
RAW=$HOME/Source/negative-mass-raw/I168-rpi5
cd "$HOME/Source/negative-mass-i168/notes/warp"
for m in d-sign P-drop ehat-sign f-sigma eig-plus shape-3 shape-om ehat-alpha A-u0 A-cf A-kappa series-a2 series-8 stage-I link-slope local-c2 regimeb-y small-sigma huge-thr plant-hyp plant-gron plant-shape plant-local plant-series; do
  OMP_NUM_THREADS=1 nice -n 10 $PY $SCRIPT --mutate=$m --skip-num > $RAW/dev_10_ctl_$m.log 2>&1
  echo "$m exit $?" >> $RAW/dev_10_ctl_summary.txt
done
echo done > $RAW/dev_10_ctl_done
