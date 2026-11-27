#!/bin/bash
# dev_50 .. of I217-mac: near-threshold outcomes (mode family), the pulse family's two boundaries at c = -1.5, the profile of Y at c = -1, -1.01, -1.5.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
RAW=/Users/nathan/Source/negative-mass-raw/I217-mac/dev
run() { n=$1; shift; nice -n 10 /usr/bin/time -l $PY evolve_dev_runs2.py "$@" > $RAW/dev_${n}.log 2> $RAW/dev_${n}.err; echo "rc=$?" >> $RAW/dev_${n}.log; }
run 50_near_m03_h02 near -0.3 0.0 0.02 40
run 51_near_m15_h01 near -1.5 1.0 0.01 50
run 52_pulseE       pulseE
run 53_profile      profile
echo done > $RAW/run_dev_misc.done
