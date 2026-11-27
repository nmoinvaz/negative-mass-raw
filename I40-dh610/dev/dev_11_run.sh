#!/bin/bash
# D = 4 family S at the three declared h, all flags: the set the analysis-only mutations and the planted comparison are developed on
TH=/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution/threshold.py
PY=$HOME/Source/negative-mass-venv314/bin/python
D=$HOME/Source/negative-mass-raw/I40-dh610/dev/dev_11
for h in 0.02 0.01 0.005; do
  ./unit_run.sh dev_11/job_D4_S_h$h nice -n 10 $PY $TH job --D=4 --family=S --h=$h --out=$D/D4_S_h$h --ed --stall --cons
done
