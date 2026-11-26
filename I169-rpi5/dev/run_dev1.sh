#!/bin/bash
# dev run 1: numerical formal-series solutions of D = 0 in the (n; alpha, beta, gamma, delta) formulation (exploration, not of record)
PY=/home/nathan/Source/negative-mass-venv314/bin/python
D=/home/nathan/Source/negative-mass-raw/I169-rpi5/dev
for spec in "4 4 7 d 16 0.0" "4 4 7 a 16 0.0" "5 5 7 d 12 0.0" "5 5 7 a 12 0.0"; do
  set -- $spec
  echo "=== $spec" 
  nice -n 10 $PY $D/formal2.py $spec
done
echo "exit 0" > $D/dev1.rc
