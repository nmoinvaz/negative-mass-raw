#!/bin/bash
# dev_80 .. of I217-mac: linear-level departure (Y0 = 2e-5, extraction at 2e-4) at three h, for the order of A*_h and the slopes. Part (c) of the coordinator's ruling 4.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
RAW=/Users/nathan/Source/negative-mass-raw/I217-mac/dev
run() { n=$1; shift; nice -n 10 /usr/bin/time -l $PY evolve_dev_runs.py "$@" > $RAW/dev_${n}.log 2> $RAW/dev_${n}.err; echo "rc=$?" >> $RAW/dev_${n}.log; }
run 80_lin_m1_h02   mode -1.0 1.0 0.02  50 1e-4 2e-5 0.0 2e-4
run 81_lin_m1_h005  mode -1.0 1.0 0.005 50 1e-4 2e-5 0.0 2e-4
run 82_lin_m15_h02  mode -1.5 1.0 0.02  50 1e-4 2e-5 0.0 2e-4
run 83_lin_m15_h005 mode -1.5 1.0 0.005 50 1e-4 2e-5 0.0 2e-4
run 84_lin_m03_h02  mode -0.3 0.0 0.02  40 1e-4 2e-5 0.0 2e-4
run 85_lin_m03_h005 mode -0.3 0.0 0.005 40 1e-4 2e-5 0.0 2e-4
echo done > $RAW/run_dev_lin2.done
