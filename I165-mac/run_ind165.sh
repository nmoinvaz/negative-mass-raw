#!/bin/bash
# ind165 run N, then its seven mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind165.py > ind165_run$N.txt 2>&1; echo "exit $?" >> ind165_run$N.txt
for m in plant-xr toy-flat phi3-cs strip-D c3-swap cert-coef psi-zero; do
  nice -n 10 $PY ind165.py --mutate=$m > ind165_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind165_run${N}_mut_$m.txt
done
echo done > ind165_run${N}_done.txt
