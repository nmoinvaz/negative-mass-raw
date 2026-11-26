#!/bin/bash
# ind166 run N, then its seven mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind166.py > ind166_run$N.txt 2>&1; echo "exit $?" >> ind166_run$N.txt
for m in plant-K2 ode-flip t1-pert lemz-sign bracket-drop sep-swap ode-k; do
  nice -n 10 $PY ind166.py --mutate=$m > ind166_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind166_run${N}_mut_$m.txt
done
echo done > ind166_run${N}_done.txt
