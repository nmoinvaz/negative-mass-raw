#!/bin/bash
# ind169 run N, then its seven mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
N=${1:?run number}
cd "$(dirname "$0")"
nice -n 10 $PY ind169.py > ind169_run$N.txt 2>&1; echo "exit $?" >> ind169_run$N.txt
for m in j1-v0 j2-sign j3-claim j4-iota j5-factor j6-undivided j7-freq; do
  nice -n 10 $PY ind169.py --mutate=$m > ind169_run${N}_mut_$m.txt 2>&1; echo "exit $?" >> ind169_run${N}_mut_$m.txt
done
echo done > ind169_run${N}_done.txt
