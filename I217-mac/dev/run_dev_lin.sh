#!/bin/bash
# dev_63 .. of I217-mac: linear-regime departure threshold scan, h = 0.01. Y0 = departure threshold, Yext = extraction level (Y0 = Yext / 10).
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
RAW=/Users/nathan/Source/negative-mass-raw/I217-mac/dev
run() { n=$1; shift; nice -n 10 /usr/bin/time -l $PY evolve_dev_runs.py "$@" > $RAW/dev_${n}.log 2> $RAW/dev_${n}.err; echo "rc=$?" >> $RAW/dev_${n}.log; }
run 63_lin_m15_Y6  mode -1.5 1.0 0.01 50 1e-5 2e-6 0.0 2e-5
run 64_lin_m15_Y7  mode -1.5 1.0 0.01 50 1e-6 2e-7 0.0 2e-6
run 65_lin_m1_Y5   mode -1.0 1.0 0.01 50 1e-4 2e-5 0.0 2e-4
run 66_lin_m1_Y6   mode -1.0 1.0 0.01 50 1e-5 2e-6 0.0 2e-5
run 67_lin_m03_Y6  mode -0.3 0.0 0.01 40 1e-5 2e-6 0.0 2e-5
run 68_lin_m03_Y7  mode -0.3 0.0 0.01 40 1e-6 2e-7 0.0 2e-6
echo done > $RAW/run_dev_lin.done
