#!/bin/bash
# ind157 run 3, then its six mutations, one process at a time at nice 10.
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
cd "$(dirname "$0")"
nice -n 10 $PY -I ind157_run3.py > ind157_run3.txt 2>&1; echo "exit $?" >> ind157_run3.txt
for m in det-L ric-sign point ode H-b weight; do
  nice -n 10 $PY -I ind157_run3.py --mutate=$m > ind157_mut_$m.txt 2>&1; echo "exit $?" >> ind157_mut_$m.txt
done
echo done > controls_done.txt
