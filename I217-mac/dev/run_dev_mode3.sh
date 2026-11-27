#!/bin/bash
# dev_40 .. of I217-mac: mode family with the extraction from the untuned member's own truncation-seeded departure at |Y| = 2e-3 (no pulse). Supersedes dev_20 .. dev_29:
# their extraction ran at t = 14 with a pulse of 1e-4 and, at c = -0.3, at Y ~ 0.7 (nonlinear), found by comparing the corner node with the static member.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
RAW=/Users/nathan/Source/negative-mass-raw/I217-mac/dev
run() { n=$1; shift; nice -n 10 /usr/bin/time -l $PY evolve_dev_runs.py "$@" > $RAW/dev_${n}.log 2> $RAW/dev_${n}.err; echo "rc=$?" >> $RAW/dev_${n}.log; }
run 40_mode_m03_h02  mode -0.3 0.0 0.02  40 1e-4
run 41_mode_m03_h01  mode -0.3 0.0 0.01  40 1e-4
run 42_mode_m03_h005 mode -0.3 0.0 0.005 40 1e-4
run 43_mode_m15_h02  mode -1.5 1.0 0.02  50 1e-4
run 44_mode_m15_h01  mode -1.5 1.0 0.01  50 1e-4
run 45_mode_m15_h005 mode -1.5 1.0 0.005 50 1e-4
run 46_mode_m15_rc2  mode -1.5 2.0 0.01  50 1e-4
run 47_mode_m15_rc06 mode -1.5 0.6 0.01  50 1e-4
run 48_mode_m1_h01   mode -1.0 1.0 0.01  50 1e-4
run 49_mode_m1_h02   mode -1.0 1.0 0.02  50 1e-4
echo done > $RAW/run_dev_mode3.done
