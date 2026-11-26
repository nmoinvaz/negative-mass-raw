#!/bin/bash
# ind168 run N, then its nine mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind168.py > ind168_run$N.txt 2>&1; echo "exit $?" >> ind168_run$N.txt
for m in D-sign P-omega red-sigma box-omega ehat-alpha regb-y cf-49 y-thr small-root; do
  nice -n 10 $PY ind168.py --mutate=$m > ind168_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind168_run${N}_mut_$m.txt
done
echo done > ind168_run${N}_done.txt
