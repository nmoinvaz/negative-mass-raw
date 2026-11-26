#!/bin/bash
# ind167 run N, then its five mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind167.py > ind167_run$N.txt 2>&1; echo "exit $?" >> ind167_run$N.txt
for m in d-sign eta0-coef even-b balance-coef start-C; do
  nice -n 10 $PY ind167.py --mutate=$m > ind167_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind167_run${N}_mut_$m.txt
done
echo done > ind167_run${N}_done.txt
