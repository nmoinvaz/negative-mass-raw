#!/bin/bash
# ind171 run N, then its four mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind171.py > ind171_run$N.txt 2>&1; echo "exit $?" >> ind171_run$N.txt
for m in alpha-11 phantom-sign uniq-claim p1-V; do
  nice -n 10 $PY ind171.py --mutate=$m > ind171_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind171_run${N}_mut_$m.txt
done
echo done > ind171_run${N}_done.txt
