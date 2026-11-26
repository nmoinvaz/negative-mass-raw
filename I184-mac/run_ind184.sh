#!/bin/bash
# ind184 run N, then its three mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind184.py > ind184_run$N.txt 2>&1; echo "exit $?" >> ind184_run$N.txt
for m in q1-sign q2-coef q3-start; do
  nice -n 10 $PY ind184.py --mutate=$m > ind184_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind184_run${N}_mut_$m.txt
done
echo done > ind184_run${N}_done.txt
